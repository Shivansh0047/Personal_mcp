import psutil
from datetime import datetime


def register(mcp):
    @mcp.tool()
    def get_disk_usage(path: str = "C:\\") -> dict:
        """
        Get disk usage for a given path.
        Defaults to C:\\ on Windows. Pass '/' for Linux/Mac.
        Returns total, used, free space in GB and usage percentage.
        """
        usage = psutil.disk_usage(path)

        def to_gb(bytes_val: int) -> float:
            return round(bytes_val / (1024 ** 3), 2)

        # Also grab all disk partitions for a full picture
        partitions = []
        for p in psutil.disk_partitions():
            try:
                u = psutil.disk_usage(p.mountpoint)
                partitions.append({
                    "device":     p.device,
                    "mountpoint": p.mountpoint,
                    "fstype":     p.fstype,
                    "total_gb":   to_gb(u.total),
                    "used_gb":    to_gb(u.used),
                    "free_gb":    to_gb(u.free),
                    "percent":    u.percent,
                })
            except PermissionError:
                # Some partitions (like CD drives) throw this — just skip them
                continue

        return {
            "queried_path": path,
            "total_gb":     to_gb(usage.total),
            "used_gb":      to_gb(usage.used),
            "free_gb":      to_gb(usage.free),
            "percent_used": usage.percent,
            "all_partitions": partitions,
            "sampled_at": datetime.now().isoformat(),
        }