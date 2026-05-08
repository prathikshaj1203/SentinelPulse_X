"""Lightweight CSV-based logger for diagnostics + system events."""
import csv
from datetime import datetime
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
DIAG_LOG = LOG_DIR / "diagnostics.csv"
SYS_LOG = LOG_DIR / "system.csv"


def _ensure(path: Path, headers: list[str]) -> None:
    if not path.exists():
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(headers)


def log_diagnostic(machine: str, failure: str, severity: str, score: float) -> None:
    _ensure(DIAG_LOG, ["timestamp", "machine", "failure", "severity", "health_score"])
    with open(DIAG_LOG, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([datetime.utcnow().isoformat(timespec="seconds"),
                                machine, failure, severity, round(score, 2)])


def log_system(event: str, detail: str = "") -> None:
    _ensure(SYS_LOG, ["timestamp", "event", "detail"])
    with open(SYS_LOG, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([datetime.utcnow().isoformat(timespec="seconds"), event, detail])


def read_log(path: Path):
    import pandas as pd
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)
