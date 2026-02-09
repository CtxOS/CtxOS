import subprocess
import os
import logging
from providers.snapshot import SnapshotProvider
from api.health import HealthChecker

logger = logging.getLogger("ctxos.actions")

class ActionManager:
    """Handles installation and removal of packages with safety guards."""

    def __init__(self):
        self.snapshots = SnapshotProvider()
        self.health = HealthChecker()

    def install(self, package_id, use_snapshot=False):
        """Installs a package using APT or Flatpak."""
        snapshot_desc = None
        if use_snapshot:
            res = self.snapshots.create_snapshot(f"Installing {package_id}")
            if res["success"]:
                snapshot_desc = res["description"]

        if "." in package_id and not package_id.startswith("debian-base"):
            # Assume it's a flatpak
            cmd = ["flatpak", "install", "-y", "flathub", package_id]
        else:
            cmd = ["apt-get", "install", "-y", package_id]
        
        result = self._run_command(cmd)
        
        # If install failed and we have a snapshot, we could rollback or just report
        if not result["success"] and snapshot_desc:
            logger.error(f"Install failed. Snapshot {snapshot_desc} is available for manual rollback.")

        return result

    def remove(self, package_id):
        """Removes a package using APT or Flatpak."""
        if "." in package_id and not package_id.startswith("debian-base"):
            cmd = ["flatpak", "uninstall", "-y", package_id]
        else:
            cmd = ["apt-get", "remove", "-y", package_id]
        return self._run_command(cmd)

    def update_cache(self):
        """Updates APT and Flatpak cache."""
        # For APT
        self._run_command(["apt-get", "update"])
        # For Flatpak
        return self._run_command(["flatpak", "update", "--appstream"])

    def _run_command(self, cmd):
        """Runs a system command and returns status."""
        try:
            # We use env to ensure non-interactive
            env = os.environ.copy()
            env["DEBIAN_FRONTEND"] = "noninteractive"
            
            # Using Popen to eventually support progress tracking
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=env
            )
            
            # For Phase 1, we just wait and return output
            # Phase 2 will involve streaming this to the UI
            stdout, stderr = process.communicate()
            
            return {
                "success": process.returncode == 0,
                "output": stdout,
                "exit_code": process.returncode
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
