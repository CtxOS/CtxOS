import datetime
import logging

import psutil

logger = logging.getLogger("ctxos.health_monitor")


class HealthMonitor:
    """Collects system metrics and calculates overall health score."""

    def __init__(self):
        pass

    def get_system_metrics(self):
        """Returns current CPU, Memory, Disk, and Network usage."""
        return {
            "cpu_percent": psutil.cpu_percent(interval=None),
            "memory": self._get_memory_metrics(),
            "disk": self._get_disk_metrics(),
            "network": self._get_network_metrics(),
            "timestamp": datetime.datetime.now().isoformat(),
        }

    def calculate_health_score(self):
        """Calculates a health score from 0-100 based on metrics."""
        metrics = self.get_system_metrics()

        score = 100
        penalties = []

        # CPU Penalty (> 80% is bad)
        if metrics["cpu_percent"] > 80:
            penalty = int((metrics["cpu_percent"] - 80) * 1.5)
            score -= penalty
            penalties.append(f"High CPU usage: {metrics['cpu_percent']}%")

        # Memory Penalty (> 90% is bad)
        mem_percent = metrics["memory"]["percent"]
        if mem_percent > 90:
            penalty = int((mem_percent - 90) * 2)
            score -= penalty
            penalties.append(f"High memory usage: {mem_percent}%")

        # Disk Penalty (> 95% is bad)
        disk_percent = metrics["disk"]["percent"]
        if disk_percent > 95:
            score -= 20
            penalties.append(f"Disk almost full: {disk_percent}%")

        # Floor score to 0
        score = max(0, score)

        return {
            "score": score,
            "status": "healthy" if score > 80 else "warning" if score > 50 else "critical",
            "penalties": penalties,
            "metrics": metrics,
        }

    def _get_memory_metrics(self):
        mem = psutil.virtual_memory()
        return {
            "total": mem.total,
            "available": mem.available,
            "percent": mem.percent,
            "used": mem.used,
        }

    def _get_disk_metrics(self):
        disk = psutil.disk_usage("/")
        return {"total": disk.total, "used": disk.used, "free": disk.free, "percent": disk.percent}

    def _get_network_metrics(self):
        net = psutil.net_io_counters()
        return {"bytes_sent": net.bytes_sent, "bytes_recv": net.bytes_recv}
