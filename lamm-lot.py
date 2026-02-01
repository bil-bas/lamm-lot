#!/usr/bin/env python


from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.widget import MDWidget
from kivymd.toast import toast


class LAMMLotWindow(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._locations: list[dict] = []
        self.ids.location_picker.text = "Lancaster Community Makerspace"

    def refresh_locations(self, widget: MDWidget = None):
        self._locations = [
            {
                "text": location,
                "on_release": lambda x=location: self.callback_location_menu(x),
            } for location in ["Lancaster Community Makerspace", "Lancaster BID", "Good Things Collective"]
        ]

    def open_location_menu(self, item: MDDropDownItem):
        if not self._locations:
            self.refresh_locations()

        # This should be left-aligned from the button, but no idea how to do that right now!
        self._location_menu = MDDropdownMenu(caller=item, items=self._locations,
                                             pos_hint={"center_x": 0.5})
        self._location_menu.open()

    def callback_location_menu(self, text_item: str):
        self._location_menu.dismiss()
        toast(f"Changed location to {text_item}")
        self.ids.location_picker.text = text_item


class LAMMLoTApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        return LAMMLotWindow()


if __name__ == "__main__":
    LAMMLoTApp().run()
