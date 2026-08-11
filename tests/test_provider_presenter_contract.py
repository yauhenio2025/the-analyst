import asyncio

from src.api.routes.presenter import (
    get_page_presentation,
    get_presentation_manifest,
    get_presentation_trace,
)


# The production Varoufakis run is not checked into this repository. This is
# the closest completed intellectual-genealogy fixture and exercises the same
# presenter provider contract without rewriting or migrating saved analysis.
COMPLETED_GENEALOGY_FIXTURE_JOB_ID = "proof-round3-adaptive-dossier-final-1774002300"


def test_completed_genealogy_fixture_serves_page_manifest_and_trace_routes():
    page = asyncio.run(
        get_page_presentation(
            COMPLETED_GENEALOGY_FIXTURE_JOB_ID,
            slim=True,
            consumer_key="the-critic",
            composition_mode=None,
        )
    )
    manifest = asyncio.run(
        get_presentation_manifest(
            COMPLETED_GENEALOGY_FIXTURE_JOB_ID,
            consumer_key="the-critic",
            slim=True,
            composition_mode=None,
        )
    )
    trace = asyncio.run(
        get_presentation_trace(
            COMPLETED_GENEALOGY_FIXTURE_JOB_ID,
            consumer_key="the-critic",
            composition_mode=None,
        )
    )

    assert page["job_id"] == COMPLETED_GENEALOGY_FIXTURE_JOB_ID
    assert page["consumer_key"] == "the-critic"
    assert page["presentation_contract_version"] == 1
    assert page["views"]

    assert manifest.job_id == COMPLETED_GENEALOGY_FIXTURE_JOB_ID
    assert manifest.consumer_key == "the-critic"
    assert manifest.presentation_contract_version == 1
    assert manifest.views

    assert trace.job_id == COMPLETED_GENEALOGY_FIXTURE_JOB_ID
    assert trace.consumer_key == "the-critic"
    assert trace.composition_status == "not_requested"
    assert trace.final_manifest.consumer_key == "the-critic"
