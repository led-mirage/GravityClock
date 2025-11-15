# GravityClock
#
# アプリケーション設定
#
# Copyright (c) 2025 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください

import json
import os
import re


class Settings:
    FILE_VERSION = 1
    FILE_NAME = "settings.json"

    def __init__(self):
        self._init_member()

    def _init_member(self):
        self.simulation = {
            "N": 15,                    # ボールの数
            "G": 0.2,                   # 重力定数
        }
        self.mass = {
            "type": "random",           # "fixed" or "random"
            "fixedValue": 100,          # typeが"fixed"のときの質量
            "randomMinValue": 1,        # typeが"random"のときの質量の最小値
            "randomMaxValue": 500,      # typeが"random"のときの質量の最大値
        }
        self.radius = {
            "type": "mass_based",       # "fixed" or "random" or "mass_based"
            "fixedValue": 5,            # typeが"fixed"のときの半径
            "randomMinValue": 2,        # typeが"random"のときの半径の最小値
            "randomMaxValue": 6,        # typeが"random"のときの半径の最大値
        }
        self.color = {
            "type": "mass_based",       # "fixed" or "random" or "mass_based" or "cycling"
            "fixedValue": "#30dd80",  # typeが"fixed"のときの色
            "massBased0": "#00ffff",
            "massBased1": "#ffff00",
        }
        self.clock = {
            "visible": True,            # 時計表示の有無
            "fontSize": 48,             # 時計のフォントサイズ
            "fontFamily": "\"Segoe UI\", sans-serif",
        }
        self.window = {
            "onTop": True,              # 最前面に表示するか
            "x": 0,                     # ウィンドウ位置X座標（物理ピクセル座標）
            "y": 0,                     # ウィンドウ位置Y座標（物理ピクセル座標）
            "width": 400,               # ウィンドウ幅（物理ピクセル数）
            "height": 180,              # ウィンドウ高さ（物理ピクセル数）
        }   
    
    def save(self):
        with open(self.FILE_NAME, 'w', encoding="utf-8") as file:
            settings = {}
            settings["file_ver"] = self.FILE_VERSION
            settings["simulation"] = self.simulation
            settings["mass"] = self.mass
            settings["radius"] = self.radius
            settings["color"] = self.color
            settings["clock"] = self.clock
            settings["window"] = self.window
            json.dump(settings, file, ensure_ascii=False, indent=4)            

    def load(self):
        if not os.path.exists(self.FILE_NAME):
            self.save()
            return

        with open(self.FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)
            file_ver = data.get("file_ver", 0)
            self.from_dict(data)

        if file_ver < self.FILE_VERSION:
            self.save()

    def _update_dict(self, target: dict, src: dict):
        for key in target.keys():
            if key in src:
                target[key] = src[key]

    def to_dict(self):
        return {
            "simulation": self.simulation,
            "mass": self.mass,
            "radius": self.radius,
            "color": self.color,
            "clock": self.clock,
            "window": self.window,
        }

    def from_dict(self, data: dict):
        self._update_dict(self.simulation, data.get("simulation", {}))
        self._update_dict(self.mass, data.get("mass", {}))
        self._update_dict(self.radius, data.get("radius", {}))
        self._update_dict(self.color, data.get("color", {}))
        self._update_dict(self.clock, data.get("clock", {}))
        self._update_dict(self.window, data.get("window", {}))
        self._validate()

    def _validate(self):
        # ---- simulation ----
        if not isinstance(self.simulation.get("N"), int) \
           or (self.simulation["N"] < 0 or self.simulation["N"] > 100):
            self.simulation["N"] = 15

        if not isinstance(self.simulation.get("G"), (int, float)) \
           or (self.simulation["G"] < 0 or self.simulation["G"] > 10):
            self.simulation["G"] = 1.0

        # ---- mass ----
        mass_type = self.mass.get("type")
        if mass_type not in ("random", "fixed"):
            self.mass["type"] = "random"

        for key, default, minv, maxv in [
            ("fixedValue", 100, 1, 1000),
            ("randomMinValue", 1, 1, 1000),
            ("randomMaxValue", 500, 1, 1000),
        ]:
            v = self.mass.get(key)
            if not isinstance(v, (int, float)) or not (minv <= v <= maxv):
                self.mass[key] = default

        if self.mass["randomMinValue"] > self.mass["randomMaxValue"]:
            self.mass["randomMinValue"], self.mass["randomMaxValue"] = (
                self.mass["randomMaxValue"], self.mass["randomMinValue"])

        # ---- radius ----
        radius_type = self.radius.get("type")
        if radius_type not in ("fixed", "random", "mass_based"):
            self.radius["type"] = "random"

        for key, default, minv, maxv in [
            ("fixedValue", 3, 1, 10),
            ("randomMinValue", 1, 1, 10),
            ("randomMaxValue", 6, 1, 10),
        ]:
            v = self.radius.get(key)
            if not isinstance(v, (int, float)) or not (minv <= v <= maxv):
                self.radius[key] = default

        if self.radius["randomMinValue"] > self.radius["randomMaxValue"]:
            self.radius["randomMinValue"], self.radius["randomMaxValue"] = \
                self.radius["randomMaxValue"], self.radius["randomMinValue"]

        # ---- color ----
        color_type = self.color.get("type")
        if color_type not in ("fixed", "random", "mass_based", "cycling"):
            self.color["type"] = "fixed"
        if not isinstance(self.color.get("fixedValue"), str) or \
           not self._is_valid_color(self.color["fixedValue"]):
            self.color["fixedValue"] = "#30dd80"
        if not isinstance(self.color.get("massBased0"), str) or \
           not self._is_valid_color(self.color["massBased0"]):
            self.color["massBased0"] = "#00ffff"
        if not isinstance(self.color.get("massBased1"), str) or \
           not self._is_valid_color(self.color["massBased1"]):
            self.color["massBased1"] = "#ffff00"

        # ---- clock ----
        if not isinstance(self.clock.get("visible"), bool):
            self.clock["visible"] = True
        if not isinstance(self.clock.get("fontSize"), int) or (
            self.clock["fontSize"] <= 0 or self.clock["fontSize"] > 1000):
            self.clock["fontSize"] = 48

        # ---- Window ----
        if not isinstance(self.window.get("onTop"), bool):
            self.window["onTop"] = True

    def _is_valid_color(self, color: str) -> bool:
        pattern = r"^#(?:[0-9A-Fa-f]{3}){1,2}$"
        return re.match(pattern, color) is not None
