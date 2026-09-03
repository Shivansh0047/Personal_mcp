import psutil
from datetime import datetime


def register(mcp):
    @mcp.tool()
    def get_cpu_usage() -> dict:
        """
        Get current CPU usage statistics.
        Returns overall CPU percent, per-core usage, core count, and current frequency.
        """
        freq = psutil.cpu_freq()

        return {
            "cpu_percent_overall": psutil.cpu_percent(interval=1),  # 1 sec sample for accuracy
            "cpu_percent_per_core": psutil.cpu_percent(interval=1, percpu=True),
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "frequency_mhz": {
                "current": round(freq.current, 1) if freq else None,
                "min":     round(freq.min, 1)     if freq else None,
                "max":     round(freq.max, 1)     if freq else None,
            },
            "sampled_at": datetime.now().isoformat(),
        }