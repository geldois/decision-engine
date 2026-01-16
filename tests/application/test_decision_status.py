from app.application.dto.decision_status import DecisionStatus

# === VALID CASE ===
def test_decision_status_values_are_strings():
    # GIVEN
    approved = DecisionStatus.APPROVED
    rejected = DecisionStatus.REJECTED
    # WHEN / THEN
    assert isinstance(approved, str) and approved == "approved"
    assert isinstance(rejected, str) and rejected == "rejected"
    assert set(DecisionStatus) == {
        approved,
        rejected
    }
    