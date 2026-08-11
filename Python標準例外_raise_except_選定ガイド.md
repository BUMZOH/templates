# Python標準例外の選び方 ― `raise` と `except` の実践ガイド

## 1. はじめに

Pythonでは、異常な状態を検出したときに `raise` を使って例外を送出できます。

```python
raise RuntimeError("想定外の状態です")
```

自分で例外を発生させる場合、「どの例外を使えばよいのか？」という疑問が出てきます。

結論として、**よく使う標準例外を一覧として手元に置き、その中から「何が問題なのか」に最も合う例外を選ぶ方法は非常に有効です。**

Pythonの組み込み例外をすべて暗記する必要はありません。まず実務で頻繁に使うものを理解し、必要なとき一覧から選べれば十分です。

---

## 2. `raise` の基本

```python
if len(values) != 1000:
    raise ValueError("データ点数が1000点ではありません")
```

処理の流れは、

```text
異常を検出
    ↓
raise
    ↓
通常処理を中断
    ↓
上位のexceptへ伝播
```

です。

例外クラスはさまざまな種類を指定できますが、**「動くか」と「意味として適切か」は別問題**です。

例外名は「何が問題だったのか」を表す情報なので、意味に合った種類を選びます。

---

## 3. まず覚えておきたい標準例外

| 例外 | 主な意味 | 使用例 |
|---|---|---|
| `ValueError` | 値・内容が不正 | データ点数が1000点ではない |
| `TypeError` | 型が不正 | 数値を期待した場所に不適切な型 |
| `RuntimeError` | 実行中の想定外状態 | PLCから想定外の応答 |
| `TimeoutError` | タイムアウト | 通信が時間内に完了しない |
| `ConnectionError` | 接続関係の問題 | PLCやサーバーへの接続異常 |
| `OSError` | OS・入出力関係 | ファイル・通信などの低レベルエラー |
| `FileNotFoundError` | ファイルが存在しない | 設定ファイルが見つからない |
| `PermissionError` | 権限がない | ファイルを書き込めない |
| `KeyError` | 辞書にキーがない | `data["motor1"]` が存在しない |
| `IndexError` | インデックスが範囲外 | リストの存在しない要素へアクセス |
| `AttributeError` | 属性が存在しない | 存在しない属性やメソッドへアクセス |
| `NotImplementedError` | 処理が未実装 | 派生クラス側で実装させたい処理 |

---

## 4. よく使う例外の意味

### `ValueError`

型は問題ないものの、**値・内容が不適切**な場合です。

```python
if len(values) != DATA_POINT_COUNT:
    raise ValueError(
        f"データ点数エラー: "
        f"expected={DATA_POINT_COUNT}, actual={len(values)}"
    )
```

覚え方：

```text
値がおかしい
    → ValueError
```

### `TypeError`

**型そのものが不適切**な場合です。

```python
if not isinstance(machine_no, int):
    raise TypeError("machine_noはintで指定してください")
```

`ValueError` との違いは、

```text
TypeError  → 型がおかしい
ValueError → 型は合っているが値がおかしい
```

です。

### `RuntimeError`

他の具体的な標準例外にきれいに分類できない、**実行時の想定外状態**に使えます。

今回のPLC監視なら、

```python
if response == "1":
    request_is_on = True
elif response == "0":
    request_is_on = False
else:
    raise RuntimeError(
        f"デバイス読み込みエラー: "
        f"device={config.request_device}, response={response}"
    )
```

という使い方です。

```text
"0" / "1" を想定
    ↓
それ以外が返った
    ↓
実行中の想定外状態
    ↓
RuntimeError
```

### `TimeoutError`

処理が指定時間内に完了しなかった場合です。

```text
PLCへ要求
    ↓
応答待ち
    ↓
規定時間を超過
    ↓
TimeoutError
```

### `ConnectionError`

接続関係の問題です。さらに具体的な子例外として、たとえば次があります。

```text
ConnectionError
├─ BrokenPipeError
├─ ConnectionAbortedError
├─ ConnectionRefusedError
└─ ConnectionResetError
```

### `OSError`

OSや入出力処理に関係する広い範囲のエラーです。ファイル、ディレクトリ、ネットワーク、ソケットなどが関係します。

### `FileNotFoundError`

指定したファイルやディレクトリが存在しない場合です。

### `PermissionError`

ファイルやディレクトリへアクセスする権限がない場合などです。

### `KeyError`

辞書に存在しないキーへアクセスした場合です。

```python
data = {"motor1": 100}
print(data["motor2"])
```

### `IndexError`

リストやタプルなどで存在しない位置へアクセスした場合です。

```python
values = [10, 20, 30]
print(values[10])
```

### `AttributeError`

オブジェクトに存在しない属性やメソッドへアクセスした場合です。

### `NotImplementedError`

「この処理はここでは実装しない」ことを示す場合に使います。

```python
def save(self):
    raise NotImplementedError
```

通常のデータ異常や通信異常に使うものではありません。

---

## 5. 例外を選ぶ簡易判断表

```text
何がおかしい？
    │
    ├─ 値・内容
    │      → ValueError
    │
    ├─ 型
    │      → TypeError
    │
    ├─ ファイルがない
    │      → FileNotFoundError
    │
    ├─ 権限がない
    │      → PermissionError
    │
    ├─ 時間切れ
    │      → TimeoutError
    │
    ├─ 接続
    │      → ConnectionError
    │
    ├─ OS・I/O
    │      → OSError
    │
    └─ どれにもきれいに当てはまらない
           実行時の想定外状態
           → RuntimeError
```

---

## 6. 例外には親子関係がある

Pythonの例外はクラスなので、継承関係があります。

代表的な部分を簡略化すると、

```text
BaseException
└─ Exception
   ├─ RuntimeError
   │  └─ NotImplementedError
   ├─ ValueError
   ├─ TypeError
   ├─ LookupError
   │  ├─ KeyError
   │  └─ IndexError
   ├─ AttributeError
   └─ OSError
      ├─ FileNotFoundError
      ├─ PermissionError
      ├─ TimeoutError
      └─ ConnectionError
         ├─ BrokenPipeError
         ├─ ConnectionAbortedError
         ├─ ConnectionRefusedError
         └─ ConnectionResetError
```

この親子関係は `except` を書くときに重要です。

---

## 7. 親例外で子例外も捕捉できる

```python
try:
    ...
except OSError as error:
    print(error)
```

とすると、`OSError` の子クラスも捕捉できます。

たとえば、

```text
FileNotFoundError
PermissionError
TimeoutError
ConnectionError
```

などです。

したがって、

```text
エラーごとに処理を変えたい
    → 具体的な子例外を捕捉

同じ処理でまとめたい
    → 共通の親例外を捕捉
```

という考え方ができます。

---

## 8. 現在のPLC監視コードを考える

現在のコードでは概念的に、

```python
except (
    ConnectionError,
    OSError,
    TimeoutError,
    RuntimeError,
) as error:
    print(f"PLC通信エラー: {error}")
```

のように複数の例外をまとめています。

`ConnectionError` と `TimeoutError` は `OSError` の子クラスなので、**すべて同じ処理をするだけなら**、

```python
except (OSError, RuntimeError) as error:
    print(f"PLC通信エラー: {error}")
```

のように整理することもできます。

ただし、あえて具体的な例外を列挙することで、「この処理では接続異常やタイムアウトも想定している」と読み手へ伝える書き方もあります。

単純に短ければよいのではなく、**例外の継承関係とコードから伝えたい意図の両方を考える**ことが大切です。

---

## 9. `except Exception` はどうなのか

```python
try:
    ...
except Exception as error:
    print(error)
```

とすれば、多くの通常例外をまとめて捕捉できます。

便利ですが、必要以上に広く捕捉すると、本来気付くべきプログラムミスまで同じ扱いにしてしまう可能性があります。

通常は、

```python
except ValueError:
```

```python
except OSError:
```

```python
except RuntimeError:
```

など、**予想できる例外をできるだけ具体的に捕捉する**方が原因を理解しやすくなります。

---

## 10. `raise` と `except` はセットで考える

例外処理では、

```text
どこで異常を検出するか
    ↓
何の例外をraiseするか
    ↓
どこまで伝播させるか
    ↓
どこでexceptするか
    ↓
そこでどう処理するか
```

までセットで考えることが重要です。

例：

```python
if len(values) != DATA_POINT_COUNT:
    raise ValueError("データ点数が不正です")
```

上位側：

```python
try:
    ...
except ValueError as error:
    print(f"PLCデータエラー: {error}")
```

こうすると、「データ内容の異常」という意味が `raise` から `except` まで一貫します。

---

## 11. 今回のPLCアプリでの使い分け

### PLCから想定外の応答

```python
raise RuntimeError(
    f"デバイス読み込みエラー: "
    f"device={config.request_device}, response={response}"
)
```

```text
PLC処理中
    ↓
"0" / "1" 以外の想定外応答
    ↓
RuntimeError
```

### 受信データ点数が不正

```python
if len(values) != DATA_POINT_COUNT:
    raise ValueError(...)
```

```text
データは受信した
    ↓
しかし内容・点数が不正
    ↓
ValueError
```

### 通信タイムアウト

```text
PLC応答待ち
    ↓
時間切れ
    ↓
TimeoutError
```

### 接続異常

```text
PLC接続
    ↓
接続失敗
    ↓
ConnectionError
```

---

## 12. 独自例外という選択肢

アプリが大きくなると、標準例外だけでは分類しにくい場合があります。

```python
class PlcError(Exception):
    """PLC関連の基底例外。"""
```

さらに、

```python
class PlcResponseError(PlcError):
    """PLC応答内容が不正な場合の例外。"""
```

として、

```python
raise PlcResponseError(
    f"想定外のPLC応答: {response}"
)
```

のようにできます。

上位側では、

```python
except PlcError as error:
    print(f"PLCエラー: {error}")
```

とまとめることもできます。

ただし、小規模なアプリで無理に独自例外を増やす必要はありません。まず標準例外を適切に使う方がシンプルです。

---

## 13. 実務でのおすすめ方針

```text
1. よく使う例外一覧を手元に置く

2. 異常を見つけたら
   「何がおかしいのか？」を考える

3. 一覧から意味の近い例外を選ぶ

4. 上位のexceptでどう扱うか確認する

5. 必要なら例外の親子関係を確認する
```

まず優先して理解したいのは、

```text
ValueError   → 値がおかしい
TypeError    → 型がおかしい
RuntimeError → 実行中の想定外状態
OSError      → OS・I/O関係
```

です。

その次に、

```text
TimeoutError
ConnectionError
FileNotFoundError
PermissionError
KeyError
IndexError
AttributeError
```

を必要に応じて覚えていけば十分です。

---

## 14. 忘備録用チートシート

```text
【raiseするとき】

値がおかしい？             → ValueError
型がおかしい？             → TypeError
時間切れ？                 → TimeoutError
接続がおかしい？           → ConnectionError
ファイルがない？           → FileNotFoundError
権限がない？               → PermissionError
OS・I/O関係？              → OSError
辞書のキーがない？         → KeyError
リスト等の範囲外？         → IndexError
属性がない？               → AttributeError
実行時の想定外状態？       → RuntimeError


【exceptするとき】

具体的に処理を分けたい
    ↓
具体的な子例外を捕捉

同じ処理でまとめたい
    ↓
共通の親例外を捕捉


【最重要】

例外名は単なるエラー番号ではない。

「何が問題だったのか」を
コード上で表現するための情報である。
```

---

## 15. まとめ

Pythonで自分から例外を送出するときは、**「何が問題なのか」を最も適切に表す例外を選ぶ**ことが基本です。

そして例外には親子関係があるため、`raise` だけでなく `except` 側でどの範囲を捕捉するかも重要です。

最終的には、

```text
異常を検出
    ↓
意味に合った例外をraise
    ↓
上位へ伝播
    ↓
適切なexceptで捕捉
    ↓
ログ・再試行・終了などを判断
```

という一連の流れとして考えると、例外処理が整理しやすくなります。
