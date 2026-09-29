# MADO Mobile QA Loop

MADO Mobile QA Loop (MMQL) is an evidence-first Android QA runner for human testers.

The first milestone, **MMQL-M0.0 Skeleton**, connects to an Android device over ADB, launches an installed package, captures a screenshot and device/app metadata, and writes a Markdown report.

## Goals

- Reduce repetitive mobile QA work for indie developers and human testers.
- Keep evidence attached to every observation.
- Keep human judgment in the loop.
- Avoid fake engagement, fake reviews, or attempts to bypass Google Play requirements.

## M0.0 quick start

Requirements: Python 3.12+, Android SDK Platform Tools (`adb`) on PATH, and an unlocked Android device with USB debugging or Wireless ADB enabled.

~~~bash
python -m pip install -e .
mmql doctor
mmql run --package com.example.app --duration 3
~~~

Evidence is written under `evidence/<run-id>/<package>/` with `session.json`, `screenshot.png`, and `report.md`.

## Milestones

- M0.0: ADB device discovery, package launch, screenshot, metadata, report
- M0.1: UI hierarchy, logcat, trace and richer evidence bundles
- M0.2: deterministic UiAutomator explorer
- M0.3: visual auditor
- M0.4: human-reviewed feedback composer
- M0.5: daily batch runner
- M0.6: regression memory
- M0.7: tester evidence bundle

See `docs/MADO_MOBILE_QA_LOOP_SPEC.md`.
