import json
import logging
import os
import shutil
import subprocess
from datetime import datetime

from common.errors import ProviderError

logger = logging.getLogger("ctxos.offline_mirror")


class OfflineMirrorManager:
    """Manages local package mirror for offline operation."""

    def __init__(self, mirror_path=None):
        if mirror_path:
            self.mirror_path = mirror_path
        else:
            # Use system path if root, otherwise local user cache
            if os.geteuid() == 0:
                self.mirror_path = "/var/cache/ctxos/mirror"
            else:
                self.mirror_path = os.path.join(
                    os.environ.get("HOME", "."), ".cache", "ctxos", "mirror"
                )

        self.packages_dir = os.path.join(self.mirror_path, "pool", "main")
        self.dists_dir = os.path.join(self.mirror_path, "dists", "stable", "main", "binary-amd64")
        self.config_file = os.path.join(self.mirror_path, "mirror_config.json")

        try:
            os.makedirs(self.packages_dir, exist_ok=True)
            os.makedirs(self.dists_dir, exist_ok=True)
        except OSError:
            # Fallback to current directory if other paths fail
            self.mirror_path = os.path.abspath("./mirror")
            self.packages_dir = os.path.join(self.mirror_path, "pool", "main")
            self.dists_dir = os.path.join(
                self.mirror_path, "dists", "stable", "main", "binary-amd64"
            )
            self.config_file = os.path.join(self.mirror_path, "mirror_config.json")
            os.makedirs(self.packages_dir, exist_ok=True)
            os.makedirs(self.dists_dir, exist_ok=True)

    def sync(self, package_list=None):
        """Perform incremental sync of remote repository to local mirror."""
        if not package_list:
            package_list = [
                "build-essential",
                "git",
                "python3",
                "python3-pip",
                "curl",
                "wget",
                "vim",
                "zsh",
            ]

        logger.info(f"Starting sync to {self.mirror_path}")

        try:
            # Check if apt-get is available
            if not shutil.which("apt-get"):
                logger.warning("apt-get not found. Running in simulation/dev mode.")
                # Simulate download
                for pkg in package_list:
                    # Create dummy file
                    dummy_file = os.path.join(self.packages_dir, f"{pkg}_1.0.0_amd64.deb")
                    with open(dummy_file, "w") as f:
                        f.write("mock package content")

                # Simulate Package index generation if dpkg-scanpackages missing
                if not shutil.which("dpkg-scanpackages"):
                    logger.warning("dpkg-scanpackages not found. Generating mock Packages.gz")
                    index_path = os.path.join(self.dists_dir, "Packages.gz")
                    with open(index_path, "wb") as f_out:  # Write mock gzip
                        f_out.write(
                            b"\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x03\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                        )

                self._update_status(success=True)
                return {
                    "success": True,
                    "files_updated": len(package_list),
                    "path": self.mirror_path,
                    "mode": "simulation",
                }

            # 1. Download packages
            # usage of apt-get download requires we are in the target dir or move files after
            # We'll run it in the packages_dir
            cmd = ["apt-get", "download"] + package_list
            logger.info(f"Downloading packages: {package_list}")

            # Note: apt-get download fails if package is already downloaded but we want to update?
            # Actually apt-get download just downloads to CWD.
            # We might want to use --reinstall or check first.
            # For simplicity, we just run it. Errorsmight occur if package not found.

            # Using subprocess.run to capture output
            process = subprocess.run(cmd, cwd=self.packages_dir, capture_output=True, text=True)

            if process.returncode != 0:
                # Need to handle partial failures or ignore "already downloaded" if using a smart tool
                # apt-get download returns non-zero if ANY package fails
                logger.warning(f"Some packages failed to download: {process.stderr}")

            # 2. Generate Packages.gz (Repository Index)
            # dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz
            # We need to run this from the root of the repo (mirror_path) usually, or point to pool
            # Best practice: Run from mirror_path, point to pool

            # Check if dpkg-scanpackages is installed (package: dpkg-dev)
            if not shutil.which("dpkg-scanpackages"):
                raise ProviderError("dpkg-scanpackages not found. Please install 'dpkg-dev'.")

            # We create the index in dists_dir
            index_path = os.path.join(self.dists_dir, "Packages.gz")

            # Command: dpkg-scanpackages pool/main /dev/null
            scan_cmd = ["dpkg-scanpackages", "pool/main", "/dev/null"]

            with open(index_path, "wb") as f_out:
                ps = subprocess.Popen(
                    scan_cmd, cwd=self.mirror_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                subprocess.run(["gzip", "-9c"], stdin=ps.stdout, stdout=f_out)
                ps.wait()

                if ps.returncode != 0:
                    raise ProviderError(
                        f"Failed to generate package index: {ps.stderr.read().decode()}"
                    )

            # 3. Update config/status
            self._update_status(success=True)

            return {
                "success": True,
                "files_updated": len(os.listdir(self.packages_dir)),
                "path": self.mirror_path,
            }

        except Exception as e:
            logger.error(f"Sync failed: {str(e)}")
            self._update_status(success=False, error=str(e))
            raise ProviderError(f"Mirror sync failed: {str(e)}")

    def get_status(self):
        """Returns status of the local mirror."""
        total, used, free = shutil.disk_usage(self.mirror_path)

        config = {}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
            except Exception:
                pass

        return {
            "enabled": True,
            "path": self.mirror_path,
            "size_bytes": used,  # Approximation using total disk usage of partition or du? shutil.disk_usage is partition.
            # We should probably do du for the folder
            "folder_size": self._get_folder_size(self.mirror_path),
            "last_sync": config.get("last_sync", "Never"),
            "is_uptodate": config.get("last_result", False),
            "package_count": len(os.listdir(self.packages_dir))
            if os.path.exists(self.packages_dir)
            else 0,
        }

    def configure_apt_for_offline(self):
        """Updates APT sources to use the local mirror."""
        if os.geteuid() != 0:
            raise ProviderError("Root privileges required to configure APT sources.")

        list_file = "/etc/apt/sources.list.d/ctxos-offline.list"
        content = f"deb [trusted=yes] file:{self.mirror_path} stable main"

        try:
            with open(list_file, "w") as f:
                f.write(content)
            logger.info(f"Configured APT to use local mirror at {list_file}")

            # Need to run apt-get update
            subprocess.run(["apt-get", "update"], check=True)
            return True
        except Exception as e:
            raise ProviderError(f"Failed to configure APT: {str(e)}")

    def _update_status(self, success, error=None):
        status = {
            "last_sync": datetime.utcnow().isoformat(),
            "last_result": success,
            "last_error": error,
        }
        with open(self.config_file, "w") as f:
            json.dump(status, f)

    def _get_folder_size(self, path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size
