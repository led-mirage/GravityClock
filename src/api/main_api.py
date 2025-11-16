# GravityClock
#
# メインウィンドウからのAPI呼び出しを処理するクラス
#
# Copyright (c) 2025 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください

import sys
import threading

import webview
from webview.window import FixPoint

from api.settings_api import SettingsAPI
from const import APP_NAME
from util.utility import get_display_scale, adjust_window_size


class MainAPI:
    def __init__(self, settings):
        self._settings = settings
        self._window = None
        self._is_window_maximized = False
        self._move_timer = None
        self._resize_timer = None
        self._settings_window = None
        self._is_settings_window_opend = False

    def set_window(self, window):
        self._window = window
        self._window.events.maximized += self.on_window_maximized
        self._window.events.restored += self.on_window_restored
        self._window.events.moved += self.on_window_moved
        self._window.events.resized += self.on_window_resized
        self._window.events.shown += self.on_window_shown

    def get_settings(self):
        return self._settings.to_dict()

    def get_window_position(self):
        # DPIスケーリングを考慮して位置を取得（Windowsのみ）
        scale = get_display_scale()
        x = round(self._window.x / scale)
        y = round(self._window.y / scale)
        return {"x": x, "y": y}

    def resize_window(self, width, height, resizeDir):
        scale = get_display_scale()
        width = round(width * scale)
        height = round(height * scale)

        fp = FixPoint.NORTH | FixPoint.WEST
        if (resizeDir["onLeft"] or resizeDir["onTop"]):
            fp = FixPoint.SOUTH | FixPoint.EAST
        self._window.resize(width, height, fix_point=fp)

    def move_window(self, x, y):
        self._window.move(x, y)

    def maximize_window(self):
        if not self._is_window_maximized:
            self._window.maximize()
        else:
            self._window.restore()

    def minimize_window(self):
        self._window.minimize()

    def restore_window(self):
        self._window.restore()

    def on_window_maximized(self):
        self._is_window_maximized = True
        self._window.evaluate_js("onWindowMaximized()")

    def on_window_restored(self):
        self._is_window_maximized = False
        self._window.evaluate_js("onWindowRestored()")

    def on_window_moved(self, x: int, y: int):
        # 既存タイマーをキャンセル
        if self._move_timer and self._move_timer.is_alive():
            self._move_timer.cancel()
        
        # 一定時間後に保存
        self._move_timer = threading.Timer(1.0, self._save_window_pos, args=(x, y))
        self._move_timer.start()
    
    def _save_window_pos(self, x: int, y: int):
        self._settings.window["x"] = x
        self._settings.window["y"] = y
        self._settings.save()

    def on_window_resized(self, width: int, height: int):
        if self._is_window_maximized or self._window.minimized:
            return

        # 既存タイマーをキャンセル
        if self._resize_timer and self._resize_timer.is_alive():
            self._resize_timer.cancel()
        
        # 一定時間後に保存
        self._resize_timer = threading.Timer(1.0, self._save_size, args=(width, height))
        self._resize_timer.start()
  
    def _save_size(self, width: int, height: int):
        self._settings.window["width"] = width
        self._settings.window["height"] = height
        self._settings.save()

    def on_window_shown(self):
        if sys.platform == "win32":
            # Windowsの場合、画面スケーリングが100%以外だと、
            # webviewの初期表示が拡大率に影響され物理ピクセル数にならない。
            # そのため、表示後にウィンドウサイズを調整する。
            #
            # また、LinuxではPyWebViewのresizeメソッドを呼ぶと、
            # それ以降ウィンドウサイズの変更ができなくなるため（たぶんPyWebViewのバグ）
            # main.pyの中でサイズ調整を行っている。
            # Linuxには画面スケーリングの概念がないため、これで問題ない。
            x, y, width, height = adjust_window_size(
                self._settings.window.get("x", 0),
                self._settings.window.get("y", 0),
                self._settings.window.get("width", 400),
                self._settings.window.get("height", 180),
                self._window.native.Handle
            )
            sclale = get_display_scale()
            self._window.move(round(x / sclale), round(y / sclale))
            self._window.resize(width, height)

    def open_settings_window(self):
        if self._is_settings_window_opend:
            return

        api = SettingsAPI(self._settings)
        self._settings_window = webview.create_window(
            f"{APP_NAME} - Settings",
            url="view/settings.html",
            width=650,
            height=850,
            js_api=api,
            on_top=self._settings.window.get("onTop"))
        api.set_window(self._settings_window, self.on_settings_window_closed)
        api.set_main_window(self._window)
        self._is_settings_window_opend = True
    
    def on_settings_window_closed(self):
        self._is_settings_window_opend = False

    def close_app(self):
        if self._is_settings_window_opend:
            self._settings_window.destroy()
        self._window.destroy()
        sys.exit(0)
