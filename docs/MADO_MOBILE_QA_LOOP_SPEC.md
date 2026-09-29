# MADO MOBILE QA LOOP SPEC v0.1

Status: Active draft

## Mission

Reduce repetitive Android QA work while preserving real human judgment.

MMQL is an evidence-first QA runner. It is not a tool for generating fake testers, fake reviews, fake engagement, or bypassing Google Play requirements.

## Core principle

**Evidence first, automation second.**

Automate repeatable observation and collection. Keep consequential judgment and external feedback submission under human control.

## M0.0 Skeleton

End-to-end contract:

1. Find `adb`.
2. Detect exactly one ready Android device, or require `--serial`.
3. Verify that the requested package is installed.
4. Force-stop the package.
5. Cold-launch its launcher activity.
6. Observe for a configured duration.
7. Capture a PNG screenshot.
8. Capture device and package metadata.
9. Write `session.json` and `report.md`.
10. On failure, preserve a failed session report when possible.

### Definition of Done

- `mmql doctor` reports ADB/device readiness.
- `mmql run --package <id>` creates one evidence bundle.
- No AI model is required.
- No AccessibilityService is required.
- No external account credentials are required.

## Evidence bundle

~~~text
evidence/
└── <run-id>/
    └── <package>/
        ├── session.json
        ├── screenshot.png
        └── report.md
~~~

## Safety boundaries

M0.0 performs launch and observation only.

Future explorers must classify actions as SAFE, CAUTION, or DANGEROUS. Purchases, publishing, account deletion, message sending, subscriptions, and irreversible actions are forbidden by default.

## Roadmap

- M0.1 Evidence Capture: UI hierarchy, logcat, process state, trace.jsonl
- M0.2 Deterministic Explorer: UiAutomator and safe navigation
- M0.3 Visual Auditor: evidence-linked issue candidates
- M0.4 Feedback Composer: human-reviewed drafts
- M0.5 Daily Batch: 10–20 app unattended巡回 with resume/retry
- M0.6 Regression Memory: compare previous runs and verify fixes
- M0.7 Tester Evidence Bundle: multi-day developer-facing report

## North Star

Measure reduction in human QA time without reducing evidence quality or human agency.
