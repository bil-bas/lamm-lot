from kivy.uix.screenmanager import Screen

from .config import get_config, save_config, get_secrets, save_secrets


class SettingsScreen(Screen):
    def on_enter(self, *args):
        self.ids["secret_token"].text = get_secrets().lend_engine_token

        self.ids["image_url"].text = get_config().lend_engine.image_url
        self.ids["site_url"].text = get_config().lend_engine.site_url

    def save(self):
        get_secrets().lend_engine_token = self.ids["secret_token"].text.strip()
        save_secrets()

        get_config().lend_engine.image_url = self.ids["image_url"].text.strip()
        get_config().lend_engine.site_url = self.ids["site_url"].text.strip()
        save_config()
