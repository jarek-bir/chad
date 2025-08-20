!/bin/bash

# Chad Bug Hunting Script
# Usage examples for enhanced Google Dorking

echo "=================================================="
echo "         Chad Bug Hunting Examples"
echo "=================================================="

# Create results directory
mkdir -p results

echo ""
echo "1. Basic Directory Traversal Hunt"
chad -q 'intitle:"index of /" "parent directory"' -tr 100 -o results/index_of_results.json -nsos

echo ""
echo "2. Database Leak Hunt"
chad -q 'intext:"#mysql dump" filetype:sql' -tr 50 -o results/db_leaks.json -nsos

echo ""
echo "3. Config Files Hunt"
chad -q 'ext:conf inurl:rsyncd.conf -cvs -man' -tr 75 -o results/config_files.json -nsos

echo ""
echo "4. Admin Panel Discovery"
chad -q 'intitle:admin intitle:login' -tr 100 -o results/admin_panels.json -nsos

echo ""
echo "5. Sensitive Documents Hunt"
chad -q 'intext:"confidential" filetype:pdf' -tr 50 -o results/confidential_docs.json -nsos

echo ""
echo "6. Web Application Vulnerabilities"
chad -q 'inurl:index.php?id=' -tr 100 -o results/webapp_vulns.json -nsos

echo ""
echo "7. Upload Directories"
chad -q 'intitle:"Index of" upload' -tr 75 -o results/upload_dirs.json -nsos

echo ""
echo "8. Webcams and IoT"
chad -q 'intitle:"Live View" intitle:axis' -tr 50 -o results/webcams.json -nsos

echo ""
echo "9. Log Files Hunt"
chad -q 'filetype:log access.log -CVS' -tr 75 -o results/log_files.json -nsos

echo ""
echo "10. Backup Files Hunt"
chad -q 'filetype:bak inurl:"htaccess|passwd|shadow|htusers"' -tr 50 -o results/backup_files.json -nsos

echo ""
echo "=================================================="
echo "         Site-Specific Bug Hunting"
echo "=================================================="

echo ""
echo "Target specific domain for comprehensive testing:"
echo "chad -q bug_hunting_dorks.txt -s '*.target.com' -tr 200 -o results/target_comprehensive.json"

echo ""
echo "Multiple target scanning:"
echo "Create sites.txt with domains and run:"
echo "IFS=\$'\\n'; count=0; for site in \$(cat sites.txt); do count=\$((count+1)); echo \"#\${count} | \${site}\"; chad -q bug_hunting_dorks.txt -s \"\${site}\" -tr 200 -o \"results/target_\${count}.json\"; done"

echo ""
echo "=================================================="
echo "         Extraction and Analysis"
echo "=================================================="

echo ""
echo "Extract social media links from results:"
echo "chad-extractor -t social_media_template.json -res results/ -o analysis/social_media_report.json -v"

echo ""
echo "=================================================="
echo "         Safety Reminders"
echo "=================================================="
echo "- Always use appropriate delays to avoid rate limiting"
echo "- Only test against systems you own or have permission to test"
echo "- Be respectful of robots.txt and website terms of service"
echo "- Use proxies if conducting extensive testing"
echo "- Monitor your queries to avoid detection"
echo "=================================================="
