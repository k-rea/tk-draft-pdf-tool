# 📄 PDF 加工ツール

透かし追加、ページ番号挿入、パスワード保護、ファイル名変更に対応した PDF 加工ツールです。  
Python 3.11 + Poetry + PyPDF + ReportLab を使用しています。

---

## ✅ 前提環境

- Python **3.11.x**
- [Poetry](https://python-poetry.org/)（依存管理ツール）

---

## 📦 セットアップ

```bash
# Python 3.11 を使用して仮想環境を作成
poetry env use $(which python3.11)

# 依存関係をインストール
poetry install
```

## 🚀 使い方

```bash
poetry run python main.py [オプション]
```

### 🔧 オプション一覧

| オプション           | 説明                                               |
|----------------------|----------------------------------------------------|
| `--watermark`        | PDF に透かし（sign.pdf または draft.pdf）を追加   |
| `--pagenumber`       | 3 ページ目以降にページ番号を挿入                   |
| `--password`         | パスワードを設定（閲覧: 空文字、操作: tanikan）    |
| `--all`              | 上記すべてを適用                                  |
| `--prefix "文字列"`  | 出力ファイル名の接頭語（例: `"P_"`）               |
| `--suffix "文字列"`  | 出力ファイル名の接尾語（例: `"_draft"`）           |

> 💡 `--all` を指定すると、`--watermark` `--pagenumber` `--password` がすべて有効になります。


# 📄 PDF加工ツールの使い方（Windows向け）

## ✅ Step 1: 必要な準備

### ① Python のインストール

以下のリンクから「**Python 3.11.x**」をダウンロードしてインストールします：

👉 https://www.python.org/downloads/release/python-3119/
 最新版ではなくて、**Python 3.11.x** を選んでください。

**インストール時に「Add Python to PATH」にチェックを入れてください。**

インストール後、**コマンドプロンプト**を開いて以下を入力：
```shell
python --version
````

正常にインストールされていれば、以下のような出力が表示されます：

```shell
Python 3.11.x
```
---

## 🔽 Step 2: ツールのダウンロード

以下のページから「Code ▾ → Download ZIP」をクリックして、ツールをダウンロード・解凍してください：

👉 [https://github.com/k-rea/tk-draft-pdf-tool](https://github.com/k-rea/tk-draft-pdf-tool)


## ✅ Step 3: Poetry のインストール

コマンドプロンプトを開いて以下を実行してください：

```shell
pip install poetry
```

---

## ✅ Step 4: 必要なライブラリのインストール

以下のコマンドを解凍フォルダ内で実行します：

```shell
cd path\to\pdf-tool
poetry install
```
---

## ✅ 使い方

1. コマンドプロンプトで解答したフォルダに移動
例
```shell
cd path\to\pdf-tool
```
2. 移動先で下記コマンドを実行

```shell
poetry run python main.py --watermark --password --prefix "" --suffix "(draft)"
```

---

## 💡 注意点

- `pdf/` フォルダに **加工対象の PDF** を入れてください  
- `mark/` フォルダに **`sign.pdf` と `draft.pdf`** を配置してください  
- `output/` フォルダは自動で作成されます
