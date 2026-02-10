import psutil
from providers.hardware import HardwareProvider


class ProfileRecommender:
    """Recommends system profiles based on hardware and usage."""

    def __init__(self, hardware_provider=None):
        self.hardware = hardware_provider or HardwareProvider()

    def recommend(self):
        """Analyzes hardware and returns sorted list of profile recommendations."""
        recommendations = []

        # Hardware-based scores
        gpu_vendors = self.hardware.gpu_info
        cpu_count = psutil.cpu_count()
        total_ram_gb = psutil.virtual_memory().total / (1024**3)

        # AI Developer recommendation
        if "nvidia" in gpu_vendors and total_ram_gb >= 16:
            recommendations.append(
                {
                    "profile_id": "ai-developer",
                    "confidence": 0.9,
                    "reason": "NVIDIA GPU and high RAM detected, suitable for ML/AI.",
                }
            )

        # Creative Workstation recommendation
        if ("nvidia" in gpu_vendors or "amd" in gpu_vendors) and total_ram_gb >= 8:
            recommendations.append(
                {
                    "profile_id": "creative-workstation",
                    "confidence": 0.75,
                    "reason": "Dedicated GPU detected, good for media production.",
                }
            )

        # Server profile
        if cpu_count >= 4 and not any(v in gpu_vendors for v in ["nvidia", "amd"]):
            recommendations.append(
                {
                    "profile_id": "server",
                    "confidence": 0.8,
                    "reason": "Multi-core CPU detected without dedicated graphics.",
                }
            )

        # Default fallback
        recommendations.append(
            {
                "profile_id": "standard-desktop",
                "confidence": 0.5,
                "reason": "Balanced configuration for general use.",
            }
        )

        # Sort by confidence
        return sorted(recommendations, key=lambda x: x["confidence"], reverse=True)
