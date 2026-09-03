import psutil
from datetime import datetime


def register(mcp):
    @mcp.tool()
    def get_ram_usage() -> dict:
        """
        Get current RAM (memory) usage statistics.
        Returns total, used, available memory in GB and usage percentage.
        """
        vm  = psutil.virtual_memory() # computer's physical RAM.
        swp = psutil.swap_memory() # Swap is disk space that the operating system can use as an extension of RAM when RAM becomes scarce.

        def to_gb(bytes_val: int) -> float:
            return round(bytes_val / (1024 ** 3), 2)

        return {
            "ram": {
                "total_gb":     to_gb(vm.total),
                "used_gb":      to_gb(vm.used),
                "available_gb": to_gb(vm.available),
                "percent_used": vm.percent,
            },
            "swap": {
                "total_gb":  to_gb(swp.total),
                "used_gb":   to_gb(swp.used),
                "free_gb":   to_gb(swp.free),
                "percent_used": swp.percent,
            },
            "sampled_at": datetime.now().isoformat(),
        }