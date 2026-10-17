from pathlib import Path

ROOT = Path(__file__).parents[1]
WEIGHTS = {"RESOLVED": 0, "MULTIPLE": 2, "MISSING": 3}


def score(statuses):
    return sum(WEIGHTS[value] for value in statuses)


def accepts_revision(old, new):
    return score(new) < score(old) and all(WEIGHTS[new[i]] <= WEIGHTS[old[i]] for i in range(len(old)))


def test_budget_and_monotonic_revision_rules():
    draft = ["MULTIPLE", "RESOLVED", "MISSING", "RESOLVED"]
    revised = ["RESOLVED"] * 4
    regression = ["RESOLVED", "MISSING", "RESOLVED", "RESOLVED"]
    assert score(draft) == 5
    assert accepts_revision(draft, revised)
    assert not accepts_revision(draft, regression)


def test_contract_binds_all_state_driving_fields():
    source = (ROOT / "contracts/contract.py").read_text(encoding="utf-8")
    for token in (
        "one finding per decision point required",
        "ordered exact findings required",
        "citations do not support the ambiguity status",
        "revision must strictly reduce ambiguity without regression",
        "source_digest",
        "prompt_comparative",
    ):
        assert token in source
    assert "[:12000]" not in source


def test_fixtures_expose_ambiguity_then_resolve_it():
    draft = (ROOT / "fixtures/draft-spec.md").read_text(encoding="utf-8")
    revised = (ROOT / "fixtures/revised-spec.md").read_text(encoding="utf-8")
    assert "either" in draft and "not assigned" in draft
    assert "fixed at" in revised and "exclusively" in revised
