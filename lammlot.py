#!/usr/bin/env python

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

from lammlot.sticker_screen import StickerScreen
from lammlot.search_screen import SearchScreen
from lammlot.sheet_screen import SheetScreen
from lammlot.settings_screen import SettingsScreen
from lammlot.home_screen import HomeScreen


class LAMMLoTApp(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(HomeScreen())  # Initial.
        sm.add_widget(SettingsScreen())
        sm.add_widget(SearchScreen())
        sm.add_widget(StickerScreen())
        sm.add_widget(SheetScreen())
        return sm


if __name__ == "__main__":
    LAMMLoTApp().run()
