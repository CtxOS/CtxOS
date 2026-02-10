/**
 * API Client Bridge
 * Handles communication between the Web UI and the Python Backend.
 */
const API = {
    async fetch(action, params = {}) {
        console.log(`[UI] Calling ${action}`, params);

        // Map actions to REST endpoints
        const endpoints = {
            'list_featured': '/api/v1/profiles',
            'get_details': `/api/v1/packages/${params.id}`,
            'search': `/api/v1/packages?search=${params.query}`,
            'install': `/api/v1/packages/${params.id}/install`,
            'remove': `/api/v1/packages/${params.id}/install`, // DELETE method in real REST, but using same endpoint for now
            'get_repo_status': '/api/v1/system/mirror',
            'get_health': '/api/v1/system/health',
            'get_recommendations': '/api/v1/recommendations'
        };

        const url = endpoints[action];

        if (url) {
            try {
                const method = action === 'install' ? 'POST' : 'GET';
                // Note: Connects to local REST API
                const response = await fetch(`http://127.0.0.1:8000${url}`, {
                    method: method
                });
                return await response.json();
            } catch (err) {
                console.error("REST Error:", err);
                // Fallback for demo if API is down
            }
        }

        // Use pywebview bridge if available
        if (window.pywebview && window.pywebview.api) {
            try {
                return await window.pywebview.api.call_backend(action, params);
            } catch (err) {
                console.error("Bridge Error:", err);
                return { success: false, error: err.message };
            }
        }

        // Fallback for browser-only development (simulating bridge)
        return new Promise(resolve => {
            setTimeout(() => {
                if (action === 'list_featured') {
                    resolve([
                        { id: 'debian-base-desktop', name: 'Desktop Environment', type: 'profile', icon: '🖥️', description: 'Full desktop stack', installed: false },
                        { id: 'debian-base-server', name: 'Server Base', type: 'profile', icon: '☁️', description: 'Minimal server environment', installed: false },
                        { id: 'debian-base-dev', name: 'Development Stack', type: 'profile', icon: '🛠️', description: 'Development tools', installed: true }
                    ]);
                } else if (action === 'get_details') {
                    resolve({
                        id: params.id,
                        name: params.id.split('-').pop().toUpperCase(),
                        repo: 'ctxos-base-kit',
                        description: `Detailed view for ${params.id}. This is a critical system profile for CtxOS.`,
                        version: '1.2.0-stable',
                        size: '512 MB',
                        installed: params.id === 'debian-base-dev'
                    });
                } else if (action === 'get_translations') {
                    resolve({
                        ui: { search_placeholder: "Search mocks...", featured_title: "Featured Mocks", updates_title: "Updates", settings_title: "Settings", migration_details: "Migration", switch_profile: "Switch", remove: "Remove", install: "Install", create_snapshot: "Snapshot...", apply_changes: "Applying...", protection_active: "Protected", protection_desc: "Auto-snapshot active", repo_primary: "Main Repo", repo_status: "Status", repo_priority: "Priority" },
                        alerts: { updates_available: "Updates!", updates_desc: "{count} updates found." }
                    });
                } else if (action === 'get_repo_status') {
                    resolve({ primary: "repo.mock.org", status: "online", priority_enforced: true });
                } else {
                    resolve({ success: true });
                }
            }, 300);
        });
    }
};
