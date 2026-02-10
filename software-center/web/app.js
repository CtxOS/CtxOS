document.addEventListener('DOMContentLoaded', () => {
    // Wait for pywebview to be ready if it's there
    if (window.pywebview) {
        window.addEventListener('pywebviewready', init);
    } else {
        init();
    }
});

let i18n = {};
let branding = {};

async function init() {
    const featuredGrid = document.getElementById('featured-grid');
    const homePage = document.getElementById('home-page');
    const detailsPage = document.getElementById('details-page');
    const backBtn = document.querySelector('.back-btn');
    const searchInput = document.getElementById('search-input');
    const settingsPage = document.getElementById('settings-page');

    // Load Translations & Branding
    i18n = await API.fetch('get_translations');
    branding = await API.fetch('get_branding');

    applyBranding();
    applyTranslations();

    // Initial Load: Featured Apps
    const apps = await API.fetch('list_featured');
    renderApps(apps);

    // Simple Onboarding
    if (!localStorage.getItem('onboarded')) {
        document.querySelector('.content').scrollTop = 0;
        localStorage.setItem('onboarded', 'true');
    }

    function applyBranding() {
        if (!branding.primary_color) return;

        const root = document.documentElement;
        root.style.setProperty('--accent-color', branding.primary_color);
        root.style.setProperty('--accent-glow', branding.primary_color + '44');

        if (branding.name) {
            document.querySelector('.sidebar h1').textContent = branding.name;
            document.title = branding.name + " Software Center";
        }
    }

    function applyTranslations() {
        if (!i18n.ui) return;
        searchInput.placeholder = i18n.ui.search_placeholder;
        document.getElementById('home-view-title').textContent = i18n.ui.featured_title;
        document.getElementById('nav-updates-text').textContent = i18n.ui.updates_title;
        document.getElementById('nav-settings-text').textContent = i18n.ui.settings_title;
        document.querySelector('#settings-page h1').textContent = i18n.ui.settings_title;
    }

    function renderApps(appsList) {
        featuredGrid.innerHTML = '';
        if (appsList.length === 0) {
            featuredGrid.innerHTML = '<p class="status">No results found.</p>';
            return;
        }

        appsList.forEach(app => {
            const card = document.createElement('div');
            card.className = 'app-card';
            const typeLabel = app.type === 'flatpak' ? '<span class="type-badge">Flatpak</span>' : '';
            card.innerHTML = `
                <div class="icon">${app.icon || '📦'}</div>
                <h3>${app.name}</h3>
                ${typeLabel}
                <div class="status ${app.installed ? 'installed' : ''}">
                    ${app.installed ? '✓ Installed' : 'Ready to Install'}
                </div>
            `;
            card.onclick = () => showDetails(app.id);
            featuredGrid.appendChild(card);
        });
    }

    async function showDetails(appId) {
        document.querySelector('.content').scrollTop = 0;
        const app = await API.fetch('get_details', { id: appId });

        document.getElementById('details-name').textContent = app.name;
        document.getElementById('details-desc').textContent = app.description || "No description available.";
        document.getElementById('details-version').textContent = `Version: ${app.version || 'unknown'}`;
        document.getElementById('details-size').textContent = `Size: ${app.size || 'unknown'}`;
        document.getElementById('details-repo').textContent = app.repo || 'ctxos';

        // Screenshots
        const detailsMain = document.querySelector('.details-main');
        let gallery = document.getElementById('screenshot-gallery');
        if (!gallery) {
            gallery = document.createElement('div');
            gallery.id = 'screenshot-gallery';
            gallery.className = 'screenshot-gallery';
            detailsMain.insertBefore(gallery, document.querySelector('.details-content'));
        }
        gallery.innerHTML = '';
        if (app.screenshots && app.screenshots.length > 0) {
            app.screenshots.forEach(src => {
                const img = document.createElement('img');
                img.src = src;
                img.className = 'screenshot-item';
                gallery.appendChild(img);
            });
        }

        // Action Button & Profiles
        const installBtn = document.getElementById('install-btn');
        const detailsBody = document.querySelector('.details-body');
        let migrationInfo = document.getElementById('migration-info');

        if (app.can_switch) {
            installBtn.textContent = i18n.ui.switch_profile;
            installBtn.className = 'primary-btn highlight-btn';

            if (!migrationInfo) {
                migrationInfo = document.createElement('div');
                migrationInfo.id = 'migration-info';
                migrationInfo.className = 'migration-card';
                detailsBody.insertBefore(migrationInfo, document.querySelector('.details-content'));
            }

            migrationInfo.innerHTML = `
                <div class="migration-header">
                    <span class="risk-badge risk-${app.migration.risk}">${app.migration.risk}</span>
                    <h3>${i18n.ui.migration_details}</h3>
                </div>
                <div class="protection-badge">
                    <span>${i18n.ui.protection_active}</span>
                    <small>${i18n.ui.protection_desc}</small>
                </div>
                <p>${app.migration.message || 'This will switch your system environment.'}</p>
                <ul>
                    ${app.migration.to_remove.map(name => `<li class="remove-item">Remove: ${name}</li>`).join('')}
                    ${app.migration.to_install.map(name => `<li class="install-item">Install: ${name}</li>`).join('')}
                </ul>
            `;
            migrationInfo.classList.remove('hidden');
        } else {
            installBtn.textContent = app.installed ? i18n.ui.remove : i18n.ui.install;
            installBtn.className = app.installed ? 'secondary-btn' : 'primary-btn';
            if (migrationInfo) migrationInfo.classList.add('hidden');
        }

        installBtn.onclick = async () => {
            installBtn.textContent = app.can_switch ? i18n.ui.create_snapshot : 'Processing...';
            installBtn.disabled = true;
            if (app.can_switch) {
                setTimeout(() => { if (installBtn.disabled) installBtn.textContent = i18n.ui.apply_changes; }, 3000);
            }
            await API.fetch(app.can_switch ? 'switch_profile' : (app.installed ? 'remove' : 'install'), { id: appId });
            showDetails(appId);
        };

        homePage.classList.add('hidden');
        settingsPage.classList.add('hidden');
        detailsPage.classList.remove('hidden');
    }

    backBtn.onclick = () => {
        detailsPage.classList.add('hidden');
        homePage.classList.remove('hidden');
        refreshHome();
    };

    async function refreshHome() {
        const apps = await API.fetch('list_featured');
        renderApps(apps);

        // Fetch Parallel Data
        const health = await API.fetch('get_health');
        const mirror = await API.fetch('get_repo_status');
        const recommendations = await API.fetch('get_recommendations');

        renderHealth(health);
        renderRecommendations(recommendations);
        renderMirrorStatus(mirror);
    }

    function renderHealth(health) {
        if (!health) return;

        let container = document.getElementById('health-widget');
        if (!container) {
            container = document.createElement('div');
            container.id = 'health-widget';
            container.className = 'health-card';
            // Insert before featured grid
            featuredGrid.parentNode.insertBefore(container, featuredGrid);
        }

        const scoreColor = health.score > 80 ? 'var(--success)' : health.score > 50 ? '#f59e0b' : 'var(--danger)';

        container.innerHTML = `
            <div class="health-header">
                <h3>System Health</h3>
                <div class="health-score" style="color: ${scoreColor}">${health.score}/100</div>
            </div>
            <div class="health-metrics">
                <div class="metric">
                    <span>CPU</span>
                    <div class="bar-bg"><div class="bar-fill" style="width: ${health.metrics.cpu_percent}%"></div></div>
                </div>
                <div class="metric">
                    <span>RAM</span>
                    <div class="bar-bg"><div class="bar-fill" style="width: ${health.metrics.memory.percent}%"></div></div>
                </div>
                <div class="metric">
                    <span>Disk</span>
                    <div class="bar-bg"><div class="bar-fill" style="width: ${health.metrics.disk.percent}%"></div></div>
                </div>
            </div>
        `;
    }

    function renderRecommendations(recs) {
        if (!recs || recs.length === 0) return;

        let section = document.getElementById('recommendations-section');
        if (!section) {
            section = document.createElement('section');
            section.id = 'recommendations-section';
            section.innerHTML = '<h2>AI Recommendations</h2><div class="app-grid" id="recs-grid"></div>';
            featuredGrid.parentNode.insertBefore(section, featuredGrid);
        }

        const grid = document.getElementById('recs-grid');
        grid.innerHTML = '';

        recs.forEach(rec => {
            const card = document.createElement('div');
            card.className = 'app-card recommendation-card';
            card.innerHTML = `
                <div class="confidence-badge">${Math.round(rec.confidence * 100)}% Match</div>
                <div class="icon">✨</div>
                <h3>${rec.profile_id}</h3>
                <p class="reason">"${rec.reason}"</p>
                <button class="primary-btn small-btn">Apply Profile</button>
            `;
            grid.appendChild(card);
        });
    }

    function renderMirrorStatus(status) {
        // Update settings page
        if (status) {
            const el = document.getElementById('repo-status');
            if (el) el.textContent = status.enabled ? "Local Mirror Active" : "Online";
        }
    }

    // Search
    let searchTimeout;
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        const query = e.target.value;
        searchTimeout = setTimeout(async () => {
            if (!query) { refreshHome(); return; }
            const results = await API.fetch('search', { query });
            renderApps(results);
        }, 300);
    });

    // Navigation
    document.querySelectorAll('.sidebar li').forEach(li => {
        li.onclick = () => {
            document.querySelector('.sidebar li.active').classList.remove('active');
            li.classList.add('active');
            const page = li.getAttribute('data-page');

            homePage.classList.add('hidden');
            detailsPage.classList.add('hidden');
            settingsPage.classList.add('hidden');

            if (page === 'home') {
                homePage.classList.remove('hidden');
                refreshHome();
            } else if (page === 'settings') {
                settingsPage.classList.remove('hidden');
                showSettings();
            } else if (page === 'updates') {
                const badge = li.querySelector('.update-badge');
                if (badge) badge.remove();
            }
        };
    });

    async function showSettings() {
        const mirror = await API.fetch('get_repo_status');

        document.getElementById('repo-primary').textContent = mirror.path || "Debian Main";
        document.getElementById('repo-status').textContent = mirror.enabled ? "Offline Mirror" : "Online";

        document.getElementById('repo-priority-badge').style.display = 'block';
        document.getElementById('repo-priority-badge').textContent = mirror.is_uptodate ? "Synced" : "Sync Required";

        document.getElementById('repo-primary-label').textContent = i18n.ui.repo_primary;
        document.getElementById('repo-status-label').textContent = i18n.ui.repo_status;
    }

    window.showUpdateNotification = (count) => {
        const toast = document.createElement('div');
        toast.className = 'notification-toast';
        toast.innerHTML = `
            <span>🔄</span>
            <div>
                <strong>${i18n.alerts.updates_available}</strong>
                <p>${i18n.alerts.updates_desc.replace('{count}', count)}</p>
            </div>
        `;
        toast.onclick = () => {
            document.querySelector('[data-page="updates"]').click();
            toast.remove();
        };
        document.body.appendChild(toast);

        const updatesTab = document.querySelector('[data-page="updates"]');
        if (!updatesTab.querySelector('.update-badge')) {
            const badge = document.createElement('span');
            badge.className = 'update-badge';
            badge.textContent = count;
            updatesTab.appendChild(badge);
        }
        setTimeout(() => toast.remove(), 8000);
    };
}
