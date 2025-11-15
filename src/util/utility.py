# GravityClock
#
# ユーティリティ関数
#
# Copyright (c) 2025 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください

import ctypes
import sys


# プライマリディスプレイのサイズを取得する
def get_screen_size(window_handle=None) -> tuple[int, int]:
    if sys.platform == "win32":
        from util.win32 import get_monitor_size_for_window
        return get_monitor_size_for_window(window_handle, use_work_area=False)
    else:
        try:
            root = tk.Tk()
            root.withdraw()
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            root.destroy()
            return screen_width, screen_height
        except Exception:
            # 取得できない場合はデフォルトサイズを返す
            return 800, 600


# ウィンドウサイズを画面に収まるように調整する
def adjust_window_size(x: int, y: int, width: int, height: int, window_handle=None):
    screen_width, screen_height = get_screen_size(window_handle)
    if width > screen_width:
        width = screen_width
    if height > screen_height:
        height = screen_height

    # x, y が左上に来るように補正
    if x < 0:
        x = 0
    if y < 0:
        y = 0

    # 右や下にはみ出さないように補正
    if x + width > screen_width:
        x = screen_width - width
    if y + height > screen_height:
        y = screen_height - height

    return x, y, width, height


# 画面のスケーリングを取得する
def get_display_scale():
    # --- Windowsの場合 ---
    if sys.platform == "win32":
        try:
            user32 = ctypes.windll.user32
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
            hDC = user32.GetDC(0)
            dpi_x = ctypes.windll.gdi32.GetDeviceCaps(hDC, 88)
            user32.ReleaseDC(0, hDC)
            scale = dpi_x / 96.0
            return scale
        except Exception:
            return 1.0

    # --- Linux/macOSなど他OSの場合 ---
    else:
        return 1.0


# 使い方例
if __name__ == "__main__":
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

    size = get_screen_size()
    print(f"画面サイズ: {size[0]}x{size[1]}")

    scale = get_display_scale()
    print(f"現在のスケーリング: {scale*100:.0f}%")
