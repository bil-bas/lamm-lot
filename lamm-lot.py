#!/usr/bin/env python


from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivymd.toast import toast


class LAMMLotWindow(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._locations: list[str] = []
        self._item_data: list[dict] = []

        self.refresh_locations()
        self.refresh_items()

        self.ids.location_picker.text = self._locations[0]  # TODO: read from settings file.

    def refresh_locations(self):
        self._locations = ["Lancaster Community Makerspace", "Lancaster BID", "Good Things Collective"]

    def refresh_items(self):
        self._items = [
            {
                "text": "fish",

            },
            {
                "text": "cheese",
            }
        ]

        items = self.ids.item_list

        items.clear_widgets()

        for item in self._items:
            items.add_widget(MDLabel(text=item["text"]))

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


class LAMMLoTApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        return LAMMLotWindow()


if __name__ == "__main__":
    LAMMLoTApp().run()
