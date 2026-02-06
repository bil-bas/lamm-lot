from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

from .lend_engine_client import LendEngineClient
from lammlot.search_results import SearchResult, SearchResults


class SearchScreen(Screen):
    @property
    def selected_items(self) -> list[SearchResult]:
        results: SearchResults = self.ids["item_list"]

        return [self._items[c.index] for c in results.children[0].children if c.selected]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._sticker_type = "large"
        self._sites: list[str] = []
        self._site = None
        self._items: list[dict] = []
        self._api_client = LendEngineClient()

        Clock.schedule_once(self.fetch_sites, 0.25)

    def set_sticker_type(self, button: ToggleButton, value: str) -> bool:
        # TODO: prevent button being toggled off.
        self._sticker_type = value

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

            # flake8 doesn't like aquare brackets in a string and inside the replacement braces.
            sku, name = item["sku"], item["name"]["en"]
            item["title_"] = f"[b]{sku}[/b] - {name}"

            item["description_"] = item["description"]["en"] or ""
            item["loan_fee_"] = f"£{item["loanFee"]} per week"
            item["screen"] = self

        self.ids["item_list"].data = self._items
        self.ids["generate_button"].disabled = True

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
        self._items.clear()

    def find_site(self, name: str) -> None:
        for site in self._sites:
            if site["name"] == name:
                return site

        raise RuntimeError("Site not found")

    def on_generate(self) -> None:
        if self._sticker_type == "sheet":
            screen = self.manager.get_screen("sheet")
        else:
            screen = self.manager.get_screen("sticker")
            screen.sticker_type = self._sticker_type

        screen.selected = self.selected_items
        screen.site = self._site

        self.manager.current = "sheet" if self._sticker_type == "sheet" else "sticker"

    def update_selected(self) -> None:
        self.ids["generate_button"].disabled = not self.selected_items

