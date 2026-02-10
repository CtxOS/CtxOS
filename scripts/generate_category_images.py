
import os
import glob
import re

# Paths
DESKTOP_FILES_DIR = "modules/menu/files/desktop-files"
DESKTOP_DIRS_DIR = "modules/menu/files/desktop-directories"
TOOLS_DIR = "containers/tools"

def parse_desktop_file(filepath):
    """Extracts Categories and X-Ctxos-Package from a .desktop file."""
    categories = []
    package = None
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if line.startswith("Categories="):
                cats = line.split("=", 1)[1]
                categories = [c for c in cats.split(";") if c]
            elif line.startswith("X-Ctxos-Package="):
                package = line.split("=", 1)[1]
    return categories, package

def parse_directory_file(filepath):
    """Extracts Name and returns filtering ID from filename."""
    name = "Unknown"
    filename = os.path.basename(filepath)
    category_id = filename.replace(".directory", "")
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.startswith("Name="):
                name = line.split("=", 1)[1].strip()
                break
    return category_id, name

def generate_dockerfile(category_id, friendly_name, packages):
    if not packages:
        return
    
    dir_path = os.path.join(TOOLS_DIR, category_id)
    os.makedirs(dir_path, exist_ok=True)
    
    dockerfile_content = f"""# CtxOS Tool Collection - {friendly_name}
# Category: {category_id}
# Automatically generated from CtxOS Menu Definitions

FROM ctxos/core

# Install tools for {friendly_name}
RUN apt-get update && \\
"""
    # Deduplicate packages
    unique_packages = sorted(list(set(packages)))
    
    # Blacklist of known problematic packages
    BLACKLIST = {
        "nikto", "radare2", "metasploit-framework", "burpsuite", "maltego",
        "nessus", "openvas", "cobaltstrike", "seclists", "exploitdb",
        "routersploit", "wifite", "airgeddon", "beef-xss", "bettercap",
        "bloodhound", "commix", "crackmapexec", "dirbuster", "empire",
        "faraday", "ferret", "gerix-wifi-cracker", "guymager", "kismet",
        "netdiscover", "ophcrack", "owasp-zap", "proxychains", "proxychains4",
        "recon-ng", "responder", "set", "skipfish", "sleuthkit", "spiderfoot",
        "theharvester", "volatility", "wpscan", "xplico", "yersinia",
        "zaproxy", "zenmap"
    }

    final_packages = []
    for pkg in unique_packages:
        if pkg in BLACKLIST:
            # print(f"Skipping blacklisted package: {pkg}")
            continue
        final_packages.append(pkg)

    if not final_packages:
        print(f"Skipping {category_id} (All packages blacklisted)")
        return

    # Use a loop to try installing each package individually (Best Effort)
    pkg_list_str = " ".join(final_packages)
    
    dockerfile_content += f"""    # Best-effort installation loop
    PACKAGES="{pkg_list_str}" && \\
    for pkg in $PACKAGES; do \\
        apt-get install -y --no-install-recommends "$pkg" || echo "⚠️  Failed to install $pkg (Safety fallback)"; \\
    done \\
    && rm -rf /var/lib/apt/lists/*
"""

    dockerfile_content += """
# Set default command
CMD ["/bin/bash"]
"""
    
    with open(os.path.join(dir_path, "Dockerfile"), "w") as f:
        f.write(dockerfile_content)
    print(f"Generated Dockerfile for {category_id} with {len(unique_packages)} packages.")

def main():
    # 1. Map Categories to Packages
    category_map = {} # category_id -> set(packages)
    
    desktop_files = glob.glob(os.path.join(DESKTOP_FILES_DIR, "*.desktop"))
    print(f"Found {len(desktop_files)} desktop files.")
    
    for df in desktop_files:
        cats, pkg = parse_desktop_file(df)
        if pkg:
            for cat in cats:
                if cat not in category_map:
                    category_map[cat] = set()
                category_map[cat].add(pkg)
    
    # 2. Process Desktop Directories
    directory_files = glob.glob(os.path.join(DESKTOP_DIRS_DIR, "*.directory"))
    print(f"Found {len(directory_files)} directory files.")
    
    if not directory_files:
        print("No directory files found. Checking path...")
        print(os.path.abspath(DESKTOP_DIRS_DIR))

    for df in directory_files:
        cat_id, name = parse_directory_file(df)
        
        # Check if we have packages for this category
        # The category ID in .directory filename usually matches the Category string in .desktop
        # Example: 01-info-gathering.directory -> Categories=01-info-gathering;
        
        if cat_id in category_map:
            packages = category_map[cat_id]
            generate_dockerfile(cat_id, name, list(packages))
        else:
            print(f"Skipping {cat_id} (No packages found)")

if __name__ == "__main__":
    main()
