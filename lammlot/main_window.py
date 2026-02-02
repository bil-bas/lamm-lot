from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import ThreeLineIconListItem, IconLeftWidgetWithoutTouch
from kivymd.toast import toast

from .lend_engine_client import LendEngineClient


class MainWindow(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._sites: list[str] = []
        self._item_data: list[dict] = []

        self._client = LendEngineClient()

        self.refresh_sites()
        self._current_site = self._sites[0]  # TODO: read from settings file.
        self.ids.site_picker.text = self._current_site["name"]

        self.refresh_items()

    def refresh_sites(self):
        self._sites = self._client.fetch_sites()

    def refresh_items(self):
        items = self._client.fetch_items(site=self._current_site["@id"], query=self.ids.search.text)

        items_list = self.ids.item_list

        items_list.clear_widgets()

        for item in items:
            item_widget = ThreeLineIconListItem(
                text=f"{item["sku"]} - {item["name"]["en"]}",
                secondary_text=item["description"]["en"] or "",
                tertiary_text=f"£{item["loanFee"]} per week",
            )
            if "image" in item:
                item_widget.add_widget(IconLeftWidgetWithoutTouch(icon=item["image"], width=100))

            items_list.add_widget(item_widget)

    def site_data(self):
        if not self._sites:
            self.refresh_sites()

        return [
            {
                "text": f"{site["name"]}",
                "on_release": lambda x=f"{i}": self.callback_site_menu(x),
            } for i, site in enumerate(self._sites)
        ]

    def open_site_menu(self, item: MDDropDownItem):
        self._site_menu = MDDropdownMenu(caller=item, items=self.site_data(), width=500)
        self._site_menu.open()

    def callback_site_menu(self, item_index: str):
        self._site_menu.dismiss()
        self._current_site = self._sites[int(item_index)]
        self.ids.site_picker.text = self._current_site["name"]

        self.refresh_items()
