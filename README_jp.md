# <img src="assets/GravityClock.ico" width="48"> GravityClock

**GravityClock** は、重力で引き合う粒子をモチーフにした美しいデスクトップ時計アプリです。  
星々のように光る粒子が引き合い、ゆらめきながら時を刻みます。  

## 💎 スクリーンショット

https://github.com/user-attachments/assets/c9922578-86ae-40c6-abe9-26b98560236a

## 💎 特徴

- **N体重力シミュレーション**
  - 粒子同士が万有引力で引き合い、リアルな物理挙動で漂います。

- **美しい光の描画**
  - 各粒子が発光色で表現され、軌跡がふんわり残る幻想的な演出。

- **デジタル時計表示**
  - 中央に時刻をネオン風に表示。表示ON/OFFやフォント・サイズ変更に対応。

- **操作性**
  - ウィンドウはドラッグで移動、右下ドラッグでリサイズ可能。
  - ウィンドウ位置・サイズを自動記憶。

- **軽量設計**
  - PyWebViewによるネイティブウィンドウ表示で軽快に動作。

## 💎 動作環境

- OS: Windows 11
- Python: Python 3.9 - 3.13

## 💎 実行方法

### ① 実行ファイルから使う場合（簡単）

1. [Releases](https://github.com/led-mirage/GravityClock/releases/) ページから最新版の **`GravityClock.exe`** をダウンロードします。  
2. ダウンロードしたファイルをそのまま実行してください。  

> ⚠️ 一部のウイルス対策ソフトで誤検知される場合があります。  
>  詳しくは下の「ウイルス対策ソフトによる誤検知について」をご確認ください。

### ② Pythonで実行する場合（開発者向け）

1. リポジトリをクローンまたはダウンロードします。  
   ```bash
   git clone https://github.com/led-mirage/GravityClock.git
   cd GravityClock
   ```

2. 依存パッケージをインストールします。  
   ```bash
   pip install pywebview==6.1.0
   ```

3. アプリを起動します。  
   ```bash
   python src/main.py
   ```

> 💡 Pyrhon環境を汚したくない場合は、次のように **仮想環境 (venv)** での利用をおすすめします：  
> ```bash
> python -m venv venv
> .\venv\Scripts\activate  # Windowsの場合
> pip install pywebview==6.1.0
> python src/main.py
> ```

## 💎 設定

設定は設定画面から行うことが可能です。

<img src="documents/images/settings.png" width="300">

設定項目の詳細は以下の通りです。

### 🏷️ Simulation

- **N:** 粒子の数（0～100）
- **G:** 重力の大きさ（0.0～10.0）

### 🏷️ Mass

- **type:** 粒子の質量の決め方
    - **fixed:** 固定値
    - **random:** ランダム
- **fixedValue:** `type`が`fixed`の場合の質量
- **randomMinValue:** `type`が`random`の場合の、質量下限
- **randomMaxValue:** `type`が`random`の場合の、質量上限

### 🏷️ Radius

- **type:** 粒子の半径の決め方
    - **fixed:** 固定値
    - **random:** ランダム
    - **mass_based:** 質量依存
- **fixedValue:** `type`が`fixed`の場合の半径
- **randomMinValue:** `type`が`random`の場合の、半径下限
- **randomMaxValue:** `type`が`random`の場合の、半径上限

### 🏷️ Color

- **type:** 粒子の色の決め方
    - **fixed:** 固定値
    - **random:** ランダム
    - **mass_based:** 質量依存
    - **cycling:** 10色を循環して使用
- **fixedValue:** `type`が`fixed`の場合の色（#ffffff形式）
- **massBased0:** `type`が`mass_based`の場合の開始色（#ffffff形式）
- **massBased1:** `type`が`mass_based`の場合の終了色（#ffffff形式）

### 🏷️ Clock

- **visible:** 時計を表示するかどうか
- **fontSize:** 時計のフォントサイズ（px）
- **fontFamily:** 時計のフォントファミリー

### 🏷️ Window

- **onTop:** 他のウィンドウよりも手前に表示するかどうか

## 💎 操作方法

| 操作 | 内容 |
| ---------- | ----------- |
| ドラッグ | ウィンドウ移動 |
| 右辺、下辺、右下ドラッグ | ウィンドウサイズ変更 |
| ダブルクリック | ウィンドウ最大化／元に戻す |
| `Esc`      | 最大化されたウィンドウを元に戻す |
| `Ctrl + M` | 最小化 |
| `R`        | 粒子位置の初期化 |
| 左上付近にマウスを移動 | 設定ボタン（⚙️）が表示される |
| 右上付近にマウスを移動 | 右上付近にマウスを移動る |

## 💎 注意事項

### ウィルス対策ソフトの誤認問題

本アプリ（GravityClock.exe）は PyInstaller を使用してビルドした実行ファイルです。
一部のウイルス対策ソフトによって、誤ってマルウェアと判定される場合があります。

このアプリには悪意のあるコードは含まれていませんが、
気になる方は「Pythonで実行する」手順でのご利用をおすすめします。

誤検知の問題は継続的に改善を試みていますが、現時点では完全な解決に至っていません。
ご不便をおかけしますが、ご了承ください。

VirusTotalでのスキャン結果は [こちら](https://www.virustotal.com/gui/file/11b158358f515b2d8474cd0c6a4cdca0d5bc6f80f59e289b1a59f122b1f9e622?nocache=1) から確認できます。  
（2025/11/16 時点、3/72 検出）

## 💎 使用しているライブラリ

### 🔖 pywebview 6.1.0
ホームページ： https://github.com/r0x0r/pywebview  
ライセンス： BSD-3-Clause license

### 🔖 pyinstaller-versionfile 3.0.1
ホームページ：https://github.com/DudeNr33/pyinstaller-versionfile  
ライセンス：MIT license

### 🔖 PyInstaller 6.16.0
ホームページ： https://github.com/pyinstaller/pyinstaller  
ライセンス： GPL 2.0 License / Apache License 2.0

## 💎 ライセンス

本アプリケーションは [MITライセンス](https://opensource.org/licenses/MIT) の下で公開されています。詳細については、プロジェクトに含まれる **LICENSE** ファイルを参照してください。

© 2025 led-mirage

## 💎 バージョン履歴

### 1.0.0 (2025/11/16)

- ファーストリリース
