# Podman環境セットアップガイド

このドキュメントでは、Podman/Dockerを使用してIEEE論文検索ツールを実行する方法を説明します。

## 前提条件

- Podman 3.0+ または Docker 20.10+
- X Server（GUIモード使用時）

## セットアップ手順

### 1. Podmanのインストール確認

```bash
# Podmanバージョン確認
podman --version

# インストールされていない場合
# Ubuntu/Debian
sudo apt install podman podman-compose -y

# Fedora/RHEL
sudo dnf install podman podman-compose -y
```

### 2. イメージのビルド

```bash
# プロジェクトディレクトリで実行
cd /path/to/browser-use-automation

# Podman Composeでビルド（推奨）
podman-compose build

# または、直接Podmanでビルド
podman build -t browser-use-automation:latest -f Containerfile .
```

**ビルド時間**: 初回は5-10分程度（依存関係のダウンロードとインストール）

### 3. 環境変数の設定

```bash
# .envファイルを作成
cp .env.example .env

# .envファイルを編集
nano .env
```

**最小限の設定** (`.env`):
```bash
# ブラウザ設定
HEADLESS=false  # IEEE検索にはfalseを推奨

# ログ設定
BROWSER_USE_LOGGING_LEVEL=info
BROWSER_USE_DEBUG_LOG_FILE=debug.log
BROWSER_USE_INFO_LOG_FILE=info.log
```

## 実行方法

### 方法1: ヘッドレスモード（サーバー環境）

X Serverなしで実行。IEEE検索ではブロックされる可能性があります。

```bash
# ヘッドレスモードで検索
podman run --rm \
  --env-file .env \
  -e HEADLESS=true \
  -v ./papers:/app/papers:z \
  localhost/browser-use-automation_ieee-search:latest \
  uv run python examples/ieee_paper_search.py -q "machine learning" -n 3
```

### 方法2: GUIモード（X11転送）- 推奨

X Serverを使用してブラウザGUIを表示。IEEE検索に最適。

```bash
# X11転送の許可
xhost +local:

# GUIモードで検索（X11転送）
podman run --rm \
  --env-file .env \
  -e HEADLESS=false \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
  -v ./papers:/app/papers:z \
  --network host \
  localhost/browser-use-automation_ieee-search:latest \
  uv run python examples/ieee_paper_search.py -q "deep learning" -n 5
```

**注意**: SELinux有効時は `-v` オプションに `:z` を追加してください。

### 方法3: テーマ別検索（推奨）

複数のテーマで自動的に論文を検索し、テーマごとにディレクトリを分けて保存。

```bash
# 全テーマを検索
podman run --rm \
  --env-file .env \
  -e HEADLESS=false \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
  -v ./papers:/app/papers:z \
  --network host \
  localhost/browser-use-automation_ieee-search:latest \
  uv run python examples/ieee_theme_based_search.py -n 3

# 特定のテーマのみ検索
podman run --rm \
  --env-file .env \
  -e HEADLESS=false \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
  -v ./papers:/app/papers:z \
  --network host \
  localhost/browser-use-automation_ieee-search:latest \
  uv run python examples/ieee_theme_based_search.py \
    -t machine_learning -t cybersecurity -n 5
```

### 方法4: 対話的インターフェース

コンテナ内でインタラクティブシェルを起動。

```bash
# インタラクティブモードでコンテナ起動
podman run -it --rm \
  --env-file .env \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
  -v ./papers:/app/papers:z \
  --network host \
  localhost/browser-use-automation_ieee-search:latest \
  /bin/bash

# コンテナ内で実行
uv run python examples/ieee_chat_interface.py
```

## トラブルシューティング

### 問題1: `DISPLAY environment variable not set`

**原因**: DISPLAY環境変数が設定されていない

**解決方法**:
```bash
# DISPLAY環境変数を確認
echo $DISPLAY

# 設定されていない場合
export DISPLAY=:0

# Podman実行時に明示的に指定
podman run ... -e DISPLAY=:0 ...
```

### 問題2: `cannot open display`

**原因**: X11転送の権限がない

**解決方法**:
```bash
# ローカルアクセスを許可
xhost +local:

# または、特定のユーザーを許可
xhost +SI:localuser:$(whoami)
```

### 問題3: Permission denied (`/app/papers`)

**原因**: SELinuxの制限（Fedora/RHEL）

**解決方法**:
```bash
# ボリュームマウント時に :z を追加
podman run ... -v ./papers:/app/papers:z ...

# または、ディレクトリ権限を変更
chmod 777 ./papers
```

### 問題4: イメージが見つからない

**原因**: イメージがビルドされていない

**解決方法**:
```bash
# イメージ一覧を確認
podman images

# イメージを再ビルド
podman-compose build
```

### 問題5: ネットワーク接続エラー

**原因**: コンテナのネットワーク設定

**解決方法**:
```bash
# ホストネットワークを使用
podman run ... --network host ...

# または、ブリッジネットワークでDNSを指定
podman run ... --dns 8.8.8.8 --dns 8.8.4.4 ...
```

## 出力ディレクトリ構造

テーマ別検索を実行すると、以下のディレクトリ構造で結果が保存されます：

```
papers/
├── machine_learning/
│   └── search_results.json
├── cybersecurity/
│   └── search_results.json
├── blockchain/
│   └── search_results.json
├── iot/
│   └── search_results.json
├── quantum_computing/
│   └── search_results.json
└── search_summary.json
```

## コンテナイメージの管理

### イメージの再ビルド

```bash
# キャッシュなしで再ビルド
podman-compose build --no-cache
```

### イメージの削除

```bash
# 特定のイメージを削除
podman rmi localhost/browser-use-automation_ieee-search:latest

# 未使用イメージをすべて削除
podman image prune -a
```

### イメージのエクスポート/インポート

```bash
# イメージをtarファイルにエクスポート
podman save -o browser-use-automation.tar localhost/browser-use-automation_ieee-search:latest

# tarファイルからインポート
podman load -i browser-use-automation.tar
```

## パフォーマンス最適化

### 1. ビルドキャッシュの活用

Containerfileの依存関係部分は変更されない限りキャッシュされます。

### 2. マルチステージビルドの利用

現在のContainerfileは単一ステージですが、必要に応じて最適化可能。

### 3. ボリュームマウントの最適化

SELinux無効環境では `:z` フラグを省略することで若干高速化されます。

```bash
# SELinux無効時（Ubuntu等）
podman run ... -v ./papers:/app/papers ...
```

## セキュリティ考慮事項

### 1. 最小限の権限で実行

```bash
# rootlessモードで実行（推奨）
podman run --rm --user $(id -u):$(id -g) ...
```

### 2. ネットワーク制限

```bash
# インターネットアクセスのみ許可（IEEE Xploreへのアクセスのみ）
podman run ... --network bridge ...
```

### 3. 読み取り専用ファイルシステム

```bash
# コンテナファイルシステムを読み取り専用に
podman run ... --read-only --tmpfs /tmp ...
```

## よくある質問（FAQ）

### Q1: DockerではなくPodmanを使う理由は？

**A**: Podmanはrootless実行が可能で、より安全です。また、Dockerとコマンド互換性があります。

### Q2: コンテナ起動が遅い

**A**: 初回起動時はChromiumの初期化に時間がかかります。2回目以降は高速化されます。

### Q3: 複数のコンテナを同時実行できますか？

**A**: 可能ですが、X11転送を使用する場合はDISPLAY番号を変更する必要があります。

```bash
# 1つ目のコンテナ
podman run ... -e DISPLAY=:0 ...

# 2つ目のコンテナ
podman run ... -e DISPLAY=:1 ...
```

## リファレンス

- **Podman公式ドキュメント**: https://docs.podman.io/
- **Docker互換性**: https://podman.io/whatis.html
- **X11転送ガイド**: https://wiki.archlinux.org/title/X11_forwarding

---

**作成日**: 2025-10-16
**更新日**: 2025-10-16
