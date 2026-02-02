import os
import requests

class LendEngineClient:
    BASE_URL = "https://lammlibrary.lend-engine-app.com/api/2"
    ENV_TOKEN = "LEND_ENGINE_TOKEN"

    def __init__(self):
        response = requests.post(f"{self.BASE_URL}/token/refresh",
                                 data={"refresh_token": os.environ[self.ENV_TOKEN]},
                                 verify=False)
        self._token = response.json()["token"]

    def _get_list(self, uri, **kwargs):
        response = requests.get(f"{self.BASE_URL}{uri}",
                                headers={"Authorization": f"Bearer {self._token}"},
                                verify=False,
                                **kwargs)
        return response.json()

    def fetch_sites(self) -> list[str]:
        sites = self._get_list("/sites")["hydra:member"]
        return [site for site in sites if site["isActive"]]

    def fetch_items(self, site: str, query: str) -> list[dict]:
        items = self._get_list("/items", params={})["hydra:member"]
        return [item for item in items if item["isActive"] and item["itemType"] == "loan" and site in item["sites"]]
