"""The field packet builder reads the program's venues beside the bearing sources (2026-09-11)."""
from tools.build_field_packet import select_by_bearing, venue_hosts


def _row(uid, url, chars=1000, state="available"):
    return {"uid": uid, "source_url": url, "source_metadata": {"url": url}, "body": "x" * chars if state == "available" else "", "body_chars": chars if state == "available" else 0,
            "body_state": state, "body_sha256": "h", "page_spans": []}


def test_venue_hosts_and_selection_read_the_program_venues_first():
    rs = {"lanes": [{"venues": "treasury.gov; federalreserve.gov; https://www.congress.gov/"}, {"venues": "third-party interviews; podcasts"}]}
    assert venue_hosts(rs) == ["treasury.gov", "federalreserve.gov", "congress.gov"] and venue_hosts(None) == []
    rows = [_row("r:1", "https://www.reuters.com/a"), _row("r:2", "https://home.treasury.gov/system/files/x.pdf", 300000),
            _row("r:3", "https://desmog.com/b"), _row("r:4", "https://coindesk.com/c"), _row("r:5", "https://ft.com/d", state="missing")]
    bearings = [{"url": "https://desmog.com/b", "bearing": "supports"}, {"url": "https://www.reuters.com/a", "bearing": "context"}]
    out = select_by_bearing(rows, bearings, 2, venue_hosts(rs))
    kept = [r["uid"] for r in out if r["body_state"] == "available"]
    assert kept == ["r:2", "r:3"]                                                   # the Treasury document and the supporting source
    assert [r["uid"] for r in out if "reading cap" in (r.get("selection_reason") or "")] == ["r:1", "r:4"]
    assert {r["uid"] for r in select_by_bearing(rows, bearings, 2) if r["body_state"] == "available"} == {"r:3", "r:1"}   # without venues, bearing then context
    kept = select_by_bearing(rows, bearings, 2, venue_hosts(rs), keep={"r:4"})
    assert {r["uid"] for r in kept if r["body_state"] == "available"} == {"r:4", "r:2"}                                  # already read first, then the venue document
