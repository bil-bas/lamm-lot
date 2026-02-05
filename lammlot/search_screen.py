from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

from .lend_engine_client import LendEngineClient
from . import search_results


class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._sites: list[str] = []
        self._site = None
        self._items: list[dict] = []
        self._api_client = LendEngineClient()

        Clock.schedule_once(self.fetch_sites, 0.25)

    def fetch_sites(self, called_after: float = 0) -> None:
        self._sites = self._api_client.fetch_sites()
        self._site = self._sites[0]  # TODO: read from settings file.
        self.ids["site_picker"].text = self._site["name"]

    def refresh_items(self) -> None:
        self._items = self._api_client.fetch_items(site=self._site["@id"],
                                                   name=self.ids["name_search"].text,
                                                   sku=self.ids["sku_search"].text)

        for i, item in enumerate(self._items):
            item["index"] = i
            item["image_"] = item["image"] if "image" in item else ""
            item["title_"] = f"[b]{item["sku"]}[/b] - {item["name"]["en"]}"
            item["description_"] = item["description"]["en"] or ""
            item["loan_fee_"] = f"£{item["loanFee"]} per week"

        self.ids["item_list"].data = self._items

    def open_site_menu(self, widget: Button) -> None:
        drop_down = DropDown()

        for site in self._sites:
            button = Button(text=site["name"], size_hint_y=None, height=50)
            button.bind(on_release=lambda b: self.callback_site_menu(b, drop_down))
            drop_down.add_widget(button)

        drop_down.open(widget)

    def callback_site_menu(self, button: Button, drop_down: DropDown) -> None:
        drop_down.dismiss()
        self._site = self.find_site(button.text)
        self.ids["site_picker"].text = button.text
        self._item.clear()

    def find_site(self, name: str) -> None:
        for site in self._sites:
            if site["name"] == name:
                return site

        raise RuntimeError("Site not found")

    def on_generate(self) -> None:
        self.manager.get_screen('sticker').selected = self._items
        self.manager.get_screen('sticker').site = self._site

        self.manager.current = 'sticker'

