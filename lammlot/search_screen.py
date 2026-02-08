from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ListProperty
from omegaconf import OmegaConf

from .lend_engine_client import LendEngineClient
from .search_result import SearchResult, SearchResults
from .sticker_generator import StickerGenerator
from .config import get_config, save_config


class SearchScreen(Screen):
    @property
    def selected_items(self) -> list[SearchResult]:
        results: SearchResults = self.ids["item_list"]

        return [self._items[c.index] for c in results.children[0].children if c.selected]
    
    @property
    def sticker_size(self) -> list[int, int]:
        return self._sticker_size

    def __init__(self, **kwargs):
        self._sticker_size = get_config().options.sticker_size

        super().__init__(**kwargs)

        self._sites: list[str] = []
        self._site = None
        self._items: list[dict] = []
        self._api_client = LendEngineClient()

        Clock.schedule_once(self.fetch_sites, 0.25)

    def set_sticker_size(self, size: list[int, int]) -> None:
        self._sticker_size = size
        get_config().options.sticker_size = size
        save_config()

    def fetch_sites(self, called_after: float = 0) -> None:
        self._sites = self._api_client.fetch_sites()
        self._site = self.find_site(get_config().options.current_site) or self._sites[0]
        self.ids["site_picker"].text = self._site["name"]

    def refresh_items(self) -> None:
        self._items = self._api_client.fetch_items(site=self._site["@id"],
                                                   name=self.ids["name_search"].text,
                                                   sku=self.ids["sku_search"].text)
        
        for item in self._items:
            item["url"] = self._api_client.site_url(f"product/{item["id"]}")

        self.ids["item_list"].data = [self._list_data(item, i) for i, item in enumerate(self._items)]
        self.ids["generate_button"].disabled = True

    def _list_data(self, item: dict, index: int) -> dict:
        sku, name = item["sku"], item["name"]["en"]

        assert isinstance(item.get("image", ""), str)

        return {
            "index": index,
            "image": item.get("image", ""),
            # flake8 doesn't like square brackets in a string and inside the replacement braces.
            "title": f"[b]{sku}[/b] - {name}",
            "description": item["description"]["en"] or "",
            "loan_fee_": f"£{item["loanFee"]} per week",
            "screen": self,
        }

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
        self.ids["item_list"].data.clear()

        get_config().options.current_site = button.text
        save_config()

    def find_site(self, name: str) -> None:
        for site in self._sites:
            if site["name"] == name:
                return site

        raise RuntimeError("Site not found")

    def on_generate(self) -> None:
        screen = self.manager.get_screen("sticker")
        screen.sticker_size = self.sticker_size
        screen.selected = self.selected_items
        screen.site = self._site

        self.manager.current = "sticker"

    def update_selected(self) -> None:
        self.ids["generate_button"].disabled = not self.selected_items
