import os
import json

class MetaProvider:
    """Handles meta-packages and system profiles (stacks)."""

    METAPACKAGE_PREFIX = "ctxos-"
    
    # Predefined profiles for the software center
    PROFILES = {
        "desktop": {
            "id": "ctxos-desktop",
            "name": "Desktop Environment",
            "description": "A full-featured desktop environment with productivity tools.",
            "type": "profile",
            "icon": "desktop-symbolic"
        },
        "server": {
            "id": "ctxos-server",
            "name": "Server Base",
            "description": "Minimal server environment with core networking and security tools.",
            "type": "profile",
            "icon": "server-symbolic"
        },
        "dev": {
            "id": "ctxos-dev",
            "name": "Development Stack",
            "description": "Compilers, debuggers, and essential development libraries.",
            "type": "profile",
            "icon": "builder-symbolic"
        },
        "security-web": {
            "id": "ctxos-tools-web",
            "name": "Web Security Stack",
            "description": "Comprehensive tools for web application assessment and exploitation.",
            "type": "profile",
            "icon": "network-wired-symbolic"
        },
        "security-wireless": {
            "id": "ctxos-tools-wireless",
            "name": "Wireless Auditing Stack",
            "description": "Tools for WiFi, Bluetooth, and RF security research.",
            "type": "profile",
            "icon": "network-wireless-symbolic"
        },
        "security-forensics": {
            "id": "ctxos-tools-forensics",
            "name": "Digital Forensics Stack",
            "description": "Evidence collection, file carving, and memory analysis utilities.",
            "type": "profile",
            "icon": "drive-harddisk-symbolic"
        },
        "security-reversing": {
            "id": "ctxos-tools-reversing",
            "name": "Reverse Engineering Stack",
            "description": "Disassemblers, decompilers, and binary analysis frameworks.",
            "type": "profile",
            "icon": "emblem-system-symbolic"
        },
        "security-automotive": {
            "id": "ctxos-tools-automotive",
            "name": "Automotive Security Stack",
            "description": "Specialized tools for CAN bus analysis and automotive security research.",
            "type": "profile",
            "icon": "car-symbolic"
        }
    }

    def __init__(self, apt_provider):
        self.apt = apt_provider

    def list_profiles(self):
        """Returns the list of available profiles with their status."""
        profiles = []
        for p_id, p_info in self.PROFILES.items():
            pkg_id = p_info["id"]
            is_installed = self.apt.is_installed(pkg_id)
            
            profile_data = p_info.copy()
            profile_data["installed"] = is_installed
            
            # Fetch extra metadata if available from APT
            apt_info = self.apt.get_package_info(pkg_id)
            if apt_info:
                profile_data["version"] = apt_info.get("Version", "N/A")
                profile_data["size"] = apt_info.get("Installed-Size", "N/A")
                if "Description" in apt_info and not profile_data["description"]:
                    profile_data["description"] = apt_info["Description"]
            
            profiles.append(profile_data)
        return profiles

    def get_meta_packages(self):
        """Discovers meta-packages in the repo following the prefix."""
        # This would normally search the APT cache for our prefix
        pkgs = self.apt.list_packages(self.METAPACKAGE_PREFIX)
        meta_pkgs = []
        for pkg in pkgs:
            # Avoid duplicating profiles already defined
            if any(p["id"] == pkg for p in self.PROFILES.values()):
                continue
                
            info = self.apt.get_package_info(pkg)
            if info:
                meta_pkgs.append({
                    "id": pkg,
                    "name": info.get("Name", pkg.replace(self.METAPACKAGE_PREFIX, "").title()),
                    "description": info.get("Description", ""),
                    "installed": self.apt.is_installed(pkg),
                    "type": "stack",
                    "repo": info.get("Origin", "ctxos")
                })
        return meta_pkgs
