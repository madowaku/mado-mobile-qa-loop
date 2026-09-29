from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import adb
from .runner import run_package


def _doctor(serial: str | None) -> int:
    try:
        path = adb.adb_path()
        device = adb.choose_device(serial)
        model = adb.shell(device.serial, "getprop", "ro.product.model")
        android = adb.shell(device.serial, "getprop", "ro.build.version.release")
    except adb.AdbError as exc:
        print(f"MMQL doctor: FAILED\n{exc}", file=sys.stderr)
        return 1

    print("MMQL doctor: READY")
    print(f"adb: {path}")
    print(f"device: {device.serial}")
    print(f"model: {model or 'unknown'}")
    print(f"android: {android or 'unknown'}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mmql")
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="verify ADB and Android device readiness")
    doctor.add_argument("--serial")

    run = sub.add_parser("run", help="capture M0.0 evidence for one installed package")
    run.add_argument("--package", required=True)
    run.add_argument("--duration", type=float, default=3.0)
    run.add_argument("--serial")
    run.add_argument("--evidence-root", type=Path, default=Path("evidence"))

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "doctor":
        return _doctor(args.serial)

    if args.command == "run":
        try:
            out = run_package(package=args.package, duration=args.duration, serial=args.serial, evidence_root=args.evidence_root)
        except adb.AdbError as exc:
            print(f"MMQL run: FAILED\n{exc}", file=sys.stderr)
            return 1
        print(f"MMQL run: COMPLETE\nevidence: {out}")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
