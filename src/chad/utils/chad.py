#!/usr/bin/env python3

import json
import os
import random
import requests
import sys
import time
from datetime import datetime

from . import array, file, general, grep, proxy, validate
from .tor_manager import TorManager
from .rate_limiter import AdvancedRateLimiter, RateLimitConfig

import alive_progress, concurrent.futures, dataclasses, dateutil.relativedelta, nagooglesearch, threading
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ----------------------------------------

@dataclasses.dataclass
class Google:
	"""
	Class for storing Google search details.
	"""
	query: str
	proxy: str       = ""
	urls : list[str] = dataclasses.field(default_factory = list)

# ----------------------------------------

class Chad:

	def __init__(
		self,
		queries        : list[str],
		site           : str,
		time           : int,
		total_results  : int,
		page_results   : int,
		minimum_queries: int,
		maximum_queries: int,
		minimum_pages  : int,
		maximum_pages  : int,
		user_agents    : list[str],
		proxies        : list[str],
		sleep_on_start : bool,
		debug          : bool,
		use_tor        : bool = False,
		tor_rotation   : int = 10
	):
		"""
		Class for Google searching.
		Enhanced with Tor support and user agent rotation.
		"""
		self.__queries = queries
		self.__site            = site
		self.__tbs             = self.__get_tbs(time)
		self.__total_results   = total_results
		self.__page_results    = page_results
		self.__minimum_queries = minimum_queries
		self.__maximum_queries = maximum_queries
		self.__minimum_pages   = minimum_pages
		self.__maximum_pages   = maximum_pages
		self.__user_agents     = user_agents
		self.__user_agents_len = len(self.__user_agents)
		self.__proxies         = proxy.Proxies(proxies)
		self.__sleep_on_start  = sleep_on_start
		self.__debug           = debug
		self.__debug_lock      = threading.Lock()
		self.__blacklist       = grep.get_blacklist()
		self.__results         = []
		
		# Tor integration
		self.__use_tor         = use_tor
		self.__tor_rotation    = tor_rotation  # Rotate IP every N queries
		self.__tor_manager     = None
		self.__query_count     = 0
		
		# Initialize Tor Manager
		if use_tor:
			self.__tor_manager = TorManager()
			if self.__tor_manager.check_tor_status():
				print(general.get_timestamp("Tor service is available"))
			else:
				print(general.get_timestamp("Warning: Tor service not available"))
				self.__use_tor = False
				self.__tor_manager = None
		else:
			self.__tor_manager = None
		
		# Initialize Rate Limiter (always create one)
		if self.__use_tor and self.__tor_manager:
			# Intelligent rate limiting for Tor
			rate_config = RateLimitConfig(
				min_query_delay=15.0,      # Longer delays for Tor
				max_query_delay=45.0,
				enable_adaptive=True,
				success_speedup=0.8,
				error_slowdown=2.0,
				min_speedup_delay=10.0,
				max_slowdown_delay=120.0
			)
		else:
			# Standard rate limiting for regular usage
			rate_config = RateLimitConfig(
				min_query_delay=5.0,       # Standard delays for regular usage
				max_query_delay=20.0,
				enable_adaptive=True,
				success_speedup=0.9,
				error_slowdown=1.5,
				min_speedup_delay=3.0,
				max_slowdown_delay=60.0
			)
		
		self.__rate_limiter = AdvancedRateLimiter(
			config=rate_config,
			tor_manager=self.__tor_manager
		)		# Initialize standard rate limiter if not using Tor
		if not self.__rate_limiter:
			rate_config = RateLimitConfig(
				min_query_delay=minimum_queries,
				max_query_delay=maximum_queries,
				min_page_delay=minimum_pages,
				max_page_delay=maximum_pages,
				enable_adaptive=False  # Conservative without Tor
			)
			self.__rate_limiter = AdvancedRateLimiter(rate_config)

	def __get_tbs(self, time: int) -> str:
		"""
		Get a value for the 'to be searched' Google query parameter.
		"""
		tmp = "li:1"
		if time:
			now = datetime.today()
			tmp = nagooglesearch.get_tbs(now, now - dateutil.relativedelta.relativedelta(months = time))
		return tmp

	def prepare(self):
		"""
		Validate Google Dorks, and, if applicable, prepend the specified site to each one.
		"""
		print(general.get_timestamp("Validating Google Dorks..."))
		print("Google only allows Google Dorks up to 32 words in length, separated by spaces")
		print("If the site is specified, Google Dorks containing the 'site:' operator will be ignored")
		tmp = []
		ignored = []
		for query in self.__queries:
			if self.__site:
				if grep.has_site(query):
					ignored.append(query)
					continue
				query = f"site:{self.__site} {query}"
			if len(query.split(" ")) > 32:
				ignored.append(query)
				continue
			tmp.append(query)
		if ignored:
			print(f"IGNORED GOOGLE DORKS: {len(ignored)}")
			for query in ignored:
				general.print_cyan(query)
		if not tmp:
			general.print_red("No valid Google Dorks were found!")
		self.__queries = array.unique(tmp)
		return self.__queries

	def run(self):
		"""
		Run a Google search with enhanced Tor and advanced rate limiting.
		"""
		print(general.get_timestamp("Searching Google Dorks..."))
		if self.__use_tor:
			print(general.get_timestamp("Using Tor for enhanced anonymity"))
			print(f"IP rotation every {self.__tor_rotation} queries")
		print("Press CTRL + C to exit early - results will be saved")
		self.__results = []
		count = 0
		exit_program = False
		try:
			if self.__sleep_on_start:
				self.__wait()
			for query in self.__queries:
				count += 1
				self.__query_count += 1
				result = Google(query)
				
				# Start query tracking
				query_metrics = self.__rate_limiter.start_query(query)
				
				while not exit_program:
					# Handle proxy selection (Tor takes precedence)
					if self.__use_tor and self.__tor_manager:
						# Use Tor proxy
						result.proxy = f"socks5://127.0.0.1:{self.__tor_manager.tor_port}"
					elif not self.__proxies.is_empty():
						if self.__proxies.is_round_robin():
							self.__rate_limiter.wait_between_queries()
						result.proxy = self.__proxies.get()
					elif count > 1:
						self.__rate_limiter.wait_between_queries()
					
					self.__print_status(count, result)
					search_parameters = {
						"q"     : result.query,
						"tbs"   : self.__tbs,
						"hl"    : "en",
						"filter": "0",
						"safe"  : "images",
						"num"   : self.__get_num()
					}
					
					# Enhanced user agent selection
					user_agent = self.__get_enhanced_user_agent()
					
					try:
						client = nagooglesearch.GoogleClient(
							tld               = "com",
							search_parameters = search_parameters,
							user_agent        = user_agent,
							proxy             = result.proxy,
							max_results       = self.__total_results,
							min_sleep         = self.__minimum_pages,
							max_sleep         = self.__maximum_pages,
							debug             = self.__debug
						)
						result.urls = client.search()
						
						if not grep.has_site(result.query):
							result.urls = grep.filter_blacklist(result.urls, self.__blacklist)
						
						# Query successful
						self.__rate_limiter.end_query(
							query_metrics, 
							success=True, 
							results_count=len(result.urls)
						)
						
						if result.urls:
							self.__results.append(result)
						
						error = client.get_error()
						if error in ["REQUESTS_EXCEPTION", "429_TOO_MANY_REQUESTS"]:
							general.print_yellow(error)
							
							# Update metrics with error
							self.__rate_limiter.end_query(
								query_metrics, 
								success=False, 
								error_type=error
							)
							
							if self.__use_tor and self.__tor_manager:
								# For Tor, try rotating IP instead of removing proxy
								print(general.get_timestamp("Rate limited - adaptive delay and IP rotation..."))
								self.__rate_limiter.wait_between_queries()
								continue
							elif result.proxy:
								message = self.__proxies.remove(result.proxy)
								if message:
									print(message)
								if self.__proxies.is_empty():
									general.print_red("All proxies has been exhausted!")
									exit_program = True
									break
							else:
								exit_program = True
								break
						else:
							break
							
					except Exception as e:
						# Handle unexpected errors
						self.__rate_limiter.end_query(
							query_metrics, 
							success=False, 
							error_type=str(e)
						)
						print(f"[!] Unexpected error: {e}")
						break
						
				if exit_program:
					break
		except KeyboardInterrupt:
			print(general.get_timestamp("Interrupted by user"))
		finally:
			# Print performance report
			self.__rate_limiter.print_performance_report()
			
			# Export metrics if available
			timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
			metrics_file = f"chad_metrics_{timestamp}.json"
			self.__rate_limiter.export_metrics(metrics_file)
			
			# Cleanup Tor if used
			if self.__use_tor and self.__tor_manager:
				print(general.get_timestamp("Cleaning up Tor connection..."))
		
		if not self.__results:
			print("No results")
		else:
			print(general.jdump(self.__to_dict()))
		return self.__results

	def __wait(self):
		"""
		Sleep for a random amount of time in seconds.
		"""
		seconds = random.randint(self.__minimum_queries, self.__maximum_queries)
		print(f"Sleeping between Google Dorks for {seconds} sec...")
		time.sleep(seconds)

	def __print_status(self, id: int, data: Google):
		"""
		Print the current status.
		"""
		text = f"QUERY {id}/{len(self.__queries)}: {data.query}"
		if data.proxy:
			text = f"{text} | PROXY: {data.proxy}"
		general.print_green(general.get_timestamp(text))

	def __get_num(self):
		"""
		Get the number of results per page as a string.\n
		If not specified, return a random number between 70 and 100 as a string.
		"""
		return str(self.__page_results if self.__page_results > 0 else random.randint(70, 100))

	def __get_headers(self):
		"""
		Get HTTP request headers.
		"""
		return {
			"User-Agent": self.__get_user_agent(),
			"Accept-Language": "en-US, *",
			"Accept": "*/*",
			"Referer": "https://www.google.com/",
			"Upgrade-Insecure-Requests": "1"
		}

	def __get_user_agent(self):
		"""
		Get a [random] user agent.\n
		Returns an empty string if there are no user agents.
		"""
		user_agent = ""
		if self.__user_agents_len > 0:
			user_agent = self.__user_agents[random.randint(0, self.__user_agents_len - 1)]
		return user_agent
	
	def __get_enhanced_user_agent(self):
		"""
		Get enhanced user agent with Tor integration support.
		"""
		if self.__use_tor and self.__tor_manager:
			# Use Tor manager's user agent rotation
			return self.__tor_manager.get_random_user_agent()
		else:
			# Use standard user agent rotation
			return self.__get_user_agent()

	def __get_urls(self) -> list[str]:
		"""
		Combine all Google Dork result URLs into a single list.
		"""
		tmp = []
		for result in self.__results:
			tmp.extend(result.urls)
		tmp = array.unique(tmp)
		random.shuffle(tmp)
		return tmp

	def download_files(self, threads: int, directory: str):
		"""
		Download the content from all Google Dork result URLs into files.\n
		Proxies are ignored.
		"""
		print(general.get_timestamp("Downloading files... Proxies are ignored"))
		urls = self.__get_urls()
		with alive_progress.alive_bar(len(urls), title = "Progress:") as bar:
			with concurrent.futures.ThreadPoolExecutor(max_workers = threads) as executor:
				subprocesses = []
				for url in urls:
					subprocesses.append(executor.submit(self.__get, url, directory))
				for subprocess in concurrent.futures.as_completed(subprocesses):
					result: file.File = subprocess.result()
					if result.content and result.path:
						file.write_binary_silent(result.content, result.path)
					bar()

	def __get(self, url: str, downloads_directory: str):
		"""
		Get the content from a URL.
		"""
		tmp = file.File()
		session = None
		response = None
		try:
			session = requests.Session()
			session.max_redirects = 10
			response = session.get(url, headers = self.__get_headers(), proxies = None, verify = False, allow_redirects = True, timeout = 30)
			if response.status_code == 200:
				tmp.content = response.content
				tmp.path = file.get_url_filename(url, downloads_directory)
		except (requests.exceptions.RequestException, urllib3.exceptions.HTTPError) as ex:
			self.__print_debug(str(ex))
		finally:
			if response:
				response.close()
			if session:
				session.close()
		return tmp

	def __print_debug(self, message: str):
		"""
		Print a debug message.
		"""
		if self.__debug:
			with self.__debug_lock:
				general.print_yellow(message)

	def save(self, out: str):
		"""
		Save the results in an output file.\n
		If the output file exists, prompt to overwrite it.
		"""
		if self.__results:
			file.overwrite(general.jdump(self.__to_dict()), out)

	def __to_dict(self):
		"""
		Convert an instance of a class into a dictionary.
		"""
		return [dataclasses.asdict(result) for result in self.__results]
