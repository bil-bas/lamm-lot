#!/usr/bin/env python

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from kivy.app import App

from lammlot.main_window import MainWindow

class LAMMLoTApp(App):
    def build(self):
        return MainWindow()


if __name__ == "__main__":
    LAMMLoTApp().run()
