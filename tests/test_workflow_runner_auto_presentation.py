from src.executor.workflow_runner import (
    _resolve_auto_presentation_consumer_key,
    _run_auto_presentation,
)


def test_resolve_auto_presentation_consumer_key_prefers_job_value(monkeypatch):
    monkeypatch.setattr(
        "src.executor.workflow_runner.get_job",
        lambda job_id: {
            "job_id": job_id,
            "consumer_key": "custom-consumer",
            "plan_data": {
                "plan_request": {"consumer_key": "ignored-nested"},
            },
        },
    )

    resolved = _resolve_auto_presentation_consumer_key("job-1", default="the-critic")

    assert resolved == "custom-consumer"


def test_resolve_auto_presentation_consumer_key_uses_nested_plan_data(monkeypatch):
    monkeypatch.setattr(
        "src.executor.workflow_runner.get_job",
        lambda job_id: {
            "job_id": job_id,
            "consumer_key": None,
            "plan_data": {
                "task_request": {"consumer_key": "nested-consumer"},
            },
        },
    )

    resolved = _resolve_auto_presentation_consumer_key("job-1", default="the-critic")

    assert resolved == "nested-consumer"


def test_run_auto_presentation_uses_preparation_coordinator(monkeypatch):
    calls = {}

    monkeypatch.setattr(
        "src.executor.workflow_runner.get_job",
        lambda job_id: {
            "job_id": job_id,
            "consumer_key": None,
            "plan_data": {
                "plan_request": {"consumer_key": "the-critic"},
            },
        },
    )

    def _run(job_id, plan_id, *, consumer_key, wait_if_active=False, **kwargs):
        calls["job_id"] = job_id
        calls["plan_id"] = plan_id
        calls["consumer_key"] = consumer_key
        calls["wait_if_active"] = wait_if_active
        calls["kwargs"] = kwargs
        return {
            "status": "completed",
            "detail": "Presentation ready",
            "stats": {"tasks_completed": 3},
        }

    monkeypatch.setattr(
        "src.presenter.preparation_coordinator.run_presentation_pipeline_sync",
        _run,
    )

    _run_auto_presentation("job-1", "plan-1")

    assert calls == {
        "job_id": "job-1",
        "plan_id": "plan-1",
        "consumer_key": "the-critic",
        "wait_if_active": True,
        "kwargs": {},
    }


def test_resolve_auto_presentation_consumer_key_falls_back_to_default(monkeypatch):
    monkeypatch.setattr(
        "src.executor.workflow_runner.get_job",
        lambda job_id: {
            "job_id": job_id,
            "consumer_key": None,
            "plan_data": {},
        },
    )

    resolved = _resolve_auto_presentation_consumer_key("job-1", default="the-critic")

    assert resolved == "the-critic"
