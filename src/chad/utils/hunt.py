#!/usr/bin/env python3

"""
Chad Bug Hunting Examples
Advanced Google Dorking for security testing
"""

import os
import subprocess
from pathlib import Path

class ChadBugHunter:
    """Class for running automated bug hunting with Chad"""
    
    def __init__(self, output_dir: str = "results"):
        """Initialize with output directory"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def run_dork(self, query: str, filename: str, max_results: int = 50):
        """Run a single Google dork"""
        output_file = self.output_dir / filename
        cmd = [
            "chad",
            "-q", query,
            "-tr", str(max_results),
            "-o", str(output_file),
            "-nsos"
        ]
        
        print(f"Running: {query}")
        print(f"Output: {output_file}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ Success")
                if output_file.exists():
                    print(f"  Results file created: {output_file}")
                else:
                    print("  No results found (rate limited or no matches)")
            else:
                print(f"✗ Error: {result.stderr}")
                if "429_TOO_MANY_REQUESTS" in result.stderr:
                    print("  ⚠️  Google rate limiting detected - consider using proxies or longer delays")
        except Exception as e:
            print(f"✗ Exception: {e}")
        print("-" * 50)
    
    def directory_traversal_hunt(self):
        """Hunt for directory listings"""
        print("=== DIRECTORY TRAVERSAL HUNT ===")
        dorks = [
            ('intitle:"index of /" "parent directory"', "index_of_results.json"),
            ('intitle:"Index of" upload size parent directory', "upload_dirs.json"),
            ('intitle:"index of" mysql.conf OR mysql_config', "mysql_configs.json"),
            ('intitle:"Index Of" cookies.txt size', "cookies_files.json"),
        ]
        
        for query, filename in dorks:
            self.run_dork(query, filename)
    
    def database_leak_hunt(self):
        """Hunt for database leaks"""
        print("=== DATABASE LEAK HUNT ===")
        dorks = [
            ('intext:"#mysql dump" filetype:sql', "mysql_dumps.json"),
            ('intext:"Dumping data for table"', "table_dumps.json"),
            ('filetype:sql "insert into" (pass|passwd|password)', "sql_passwords.json"),
            ('intext:"phpMyAdmin MySQL-Dump" filetype:txt', "phpmyadmin_dumps.json"),
        ]
        
        for query, filename in dorks:
            self.run_dork(query, filename)
    
    def config_files_hunt(self):
        """Hunt for configuration files"""
        print("=== CONFIG FILES HUNT ===")
        dorks = [
            ('ext:conf inurl:rsyncd.conf -cvs -man', "rsyncd_configs.json"),
            ('filetype:conf inurl:firewall -intitle:cvs', "firewall_configs.json"),
            ('filetype:config web.config -CVS', "web_configs.json"),
            ('ext:ini intext:env.ini', "env_configs.json"),
        ]
        
        for query, filename in dorks:
            self.run_dork(query, filename)
    
    def admin_panels_hunt(self):
        """Hunt for admin panels"""
        print("=== ADMIN PANELS HUNT ===")
        dorks = [
            ('intitle:admin intitle:login', "admin_logins.json"),
            ('inurl:admin intitle:login', "admin_urls.json"),
            ('intitle:"phpMyAdmin" "running on" inurl:"main.php"', "phpmyadmin_panels.json"),
            ('inurl:admin filetype:db', "admin_databases.json"),
        ]
        
        for query, filename in dorks:
            self.run_dork(query, filename)
    
    def log_files_hunt(self):
        """Hunt for log files"""
        print("=== LOG FILES HUNT ===")
        dorks = [
            ('filetype:log access.log -CVS', "access_logs.json"),
            ('filetype:log cron.log', "cron_logs.json"),
            ('filetype:log "PHP Parse error"', "php_error_logs.json"),
            ('intext:"Session Start" filetype:log', "session_logs.json"),
        ]
        
        for query, filename in dorks:
            self.run_dork(query, filename)
    
    def backup_files_hunt(self):
        """Hunt for backup files"""
        print("=== BACKUP FILES HUNT ===")
        dorks = [
            ('filetype:bak inurl:"htaccess|passwd|shadow|htusers"', "backup_files.json"),
            ('filetype:bkf bkf', "windows_backups.json"),
            ('ext:gho gho', "ghost_images.json"),
            ('inurl:backup filetype:mdb', "backup_databases.json"),
        ]
        
        for query, filename in dorks:
            self.run_dork(query, filename)
    
    def sensitive_docs_hunt(self):
        """Hunt for sensitive documents"""
        print("=== SENSITIVE DOCUMENTS HUNT ===")
        dorks = [
            ('intext:"confidential" filetype:pdf', "confidential_pdfs.json"),
            ('intext:"not for distribution" confidential', "restricted_docs.json"),
            ('filetype:doc "confidential" "proprietary"', "proprietary_docs.json"),
            ('filetype:xls "customer" "phone" "email"', "customer_data.json"),
        ]
        
        for query, filename in dorks:
            self.run_dork(query, filename)
    
    def run_site_specific(self, domain: str):
        """Run comprehensive scan against specific domain"""
        print(f"=== SITE-SPECIFIC HUNT: {domain} ===")
        
        # Use existing dorks file
        dorks_file = Path("src/dorks/social_media_dorks.txt")
        if dorks_file.exists():
            output_file = self.output_dir / f"{domain.replace('*', 'wildcard').replace('.', '_')}_comprehensive.json"
            cmd = [
                "chad",
                "-q", str(dorks_file),
                "-s", domain,
                "-tr", "200",
                "-o", str(output_file),
                "-nsos"
            ]
            
            print(f"Running comprehensive scan against: {domain}")
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✓ Results saved to: {output_file}")
                else:
                    print(f"✗ Error: {result.stderr}")
            except Exception as e:
                print(f"✗ Exception: {e}")
        else:
            print("✗ Dorks file not found")
    
    def run_all_hunts(self):
        """Run all hunting methods"""
        print("Starting comprehensive bug hunting with Chad...")
        print("=" * 60)
        
        self.directory_traversal_hunt()
        self.database_leak_hunt()
        self.config_files_hunt()
        self.admin_panels_hunt()
        self.log_files_hunt()
        self.backup_files_hunt()
        self.sensitive_docs_hunt()
        
        print("=" * 60)
        print("Bug hunting completed!")
        print(f"Results saved in: {self.output_dir}")
        print("\nSAFETY REMINDERS:")
        print("- Only test against systems you own or have permission to test")
        print("- Be respectful of robots.txt and website terms of service")
        print("- Use appropriate delays to avoid rate limiting")
        print("- Monitor your queries to avoid detection")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Chad Bug Hunting Examples")
    parser.add_argument("-o", "--output", default="results", help="Output directory")
    parser.add_argument("-s", "--site", help="Target specific site (e.g., *.example.com)")
    parser.add_argument("--all", action="store_true", help="Run all hunting methods")
    parser.add_argument("--directory", action="store_true", help="Directory traversal hunt")
    parser.add_argument("--database", action="store_true", help="Database leak hunt")
    parser.add_argument("--config", action="store_true", help="Config files hunt")
    parser.add_argument("--admin", action="store_true", help="Admin panels hunt")
    parser.add_argument("--logs", action="store_true", help="Log files hunt")
    parser.add_argument("--backup", action="store_true", help="Backup files hunt")
    parser.add_argument("--sensitive", action="store_true", help="Sensitive documents hunt")
    
    args = parser.parse_args()
    
    hunter = ChadBugHunter(args.output)
    
    if args.site:
        hunter.run_site_specific(args.site)
    elif args.all:
        hunter.run_all_hunts()
    elif args.directory:
        hunter.directory_traversal_hunt()
    elif args.database:
        hunter.database_leak_hunt()
    elif args.config:
        hunter.config_files_hunt()
    elif args.admin:
        hunter.admin_panels_hunt()
    elif args.logs:
        hunter.log_files_hunt()
    elif args.backup:
        hunter.backup_files_hunt()
    elif args.sensitive:
        hunter.sensitive_docs_hunt()
    else:
        print("Chad Bug Hunting Examples")
        print("Usage examples:")
        print("  python hunt.py --all                    # Run all hunting methods")
        print("  python hunt.py --directory              # Directory traversal hunt")
        print("  python hunt.py --database               # Database leak hunt")
        print("  python hunt.py --admin                  # Admin panels hunt")
        print("  python hunt.py -s '*.example.com'       # Site-specific hunt")
        print("  python hunt.py --all -o custom_results  # Custom output directory")

if __name__ == "__main__":
    main()
