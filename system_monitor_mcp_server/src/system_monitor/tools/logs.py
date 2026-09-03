import re
from pathlib import Path
from datetime import datetime
from collections import Counter


def register(mcp):
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