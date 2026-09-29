from __future__ import annotations

import time
from datetime import datetime, timezone
from pathlib import Path

from . import adb
from .evidence import Session, bundle_dir, new_run_id, write_report, write_session


def _prop(serial: str, key: str) -> str | None:
    value = adb.shell(serial, "getprop", key).strip()
    return value or None


def _package_field(serial: str, package: str, key: str) -> str | None:
    dump = adb.shell(serial, "dumpsys", "package", package)
    for line in dump.splitlines():
        stripped = line.strip()
        if stripped.startswith(key + "="):
            return stripped.split("=", 1)[1].strip() or None
    return None


def run_package(package: str, duration: float = 3.0, serial: str | None = None, evidence_root: Path = Path("evidence")) -> Path:
    device = adb.choose_device(serial)
    if not adb.package_installed(device.serial, package):
        raise adb.AdbError(f"package {package} is not installed on {device.serial}")

    run_id = new_run_id()
    out = bundle_dir(evidence_root, run_id, package)
    started = datetime.now(timezone.utc)
    status = "completed"
    error: str | None = None

    try:
        adb.force_stop(device.serial, package)
        adb.launch_package(device.serial, package)
        time.sleep(max(0.0, duration))
        adb.screenshot(device.serial, out / "screenshot.png")
    except Exception as exc:
        status = "failed"
        error = str(exc)
        raise
    finally:
        finished = datetime.now(timezone.utc)
        session = Session(
            run_id=run_id,
            package=package,
            serial=device.serial,
            started_at=started.isoformat(),
            finished_at=finished.isoformat(),
            duration_seconds=(finished - started).total_seconds(),
            app_version_name=_package_field(device.serial, package, "versionName"),
            app_version_code=_package_field(device.serial, package, "versionCode"),
            device_model=_prop(device.serial, "ro.product.model"),
            android_version=_prop(device.serial, "ro.build.version.release"),
            status=status,
            error=error,
        )
        write_session(out / "session.json", session)
        write_report(out / "report.md", session)

    return out
