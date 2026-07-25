import requests
import urllib.parse as urlparse
from pathlib import Path
from typing import Iterator

from .item import Item
from .config import get_config, get_secrets


class LendEngineClient:
    ENV_TOKEN = "LEND_ENGINE_TOKEN"
    API_FRAGMENT = "api/2/"
    TOKEN_FRAGMENT = "token/refresh"

    def fetch_token(self) -> None:
        response = requests.post(
            self.api_url(self.TOKEN_FRAGMENT),
            data={"refresh_token": get_secrets().lend_engine_token},
            verify=False)

        try:
            self._token = response.json()["token"]
        except KeyError:
            print(response.json())
            exit()
        except Exception as ex:
            print(type(ex))
            exit()

    def site_url(self, relative_path: str) -> str:
        return urlparse.urljoin(get_config().lend_engine.site_url,
                                relative_path)

    def api_url(self, relative_path: str) -> str:
        return urlparse.urljoin(self.site_url(self.API_FRAGMENT),
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

    def fetch_items(self, site: str, name: str, sku: str) -> Iterator[Item]:
        params = {"name": name, "sku": sku, "page": 1}

        while True:
            response = self._get_list("items", params=params)
            items = response["hydra:member"]

            yield from self._loan_items(site, items)

            if "hydra:next" in response["hydra:view"]:
                params["page"] += 1
            else:
                return

    def _loan_items(self, site: str, items: list[dict]) -> Iterator[Item]:
        for data in items:
            item = Item(data)
            if item.is_valid and site in item.sites:
                if item.image_name:
                    item.image = self._fetch_image(item.image_name)
                yield item

    def _fetch_image(self, filename: str) -> str:
        folder = Path("./images_cache")
        folder.mkdir(exist_ok=True)

        image_path = folder / filename
        if not image_path.exists():
            response = requests.get(
                urlparse.urljoin(get_config().lend_engine.image_url, filename))
            image_path.write_bytes(response.content)

        return str(image_path)
