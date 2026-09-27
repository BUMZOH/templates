"""
Tkinter UI 開発用プレビューツール

Tkinterアプリのソースファイル変更を監視し、
ファイルが保存されたときにアプリを自動的に再起動します。

UIのレイアウトやデザインを調整するときに、
毎回アプリを手動で終了・再起動する手間を減らすことが目的です。

再起動前のTkinterウィンドウ位置を取得し、
再起動後も同じ位置にウィンドウを表示します。

使い方
------
1. このファイルと app.py を同じフォルダに配置します。

2. 必要なライブラリをインストールします。

   pip install watchfiles pygetwindow

3. WINDOW_TITLE を app.py のウィンドウタイトルに合わせます。

   WINDOW_TITLE = "Tkinter Preview"

4. このファイルを実行します。

   python tkinter_ui_preview.py

5. app.py などのファイルを編集して保存すると、
   Tkinterアプリが自動的に再起動します。

注意
----
・Windows環境での使用を想定しています。
・WINDOW_TITLE はTkinterウィンドウのタイトルと一致させてください。
・同じタイトルのウィンドウを複数開いている場合、
  意図しないウィンドウを取得する可能性があります。
・このツールを複数起動すると、app.py も複数起動するため注意してください。
"""
import subprocess
import sys
import time

import pygetwindow as gw
from watchfiles import watch


# ================================================
#   Settings
# ================================================
WINDOW_TITLE = "Tkinter Preview"


# ================================================
#   Start application
# ================================================
def start_app(x=None, y=None):
    process = subprocess.Popen(
        [sys.executable, "app.py"]
    )

    if x is not None and y is not None:
        time.sleep(0.5)

        windows = gw.getWindowsWithTitle(WINDOW_TITLE)

        if windows:
            windows[0].moveTo(x, y)

    return process


# ================================================
#   Start
# ================================================
process = start_app()


# ================================================
#   Watch files
# ================================================
for changes in watch("."):
    print("File changed.")

    x = None
    y = None

    windows = gw.getWindowsWithTitle(WINDOW_TITLE)

    if windows:
        x = windows[0].left
        y = windows[0].top

    process.terminate()
    process.wait()

    process = start_app(x, y)