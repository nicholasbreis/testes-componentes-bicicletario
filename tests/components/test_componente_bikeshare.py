import pytest

from src.bike_repository import BikeRepository
from src.rider_repository import RiderRepository
from src.rental_repository import RentalRepository
from src.hold_repository import HoldRepository
from src.bike_share_service import BikeShareService

@pytest.fixture
def service():
    return BikeShareService(
        bike_repository=BikeRepository(),
        rider_repository=RiderRepository(),
        rental_repository=RentalRepository(),
        hold_repository=HoldRepository(),
    )

# Cenário 1 - Empréstimo com sucesso

def test_borrow_bike_success(service):
    result = service.borrow_bike(rider_id=10, bike_id=1)

    assert result is True


# Cenário 2 — Empréstimo de bicicleta inexistente

def test_borrow_nonexistent_bike(service):
    result = service.borrow_bike(rider_id=10, bike_id=999)

    assert result is False


# Cenário 3 — Empréstimo por usuário inexistente

def test_borrow_bike_nonexistent_rider(service):
    result = service.borrow_bike(rider_id=999, bike_id=1)

    assert result is False


# Cenário 4 — Empréstimo bloqueado por conta inativa

def test_borrow_bike_inactive_account(service):
    result = service.borrow_bike(rider_id=30, bike_id=1)

    assert result is False


# Cenário 5 — Empréstimo bloqueado por usuário bloqueado

def test_borrow_bike_blocked_rider(service):
    result = service.borrow_bike(rider_id=20, bike_id=1)

    assert result is False


# Cenário 6 — Empréstimo bloqueado por limite de 2 empréstimos ativos

def test_borrow_bike_exceeds_active_rental_limit(service):
    bike_repo = BikeRepository()
    bike_repo._bikes[5] = {"model": "Bike Extra", "available": True}
    rider_repo = RiderRepository()
    rental_repo = RentalRepository()
    hold_repo = HoldRepository()

    svc = BikeShareService(bike_repo, rider_repo, rental_repo, hold_repo)
    svc.borrow_bike(rider_id=40, bike_id=1)
    svc.borrow_bike(rider_id=40, bike_id=2)

    result = svc.borrow_bike(rider_id=40, bike_id=5)
    assert result is False


# Cenário 7 — Reserva com sucesso para bicicleta indisponível

def test_hold_bike_success(service):
    
    service.borrow_bike(rider_id=10, bike_id=1)

    result = service.hold_bike(rider_id=40, bike_id=1)

    assert result is True


# Cenário 8 — Tentativa de reserva duplicada


def test_hold_bike_duplicate(service):
    
    service.hold_bike(rider_id=40, bike_id=3)

    result = service.hold_bike(rider_id=40, bike_id=3)

    assert result is False


# Cenário 9 — Devolução simples sem reserva pendente

def test_return_bike_no_pending_hold(service):
   
    service.borrow_bike(rider_id=10, bike_id=1)

    result = service.return_bike(rider_id=10, bike_id=1)

    assert result is True
    assert service.bike_repository.is_available(bike_id=1) is True


# Cenário 10 — Devolução com reserva pendente mantém bike indisponível

def test_return_bike_with_pending_hold_keeps_bike_unavailable(service):
   
    service.borrow_bike(rider_id=10, bike_id=1)
    service.hold_bike(rider_id=40, bike_id=1)

    result = service.return_bike(rider_id=10, bike_id=1)

    assert result is True
    assert service.bike_repository.is_available(bike_id=1) is False


# Cenário 11 — Empréstimo pelo próprio usuário que tinha reserva remove a reserva

def test_borrow_bike_removes_own_hold(service):
   
    service.rental_repository.create_rental(rider_id=10, bike_id=3)

    service.hold_bike(rider_id=40, bike_id=3)

    service.return_bike(rider_id=10, bike_id=3)
    assert service.bike_repository.is_available(bike_id=3) is False

    service.bike_repository.mark_available(bike_id=3)

    result = service.borrow_bike(rider_id=40, bike_id=3)

    assert result is True
    assert service.hold_repository.has_hold(rider_id=40, bike_id=3) is False


# Cenário 12 — Sequência completa: empréstimo → reserva → devolução → novo empréstimo

def test_full_flow_borrow_hold_return_borrow(service):

    assert service.borrow_bike(rider_id=10, bike_id=1) is True

    assert service.borrow_bike(rider_id=40, bike_id=1) is False

    assert service.hold_bike(rider_id=40, bike_id=1) is True

    assert service.return_bike(rider_id=10, bike_id=1) is True
    assert service.bike_repository.is_available(bike_id=1) is False

    service.bike_repository.mark_available(bike_id=1)

    assert service.borrow_bike(rider_id=40, bike_id=1) is True
    assert service.hold_repository.has_hold(rider_id=40, bike_id=1) is False

    assert service.borrow_bike(rider_id=10, bike_id=1) is False