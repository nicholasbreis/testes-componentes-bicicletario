class BikeRepository:
    def __init__(self):
        self._bikes = {
            1: {"model": "Bike Urbana", "available": True},
            2: {"model": "Bike Híbrida", "available": True},
            3: {"model": "Bike Elétrica", "available": False},
        }

    def exists(self, bike_id: int) -> bool:
        return bike_id in self._bikes

    def is_available(self, bike_id: int) -> bool:
        if bike_id not in self._bikes:
            return False
        return self._bikes[bike_id]["available"]

    def mark_unavailable(self, bike_id: int) -> None:
        if bike_id not in self._bikes:
            raise ValueError("Bike not found")
        self._bikes[bike_id]["available"] = False

    def mark_available(self, bike_id: int) -> None:
        if bike_id not in self._bikes:
            raise ValueError("Bike not found")
        self._bikes[bike_id]["available"] = True
