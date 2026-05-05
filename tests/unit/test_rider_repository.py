from src.rider_repository import RiderRepository


def test_exists_returns_true_for_known_rider():
    repo = RiderRepository()
    assert repo.exists(10) is True


def test_exists_returns_false_for_unknown_rider():
    repo = RiderRepository()
    assert repo.exists(999) is False


def test_is_blocked_returns_true_when_rider_is_blocked():
    repo = RiderRepository()
    assert repo.is_blocked(20) is True


def test_has_active_account_returns_false_when_account_is_inactive():
    repo = RiderRepository()
    assert repo.has_active_account(30) is False
