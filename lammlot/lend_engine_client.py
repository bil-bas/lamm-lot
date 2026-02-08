import os
import requests
import urllib.parse as urlparse
from pathlib import Path

from .config import get_config


class LendEngineClient:
    ENV_TOKEN = "LEND_ENGINE_TOKEN"

    def __init__(self):
        response = requests.post(
            self.api_url("token/refresh"),
            data={"refresh_token": os.environ[self.ENV_TOKEN]},
            verify=False)
        self._token = response.json()["token"]

    def site_url(self, relative_path: str) -> str:
        return urlparse.urljoin(get_config().lend_engine.site_url,
                                relative_path)

    def api_url(self, relative_path: str) -> str:
        return urlparse.urljoin(get_config().lend_engine.api_url,
                                relative_path)

    def _get_list(self, uri, **kwargs):
        response = requests.get(
            self.api_url(uri),
            headers={"Authorization": f"Bearer {self._token}"},
            verify=False,
            **kwargs)
        return response.json()

    def fetch_sites(self) -> list[dict]:
        sites = self._get_list("sites")["hydra:member"]
        return [site for site in sites if site["isActive"]]

    def fetch_items(self, site: str, name: str, sku: str) -> list[dict]:
        params = {"name": name, "sku": sku}
        items = self._get_list("items", params=params)["hydra:member"]

        for item in items:
            if item["imageName"]:
                item["image"] = self._fetch_image(item["imageName"])

        return [item for item in items if self._valid_item(item, site)]

    def _valid_item(self, item: dict, site: str) -> bool:
        return (item["isActive"] and
                item["itemType"] == "loan" and
                site in item["sites"])

    def _fetch_image(self, filename: str) -> str:
        folder = Path("./images_cache")
        folder.mkdir(exist_ok=True)

        image_path = folder / filename
        if not image_path.exists():
            response = requests.get(
                urlparse.urljoin(get_config().lend_engine.image_url, filename))
            image_path.write_bytes(response.content)

        return str(image_path)
