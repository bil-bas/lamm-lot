from logging import Logger

_log = Logger(__name__)


SITES = {
    "lm": "Lancaster Makerspace",
    "ha": "Halton",
}

CATEGORIES = {
    "anc": "Art & Craft",
    "edc": "Education",
    "mne": "Music & Entertainment",
    "trn": "Transport",
    "spr": "Sport",
    "otd": "Outdoor pursuits",
    "env": "Environment",
    "diy": "DIY",
    "pne": "Parties & events",
    "hsh": "Household",
    "grd": "Garden",
    "tng": "Toys & games"
}


class Item:
    def __init__(self, data: dict):
        self._data = data

        self._is_selected = False

        if self.is_valid:
            self._check()

    @property
    def name(self) -> str:
        return self._data["name"]["en"]

    @property
    def sku(self) -> str:
        return self._data["sku"]

    @property
    def id(self) -> str:
        return self._data["id"]

    @property
    def description(self) -> str:
        return self._data["description"]["en"] or ""

    @property
    def is_valid(self) -> bool:
        return self._data["isActive"] and self._data["itemType"] == "loan"

    @property
    def image_name(self) -> str:
        return self._data["imageName"]

    @property
    def image(self) -> str:
        return self._data.get("image") or ""

    @property
    def deposit_amount(self) -> float:
        return self._data["depositAmount"] or 0.0

    @property
    def loan_fee(self) -> float:
        return self._data["loanFee"] or 0.0

    @image.setter
    def image(self, value: str) -> None:
        self._data["image"] = value

    @property
    def url(self) -> str:
        return self._data.get("url") or ""

    @url.setter
    def url(self, value: str) -> None:
        self._data["url"] = value

    @property
    def is_selected(self) -> bool:
        return self._is_selected

    @property
    def sites(self) -> list[str]:
        return [site["site"] for site in self._data["itemSites"]]

    def select(self) -> None:
        self._is_selected = True

    def deselect(self) -> None:
        self._is_selected = False

    def _check(self) -> None:
        self._check_sku()

        self._assert_not_in("priceSell", {0, "", None})
        self._assert_not_in("loanFee", {0, "", None})

        if self._data["priceSell"]:
            fee_multiplier = 0.75
            loan_fee = float(self._data["priceSell"]) * fee_multiplier
            self._assert_near("loanFee", loan_fee)

    def _check_sku(self) -> None:
        site, section, desc, count = self.sku.split(".")

        self._assert(f"'{site}' in {repr(list(SITES.keys()))}")
        self._assert(f"'{section}' in {repr(list(CATEGORIES.keys()))}")
        self._assert(f"len('{desc}') <= 5")
        self._assert(f"{int(count)} in range(1, 100)")

    def __str__(self) -> str:
        return f"{self.sku} {self.name}"

    def _assert(self, condition: str):
        if eval(condition):
            return
        _log.warning(f"{self} ({condition}) is False")

    def _assert_in(self, key: str, values: list):
        if self._data[key] in values:
            return
        _log.warning(f"{self} {key} not in {repr(values)} ({self._data[key]})")

    def _assert_not_in(self, key: str, values) -> None:
        if self._data[key] not in values:
            return
        _log.warning(f"{self} {key} in {repr(values)} ({self._data[key]})")

    def _assert_equal(self, key: str, value) -> None:
        if self._data[key] == value:
            return
        _log.warning(f"{self} {key} != {value} ({self._data[key]})")

    def _assert_not_equal(self, key: str, value) -> None:
        if self._data[key] != value:
            return
        _log.warning(f"{self} {key} == {value} ({self._data[key]})")

    def _assert_near(self, key: str, value) -> None:
        expected = float(value)
        if expected > value * 0.99 and expected < value * 1.01:
            return

        _log.warning(f"{self} {key} not near {value} ({self._data[key]})")
