class RentalRepository:
    def __init__(self):
        self._active_rentals = []

    def create_rental(self, rider_id: int, bike_id: int) -> None:
        self._active_rentals.append({"rider_id": rider_id, "bike_id": bike_id})

    def has_active_rental(self, bike_id: int) -> bool:
        return any(rental["bike_id"] == bike_id for rental in self._active_rentals)

    def is_bike_with_rider(self, rider_id: int, bike_id: int) -> bool:
        return any(
            rental["rider_id"] == rider_id and rental["bike_id"] == bike_id
            for rental in self._active_rentals
        )

    def count_active_rentals(self, rider_id: int) -> int:
        return sum(1 for rental in self._active_rentals if rental["rider_id"] == rider_id)

    def close_rental(self, rider_id: int, bike_id: int) -> None:
        for rental in list(self._active_rentals):
            if rental["rider_id"] == rider_id and rental["bike_id"] == bike_id:
                self._active_rentals.remove(rental)
                return
        raise ValueError("Active rental not found")
