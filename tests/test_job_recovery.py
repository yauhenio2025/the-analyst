from pathlib import Path
import sys
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parents[1]
root_str = str(ROOT)
if root_str in sys.path:
    sys.path.remove(root_str)
sys.path.insert(0, root_str)

from src.executor import job_manager


def test_recover_orphaned_jobs_skips_recent_resumable_jobs(monkeypatch):
    recent = (datetime.utcnow() - timedelta(seconds=30)).isoformat()

    monkeypatch.setattr(
        job_manager,
        "execute",
        lambda *args, **kwargs: [
            {
                "job_id": "job-recent",
                "plan_id": "plan-recent",
                "status": "running",
                "started_at": recent,
                "created_at": recent,
                "plan_data": {"plan_id": "plan-recent", "workflow_key": "concept_logical_single_concept"},
                "document_ids": {},
            }
        ]
        if kwargs.get("fetch") == "all"
        else None,
    )

    resumed, failed, skipped = job_manager.recover_orphaned_jobs()

    assert resumed == 0
    assert failed == 0
    assert skipped == 1
