from . import cpu, ram, disk, processes, logs, anomalies


def register_all(mcp):
    cpu.register(mcp)
    ram.register(mcp)
    disk.register(mcp)
    processes.register(mcp)
    logs.register(mcp)
    anomalies.register(mcp)