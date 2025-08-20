#!/usr/bin/env python3

import logging
import sys
from pathlib import Path
from typing import Optional

def setup_logging(debug: bool = False, log_file: Optional[str] = None):
    """
    Set up logging configuration for Chad.
    
    Args:
        debug: Enable debug level logging
        log_file: Optional log file path
    """
    log_level = logging.DEBUG if debug else logging.INFO
    
    # Create logs directory if it doesn't exist
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Set up console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    # Set up file handler if specified
    handlers = [console_handler]
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        handlers.append(file_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        handlers=handlers,
        force=True
    )
    
    return logging.getLogger('chad')

def log_google_search(query: str, proxy: Optional[str] = None, results_count: int = 0):
    """Log Google search details"""
    logger = logging.getLogger('chad')
    proxy_info = f" via proxy {proxy}" if proxy else ""
    logger.info(f"Executed Google search: '{query}'{proxy_info} - {results_count} results")

def log_rate_limit_hit(error_type: str, proxy: Optional[str] = None):
    """Log rate limiting incidents"""
    logger = logging.getLogger('chad')
    proxy_info = f" (proxy: {proxy})" if proxy else ""
    logger.warning(f"Rate limit hit: {error_type}{proxy_info}")

def log_file_download(url: str, success: bool, file_path: Optional[str] = None):
    """Log file download attempts"""
    logger = logging.getLogger('chad')
    if success:
        logger.info(f"Successfully downloaded: {url} -> {file_path}")
    else:
        logger.warning(f"Failed to download: {url}")

def log_proxy_status(proxy: str, status: str):
    """Log proxy status changes"""
    logger = logging.getLogger('chad')
    logger.info(f"Proxy {proxy}: {status}")

class ChadException(Exception):
    """Base exception class for Chad"""
    pass

class RateLimitException(ChadException):
    """Raised when rate limits are hit"""
    pass

class ProxyException(ChadException):
    """Raised when proxy-related issues occur"""
    pass

class ValidationException(ChadException):
    """Raised when validation fails"""
    pass
