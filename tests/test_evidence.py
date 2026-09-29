from datetime import datetime, timezone

from mmql.evidence import Session, new_run_id, write_report, write_session


def test_new_run_id_is_stable():
    now = datetime(2026, 9, 29, 6, 0, 0, tzinfo=timezone.utc)
    assert new_run_id(now) == "20260929T060000Z"


def test_writes_session_and_report(tmp_path):
    session = Session(
        run_id="run-1",
        package="com.example.app",
        serial="device-1",
        started_at="2026-09-29T06:00:00+00:00",
        finished_at="2026-09-29T06:00:03+00:00",
        duration_seconds=3.0,
        app_version_name="1.0",
        app_version_code="1",
        device_model="Example",
        android_version="16",
        status="completed",
    )
    write_session(tmp_path / "session.json", session)
    write_report(tmp_path / "report.md", session)

    assert '"package": "com.example.app"' in (tmp_path / "session.json").read_text()
    assert "PASS" in (tmp_path / "report.md").read_text()
