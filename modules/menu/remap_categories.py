#!/usr/bin/env python3
import os
import re

# Precise Mapping configuration
MAPPING = {
    # 01 Information Gathering
    "nmap": "01-04-network-scanners;01-info-gathering;",
    "dnsrecon": "01-01-dns-analysis;01-info-gathering;",
    "sublist3r": "01-info-gathering;",
    "amass": "01-info-gathering;",
    "theharvester": "01-07-osint-analysis;01-info-gathering;",
    
    # 02 Vulnerability Analysis
    "nikto": "02-01-web-vulnerability-scanners;02-vulnerability-analysis;",
    "metasploit": "04-exploitation-tools;02-vulnerability-analysis;",
    
    # 03 Web Application Analysis
    "sqlmap": "04-06-db-exploit;03-webapp-analysis;",
    "wpscan": "03-05-cms-scanners;03-webapp-analysis;",
    "burpsuite": "03-webapp-analysis;",
    
    # 05 Password Attacks
    "john": "05-02-offline-attacks;05-password-attacks;",
    "hashcat": "05-02-offline-attacks;05-password-attacks;",
    "hydra": "05-01-online-attacks;05-password-attacks;",
}

# Keyword-based fallback
# Prioritized from specific to general
KEYWORDS = [
    ("air", "06-wireless-attacks;"),
    ("wifi", "06-wireless-attacks;"),
    ("bt", "06-wireless-attacks;"),
    ("blue", "06-wireless-attacks;"),
    ("wireless", "06-wireless-attacks;"),
    ("password", "05-password-attacks;"),
    ("crack", "05-password-attacks;"),
    ("hash", "05-password-attacks;"),
    ("exploit", "04-exploitation-tools;"),
    ("msf", "04-exploitation-tools;"),
    ("metasploit", "04-exploitation-tools;"),
    ("sniff", "09-sniffing-spoofing;"),
    ("spoof", "09-sniffing-spoofing;"),
    ("reverse", "07-reverseengineer;"),
    ("debug", "07-reverseengineer;"),
    ("web", "03-webapp-analysis;"),
    ("sql", "03-webapp-analysis;"),
    ("proxy", "03-webapp-analysis;"),
    ("network", "01-info-gathering;"),
    ("scan", "01-info-gathering;"),
    ("dns", "01-01-dns-analysis;01-info-gathering;"),
    ("osint", "01-07-osint-analysis;01-info-gathering;"),
    ("forensic", "11-forensics;"),
    ("sleuth", "11-forensics;"),
    ("volatility", "11-forensics;"),
    ("malware", "11-forensics;"),
    ("car", "13-automotive;"),
    ("can", "13-automotive;"),
    ("reporting", "12-reporting;"),
    ("evidence", "12-reporting;"),
    ("serv", "14-services;"),
    ("snmp", "01-info-gathering;"),
    ("ldap", "01-info-gathering;"),
    ("smb", "01-info-gathering;"),
    ("rdp", "01-info-gathering;"),
    ("mitm", "09-sniffing-spoofing;"),
    ("proxy", "03-webapp-analysis;"),
    ("fuzz", "02-vulnerability-analysis;"),
    ("cisco", "01-info-gathering;"),
    ("javasnoop", "07-reverseengineer;"),
    ("ghidra", "07-reverseengineer;"),
    ("apk", "07-reverseengineer;"),
    ("jadx", "07-reverseengineer;"),
]

DESKTOP_DIR = "files/desktop-files"

def remap_categories():
    if not os.path.exists(DESKTOP_DIR):
        print(f"Error: Directory {DESKTOP_DIR} not found.")
        return

    count = 0
    for filename in os.listdir(DESKTOP_DIR):
        if not filename.endswith(".desktop"):
            continue

        filepath = os.path.join(DESKTOP_DIR, filename)
        # Strip extension and common prefix
        tool_name = filename.replace(".desktop", "").lower()
        clean_name = tool_name.replace("ctxos-", "")
        
        with open(filepath, "r") as f:
            lines = f.readlines()

        found_category = None
        
        # 1. Check exact match in MAPPING
        if clean_name in MAPPING:
            found_category = MAPPING[clean_name]
        
        # 2. Check prefix match (e.g. nmap-gui -> nmap)
        if not found_category:
            for key in MAPPING:
                if clean_name.startswith(key):
                    found_category = MAPPING[key]
                    break
        
        # 3. Keyword match (anywhere in clean_name)
        if not found_category:
            for kw, cat in KEYWORDS:
                if kw in clean_name:
                    found_category = cat
                    break
        
        if found_category:
            new_lines = []
            category_set = False
            for line in lines:
                if line.startswith("Categories="):
                    # Ensure it includes the custom category + original
                    # Typically we replace or prepend. Here we set it precisely.
                    new_lines.append(f"Categories={found_category}\n")
                    category_set = True
                else:
                    new_lines.append(line)
            
            if not category_set:
                new_lines.append(f"Categories={found_category}\n")

            with open(filepath, "w") as f:
                f.writelines(new_lines)
            
            count += 1
            # print(f"Categorized {filename} -> {found_category}")

    print(f"✅ Successfully remapped categories for {count} desktop files.")

if __name__ == "__main__":
    remap_categories()
