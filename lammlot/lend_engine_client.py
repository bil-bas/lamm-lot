class LendEngineClient:
    def fetch_locations(self) -> list[str]:
        return ["Lancaster Community Makerspace", "Lancaster BID", "Good Things Collective"]

    def fetch_items(self, query: str) -> list[dict]:
        return [
            {
                "title": f"{query} {i + 1}",
                "description": "Something, something, something, something, something",
                "cost": "2",
            } for i in range(20)
        ]
