class BikeShareService:
    def __init__(self, bike_repository, rider_repository, rental_repository, hold_repository):
        self.bike_repository = bike_repository
        self.rider_repository = rider_repository
        self.rental_repository = rental_repository
        self.hold_repository = hold_repository

    def borrow_bike(self, rider_id: int, bike_id: int) -> bool:
        if not rider_id or not bike_id:
            raise ValueError("Rider ID and bike ID are required")

        if not self.rider_repository.exists(rider_id):
            return False

        if not self.bike_repository.exists(bike_id):
            return False

        if self.rider_repository.is_blocked(rider_id):
            return False

        if not self.rider_repository.has_active_account(rider_id):
            return False

        if not self.bike_repository.is_available(bike_id):
            return False

        if self.rental_repository.count_active_rentals(rider_id) >= 2:
            return False

        next_rider = self.hold_repository.next_rider(bike_id)
        if next_rider is not None and next_rider != rider_id:
            return False

        self.bike_repository.mark_unavailable(bike_id)
        self.rental_repository.create_rental(rider_id, bike_id)

        if self.hold_repository.has_hold(rider_id, bike_id):
            self.hold_repository.remove_hold(rider_id, bike_id)

        return True

    def return_bike(self, rider_id: int, bike_id: int) -> bool:
        if not rider_id or not bike_id:
            raise ValueError("Rider ID and bike ID are required")

        if not self.rental_repository.is_bike_with_rider(rider_id, bike_id):
            return False

        self.rental_repository.close_rental(rider_id, bike_id)

        if not self.hold_repository.has_any_hold(bike_id):
            self.bike_repository.mark_available(bike_id)

        return True

    def hold_bike(self, rider_id: int, bike_id: int) -> bool:
        if not rider_id or not bike_id:
            raise ValueError("Rider ID and bike ID are required")

        if not self.rider_repository.exists(rider_id):
            return False

        if not self.bike_repository.exists(bike_id):
            return False

        if self.rider_repository.is_blocked(rider_id):
            return False

        if not self.rider_repository.has_active_account(rider_id):
            return False

        if self.bike_repository.is_available(bike_id):
            return False

        if self.hold_repository.has_hold(rider_id, bike_id):
            return False

        if self.rental_repository.is_bike_with_rider(rider_id, bike_id):
            return False

        self.hold_repository.add_hold(rider_id, bike_id)
        return True
