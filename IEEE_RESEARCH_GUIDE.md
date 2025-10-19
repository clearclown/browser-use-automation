# IEEE Xplore 専用研究調査ガイド

## 🎯 重要な結論

**IEEE Xplore検索には「ブラウザ自動化版」が必須です。**

理由：
- ✅ IEEE XploreはAngular + Web Componentsベースの完全動的サイト
- ❌ 静的HTMLパース（httpx + BeautifulSoup）では論文データ取得不可
- ✅ ブラウザレンダリングによる自動化が唯一の実用的手段

---

## 🚀 推奨：Streamlit Web UI使用

### 1. Streamlit起動

```bash
./run_streamlit.sh
```

ブラウザで `http://localhost:8501` にアクセス

### 2. 設定

#### サイドバー設定：
- **実行モード**: 「ブラウザ自動化版（IEEE専用・推奨）」を選択
- **LLMプロバイダー**: DeepSeek（コスパ最高）
- **最大論文数**: 10-50件
- **ヘッドレスモード**: ❌ **False**（必須・安定性のため）
- **年範囲**: 2022-2025

#### メイン画面：
- **研究トピック**: 例「Deep Learning Applications」
- **研究課題**: 例「最新の応用事例は？」
- **キーワード**: 1行に1つ
  ```
  deep learning
  neural network
  application
  ```

### 3. 実行

「🚀 研究調査を開始」ボタンをクリック

---

## 🖥️ CLI使用（IEEE専用スクリプト）

### 簡単な実行

```bash
./run_ieee_research.sh
```

デフォルト設定：
- LLM: DeepSeek
- 最大論文数: 10件
- ヘッドレス: False

### カスタマイズ実行

```bash
# LLMとMAX_PAPERSを指定
./run_ieee_research.sh deepseek 20

# または直接実行
uv run python -m automated_research.main \
  --provider deepseek \
  --max-papers 20 \
  --no-headless \
  --non-interactive
```

---

## ⚠️ トラブルシューティング

### エラー1: ブラウザタイムアウト

```
TimeoutError: Browser did not start within 180 seconds
```

**解決方法**:

```bash
# 1. ゾンビプロセスクリーンアップ
./cleanup_browsers.sh

# または
pkill -9 chromium
rm -rf /tmp/browser-use-user-data-dir-*

# 2. 再実行
./run_ieee_research.sh
```

### エラー2: CDP URL取得失敗

**原因**: ヘッドレスモードが有効

**解決方法**: `--no-headless` フラグを必ず使用

### エラー3: リソース不足

**システム要件**:
- 最低: 8GB RAM, 4コアCPU
- 推奨: 16GB RAM, 8コアCPU

**対策**:
- 他のアプリを終了
- `max_papers` を減らす（10件程度）
- クリーンアップ実行後に再試行

---

## 📊 パフォーマンス目安

| 項目 | 値 |
|------|-----|
| **ブラウザ起動時間** | 15-60秒 |
| **論文検索時間** | 30-90秒 |
| **1論文処理時間** | 5-10秒 |
| **10論文の総時間** | 5-15分 |
| **メモリ使用量** | 500-800MB |
| **CPU使用率** | 50-90% |

---

## 📝 出力ファイル

### 生成されるファイル

```
automated_research/
├── data/
│   ├── research_info_SESSION_ID.json      # 研究情報
│   ├── search_strategy_SESSION_ID.json    # 検索戦略
│   └── papers_SESSION_ID.json             # 論文リスト
└── reports/
    ├── session_SESSION_ID/
    │   ├── paper_1.md                     # 個別レポート
    │   ├── paper_2.md
    │   └── ...
    └── summary_report_SESSION_ID.md       # 統合レポート
```

### レポート形式

**統合レポート** (`summary_report_SESSION_ID.md`):
- 研究動向まとめ
- 主要な研究テーマ
- 重要論文3-5件のピックアップ
- 今後の研究方向性

**個別レポート** (落合陽一式):
1. どんなもの？
2. 先行研究と比べてどこがすごい？
3. 技術や手法のキモはどこ？
4. どうやって有効だと検証した？
5. 議論はある？
6. 次に読むべき論文は？

---

## 💡 ベストプラクティス

### 推奨設定

```yaml
実行モード: ブラウザ自動化版（IEEE専用）
LLM: DeepSeek（コスパ最高）
最大論文数: 10-20件（初回）
ヘッドレス: False（必須）
年範囲: 直近3年（2022-2025）
```

### 効率的な使い方

1. **初回は少数で試す**
   - `max_papers=5` で動作確認
   - 成功したら増やす

2. **実行前にクリーンアップ**
   ```bash
   ./cleanup_browsers.sh
   ./run_ieee_research.sh
   ```

3. **キーワードは具体的に**
   - 良い例: `transformer architecture`, `attention mechanism`
   - 悪い例: `AI`, `machine learning`（広すぎる）

4. **定期的にクリーンアップ**
   - 1日1回または5回実行ごと

---

## 🔧 詳細設定

### タイムアウト延長

環境変数で調整可能（デフォルト180秒）：

```bash
export TIMEOUT_BrowserStartEvent=300
export TIMEOUT_NavigateToUrlEvent=120
./run_ieee_research.sh
```

### LLMプロバイダー変更

```bash
# OpenAI
./run_ieee_research.sh openai 10

# Claude
./run_ieee_research.sh claude 10

# Google Gemini
./run_ieee_research.sh google 10
```

### 非対話モード

```bash
# 対話型スキップ、全自動実行
uv run python -m automated_research.main \
  --provider deepseek \
  --max-papers 10 \
  --no-headless \
  --non-interactive
```

---

## 📚 参考資料

- [BROWSER_USE_PERFORMANCE_ANALYSIS.md](BROWSER_USE_PERFORMANCE_ANALYSIS.md): パフォーマンス詳細
- [README.md](README.md): 全体ドキュメント
- [AUTOMATED_RESEARCH_SYSTEM.md](AUTOMATED_RESEARCH_SYSTEM.md): システム概要

---

## ✅ チェックリスト

実行前の確認：

- [ ] ゾンビプロセスをクリーンアップした
- [ ] ヘッドレス=Falseに設定した
- [ ] LLMプロバイダーのAPIキーが設定されている（.env）
- [ ] システムリソース十分（8GB+ RAM）
- [ ] max_papersは10-20件程度（初回）

---

**IEEE Xplore専用研究調査を快適に実行できます！** 🚀
