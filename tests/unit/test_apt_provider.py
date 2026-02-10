from unittest.mock import MagicMock, patch

import pytest
from providers.apt import AptProvider


@pytest.fixture
def apt_provider():
    return AptProvider()


def test_get_package_info_success(apt_provider):
    mock_output = "Package: test-pkg\nVersion: 1.2.3\nDescription: A test package\n"
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout=mock_output, check_returncode=MagicMock())
        info = apt_provider.get_package_info("test-pkg")

        assert info["Package"] == "test-pkg"
        assert info["Version"] == "1.2.3"
        assert "Description" in info


def test_get_package_info_mock_data(apt_provider):
    with patch("subprocess.run", side_effect=FileNotFoundError):
        info = apt_provider.get_package_info("ctxos-pkg")
        assert info["Package"] == "ctxos-pkg"
        assert info["Version"] == "1.0.0"


def test_is_installed_true(apt_provider):
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="install ok installed")
        assert apt_provider.is_installed("test-pkg") is True


def test_is_installed_false(apt_provider):
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="unknown ok not-installed")
        assert apt_provider.is_installed("test-pkg") is False


def test_list_packages(apt_provider):
    mock_output = "pkg1\npkg2\npkg3\n"
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout=mock_output)
        packages = apt_provider.list_packages()
        assert packages == ["pkg1", "pkg2", "pkg3"]
