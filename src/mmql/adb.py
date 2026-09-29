from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


class AdbError(RuntimeError):
    pass


@dataclass(frozen=True)
class Device:
    serial: str
    state: str


def adb_path() -> str:
    path = shutil.which("adb")
    if not path:
        raise AdbError("adb was not found on PATH")
    return path


def run_adb(*args: str, serial: str | None = None, timeout: int = 30) -> subprocess.CompletedProcess[bytes]:
    cmd = [adb_path()]
    if serial:
        cmd += ["-s", serial]
    cmd += list(args)
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise AdbError(f"adb timed out: {' '.join(cmd)}") from exc
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        raise AdbError(stderr or f"adb failed with exit code {result.returncode}")
    return result


def list_devices() -> list[Device]:
    result = run_adb("devices")
    devices: list[Device] = []
    for raw in result.stdout.decode("utf-8", errors="replace").splitlines()[1:]:
        line = raw.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 2:
            devices.append(Device(serial=parts[0], state=parts[1]))
    return devices


def choose_device(serial: str | None = None) -> Device:
    devices = list_devices()
    if serial:
        for device in devices:
            if device.serial == serial:
                if device.state != "device":
                    raise AdbError(f"device {serial} is in state {device.state}")
                return device
        raise AdbError(f"device {serial} was not found")

    ready = [d for d in devices if d.state == "device"]
    if not ready:
        raise AdbError("no ready Android device found")
    if len(ready) > 1:
        raise AdbError("multiple devices found; pass --serial")
    return ready[0]


def shell(serial: str, *args: str) -> str:
    result = run_adb("shell", *args, serial=serial)
    return result.stdout.decode("utf-8", errors="replace").strip()


def package_installed(serial: str, package: str) -> bool:
    return bool(shell(serial, "pm", "path", package).strip())


def force_stop(serial: str, package: str) -> None:
    shell(serial, "am", "force-stop", package)


def launch_package(serial: str, package: str) -> str:
    result = shell(serial, "monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1")
    lowered = result.lower()
    if "no activities found" in lowered or "monkey aborted" in lowered:
        raise AdbError(f"could not launch package {package}")
    return result


def screenshot(serial: str, destination: Path) -> None:
    result = run_adb("exec-out", "screencap", "-p", serial=serial)
    destination.write_bytes(result.stdout)
