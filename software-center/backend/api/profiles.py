import os
import json
import logging
from api.actions import ActionManager
from providers.snapshot import SnapshotProvider
from api.health import HealthChecker

logger = logging.getLogger("ctxos.profiles")

class ProfileSwitcher:
    """Handles migration and switching between system profiles."""

    def __init__(self, apt_provider, meta_provider):
        self.apt = apt_provider
        self.meta = meta_provider
        self.actions = ActionManager()
        self.snapshots = SnapshotProvider()
        self.health = HealthChecker()

    def get_active_profile(self):
        """Identifies the currently active profile."""
        profiles = self.meta.list_profiles()
        for p in profiles:
            if p["installed"]:
                return p
        return None

    def switch_profile(self, target_profile_id):
        """
        Switches the system from current profile to the target.
        This often involves removing conflicting packages.
        """
        current = self.get_active_profile()
        
        # 1. Create Restore Point
        snapshot_res = self.snapshots.create_snapshot(f"Switching to {target_profile_id}")
        if not snapshot_res["success"] and self.snapshots.tool != "mock":
            return {
                "success": False,
                "error": f"Failed to create system restore point: {snapshot_res.get('error')}",
                "stage": "snapshot"
            }

        operations = []
        if current and current["id"] != target_profile_id:
            # We have a conflict, need to remove current first
            # In a real distro, we might want to keep user data
            operations.append({"action": "remove", "id": current["id"]})
        
        operations.append({"action": "install", "id": target_profile_id})
        
        results = []
        for op in operations:
            if op["action"] == "remove":
                res = self.actions.remove(op["id"])
            else:
                res = self.actions.install(op["id"])
            results.append(res)
            
        success = all(r["success"] for r in results)
        
        # 3. Post-Migration Health Check
        if success:
            health_res = self.health.check_health()
            if not health_res["healthy"]:
                logger.error(f"System Unhealthy after migration: {health_res['errors']}")
                # We could trigger auto-rollback here
                # self.snapshots.restore_snapshot(snapshot_res["description"])
                return {
                    "success": False,
                    "error": "System became unhealthy after migration.",
                    "details": health_res["errors"],
                    "stage": "post-health"
                }

        return {
            "success": success,
            "steps": results
        }

    def get_migration_impact(self, target_profile_id):
        """Calculates what will be added/removed during a switch."""
        current = self.get_active_profile()
        impact = {
            "to_remove": [current["name"]] if current else [],
            "to_install": [target_profile_id],
            "risk": "low"
        }
        
        if current and "server" in current["id"] and "desktop" in target_profile_id:
            impact["message"] = "Migrating from Server to Desktop. This will install a GUI stack."
            impact["risk"] = "high"
        elif current and "desktop" in current["id"] and "server" in target_profile_id:
            impact["message"] = "Migrating from Desktop to Server. This will remove the GUI stack."
            impact["risk"] = "critical"
            
        return impact
