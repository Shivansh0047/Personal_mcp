import psutil
from datetime import datetime


def register(mcp):
    @mcp.tool()
    def get_running_processes(sort_by: str = "memory", limit: int = 20) -> dict:
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