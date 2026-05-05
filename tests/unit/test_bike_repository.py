import pytest
from src.bike_repository import BikeRepository


def test_exists_returns_true_for_existing_bike():
    repo = BikeRepository()
    assert repo.exists(1) is True


def test_is_available_returns_true_for_available_bike():
    repo = BikeRepository()
    assert repo.is_available(1) is True


def test_is_available_returns_false_for_unavailable_bike():
    repo = BikeRepository()
    assert repo.is_available(3) is False


def test_mark_unavailable_changes_bike_state():
    repo = BikeRepository()
    repo.mark_unavailable(1)
    assert repo.is_available(1) is False


def test_mark_available_changes_bike_state():
    repo = BikeRepository()
    repo.mark_available(3)
    assert repo.is_available(3) is True


def test_mark_unavailable_raises_for_unknown_bike():
    repo = BikeRepository()
    with pytest.raises(ValueError, match="Bike not found"):
        repo.mark_unavailable(999)
