import pytest
from unittest.mock import Mock
from src.bike_share_service import BikeShareService


def make_service():
    bike_repository = Mock()
    rider_repository = Mock()
    rental_repository = Mock()
    hold_repository = Mock()
    service = BikeShareService(
        bike_repository,
        rider_repository,
        rental_repository,
        hold_repository,
    )
    return service, bike_repository, rider_repository, rental_repository, hold_repository


def test_borrow_bike_raises_when_parameters_are_missing():
    service, *_ = make_service()
    with pytest.raises(ValueError, match="Rider ID and bike ID are required"):
        service.borrow_bike(None, 1)


def test_borrow_bike_returns_false_when_rider_does_not_exist():
    service, _, rider_repository, _, _ = make_service()
    rider_repository.exists.return_value = False
    assert service.borrow_bike(999, 1) is False


def test_borrow_bike_creates_rental_when_all_rules_are_satisfied():
    service, bike_repository, rider_repository, rental_repository, hold_repository = make_service()

    rider_repository.exists.return_value = True
    bike_repository.exists.return_value = True
    rider_repository.is_blocked.return_value = False
    rider_repository.has_active_account.return_value = True
    bike_repository.is_available.return_value = True
    rental_repository.count_active_rentals.return_value = 0
    hold_repository.next_rider.return_value = None
    hold_repository.has_hold.return_value = False

    result = service.borrow_bike(10, 1)

    assert result is True
    bike_repository.mark_unavailable.assert_called_once_with(1)
    rental_repository.create_rental.assert_called_once_with(10, 1)


def test_return_bike_returns_false_when_rental_does_not_exist():
    service, _, _, rental_repository, _ = make_service()
    rental_repository.is_bike_with_rider.return_value = False
    assert service.return_bike(10, 1) is False


def test_hold_bike_adds_entry_when_rules_are_satisfied():
    service, bike_repository, rider_repository, rental_repository, hold_repository = make_service()

    rider_repository.exists.return_value = True
    bike_repository.exists.return_value = True
    rider_repository.is_blocked.return_value = False
    rider_repository.has_active_account.return_value = True
    bike_repository.is_available.return_value = False
    hold_repository.has_hold.return_value = False
    rental_repository.is_bike_with_rider.return_value = False

    result = service.hold_bike(10, 1)

    assert result is True
    hold_repository.add_hold.assert_called_once_with(10, 1)


def test_hold_bike_raises_when_parameters_are_missing():
    service, *_ = make_service()
    with pytest.raises(ValueError, match="Rider ID and bike ID are required"):
        service.hold_bike(None, 1)
