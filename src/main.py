# GravityClock
#
# エントリポイント
#
# Copyright (c) 2025 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください

import sys

import webview

from api.main_api import MainAPI
from const import APP_NAME
from settings import Settings
from util.utility import adjust_window_size


def run():
    if sys.platform == "win32":
        from util.win32 import enable_high_dpi_awareness
        enable_high_dpi_awareness()

    settings = Settings()
    settings.load()

    x, y, width, height = adjust_window_size(
        settings.window.get("x", 0),
        settings.window.get("y", 0),
        settings.window.get("width", 400),
        settings.window.get("height", 180)
    )

    main_api = MainAPI(settings)
    main_window = webview.create_window(
        APP_NAME,
        url="view/main.html",
        js_api=main_api,
        background_color="#000000",
        x=x,
        y=y,
        width=width,
        height=height,
        min_size=(50,25),
        frameless=True,
        transparent=True,
        on_top=settings.window.get("onTop", True),
        easy_drag=False
    )
    main_api.set_window(main_window)
    webview.start()


if __name__ == '__main__':
    run()
