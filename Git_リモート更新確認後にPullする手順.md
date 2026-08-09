# Gitでリモート更新を確認してから安全にPullする方法

## 1. はじめに

Gitを使っていると、`git status` を実行したときに次のような表示が出ることがあります。

```text
On branch main
Your branch is behind 'origin/main' by 2 commits, and can be fast-forwarded.
  (use "git pull" to update your local branch)

nothing to commit, working tree clean
```

これは、

> **リモートの `main` ブランチには、自分のローカル環境にはまだ取り込まれていない更新が2コミット存在する**

という意味です。

この場合、すぐに `git pull` を実行してもよいのですが、

- 何が変更されたのか確認したい
- どのファイルが変更されたのか見たい
- 他のPCで自分が行った変更か確認したい
- 想定外の変更が混ざっていないか確認したい

という場合は、いきなり `git pull` せず、

```text
fetch → status → log → diff → pull
```

という順番で確認するのがおすすめです。

この資料では、この操作を定期的に行うための「安全確認手順」として整理します。

---

# 2. 結論：基本手順

普段は次の順番で操作します。

```bash
git fetch
git status
git log --oneline HEAD..origin/main
git diff HEAD origin/main --stat
git diff HEAD origin/main
git pull
```

ただし、毎回すべて実行する必要はありません。

実用上は次の4段階で十分です。

```bash
git fetch
git log --oneline HEAD..origin/main
git diff HEAD origin/main --stat
git pull
```

詳しい変更内容を確認したい場合だけ、

```bash
git diff HEAD origin/main
```

を追加します。

---

# 3. 全体の考え方

重要なのは、次の役割分担です。

```text
git fetch
    ↓
リモートの最新情報を取得する
ただし、自分の作業ファイルには反映しない
    ↓
git log / git diff
    ↓
何が変わったか確認する
    ↓
問題なし
    ↓
git pull
    ↓
ローカルへ実際に反映する
```

つまり、

> **`fetch` は「情報収集」**
>
> **`pull` は「実際の反映」**

と考えると分かりやすいです。

---

# 4. `git fetch`

## 4.1 基本

```bash
git fetch
```

`git fetch` は、GitHubなどのリモートリポジトリから最新情報を取得します。

ただし、この時点では自分の作業中のファイルは変更されません。

ここが非常に重要です。

---

## 4.2 `git pull` との違い

大まかには次の違いがあります。

### `git fetch`

```text
GitHub
  ↓
リモートの最新情報を取得
  ↓
origin/main などを更新
  ↓
自分の main や作業ファイルは変更しない
```

### `git pull`

```text
GitHub
  ↓
最新情報を取得
  ↓
自分の main に取り込む
  ↓
作業ファイルも更新される
```

つまり、

```bash
git fetch
```

は、

> 「最新情報だけ取ってきて。まだ自分のファイルには反映しないで」

という操作です。

一方、

```bash
git pull
```

は、

> 「最新情報を取ってきて、自分のブランチにも反映して」

という操作です。

そのため、内容を確認してから更新したい場合は、まず `git fetch` を使います。

---

# 5. `git status`

`git fetch` の後に、

```bash
git status
```

を実行します。

例：

```text
On branch main
Your branch is behind 'origin/main' by 2 commits, and can be fast-forwarded.

nothing to commit, working tree clean
```

---

## 5.1 `behind by 2 commits`

```text
Your branch is behind 'origin/main' by 2 commits
```

これは、

```text
origin/main
    ● 新しいコミット
    |
    ● 新しいコミット
    |
HEAD / main
    ● 現在のローカル
```

という状態です。

つまり、

> リモートの `origin/main` のほうが2コミット先に進んでいる

という意味です。

---

## 5.2 `can be fast-forwarded`

```text
and can be fast-forwarded
```

これは非常に良い状態です。

ローカル側に独自の新しいコミットがなく、単純にリモートの続きへ進めることができます。

イメージ：

```text
ローカル main

A --- B


リモート origin/main

A --- B --- C --- D
```

この場合、ローカルの `main` を

```text
A --- B --- C --- D
```

まで前進させるだけで済みます。

これが **Fast-forward（早送り）** です。

複雑なマージ処理は必要ありません。

---

# 6. `nothing to commit, working tree clean`

```text
nothing to commit, working tree clean
```

これは、

> ローカルの作業ファイルに未コミットの変更がない

という意味です。

つまり、

- ファイルを編集していない
- 保存したまま未コミットの変更もない
- Gitから見て作業フォルダがきれいな状態

です。

`git pull` 前としては非常に安心できる状態です。

---

# 7. リモートにだけ存在するコミットを確認する

次に実行する重要なコマンドがこちらです。

```bash
git log --oneline HEAD..origin/main
```

---

## 7.1 意味

これは、

> **現在の自分の位置 `HEAD` には存在せず、`origin/main` にだけ存在するコミットを表示する**

という意味です。

例えば、

```text
813e300 README更新
35037ad PLC通信処理を修正
```

と表示された場合、

「リモート側にはこの2つの新しいコミットがある」

と確認できます。

---

# 8. `HEAD` とは何か

`HEAD` はGitで頻繁に出てくる重要な言葉です。

簡単にいうと、

> **現在、自分がいるコミット**

を指します。

通常 `main` ブランチで作業しているなら、

```text
HEAD
 ↓
main
 ↓
● 現在のコミット
```

となります。

したがって、

```bash
git log --oneline HEAD..origin/main
```

は、

```text
現在地 HEAD
    ↓

● ← 自分はここ

● ← origin/main にしかない
● ← origin/main にしかない
```

という差を調べています。

---

# 9. `origin/main` とは何か

`origin/main` は、

> **最後に取得したリモートの `main` ブランチ情報**

です。

通常、

```text
main
```

はローカル側のブランチ、

```text
origin/main
```

はGitHub側の `main` を追跡するための情報、

と考えると分かりやすいです。

`git fetch` を行うと、この `origin/main` が最新状態に更新されます。

---

# 10. `HEAD..origin/main` の意味

Gitでは、

```text
A..B
```

という書き方は、

> **Bには存在するが、Aには存在しないコミット**

を表します。

したがって、

```bash
HEAD..origin/main
```

は、

> `origin/main` にはあるが、現在の自分 `HEAD` にはないコミット

という意味です。

つまり、

```bash
git log --oneline HEAD..origin/main
```

は、

> **Pullしたら新しく入ってくるコミット一覧**

を見るためのコマンドと考えると非常に分かりやすいです。

---

# 11. 変更されたファイルだけ確認する

コミット名だけではなく、

> 実際にどのファイルが変更されたのか

を確認したい場合は、

```bash
git diff HEAD origin/main --stat
```

を使います。

---

## 11.1 表示例

```text
 README.md       | 20 +++++++++++++-------
 app.py          | 15 +++++++++------
 config.json     |  4 ++--
 3 files changed, 24 insertions(+), 15 deletions(-)
```

この表示から、

- `README.md`
- `app.py`
- `config.json`

が変更されていることが分かります。

また、

```text
3 files changed
24 insertions(+)
15 deletions(-)
```

から、

- 3ファイル変更
- 24行追加
- 15行削除

という変更規模も確認できます。

---

# 12. `--stat` が便利な理由

通常の `git diff` は変更された行をすべて表示するため、変更量が多いとかなり長くなります。

そこで最初は、

```bash
git diff HEAD origin/main --stat
```

だけを見るのがおすすめです。

判断イメージ：

```text
git diff ... --stat
        ↓
READMEだけ変更
        ↓
大丈夫そう
        ↓
git pull
```

一方、

```text
app.py
database.py
config.json
```

など重要なファイルが変更されていた場合は、

```bash
git diff HEAD origin/main
```

で詳細を確認します。

---

# 13. 具体的な変更内容を見る

詳しい差分を見る場合は、

```bash
git diff HEAD origin/main
```

を使います。

例：

```diff
- TIMEOUT = 5
+ TIMEOUT = 10
```

この場合、

```text
TIMEOUT = 5
```

が削除され、

```text
TIMEOUT = 10
```

へ変更されたことが分かります。

---

## 13.1 `+` と `-` の意味

Gitのdiffでは、

```text
-
```

は削除された行、

```text
+
```

は追加された行です。

例えば、

```diff
- old_value = 10
+ new_value = 20
```

なら、

```text
old_value = 10
```

がなくなり、

```text
new_value = 20
```

が追加されたことを表します。

---

# 14. 確認後に `git pull`

内容に問題がなければ、

```bash
git pull
```

を実行します。

これでリモート側の変更がローカルへ反映されます。

今回のように、

```text
can be fast-forwarded
```

と表示されている場合は、基本的に単純なFast-forwardになります。

---

# 15. Pull後の確認

`git pull` 後に、

```bash
git status
```

を実行するのがおすすめです。

正常であれば、例えば次のようになります。

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

重要なのは、

```text
Your branch is up to date with 'origin/main'.
```

です。

これは、

> ローカルの `main` とリモートの `origin/main` が同じ状態

という意味です。

---

# 16. 実際に使う定番手順

## 手順1：リモート情報を取得

```bash
git fetch
```

この時点ではローカルファイルは変更されません。

---

## 手順2：現在の状態を確認

```bash
git status
```

例えば、

```text
behind 'origin/main' by 2 commits
```

なら、リモート側に2コミットあります。

---

## 手順3：新しいコミットを確認

```bash
git log --oneline HEAD..origin/main
```

Pullによって入ってくるコミットの概要を確認します。

---

## 手順4：変更ファイルを確認

```bash
git diff HEAD origin/main --stat
```

変更されたファイル名と変更量を確認します。

---

## 手順5：必要なら詳細確認

```bash
git diff HEAD origin/main
```

実際のコード変更を確認します。

---

## 手順6：問題なければPull

```bash
git pull
```

---

## 手順7：最後に確認

```bash
git status
```

次の表示になれば完了です。

```text
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

---

# 17. 最低限覚える3つ

毎回すべてのコマンドを暗記する必要はありません。

特に覚えておきたいのは次の3つです。

```bash
git fetch
git log --oneline HEAD..origin/main
git diff HEAD origin/main --stat
```

意味は、

```text
git fetch
    ↓
リモートの最新情報を取得

git log --oneline HEAD..origin/main
    ↓
新しいコミットを確認

git diff HEAD origin/main --stat
    ↓
変更されたファイルを確認
```

です。

そして問題なければ、

```bash
git pull
```

です。

---

# 18. 覚え方

次の言葉で覚えると分かりやすいです。

```text
fetch → log → diff → pull
```

日本語にすると、

```text
取得 → 履歴確認 → 差分確認 → 反映
```

です。

さらに簡単に言えば、

> **「取って、見て、比べて、入れる」**

です。

---

# 19. `git fetch` を先に実行する理由

例えば昨日、

```bash
git status
```

を実行して、

```text
up to date
```

だったとしても、その後別PCからGitHubへPushされている可能性があります。

ローカルPCは、それを自動的には常に把握しているわけではありません。

そのため、確認操作の最初に、

```bash
git fetch
```

を実行して、

> 「まずGitHubの最新状態を教えてもらう」

ことが重要です。

---

# 20. `git status` だけでは十分でない理由

`git status` は非常に便利ですが、

```text
behind by 2 commits
```

とは教えてくれても、

> その2コミットで何が変わったか

までは詳しく教えてくれません。

そのため、

```bash
git log --oneline HEAD..origin/main
```

と、

```bash
git diff HEAD origin/main --stat
```

を組み合わせます。

役割は次のように異なります。

| コマンド | 確認できること |
|---|---|
| `git status` | 何コミット進んでいるか |
| `git log ...` | どんなコミットなのか |
| `git diff ... --stat` | どのファイルが変わったか |
| `git diff ...` | どの行が変わったか |

---

# 21. おすすめの確認レベル

毎回すべて細かく見る必要はありません。

### 軽い確認

```bash
git fetch
git status
git log --oneline HEAD..origin/main
git diff HEAD origin/main --stat
git pull
```

普段はこちらで十分です。

---

### 慎重に確認

```bash
git fetch
git status
git log --oneline HEAD..origin/main
git diff HEAD origin/main --stat
git diff HEAD origin/main
git pull
git status
```

重要なプログラムや、変更内容が多い場合はこちらがおすすめです。

---

# 22. 今回の状態の読み方

今回の表示：

```text
On branch main
Your branch is behind 'origin/main' by 2 commits, and can be fast-forwarded.
  (use "git pull" to update your local branch)

nothing to commit, working tree clean
```

これを一つずつ読むと、

```text
On branch main
```

現在 `main` ブランチにいる。

```text
behind 'origin/main' by 2 commits
```

リモート側が2コミット進んでいる。

```text
can be fast-forwarded
```

ローカル独自の分岐がないため、単純にリモート側まで進められる。

```text
nothing to commit
```

コミットすべきローカル変更はない。

```text
working tree clean
```

作業フォルダもきれい。

つまり、

> **Pullするにはかなり安全な状態。ただし内容を確認したければ、`log` と `diff` を見てからPullする。**

という状況です。

---

# 23. 重要：`git pull` 前にローカル変更がある場合

例えば、

```bash
git status
```

で、

```text
Changes not staged for commit:
    modified: app.py
```

などが表示された場合は注意します。

これはローカル側でまだコミットしていない変更がある状態です。

この状態で無条件に `git pull` すると、リモート側の変更と競合する可能性があります。

そのため、

```text
working tree clean
```

かどうかは、Pull前の重要な確認ポイントです。

---

# 24. よく使うコマンド一覧

```bash
# リモートの最新情報だけ取得
git fetch

# 現在の状態を確認
git status

# リモートにだけあるコミットを確認
git log --oneline HEAD..origin/main

# 変更されたファイルと変更量を確認
git diff HEAD origin/main --stat

# 詳細な変更内容を確認
git diff HEAD origin/main

# リモートの変更をローカルへ反映
git pull

# Pull後の状態確認
git status
```

---

# 25. 最終まとめ

リモート側が更新されている場合、すぐに `git pull` してもよいケースはあります。

しかし、

> 「何が変わったか確認してからPullしたい」

場合には、次の流れが非常に分かりやすく安全です。

```text
git fetch
    ↓
リモートの最新情報を取得
※まだ自分のファイルは変わらない

git status
    ↓
何コミット差があるか確認

git log --oneline HEAD..origin/main
    ↓
Pullで入ってくるコミットを確認

git diff HEAD origin/main --stat
    ↓
変更されたファイルを確認

git diff HEAD origin/main
    ↓
必要ならコードの変更内容まで確認

git pull
    ↓
問題なければローカルへ反映

git status
    ↓
同期完了を確認
```

普段の合言葉は、

> **fetch → log → diff → pull**

です。

日本語なら、

> **取得 → 履歴確認 → 差分確認 → 反映**

さらに簡単に覚えるなら、

> **「取って、見て、比べて、入れる」**

です。

この手順を定番化しておけば、リモート側の更新内容を把握せずにいきなりローカル環境を変更してしまうことを避けられます。
