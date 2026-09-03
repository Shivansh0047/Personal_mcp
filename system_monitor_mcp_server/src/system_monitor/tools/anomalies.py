import psutil
from datetime import datetime


def register(mcp):
    @mcp.tool()
    def detect_anomalies() -> dict:
        """
        Run a full system health check and detect unusual resource usage.
        Checks CPU, RAM, disk, and top processes against safe thresholds.
        Returns a prioritized list of warnings and a health score (0-100).
        """

        warnings  = []   # things that need attention
        criticals = []   # things that need immediate attention
        info      = []   # just useful context

        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)

        if cpu_percent > 90:
            criticals.append(f"CPU critically high: {cpu_percent}%")
        elif cpu_percent > 70:
            warnings.append(f"CPU usage elevated: {cpu_percent}%")
        else:
            info.append(f"CPU usage normal: {cpu_percent}%")

        # Check per-core — catch single-core saturation hidden in averages
        per_core = psutil.cpu_percent(interval=0.5, percpu=True)
        saturated_cores = [i for i, c in enumerate(per_core) if c > 95]
        if saturated_cores:
            warnings.append(f"Cores fully saturated: {saturated_cores}")

        # RAM
        vm = psutil.virtual_memory()

        if vm.percent > 90:
            criticals.append(f"RAM critically high: {vm.percent}% used ({round(vm.available / 1024**3, 1)} GB free)")
        elif vm.percent > 75:
            warnings.append(f"RAM usage elevated: {vm.percent}% used ({round(vm.available / 1024**3, 1)} GB free)")
        else:
            info.append(f"RAM usage normal: {vm.percent}%")

        # Swap usage — if swap is being used heavily, RAM is under pressure
        swp = psutil.swap_memory()
        if swp.percent > 50:
            warnings.append(f"Swap heavily used: {swp.percent}% — system is memory-pressured")
        elif swp.percent > 20:
            info.append(f"Swap in use: {swp.percent}%")

        # DISK
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                pct   = usage.percent
                free  = round(usage.free / 1024**3, 1)

                if pct > 95:
                    criticals.append(f"Disk {partition.device} critically full: {pct}% used ({free} GB free)")
                elif pct > 85:
                    warnings.append(f"Disk {partition.device} getting full: {pct}% used ({free} GB free)")
                else:
                    info.append(f"Disk {partition.device} OK: {pct}% used")
            except (PermissionError, OSError):
                continue

        # TOP MEMORY PROCESSES
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Flag any single process eating >10% RAM
        memory_hogs = [p for p in processes if (p['memory_percent'] or 0) > 10]
        for p in memory_hogs:
            criticals.append(
                f"Process '{p['name']}' (pid {p['pid']}) using {round(p['memory_percent'], 1)}% RAM"
            )

        # Flag any single process eating >80% CPU
        cpu_hogs = [p for p in processes if (p['cpu_percent'] or 0) > 80]
        for p in cpu_hogs:
            warnings.append(
                f"Process '{p['name']}' (pid {p['pid']}) using {round(p['cpu_percent'], 1)}% CPU"
            )

        # HEALTH SCORE
        # Start at 100, deduct for each issue
        score = 100
        score -= len(criticals) * 20
        score -= len(warnings)  * 10
        score  = max(0, score)   # floor at 0

        if score >= 80:
            health = "Healthy"
        elif score >= 50:
            health = "Degraded"
        else:
            health = "Critical"

        return {
            "health_score":  score,
            "health_status": health,
            "criticals":     criticals,
            "warnings":      warnings,
            "info":          info,
            "summary": (
                f"{len(criticals)} critical issue(s), "
                f"{len(warnings)} warning(s), "
                f"health score: {score}/100"
            ),
            "sampled_at": datetime.now().isoformat(),
        }