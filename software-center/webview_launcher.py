#!/usr/bin/env python3
import os
import sys
import json
import webview

# Add parent directory to path to import API
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Attempt to connect to DBus Service, fallback to direct API
try:
    from pydbus import SessionBus
    bus = SessionBus()
    dbus_service = bus.get("org.ctxos.SoftwareCenter")
    HAS_DBUS = True
except Exception:
    HAS_DBUS = False
    from backend.api.apps import AppManager
    from backend.api.actions import ActionManager
    direct_apps = AppManager()
    direct_actions = ActionManager()

class APIBridge:
    """Methods in this class are exposed to JavaScript via window.pywebview.api"""
    
    def call_backend(self, action, params):
        print(f"Webview Request: {action}({params})")
        
        if HAS_DBUS:
            if action == 'list_featured':
                return json.loads(dbus_service.ListFeatured())
            elif action == 'get_details':
                return json.loads(dbus_service.GetAppDetails(params.get('id')))
            elif action == 'search':
                return json.loads(dbus_service.SearchApps(params.get('query')))
            elif action == 'install':
                return json.loads(dbus_service.Install(params.get('id')))
            elif action == 'remove':
                return json.loads(dbus_service.Remove(params.get('id')))
            elif action == 'switch_profile':
                return json.loads(dbus_service.SwitchProfile(params.get('id')))
            elif action == 'get_translations':
                return direct_apps.get_translations()
            elif action == 'get_branding':
                return direct_apps.get_branding()
        else:
            # Fallback for local development
            if action == 'list_featured':
                return direct_apps.get_featured_apps()
            elif action == 'get_details':
                return direct_apps.get_app_details(params.get('id'))
            elif action == 'get_translations':
                return direct_apps.get_translations()
            elif action == 'get_branding':
                return direct_apps.get_branding()
            elif action == 'search':
                return direct_apps.search_apps(params.get('query'))
            elif action == 'install':
                return direct_actions.install(params.get('id'))
            elif action == 'remove':
                return direct_actions.remove(params.get('id'))
            elif action == 'switch_profile':
                return direct_apps.profiles.switch_profile(params.get('id'))
        
        return {"error": "Unknown action"}

    def set_window(self, window):
        self.window = window

    def notify_updates(self, count):
        if self.window:
            self.window.evaluate_js(f"if(window.showUpdateNotification) window.showUpdateNotification({count});")

def start_webview():
    api = APIBridge()
    
    # In a real app, we'd subscribe to the DBus signal
    # For now, let's just use the monitor if available
    from api.update_monitor import UpdateMonitor
    monitor = UpdateMonitor(api.notify_updates, interval=1800)
    monitor.start()

    web_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
    index_path = os.path.join(web_dir, "index.html")
    
    window = webview.create_window(
        'CtxOS Software Center', 
        url=index_path,
        js_api=api,
        width=1100,
        height=750,
        background_color='#0f172a'
    )
    api.set_window(window)
    
    # Check if DEBUG environment variable is set
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    webview.start(debug=debug_mode)

if __name__ == "__main__":
    start_webview()
