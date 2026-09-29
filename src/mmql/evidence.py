from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class Session:
    run_id: str
    package: str
    serial: str
    started_at: str
    finished_at: str
    duration_seconds: float
    app_version_name: str | None
    app_version_code: str | None
    device_model: str | None
    android_version: str | None
    status: str
    error: str | None = None


def new_run_id(now: datetime | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    return now.strftime("%Y%m%dT%H%M%SZ")


def bundle_dir(root: Path, run_id: str, package: str) -> Path:
    path = root / run_id / package
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_session(path: Path, session: Session) -> None:
    path.write_text(json.dumps(asdict(session), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_report(path: Path, session: Session) -> None:
    outcome = "PASS" if session.status == "completed" else "FAILED"
    error = f"\n- Error: {session.error}" if session.error else ""
    body = f"""# MMQL Run Report

{outcome}

- Package: `{session.package}`
- Device serial: `{session.serial}`
- Device model: {session.device_model or 'unknown'}
- Android: {session.android_version or 'unknown'}
- App version: {session.app_version_name or 'unknown'} ({session.app_version_code or 'unknown'})
- Started: {session.started_at}
- Finished: {session.finished_at}
- Observation duration: {session.duration_seconds:.2f}s{error}

## Evidence

- `session.json`
- `screenshot.png`

## Human review

This M0.0 report records launch evidence only. It does not claim that the app is bug-free or that a human tester completed a full functional review.
"""
    path.write_text(body, encoding="utf-8")
