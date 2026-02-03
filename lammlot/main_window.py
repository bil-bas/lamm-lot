from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button

from .lend_engine_client import LendEngineClient
from .search_results import SearchResults


class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._sites: list[str] = []
        self._item_data: list[dict] = []

        self._client = LendEngineClient()

        self.fetch_sites()
        self.refresh_items()

    def fetch_sites(self) -> None:
        self._sites = self._client.fetch_sites()
        self._current_site = self._sites[0]  # TODO: read from settings file.
        self.ids["site_picker"].text = self._current_site["name"]

    def refresh_items(self) -> None:
        items = self._client.fetch_items(site=self._current_site["@id"],
                                         name=self.ids["name_search"].text,
                                         sku=self.ids["sku_search"].text)

        for item in items:
            item["image_"] = item["image"] if "image" in item else ""
            item["title_"] = f"[b]{item["sku"]}[/b] - {item["name"]["en"]}"
            item["description_"] = item["description"]["en"] or ""
            item["loan_fee_"] = f"£{item["loanFee"]} per week"

        self.ids["item_list"].data = items

    def open_site_menu(self, widget: Button) -> None:
        drop_down = DropDown()

        for site in self._sites:
            button = Button(text=site["name"], size_hint_y=None, height=50)
            button.bind(on_release=lambda b: self.callback_site_menu(b, drop_down))
            drop_down.add_widget(button)

        drop_down.open(widget)

    def callback_site_menu(self, button: Button, drop_down: DropDown) -> None:
        drop_down.dismiss()
        self._current_site = self.find_site(button.text)
        self.ids["site_picker"].text = button.text
        self.refresh_items()

    def find_site(self, name: str):
        for site in self._sites:
            if site["name"] == name:
                return site

        raise RuntimeError("Site not found")
