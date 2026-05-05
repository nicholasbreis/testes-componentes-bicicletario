class HoldRepository:
    def __init__(self):
        self._holds = []

    def add_hold(self, rider_id: int, bike_id: int) -> None:
        self._holds.append({"rider_id": rider_id, "bike_id": bike_id})

    def has_hold(self, rider_id: int, bike_id: int) -> bool:
        return any(
            entry["rider_id"] == rider_id and entry["bike_id"] == bike_id
            for entry in self._holds
        )

    def has_any_hold(self, bike_id: int) -> bool:
        return any(entry["bike_id"] == bike_id for entry in self._holds)

    def next_rider(self, bike_id: int):
        for entry in self._holds:
            if entry["bike_id"] == bike_id:
                return entry["rider_id"]
        return None

    def remove_hold(self, rider_id: int, bike_id: int) -> None:
        for entry in list(self._holds):
            if entry["rider_id"] == rider_id and entry["bike_id"] == bike_id:
                self._holds.remove(entry)
                return
        raise ValueError("Hold entry not found")
