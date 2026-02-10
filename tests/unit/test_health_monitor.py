from unittest.mock import Mock, patch

import pytest
from providers.health_monitor import HealthMonitor


@pytest.fixture
def monitor():
    return HealthMonitor()


@pytest.fixture
def mock_psutil():
    with patch("providers.health_monitor.psutil") as mock:
        yield mock


def test_get_system_metrics(monitor, mock_psutil):
    # Setup mocks
    mock_psutil.cpu_percent.return_value = 45.0
    mock_psutil.virtual_memory.return_value = Mock(
        total=16000000000, available=8000000000, percent=50.0, used=8000000000
    )
    mock_psutil.disk_usage.return_value = Mock(
        total=100000000000, used=40000000000, free=60000000000, percent=40.0
    )
    mock_psutil.net_io_counters.return_value = Mock(bytes_sent=1000, bytes_recv=2000)

    metrics = monitor.get_system_metrics()

    assert metrics["cpu_percent"] == 45.0
    assert metrics["memory"]["percent"] == 50.0
    assert metrics["disk"]["percent"] == 40.0
    assert "timestamp" in metrics


def test_calculate_health_score_healthy(monitor, mock_psutil):
    # Setup mocks for healthy system
    mock_psutil.cpu_percent.return_value = 20.0
    mock_psutil.virtual_memory.return_value = Mock(percent=40.0, total=0, available=0, used=0)
    mock_psutil.disk_usage.return_value = Mock(percent=30.0, total=0, used=0, free=0)
    mock_psutil.net_io_counters.return_value = Mock(bytes_sent=0, bytes_recv=0)

    health = monitor.calculate_health_score()

    assert health["score"] == 100
    assert health["status"] == "healthy"
    assert len(health["penalties"]) == 0


def test_calculate_health_score_critical(monitor, mock_psutil):
    # Setup mocks for critical system
    mock_psutil.cpu_percent.return_value = 95.0  # Penalty: (95-80)*1.5 = 22
    mock_psutil.virtual_memory.return_value = Mock(
        percent=95.0, total=0, available=0, used=0
    )  # Penalty: (95-90)*2 = 10
    mock_psutil.disk_usage.return_value = Mock(percent=98.0, total=0, used=0, free=0)  # Penalty: 20
    mock_psutil.net_io_counters.return_value = Mock(bytes_sent=0, bytes_recv=0)

    # Score = 100 - 22 - 10 - 20 = 48
    health = monitor.calculate_health_score()

    assert health["score"] == 48  # Calculation verified
    assert health["status"] == "critical"
    assert len(health["penalties"]) == 3
