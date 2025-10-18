# クイックスタートガイド

## 最速で動かす

```bash
# 1. 環境変数を設定（.envファイルに以下を追加）
echo "OPENAI_API_KEY=sk-your-key-here" >> .env

# 2. 実行
python automated_research/main.py

# または
python -m automated_research.main
```

## 実行例

### 対話的実行（デフォルト）

```bash
$ python -m automated_research.main
================================================================================
🤖 完全自動化研究支援システム
================================================================================

どんな内容について検索しますか？あなたの研究はなんですか？
あなたの研究について自由に語ってください。

あなた: 機械学習を使った医療画像診断の研究をしています。特にCTスキャン画像からの肺がん検出に興味があります。

推定される研究テーマ: 機械学習による医療画像診断 - 肺がん検出
推定される研究分野: Computer Vision, Medical AI

質問 1: 具体的にどのような機械学習手法に注目していますか？
あなた: CNNとTransformerを組み合わせたハイブリッドモデルに注目しています

... (対話が続く)

📊 PRISMA方式検索戦略を生成中...

✅ 検索戦略を生成しました

【主要キーワード】
  • lung cancer detection
  • medical image analysis
  • CNN
  • Transformer

【検索クエリ】
  1. (lung cancer OR pulmonary nodule) AND (deep learning OR CNN OR Transformer) AND (CT scan OR computed tomography)
  2. medical image segmentation AND lung cancer AND neural networks
  ...

🔍 IEEE Xplore自動検索を開始します

📝 検索 1/3: "(lung cancer OR pulmonary nodule) AND ..."
  ✅ 8件の論文を発見

... (検索が続く)

📝 各論文の詳細分析（落合陽一式）

[1/20] 分析中: Deep Learning for Lung Cancer Detection in CT Images...
  ✅ レポート保存: 001_Deep_Learning_for_Lung_Cancer.md

... (分析が続く)

📊 統合レポートの生成

✅ 統合レポートを生成: reports/summary_report_20241018_051500.md

================================================================================
🎉 すべての処理が完了しました！
================================================================================
```

### ヘッドレスモード（バックグラウンド実行）

```bash
# サーバーやCron実行に最適
python -m automated_research.main --headless --max-papers 50
```

### 少量論文で高速テスト

```bash
# 5件だけ収集して動作確認
python -m automated_research.main --max-papers 5
```

## 生成されるファイル

```
automated_research/
├── data/
│   ├── research_info_20241018_051500.json      ← あなたの研究情報
│   ├── search_strategy_20241018_051500.json    ← 検索戦略
│   └── collected_papers_20241018_051500.json   ← 収集した論文リスト
│
├── reports/
│   ├── session_20241018_051500/                ← 個別論文レポート
│   │   ├── 001_Deep_Learning_for_Lung_Cancer.md
│   │   ├── 002_Transformer_Based_Medical.md
│   │   └── ... (各論文の詳細分析)
│   │
│   ├── summary_report_20241018_051500.md       ← ★重要★ 統合レポート
│   └── papers_list_20241018_051500.json        ← 論文リスト
```

## 統合レポートの内容

`summary_report_YYYYMMDD_HHMMSS.md`には以下が含まれます：

- **エグゼクティブサマリー**: 研究分野の現状と主要な発見
- **検索戦略と収集結果**: 使用したクエリと収集論文数
- **主要な研究トレンド**: 最新の技術動向3-5個
- **技術的アプローチの分類**: 論文を手法別に整理
- **重要な発見と洞察**: 注目すべき研究成果
- **あなたの研究への示唆**: 具体的に何を活かせるか
- **推奨される次のステップ**: 深掘りすべき論文・技術
- **参考文献一覧**: すべての論文の書誌情報

## 個別論文レポートの内容

各論文の`.md`ファイルには落合陽一式の6項目+1が含まれます：

```markdown
## title: "論文タイトル"
date: 2024-10-18
categories: Computer Vision, Medical AI

### 1. どんなもの？
（3-4文で論文の核心を説明）

### 2. 先行研究と比べてどこがすごいの？
（先行研究の限界と本論文の新規性）

### 3. 技術や手法の"キモ"はどこにある？
（技術的な核心部分を詳しく）

### 4. どうやって有効だと検証した？
（実験設定、評価指標、結果）

### 5. 議論はあるか？
（著者の議論、制約、今後の課題）

### 6. 次に読むべき論文はあるか？
（重要な参考文献）

### 7. 自分の研究との関連        ← ★あなた専用★
（あなたの研究テーマとの関連性、応用可能性、着想）

### 論文情報・リンク
- [著者, "タイトル," 学会誌, 2023](https://ieeexplore.ieee.org/...)
```

## トラブルシューティング

### ❌ `ModuleNotFoundError: No module named 'automated_research'`

```bash
# プロジェクトルートから実行してください
cd /path/to/browser-use-automation
python -m automated_research.main
```

### ❌ `OpenAI API key not found`

```bash
# .envファイルを確認
cat .env

# なければ作成
echo "OPENAI_API_KEY=sk-..." > .env
```

### ❌ ブラウザが起動しない

```bash
# ヘッドレスモードを解除して確認
python -m automated_research.main
# （--headlessオプションを外す）
```

### ⚠️ IEEE Xploreで論文が見つからない

- 検索クエリが厳しすぎる可能性があります
- 生成された`search_strategy_*.json`を確認
- 必要に応じて手動で検索クエリを修正して再実行

## よくある質問

### Q: 何分くらいかかりますか？

A: 論文数によりますが：
- 5論文: 約5-10分
- 20論文: 約15-30分
- 50論文: 約30-60分

### Q: お金はかかりますか？

A: はい、OpenAI APIの使用料が発生します：
- 論文1件あたり約$0.05-0.10（GPT-4o使用時）
- 20論文で約$1-2程度

### Q: 日本語の論文にも対応していますか？

A: 現在はIEEE Xplore（主に英語論文）のみ対応しています。
将来的にJ-STAGEやCiNii対応予定です。

### Q: 定期実行できますか？

A: はい、cronで定期実行可能です：

```bash
# 毎週月曜9時に実行
0 9 * * 1 cd /path/to/browser-use-automation && python -m automated_research.main --headless
```

### Q: 結果をどう使えばいいですか？

A:
1. **統合レポート**を読んで分野全体を把握
2. **個別レポート**で気になる論文を深掘り
3. **papers_list.json**から元論文にアクセス
4. 自分の論文の関連研究セクションに活用

## 次のステップ

- [ ] 統合レポートを読む
- [ ] 気になる論文3つをピックアップ
- [ ] 元論文のPDFをダウンロード
- [ ] 自分の研究計画を更新

---

Happy Researching! 📚🔬
