from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.factory import Factory

from .lend_engine_client import LendEngineClient
from .search_result import SearchResult, SelectableRecycleBoxLayout
from .config import get_config, save_config


class SearchScreen(Screen):
    @property
    def selected_items(self) -> list[SearchResult]:
        return [self._items[c.index]
                for c in self.item_list_container.children if c.selected]

    @property
    def item_list_container(self) -> SelectableRecycleBoxLayout:
        return self.ids["item_list_container"]

    @property
    def sticker_size(self) -> list[int]:
        return get_config().options.current_sticker_size

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._sites: list[dict] = []
        self._site: dict = {}
        self._items: list[dict] = []
        self._api_client = LendEngineClient()
        self._add_size_buttons()

        Clock.schedule_once(self.fetch_sites, 0.25)

    def _add_size_buttons(self):
        self.ids["sticker_size_buttons"].clear_widgets()

        for size in get_config().options.sticker_sizes:
            button = Factory.StickerSizeButton()
            button.screen = self
            button.sticker_size = size
            self.ids["sticker_size_buttons"].add_widget(button)

    def set_sticker_size(self, size: list[int]) -> None:
        get_config().options.current_sticker_size = list(size)
        save_config()

    def fetch_sites(self, called_after: float = 0) -> None:
        self._sites = self._api_client.fetch_sites()
        self._site = self.find_site(get_config().options.current_site)
        self.ids["site_picker"].text = self._site["name"]

    def refresh_items(self) -> None:
        self._items = self._api_client.fetch_items(
            site=self._site["@id"],
            name=self.ids["name_search"].text,
            sku=self.ids["sku_search"].text)

        if self._items:
            for item in self._items:
                item["url"] = self._api_client.site_url(
                    f"product/{item["id"]}")
                item["selected"] = False

            self.ids["item_list"].data = [
                self._list_data(item, i) for i, item in enumerate(self._items)
            ]

            self.ids["search_empty"].text = ""

        else:
            self.ids["item_list"].data = []
            self.ids["search_empty"].text = "No results found!"

        self.item_list_container.clear_selection()

    def _list_data(self, item: dict, index: int) -> dict:
        sku, name = item["sku"], item["name"]["en"]

        assert isinstance(item.get("image", ""), str)

        return {
            "index": index,
            "image": item.get("image", ""),
            "title": f"[b]{sku}[/b] - {name}",
            "description": item["description"]["en"] or "",
            "loan_fee_": f"£{item["loanFee"]} per week",
            "screen": self,
        }

    def open_site_menu(self, widget: Button) -> None:
        drop_down = DropDown()

        def callback(button):
            self.callback_site_menu(button, drop_down)

        for site in self._sites:
            button = Button(text=site["name"], size_hint_y=None, height=50)
            button.bind(on_release=callback)  # type: ignore
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

    def find_site(self, name: str) -> dict:
        for site in self._sites:
            if site["name"] == name:
                return site

        return self._sites[0]

    def on_generate(self) -> None:
        screen = self.manager.get_screen("sticker")
        screen.sticker_size = self.sticker_size
        screen.selected = self.selected_items
        screen.site = self._site

        self.manager.current = "sticker"

    def update_selected(self) -> None:
        selected_items = self.selected_items
        self.ids["generate_button"].disabled = not selected_items
        self.ids["select_all"].disabled = (
            not self._items or len(selected_items) == len(self._items))
        self.ids["select_none"].disabled = not selected_items
