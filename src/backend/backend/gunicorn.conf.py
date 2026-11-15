"""Aggregate telemetry across workers; the metrics listener is optional."""

import os
from pathlib import Path

enabled = os.getenv("PROMETHEUS_ENABLED", "false").lower() == "true"
bind = ["0.0.0.0:8000", "0.0.0.0:8002"] if enabled else ["0.0.0.0:8000"]


def on_starting(server):
    if not enabled:
        return
    directory = Path(os.environ["PROMETHEUS_MULTIPROC_DIR"])
    # This dedicated tmpfs is reset once per master start, never per worker.
    if directory.resolve() != Path("/run/backend-metrics") or directory.is_symlink():
        raise RuntimeError("Unexpected Prometheus multiprocess directory")
    directory.mkdir(exist_ok=True)
    for metric_file in directory.glob("*.db"):
        metric_file.unlink()


def post_worker_init(worker):
    if enabled:
        from backend.metrics import WORKERS

        WORKERS.set(1)


def child_exit(server, worker):
    if enabled:
        from prometheus_client import multiprocess

        multiprocess.mark_process_dead(worker.pid)
