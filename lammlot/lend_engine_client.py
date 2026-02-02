import os
import requests
from PIL import Image
import urllib.parse as urlparse


class LendEngineClient:
    API_BASE_URL = "https://lammlibrary.lend-engine-app.com/api/2/"
    IMAGE_BASE_URL = "https://s3-us-west-2.amazonaws.com/lend-engine/lammlibrary/large/"
    ENV_TOKEN = "LEND_ENGINE_TOKEN"

    def __init__(self):
        response = requests.post(urlparse.urljoin(self.API_BASE_URL, "token/refresh"),
                                 data={"refresh_token": os.environ[self.ENV_TOKEN]},
                                 verify=False)
        self._token = response.json()["token"]

    def _get_list(self, uri, **kwargs):
        response = requests.get(urlparse.urljoin(self.API_BASE_URL, uri),
                                headers={"Authorization": f"Bearer {self._token}"},
                                verify=False,
                                **kwargs)
        return response.json()

    def fetch_sites(self) -> list[str]:
        sites = self._get_list("sites")["hydra:member"]
        return [site for site in sites if site["isActive"]]

    def fetch_items(self, site: str, query: str) -> list[dict]:
        items = self._get_list("items", params={})["hydra:member"]

        for item in items:
            if item["imageName"]:
                item["image"] = self._fetch_image(item["imageName"])

        return [item for item in items if item["isActive"] and item["itemType"] == "loan" and site in item["sites"]]

    def _fetch_image(self, filename: str) -> str:
        try:
            os.mkdir("./images_cache")
        except:
            pass

        cache_path = os.path.join("./images_cache", filename)
        if not os.path.exists(cache_path):
            response = requests.get(urlparse.urljoin(self.IMAGE_BASE_URL, filename))

            with open(cache_path, "wb") as f:
                f.write(response.content)

        return cache_path