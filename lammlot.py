#!/usr/bin/env python

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

from lammlot.sticker_screen import StickerScreen
from lammlot.search_screen import SearchScreen
from lammlot.sheet_screen import SheetScreen


class LAMMLoTApp(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(SearchScreen())  # Initial.
        sm.add_widget(StickerScreen())
        sm.add_widget(SheetScreen())
        return sm


if __name__ == "__main__":
    LAMMLoTApp().run()
