# IEEE論文検索 テーマ別デモガイド

このガイドでは、Podman環境を使用してテーマ別のIEEE論文検索デモを実行する方法を説明します。

## 概要

このプロジェクトは、複数の研究テーマに基づいてIEEE Xploreから論文を自動検索し、テーマごとにディレクトリを分けて整理するシステムです。

### 対応テーマ

1. **Machine Learning** (`machine_learning`) - 機械学習とAI基礎
2. **Cybersecurity** (`cybersecurity`) - サイバーセキュリティと脅威検出
3. **Blockchain** (`blockchain`) - ブロックチェーンと分散システム
4. **IoT** (`iot`) - IoTとセンサーネットワーク
5. **Quantum Computing** (`quantum_computing`) - 量子コンピューティングとアルゴリズム

各テーマには専用のGitブランチ（`research/<theme_name>`）が作成されており、検索結果はテーマごとに独立したディレクトリに保存されます。

## セットアップ

### 前提条件

- Podman 3.0+ または Docker 20.10+
- Git
- 約2GBのディスク空き容量（Podmanイメージ用）

### 1. プロジェクトの準備

```bash
# プロジェクトディレクトリに移動
cd /home/ablaze/research/browser-use-automation

# 依存関係の確認
podman images | grep browser-use-automation
```

### 2. イメージのビルド（必要な場合）

```bash
# Podman Composeでビルド
podman-compose build

# または、直接ビルド
podman build -t browser-use-automation_ieee-search:latest -f Containerfile .
```

## デモの実行

### デモ1: テーマ一覧の表示

利用可能な研究テーマを確認します。

```bash
podman run --rm \
  --env-file .env \
  -v ./examples:/app/examples:ro,z \
  localhost/browser-use-automation_ieee-search:latest \
  uv run python examples/ieee_theme_based_search.py --list-themes
```

**期待される出力**:
```
INFO     [__main__] Available research themes:
INFO     [__main__]   - machine_learning: Machine Learning & AI fundamentals
INFO     [__main__]   - cybersecurity: Cybersecurity & Threat Detection
INFO     [__main__]   - blockchain: Blockchain & Distributed Systems
INFO     [__main__]   - iot: IoT & Sensor Networks
INFO     [__main__]   - quantum_computing: Quantum Computing & Algorithms
```

### デモ2: 単一テーマの検索（推奨）

1つのテーマで少数の論文を検索します。

```bash
# Machine Learningテーマで2件検索
podman run --rm \
  --env-file .env \
  -e HEADLESS=true \
  -v ./papers:/app/papers:z \
  -v ./examples:/app/examples:ro,z \
  localhost/browser-use-automation_ieee-search:latest \
  uv run python examples/ieee_theme_based_search.py \
    -t machine_learning -n 2
```

**結果の確認**:
```bash
# 検索結果の確認
ls -R papers/

# JSONファイルの内容確認
cat papers/machine_learning/search_results.json
```

### デモ3: 複数テーマの検索

複数のテーマを同時に検索します。

```bash
# Machine LearningとCybersecurityで各3件検索
podman run --rm \
  --env-file .env \
  -e HEADLESS=true \
  -v ./papers:/app/papers:z \
  -v ./examples:/app/examples:ro,z \
  localhost/browser-use-automation_ieee-search:latest \
  uv run python examples/ieee_theme_based_search.py \
    -t machine_learning -t cybersecurity -n 3
```

**期待されるディレクトリ構造**:
```
papers/
├── machine_learning/
│   └── search_results.json
├── cybersecurity/
│   └── search_results.json
└── search_summary.json
```

### デモ4: 全テーマの検索（フルデモ）

すべてのテーマで論文を検索します。

```bash
# 全テーマで各2件検索（合計10件程度）
podman run --rm \
  --env-file .env \
  -e HEADLESS=true \
  -v ./papers:/app/papers:z \
  -v ./examples:/app/examples:ro,z \
  localhost/browser-use-automation_ieee-search:latest \
  uv run python examples/ieee_theme_based_search.py -n 2
```

**所要時間**: 約5-10分（IEEE Xploreの応答速度に依存）

## ブランチ構造の活用

### テーマ別ブランチへの切り替え

```bash
# 利用可能なブランチを確認
git branch

# Machine Learningブランチに切り替え
git checkout research/machine_learning

# Machine Learningテーマの検索結果のみをコミット
git add papers/machine_learning/
git commit -m "Add machine learning paper search results"

# メインブランチに戻る
git checkout main
```

### ブランチ戦略

各研究テーマは独立したブランチで管理されます：

- `main` - メインブランチ（すべてのテーマの統合）
- `research/machine_learning` - 機械学習関連の論文
- `research/cybersecurity` - サイバーセキュリティ関連の論文
- `research/blockchain` - ブロックチェーン関連の論文
- `research/iot` - IoT関連の論文
- `research/quantum_computing` - 量子コンピューティング関連の論文

### ブランチの作成・更新

```bash
# 新しいテーマブランチを作成（自動スクリプト）
./bin/setup_theme_branches.sh
```

## 出力ファイルの形式

### search_results.json（テーマ別）

各テーマディレクトリに保存されます。

```json
{
  "theme": "machine_learning",
  "description": "Machine Learning & AI fundamentals",
  "query": "machine learning",
  "results": [
    {
      "title": "Deep Learning for Network Traffic Classification",
      "authors": ["John Smith", "Jane Doe"],
      "url": "https://ieeexplore.ieee.org/document/12345"
    }
  ],
  "count": 1
}
```

### search_summary.json（全体サマリー）

すべてのテーマの検索結果をまとめたファイル。

```json
{
  "themes": [
    {
      "theme": "machine_learning",
      "description": "Machine Learning & AI fundamentals",
      "count": 2,
      "success": true
    },
    {
      "theme": "cybersecurity",
      "description": "Cybersecurity & Threat Detection",
      "count": 2,
      "success": true
    }
  ],
  "total_themes": 2
}
```

## トラブルシューティング

### 問題1: `Request Rejected` (IEEE Xploreのbot検出)

**症状**: ヘッドレスモードでIEEE Xploreにアクセスできない

**解決方法**: ヘッドレスモードではIEEE XploreがBot検出する可能性があります。GUIモード（X11転送）を使用してください。

```bash
# X11転送を有効化
xhost +local:

# GUIモードで実行
podman run --rm \
  --env-file .env \
  -e HEADLESS=false \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
  -v ./papers:/app/papers:z \
  -v ./examples:/app/examples:ro,z \
  --network host \
  localhost/browser-use-automation_ieee-search:latest \
  uv run python examples/ieee_theme_based_search.py -t machine_learning -n 2
```

### 問題2: Permission denied (`/app/papers`)

**症状**: ボリュームマウント時にパーミッションエラー

**解決方法**: SELinuxのコンテキストを設定（`:z`フラグ）

```bash
# SELinux有効時は :z を追加
-v ./papers:/app/papers:z
```

### 問題3: 検索結果が0件

**原因**: ネットワーク接続、IEEE Xploreのアクセス制限、クエリの問題

**解決方法**:
1. ネットワーク接続を確認
2. より一般的なクエリで試す
3. GUIモード（`HEADLESS=false`）で実行

### 問題4: イメージが見つからない

**解決方法**:
```bash
# イメージを再ビルド
podman-compose build --no-cache
```

## パフォーマンス

### 検索速度の目安

- 1論文あたり: 約10-30秒
- 1テーマ（5件）: 約1-3分
- 全テーマ（5件×5テーマ）: 約5-15分

### 最適化のヒント

1. **並列実行**: 複数のコンテナで異なるテーマを並列検索
2. **キャッシュ活用**: 既存の検索結果を再利用
3. **結果数の調整**: `-n` オプションで少数に設定

## 次のステップ

1. **論文の詳細分析**: 検索結果から引用を抽出
   ```bash
   uv run python examples/ieee_chat_interface.py
   ```

2. **PDF本文の抽出**: PDFから各セクションを自動抽出
   - Abstract
   - Introduction
   - Methodology
   - Results
   - Conclusion

3. **カスタムテーマの追加**: `examples/ieee_theme_based_search.py` の `RESEARCH_THEMES` を編集

## 関連ドキュメント

- **Podman詳細セットアップ**: [PODMAN_SETUP.md](./PODMAN_SETUP.md)
- **IEEE検索機能詳細**: [IEEE_SEARCH_README.md](./IEEE_SEARCH_README.md)
- **メインREADME**: [README.md](./README.md)

---

**作成日**: 2025-10-16
**最終更新**: 2025-10-16
**動作確認環境**: Podman 5.6.2, Kali Linux 6.16.8
