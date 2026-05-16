"""
同じフォルダにある main.py / run.bat のショートカットを
デスクトップに作成するプログラム

仕様：
- 同じフォルダ内に main.py がなければ終了
- main.py の1行目を読む
- 1行目が「# APP_NAME:」で始まる場合、その後ろをショートカット名として採用
- 条件に一致しない場合、「オリジナルアプリ」という名称にする
- 同じフォルダ内に run.bat があれば、run.bat のショートカットを作成
- run.bat がなければ、main.py のショートカットを作成
- デスクトップに同名ショートカットがある場合、(1)、(2) のように連番を付与
- 同一フォルダ内に app.ico があればアイコンとして使用
"""

from pathlib import Path
from win32com.client import Dispatch
import re


DEFAULT_SHORTCUT_NAME = "オリジナルアプリ"

# パス設定
BASE_DIR = Path(__file__).resolve().parent
MAIN_FILE = BASE_DIR / "main.py"
RUN_BAT_FILE = BASE_DIR / "run.bat"
DESKTOP_DIR = Path.home() / "Desktop"
ICON_FILE = BASE_DIR / "app.ico"


def sanitize_filename(name: str) -> str:
    """Windowsで使用できない文字を除去"""

    # \ / : * ? " < > |
    name = re.sub(r'[\\/:*?"<>|]', "", name)

    name = name.strip()

    if not name:
        return DEFAULT_SHORTCUT_NAME

    return name


def get_shortcut_name_from_main(main_path: Path) -> str:
    """main.py の1行目からショートカット名を取得"""

    with main_path.open("r", encoding="utf-8", errors="replace") as f:
        first_line = f.readline().strip()

    # 例:
    # # APP_NAME: 稼働率表示アプリ
    prefix = "# APP_NAME:"

    if first_line.startswith(prefix):

        shortcut_name = first_line[len(prefix):].strip()

        if shortcut_name:
            return sanitize_filename(shortcut_name)

    return DEFAULT_SHORTCUT_NAME


def get_unique_shortcut_path(
    desktop_dir: Path,
    shortcut_name: str
) -> Path:
    """重複時に(1)(2)...を付与"""

    shortcut_path = desktop_dir / f"{shortcut_name}.lnk"

    if not shortcut_path.exists():
        return shortcut_path

    count = 1

    while True:

        shortcut_path = (
            desktop_dir /
            f"{shortcut_name}({count}).lnk"
        )

        if not shortcut_path.exists():
            return shortcut_path

        count += 1


# -----------------------------
# main.py 存在確認
# -----------------------------
if not MAIN_FILE.exists():
    print("main.pyがありません")
    input("Enterキーで終了します")
    exit()


# -----------------------------
# ショートカット名取得
# -----------------------------
shortcut_name = get_shortcut_name_from_main(MAIN_FILE)

shortcut_path = get_unique_shortcut_path(
    DESKTOP_DIR,
    shortcut_name
)


# -----------------------------
# 起動対象の決定
# -----------------------------
if RUN_BAT_FILE.exists():
    # run.bat がある場合は run.bat を起動
    target_path = str(RUN_BAT_FILE)
    arguments = ""
else:
    # run.bat がない場合は main.py を直接起動
    target_path = "python"
    arguments = f'"{MAIN_FILE}"'


# -----------------------------
# ショートカット作成
# -----------------------------
shell = Dispatch("WScript.Shell")

shortcut = shell.CreateShortCut(str(shortcut_path))

# 起動対象
shortcut.TargetPath = target_path

# 引数
shortcut.Arguments = arguments

# 作業フォルダ
shortcut.WorkingDirectory = str(BASE_DIR)

# アイコン
if ICON_FILE.exists():
    shortcut.IconLocation = str(ICON_FILE)

# 保存
shortcut.save()


print("ショートカットを作成しました")
print(shortcut_path)

if RUN_BAT_FILE.exists():
    print("起動対象：run.bat")
else:
    print("起動対象：main.py")