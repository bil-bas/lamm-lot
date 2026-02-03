from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.image import Image

from .lend_engine_client import LendEngineClient
from .search_results import SearchResult


class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._sites: list[str] = []
        self._item_data: list[dict] = []

        self._client = LendEngineClient()

        self.refresh_sites()
        self._current_site = self._sites[0]  # TODO: read from settings file.
        self.ids["site_picker"].text = self._current_site["name"]

        self.refresh_items()

    def refresh_sites(self):
        self._sites = self._client.fetch_sites()

    def refresh_items(self):
        return

        items = self._client.fetch_items(site=self._current_site["@id"], query=self.ids["search"].text)

        self.ids["item_list"].data = items

        for item in items:
            result = SearchResult(text=item["sku"])
            result.sku = item["sku"]

            text = BoxLayout(orientation="vertical")
            result.add_widget(text)

            text.add_widget(Label(text=f"[b]{item["sku"]}[/b] - {item["name"]["en"]}", markup=True))
            text.add_widget(Label(text=(item["description"]["en"] or "")[:80]))
            text.add_widget(Label(text=f"£{item["loanFee"]} per week"))

            if "image" in item:
                result.add_widget(Image(source=item["image"]))

            result.bind(on_press=lambda btn: print(btn.sku))

            item_list.add_widget(result)

    def site_data(self):
        if not self._sites:
            self.refresh_sites()

        return [
            {
                "text": f"{site["name"]}",
                "on_release": lambda x=f"{i}": self.callback_site_menu(x),
            } for i, site in enumerate(self._sites)
        ]

    def open_site_menu(self, item: any):
        self._site_menu = DropDown(caller=item, items=self.site_data(), width=500)
        self._site_menu.open()

    def callback_site_menu(self, item_index: str):
        self._site_menu.dismiss()
        self._current_site = self._sites[int(item_index)]
        self.ids["site_picker"].text = self._current_site["name"]

        self.refresh_items()
