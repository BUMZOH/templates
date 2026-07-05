# Python仮想環境の構築と requirements.txt の実行手順

## 目的

この手順書では、Pythonアプリを実行するために必要な環境を準備します。

具体的には、次の作業を行います。

1. Pythonがインストールされているか確認する
2. プロジェクトフォルダを開く
3. 仮想環境 `.venv` を作成する
4. 仮想環境を有効化する
5. `requirements.txt` に記載されたライブラリをインストールする
6. アプリを実行する

---

## 前提条件

この手順は、以下の環境を想定しています。

- Windows PC
- Python がインストール済み
- アプリのフォルダ一式を受け取っている
- アプリのフォルダ内に `requirements.txt` がある

---

## 1. Pythonが使えるか確認する

コマンドプロンプト、または PowerShell を開きます。

次のコマンドを入力します。

```bash
python --version
```

または、環境によっては次のコマンドを使います。

```bash
py --version
```

次のようにPythonのバージョンが表示されればOKです。

```bash
Python 3.12.0
```

バージョンが表示されない場合は、Pythonがインストールされていないか、環境変数PATHが設定されていない可能性があります。

---

## 2. プロジェクトフォルダを開く

アプリのフォルダを開きます。

例：

```text
C:\myProgram\factory_visualize_app
```

コマンドプロンプトでそのフォルダへ移動します。

```bash
cd C:\myProgram\factory_visualize_app
```

現在のフォルダを確認したい場合は、次のコマンドを使います。

```bash
cd
```

---

## 3. 仮想環境を作成する

プロジェクトフォルダ内で、次のコマンドを実行します。

```bash
python -m venv .venv
```

または、`python` コマンドでうまくいかない場合は、次のコマンドを実行します。

```bash
py -m venv .venv
```

実行後、プロジェクトフォルダ内に次のフォルダが作成されます。

```text
.venv
```

この `.venv` フォルダが、このアプリ専用のPython環境です。

---

## 4. 仮想環境を有効化する

### コマンドプロンプトの場合

```bash
.venv\Scripts\activate
```

### PowerShellの場合

```powershell
.venv\Scripts\Activate.ps1
```

有効化に成功すると、行の先頭に次のように表示されます。

```bash
(.venv) C:\myProgram\factory_visualize_app>
```

先頭に `(.venv)` が表示されていれば、仮想環境が有効になっています。

---

## 5. requirements.txt のライブラリをインストールする

仮想環境が有効になっている状態で、次のコマンドを実行します。

```bash
pip install -r requirements.txt
```

このコマンドにより、`requirements.txt` に書かれているライブラリがまとめてインストールされます。

例：

```txt
matplotlib
pywebview
ping3
```

この場合、以下のライブラリがインストールされます。

| ライブラリ | 用途 |
|---|---|
| matplotlib | グラフ作成 |
| pywebview | デスクトップGUI表示 |
| ping3 | Ping通信 |

---

## 6. インストールできたか確認する

次のコマンドで、インストール済みライブラリを確認できます。

```bash
pip list
```

一覧の中に、次のような名前があればOKです。

```text
matplotlib
pywebview
ping3
```

---

## 7. アプリを実行する

仮想環境が有効な状態で、アプリを実行します。

例：

```bash
python main.py
```

または、環境によっては次のコマンドを使います。

```bash
py main.py
```

---

## 8. 2回目以降の起動方法

2回目以降は、仮想環境の作成とライブラリのインストールは基本的に不要です。

毎回行う作業は、次の2つです。

### 1. プロジェクトフォルダへ移動

```bash
cd C:\myProgram\factory_visualize_app
```

### 2. 仮想環境を有効化

```bash
.venv\Scripts\activate
```

### 3. アプリを実行

```bash
python main.py
```

---

## 9. よくあるエラーと対処方法

### `python` が認識されない

次のようなエラーが出る場合があります。

```text
'python' は、内部コマンドまたは外部コマンドとして認識されていません。
```

この場合は、次のコマンドを試してください。

```bash
py --version
```

`py` でPythonのバージョンが表示される場合は、以降のコマンドも `python` の代わりに `py` を使えます。

例：

```bash
py -m venv .venv
py main.py
```

---

### PowerShellで仮想環境を有効化できない

PowerShellで次のようなエラーが出る場合があります。

```text
このシステムではスクリプトの実行が無効になっているため、ファイルを読み込むことができません。
```

この場合は、コマンドプロンプトを使用してください。

コマンドプロンプトでは次のコマンドで有効化できます。

```bash
.venv\Scripts\activate
```

---

### `requirements.txt` が見つからない

次のようなエラーが出る場合があります。

```text
ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'
```

この場合、現在のフォルダが間違っている可能性があります。

次のコマンドで、現在のフォルダ内のファイル一覧を確認してください。

```bash
dir
```

一覧の中に `requirements.txt` があるフォルダで、次のコマンドを実行してください。

```bash
pip install -r requirements.txt
```

---

### `pip` が古いと言われる

次のような表示が出ることがあります。

```text
A new release of pip is available
```

通常はそのままでも問題ありません。

更新する場合は、仮想環境が有効な状態で次のコマンドを実行します。

```bash
python -m pip install --upgrade pip
```

---

## 10. 補足：仮想環境とは

仮想環境とは、アプリごとに分けて用意するPython専用の作業場所です。

仮想環境を使うことで、次のメリットがあります。

- アプリごとに必要なライブラリを分けられる
- 他のPythonアプリに影響を与えにくい
- PC全体のPython環境を汚さずに済む
- 別のPCでも同じような環境を作りやすい

基本的には、Pythonアプリごとに `.venv` を作成する運用がおすすめです。

---

## 11. 補足：requirements.txt とは

`requirements.txt` は、このアプリで使用するPythonライブラリの一覧です。

例：

```txt
matplotlib
pywebview
ping3
```

このファイルがあることで、次のコマンドだけで必要なライブラリをまとめてインストールできます。

```bash
pip install -r requirements.txt
```

手動で1つずつインストールする必要がなくなるため、配布時や別PCへの移行時に便利です。

---

## 12. 標準的な作業コマンドまとめ

初回のみ：

```bash
cd C:\myProgram\factory_visualize_app
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

2回目以降：

```bash
cd C:\myProgram\factory_visualize_app
.venv\Scripts\activate
python main.py
```

---

## 13. 注意事項

`.venv` フォルダは、このPC専用の仮想環境です。

通常、`.venv` フォルダを他の人に配布する必要はありません。

配布する場合は、次のようなファイルを渡します。

```text
main.py
requirements.txt
その他アプリに必要なファイル
```

受け取った人は、この手順書に従って自分のPCで `.venv` を作成します。

---

## 以上

これで、Python仮想環境の作成と `requirements.txt` を使ったライブラリのインストールは完了です。
