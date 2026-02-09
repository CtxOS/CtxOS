#!/usr/bin/env python3
import os
import sys
import json
import logging
from gi.repository import GLib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("ctxos.software-center")

# Try to import pydbus, if not available (Mac development), we'll mock the server logic
try:
    from pydbus import SessionBus
    HAS_PYDBUS = True
except ImportError:
    HAS_PYDBUS = False
    logger.warning("pydbus not found. This service requires a Linux environment with DBus.")

# Add parent directory to path to import API
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.apps import AppManager
from api.actions import ActionManager
from api.update_monitor import UpdateMonitor

class SoftwareCenterService:
    """
    DBus Service implementation for the Software Center.
    This class matches the interface.xml definition.
    """
    dbus = open(os.path.join(os.path.dirname(__file__), "interface.xml")).read()

    def __init__(self):
        self.app_manager = AppManager()
        self.action_manager = ActionManager()
        # Start background update monitor
        self.monitor = UpdateMonitor(self._on_updates_detected, interval=1800) # Check every 30 mins
        self.monitor.start()

    def _on_updates_detected(self, count):
        """Callback for the update monitor."""
        # This will eventually emit the DBus signal
        # We need a reference to the published object to emit signals if using pydbus
        logger.debug(f"Emitting UpdatesAvailable signal with count={count}")
        # In pydbus, signals are emitted by calling the signal name on the published object
        if hasattr(self, 'emit_updates_available'):
            self.emit_updates_available(count)

    def ListFeatured(self):
        return json.dumps(self.app_manager.get_featured_apps())

    def ListAll(self, category):
        return json.dumps(self.app_manager.get_all_apps(category))

    def GetAppDetails(self, app_id):
        return json.dumps(self.app_manager.get_app_details(app_id))

    def SearchApps(self, query):
        return json.dumps(self.app_manager.search_apps(query))

    def Install(self, app_id):
        # In production, this would be wrapped in a polkit check
        # For this prototype, we call the installer directly
        logger.info(f"Installing {app_id}...")
        result = self.action_manager.install(app_id)
        # Note: In a real async service, we'd emit signals during progress
        # and not return until polkit check passes.
        return json.dumps(result)

    def Remove(self, app_id):
        logger.info(f"Removing {app_id}...")
        result = self.action_manager.remove(app_id)
        return json.dumps(result)

    def SwitchProfile(self, app_id):
        logger.info(f"Switching system to profile: {app_id}")
        result = self.app_manager.profiles.switch_profile(app_id)
        # Ensure result has consistent keys for the bridge
        if not result.get("success") and "error" not in result:
            result["error"] = "Profile switch failed at stage: " + result.get("stage", "unknown")
        return json.dumps(result)

    def Update(self):
        logger.info("Updating system cache...")
        result = self.action_manager.update_cache()
        return json.dumps(result)

def run_service():
    if not HAS_PYDBUS:
        logger.info("Mocking service start for development...")
        return

    bus = SessionBus()
    bus.publish("org.ctxos.SoftwareCenter", SoftwareCenterService())
    
    logger.info("Software Center DBus Service is running...")
    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        loop.quit()

if __name__ == "__main__":
    run_service()
