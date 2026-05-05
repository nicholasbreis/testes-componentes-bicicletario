class RiderRepository:
    def __init__(self):
        self._riders = {
            10: {"name": "Ana", "blocked": False, "active_account": True},
            20: {"name": "Bruno", "blocked": True, "active_account": True},
            30: {"name": "Carla", "blocked": False, "active_account": False},
            40: {"name": "Diego", "blocked": False, "active_account": True},
        }

    def exists(self, rider_id: int) -> bool:
        return rider_id in self._riders

    def is_blocked(self, rider_id: int) -> bool:
        if rider_id not in self._riders:
            return False
        return self._riders[rider_id]["blocked"]

    def has_active_account(self, rider_id: int) -> bool:
        if rider_id not in self._riders:
            return False
        return self._riders[rider_id]["active_account"]
