import os
import sys

import structlog
from flask import Flask, jsonify, request

# Add parent directory to path to allow imports from sibling modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.actions import ActionManager  # noqa: E402
from api.apps import AppManager  # noqa: E402
from api.health import HealthChecker  # noqa: E402
from api.profile_recommender import ProfileRecommender  # noqa: E402
from common.errors import (  # noqa: E402
    DependencyError,
    InstallationError,
    NotFoundError,
    handle_error,
)
from common.logger import configure_logging  # noqa: E402
from providers.dependency_resolver import DependencyResolver  # noqa: E402
from providers.health_monitor import HealthMonitor  # noqa: E402
from providers.offline_mirror import OfflineMirrorManager  # noqa: E402

# Initialize structured logging
configure_logging()
logger = structlog.get_logger("ctxos.api")

app = Flask(__name__)

# Managers
apps = AppManager()
actions = ActionManager()
health = HealthChecker()
resolver = DependencyResolver()
monitor = HealthMonitor()
mirror = OfflineMirrorManager()
recommender = ProfileRecommender()


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found", "code": "NOT_FOUND"}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error", "code": "INTERNAL_ERROR"}), 500


@app.route("/")
def root():
    return jsonify({"message": "CtxOS REST API Gateway operational"})


@app.route("/api/v1/packages", methods=["GET"])
def list_packages():
    """Lists available packages, optionally filtered by category."""
    try:
        category = request.args.get("category")
        logger.info("listing_packages", category=category)
        return jsonify(apps.get_all_apps(category=category))
    except Exception as e:
        return handle_error(e)


@app.route("/api/v1/packages/<package_id>", methods=["GET"])
def get_package_details(package_id):
    """Gets detailed info for a package."""
    try:
        logger.info("getting_details", package_id=package_id)
        details = apps.get_app_details(package_id)
        if not details:
            raise NotFoundError("Package", package_id)
        return jsonify(details)
    except Exception as e:
        return handle_error(e)


@app.route("/api/v1/packages/<package_id>/install", methods=["POST"])
def install_package(package_id):
    """Installs a package."""
    try:
        use_snapshot = request.args.get("use_snapshot", "false").lower() == "true"
        logger.info("install_request", package_id=package_id, use_snapshot=use_snapshot)

        # Pre-check dependencies
        resolution = resolver.resolve(package_id)
        if resolution.get("missing"):
            logger.warning("dependency_check_failed", missing=resolution["missing"])
            raise DependencyError(
                "Missing dependencies", context={"missing": resolution["missing"]}
            )

        result = actions.install(package_id, use_snapshot=use_snapshot)
        if not result["success"]:
            logger.error("install_failed", output=result.get("output"))
            raise InstallationError(
                "Installation failed", context={"output": result.get("output", "")}
            )

        logger.info("install_success", package_id=package_id)
        return jsonify(result)
    except Exception as e:
        return handle_error(e)


@app.route("/api/v1/system/health", methods=["GET"])
def get_system_health():
    """Returns system health status."""
    return jsonify(monitor.calculate_health_score())


@app.route("/api/v1/profiles", methods=["GET"])
def list_profiles():
    """Lists available system profiles."""
    return jsonify(apps.meta.list_profiles())


@app.route("/api/v1/recommendations", methods=["GET"])
def get_recommendations():
    """Gets AI-driven profile recommendations."""
    return jsonify(recommender.recommend())


@app.route("/api/v1/system/mirror", methods=["GET"])
def get_mirror_status():
    """Returns status of local mirror."""
    try:
        return jsonify(mirror.get_status())
    except Exception as e:
        return handle_error(e)


@app.route("/api/v1/system/mirror/sync", methods=["POST"])
def sync_mirror():
    """Triggers mirror sync."""
    try:
        data = request.json if request.is_json else {}
        packages = data.get("packages")
        result = mirror.sync(package_list=packages)
        return jsonify(result)
    except Exception as e:
        return handle_error(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
