from unittest.mock import patch

import pytest
from api.actions import ActionManager


@pytest.fixture
def action_manager():
    with patch("api.actions.SnapshotProvider"), patch("api.actions.HealthChecker"):
        return ActionManager()


def test_install_apt(action_manager):
    with patch.object(ActionManager, "_run_command") as mock_run:
        mock_run.return_value = {"success": True, "output": "done"}
        res = action_manager.install("test-pkg")

        assert res["success"] is True
        mock_run.assert_called_once_with(["apt-get", "install", "-y", "test-pkg"])


def test_install_flatpak(action_manager):
    with patch.object(ActionManager, "_run_command") as mock_run:
        mock_run.return_value = {"success": True, "output": "done"}
        res = action_manager.install("org.example.App")

        assert res["success"] is True
        mock_run.assert_called_once_with(["flatpak", "install", "-y", "flathub", "org.example.App"])


def test_install_with_snapshot(action_manager):
    action_manager.snapshots.create_snapshot.return_value = {
        "success": True,
        "description": "snap1",
    }
    with patch.object(ActionManager, "_run_command") as mock_run:
        mock_run.return_value = {"success": True, "output": "done"}
        res = action_manager.install("test-pkg", use_snapshot=True)

        assert res["success"] is True
        action_manager.snapshots.create_snapshot.assert_called_once()


def test_remove_apt(action_manager):
    with patch.object(ActionManager, "_run_command") as mock_run:
        mock_run.return_value = {"success": True}
        action_manager.remove("test-pkg")
        mock_run.assert_called_once_with(["apt-get", "remove", "-y", "test-pkg"])
