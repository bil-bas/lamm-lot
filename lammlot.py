#!/usr/bin/env python

from kivymd.app import MDApp

from lammlot.main_window import MainWindow

class LAMMLoTApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        return MainWindow()


if __name__ == "__main__":
    LAMMLoTApp().run()
