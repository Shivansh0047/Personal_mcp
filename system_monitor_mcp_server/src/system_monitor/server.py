from fastmcp import FastMCP
import psutil # psutil (process and system utilities) is a cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) in Python
from datetime import datetime
import os
import re
from pathlib import Path

mcp = FastMCP(
    name = "System Monitor",
    instructions="A system monitoring server. Use these tools to check CPU, RAM, disk usage, running processes, and logs."
)

@mcp.tool()
def ping() -> str:
    """Check if the system is alive"""
    return "System Monitor MCP is online"

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

@mcp.tool()
def get_running_processes(sort_by: str = "memory",limit: int = 20) -> dict:
    """
    Get a list of currently running processes.
    
    Args:
        sort_by: Sort processes by 'memory' (default), 'cpu', or 'name'
        limit: How many processes to return (default 20, max 50)
    """
    limit = min(limit, 50)  # cap it so we don't flood the context window

    processes = []

    for proc in psutil.process_iter(['pid', 'name', 'status', 'memory_percent', 'cpu_percent', 'username', 'create_time']):
        try:
            info = proc.info

            # Skip system idle / empty entries
            if not info['name']:
                continue

            processes.append({
                "pid":            info['pid'],
                "name":           info['name'],
                "status":         info['status'],
                "memory_percent": round(info['memory_percent'] or 0, 2),
                "cpu_percent":    round(info['cpu_percent'] or 0, 2),
                "username":       info['username'],
                "running_since":  datetime.fromtimestamp(info['create_time']).isoformat() if info['create_time'] else None,
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Processes can die mid-iteration, or be protected — skip them
            continue

    # Sort
    sort_key = {
        "memory": lambda p: p["memory_percent"],
        "cpu":    lambda p: p["cpu_percent"],
        "name":   lambda p: p["name"].lower(),
    }.get(sort_by, lambda p: p["memory_percent"])

    processes.sort(key=sort_key, reverse=(sort_by != "name"))

    return {
        "total_running": len(processes),
        "showing":       min(limit, len(processes)),
        "sorted_by":     sort_by,
        "processes":     processes[:limit],
        "sampled_at":    datetime.now().isoformat(),
    }


@mcp.tool()
def find_process(name: str) -> dict:
    """
    Search for a specific process by name (case-insensitive partial match).
    Useful for checking if a specific app or service is running.

    Args:
        name: Process name to search for, e.g. 'chrome', 'python', 'postgres'
    """
    name_lower = name.lower()
    matches = []

    for proc in psutil.process_iter(['pid', 'name', 'status', 'memory_percent', 'cpu_percent', 'cmdline', 'create_time']):
        try:
            if name_lower in (proc.info['name'] or '').lower():
                info = proc.info
                matches.append({
                    "pid":            info['pid'],
                    "name":           info['name'],
                    "status":         info['status'],
                    "memory_percent": round(info['memory_percent'] or 0, 2),
                    "cpu_percent":    round(info['cpu_percent'] or 0, 2),
                    # cmdline shows full command — e.g. ['python', 'server.py']
                    "cmdline":        " ".join(info['cmdline']) if info['cmdline'] else None,
                    "running_since":  datetime.fromtimestamp(info['create_time']).isoformat() if info['create_time'] else None,
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return {
        "query":       name,
        "found":       len(matches),
        "matches":     matches,
        "sampled_at":  datetime.now().isoformat(),
    }


@mcp.tool()
def read_log_file(log_path: str, last_n_lines: int = 100, filter_level: str = "all") -> dict:
    """
    Read a log file and return its recent lines.

    Args:
        log_path: Full path to the log file
        last_n_lines: How many lines from the end to read (default 100)
        filter_level: Filter by level — 'all', 'error', 'warning', 'info'
    """
    path = Path(log_path)

    if not path.exists():
        return {"error": f"File not found: {log_path}"}

    if not path.is_file():
        return {"error": f"Path is not a file: {log_path}"}

    # Safety: don't read massive files into memory blindly
    file_size_mb = path.stat().st_size / (1024 ** 2)
    if file_size_mb > 50:
        return {"error": f"File too large ({file_size_mb:.1f} MB). Use a smaller log or tail it manually."}

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            all_lines = f.readlines()
    except PermissionError:
        return {"error": f"Permission denied reading: {log_path}"}

    # Take last N lines
    lines = all_lines[-last_n_lines:]

    # Filter by level keyword if requested
    level_keywords = {
        "error":   ["error", "exception", "traceback", "critical", "fatal"],
        "warning": ["warning", "warn"],
        "info":    ["info"],
        "all":     [],
    }

    keywords = level_keywords.get(filter_level.lower(), [])

    if keywords:
        lines = [l for l in lines if any(kw in l.lower() for kw in keywords)]

    return {
        "log_path":       log_path,
        "file_size_mb":   round(file_size_mb, 2),
        "total_lines":    len(all_lines),
        "lines_returned": len(lines),
        "filter_level":   filter_level,
        "content":        "".join(lines),
        "sampled_at":     datetime.now().isoformat(),
    }


@mcp.tool()
def analyze_log_file(log_path: str, last_n_lines: int = 500) -> dict:
    """
    Analyze a log file and return a summary: error count, warning count,
    most frequent error messages, and the most recent errors.

    Args:
        log_path: Full path to the log file
        last_n_lines: How many lines from the end to analyze (default 500)
    """
    path = Path(log_path)

    if not path.exists():
        return {"error": f"File not found: {log_path}"}

    file_size_mb = path.stat().st_size / (1024 ** 2)
    if file_size_mb > 50:
        return {"error": f"File too large ({file_size_mb:.1f} MB)."}

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            all_lines = f.readlines()
    except PermissionError:
        return {"error": f"Permission denied: {log_path}"}

    lines = all_lines[-last_n_lines:]

    errors   = [l.strip() for l in lines if re.search(r"error|exception|traceback|critical|fatal", l, re.IGNORECASE)]
    warnings = [l.strip() for l in lines if re.search(r"warning|warn", l, re.IGNORECASE)]

    # Find most repeated error patterns (strip timestamps for grouping)
    # This removes common timestamp prefixes before counting
    def strip_timestamp(line: str) -> str:
        return re.sub(r"^\[?[\d\-T:\.Z\s,]+\]?\s*", "", line).strip()

    from collections import Counter
    error_patterns = Counter(strip_timestamp(e) for e in errors)
    top_errors = [{"message": msg, "count": count}
                  for msg, count in error_patterns.most_common(5)]

    return {
        "log_path":        log_path,
        "file_size_mb":    round(file_size_mb, 2),
        "total_lines":     len(all_lines),
        "lines_analyzed":  len(lines),
        "error_count":     len(errors),
        "warning_count":   len(warnings),
        "top_errors":      top_errors,
        "recent_errors":   errors[-5:],    # last 5 error lines
        "recent_warnings": warnings[-5:],  # last 5 warning lines
        "sampled_at":      datetime.now().isoformat(),
    }


@mcp.tool()
def list_log_files(directory: str = "C:\\Windows\\Logs") -> dict:
    """
    List all .log and .txt files in a directory, sorted by most recently modified.
    Useful for discovering what logs are available to analyze.

    Args:
        directory: Directory path to scan (default: C:\\Windows\\Logs)
    """
    dir_path = Path(directory)

    if not dir_path.exists():
        return {"error": f"Directory not found: {directory}"}

    if not dir_path.is_dir():
        return {"error": f"Not a directory: {directory}"}

    log_files = []

    try:
        for f in dir_path.rglob("*.log"):
            try:
                stat = f.stat()
                log_files.append({
                    "path":          str(f),
                    "size_mb":       round(stat.st_size / (1024 ** 2), 2),
                    "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                })
            except (PermissionError, OSError):
                continue

        # Also grab .txt files that might be logs
        for f in dir_path.rglob("*.txt"):
            try:
                stat = f.stat()
                log_files.append({
                    "path":          str(f),
                    "size_mb":       round(stat.st_size / (1024 ** 2), 2),
                    "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                })
            except (PermissionError, OSError):
                continue

    except PermissionError:
        return {"error": f"Permission denied scanning: {directory}"}

    # Sort by most recently modified first
    log_files.sort(key=lambda x: x["last_modified"], reverse=True)

    return {
        "directory":   directory,
        "files_found": len(log_files),
        "log_files":   log_files[:30],  # cap at 30
        "sampled_at":  datetime.now().isoformat(),
    }

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
    freq        = psutil.cpu_freq()

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
    memory_hogs = [
        p for p in processes
        if (p['memory_percent'] or 0) > 10
    ]
    for p in memory_hogs:
        criticals.append(
            f"Process '{p['name']}' (pid {p['pid']}) using {round(p['memory_percent'], 1)}% RAM"
        )

    # Flag any single process eating >80% CPU
    cpu_hogs = [
        p for p in processes
        if (p['cpu_percent'] or 0) > 80
    ]
    for p in cpu_hogs:
        warnings.append(
            f"🟡 Process '{p['name']}' (pid {p['pid']}) using {round(p['cpu_percent'], 1)}% CPU"
        )

    # HEALTH SCORE
    # Start at 100, deduct for each issue
    score = 100
    score -= len(criticals) * 20
    score -= len(warnings)  * 10
    score  = max(0, score)   # floor at 0

    if score >= 80:
        health = "🟢 Healthy"
    elif score >= 50:
        health = "🟡 Degraded"
    else:
        health = "🔴 Critical"

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


def main():
    mcp.run()


if __name__ == "__main__":
    main()