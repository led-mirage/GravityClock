# GravityClock
#
# 設定ウィンドウからのAPI呼び出しを処理するクラス
#
# Copyright (c) 2025 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください

import json

from const import APP_NAME, APP_VERSION, COPYRIGHT
from settings import Settings


class SettingsAPI:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._window = None
        self._main_window = None

    def set_window(self, window, on_closed=None):
        self._window = window
        if on_closed:
            self._window.events.closed += on_closed

    def set_main_window(self, main_window):
        self._main_window = main_window

    def get_app_info(self):
        return {
            "name": APP_NAME,
            "version": APP_VERSION,
            "copyright": COPYRIGHT
        }
   
    def get_settings(self):
        return self._settings.to_dict()

    def get_default_settings(self):
        default = Settings()
        return default.to_dict()

    def apply_settings(self, settings_dict: dict):
        self._settings.from_dict(settings_dict)
        self._settings.save()
        self._window.destroy()
        js_literal = json.dumps(self._settings.to_dict())
        self._main_window.evaluate_js(f"updateSettings({js_literal});")
        self._main_window.on_top = self._settings.window.get("onTop")

    def cancel_settings(self):
        self._window.destroy()
