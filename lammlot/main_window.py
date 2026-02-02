from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import ThreeLineIconListItem
from kivymd.toast import toast

from .lend_engine_client import LendEngineClient


class MainWindow(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._locations: list[str] = []
        self._item_data: list[dict] = []

        self._client = LendEngineClient()
        self.refresh_locations()
        self.refresh_items()

        self.ids.location_picker.text = self._locations[0]  # TODO: read from settings file.

    def refresh_locations(self):
        self._locations = self._client.fetch_locations()

    def refresh_items(self):
        items = self._client.fetch_items(self.ids.search.text or "search")

        items_list = self.ids.item_list

        items_list.clear_widgets()

        for item in items:
            items_list.add_widget(
                ThreeLineIconListItem(
                    text=item["title"],
                    secondary_text=item["description"],
                    tertiary_text=f"£{item["cost"]} per week",
                )
            )

    def location_data(self):
        if not self._locations:
            self.refresh_locations()

        return [
            {
                "text": f"{location}",
                "on_release": lambda x=f"{location}": self.callback_location_menu(x),
            } for location in self._locations
        ]

    def open_location_menu(self, item: MDDropDownItem):
        self._location_menu = MDDropdownMenu(caller=item, items=self.location_data(), width=500)
        self._location_menu.open()

    def callback_location_menu(self, text_item: str):
        self._location_menu.dismiss()
        self.ids.location_picker.text = text_item
