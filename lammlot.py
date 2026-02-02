#!/usr/bin/env python

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from kivymd.app import MDApp

from lammlot.main_window import MainWindow

class LAMMLoTApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        return MainWindow()


if __name__ == "__main__":
    LAMMLoTApp().run()
