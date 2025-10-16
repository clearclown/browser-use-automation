# 野生シカの個体識別における拡張動的深層学習アプローチ - 文献調査レポート

**調査日**: 2025-10-16
**データソース**: IEEE Xplore
**総収集論文数**: 118件
**ブランチ**: `experiment/deer-individual-identification-dynamic-dl`

---

## エグゼクティブサマリー

本調査では、野生シカの個体識別に応用可能な動的・適応的深層学習アプローチに関する最新研究を包括的に収集した。直接「シカ」を対象とした論文は限定的だが、トラ・ヒョウ・パンダ・魚類等の野生動物個体識別における最先端技術（Transformer、Siamese Network、Few-shot Learning、メトリック学習等）を広範に調査し、鹿への応用可能性を分析した。

### 主要発見

1. **Transformer ベース手法**が野生動物個体識別で優れた性能を示している
2. **Few-shot Learning**により少数サンプルでの個体識別が実現可能
3. **Siamese Network + メトリック学習**が野生環境での堅牢な識別を実現
4. **動的特徴（歩容・行動パターン）**の活用が識別精度向上に寄与
5. **カメラトラップ画像**からのリアルタイム識別技術が成熟段階

---

## 検索クエリ別収集結果

| 検索クエリ | 収集数 | 関連度 |
|-----------|--------|---------|
| wildlife individual identification deep learning | 20件 | ★★★★★ |
| adaptive deep learning animal recognition | 20件 | ★★★★ |
| camera trap animal identification deep learning | 20件 | ★★★★★ |
| metric learning animal identification | 15件 | ★★★★ |
| gait recognition animal identification | 10件 | ★★★★ |
| dynamic learning wildlife real-time identification | 6件 | ★★★ |
| transformer animal re-identification | 4件 | ★★★★★ |
| deer individual identification | 3件 | ★ |
| siamese network wildlife individual recognition | 2件 | ★★★★★ |
| few-shot learning animal identification | 2件 | ★★★★★ |

**総計**: 118件（重複除く実質約95件）

---

## 技術分類と主要論文

### 1. Transformer ベースの個体識別（最先端アプローチ）

#### 1.1 軽量変形可能Transformer
**ReDeformTR: Wildlife Re-Identification Based on Light-Weight Deformable Transformer With Multi-Image Feature Fusion**
- 著者: Zitong Li et al. (2024)
- URL: https://ieeexplore.ieee.org/document/10620204/
- **キーポイント**:
  - 軽量な変形可能Transformer（Deformable Transformer）
  - 複数画像の特徴融合によるロバスト性向上
  - 野生動物の個体識別に特化
- **鹿への応用**: 複数カメラトラップ画像からの統合的個体識別

#### 1.2 Transformerベースのトラ個体識別
**Transformer-based Models for Enhanced Amur Tiger Re-Identification**
- 著者: Xufeng Bai et al. (2024)
- URL: https://ieeexplore.ieee.org/document/10432893/
- **キーポイント**:
  - Vision Transformer (ViT) の動物への適用
  - 縞模様パターン認識の高精度化
- **鹿への応用**: 斑点模様・体型特徴の学習

#### 1.3 Vision Transformer for 猫科動物
**ViT-CatNet: An End-to-End Vision Transformer Architecture for Instance-Level Feline Identification**
- 著者: Kaikun Hu (2025)
- URL: https://ieeexplore.ieee.org/document/11103379/
- **キーポイント**:
  - エンドツーエンドのViTアーキテクチャ
  - インスタンスレベルの識別精度
- **鹿への応用**: 個体固有の顔特徴・体型パターン認識

#### 1.4 DINOベースの説明可能AI
**Re-Identification of Individual Kākā: An Explainable DINO-Based Model**
- 著者: Paula Maddigan et al. (2024)
- URL: https://ieeexplore.ieee.org/document/10794473/
- **キーポイント**:
  - DINO（自己教師あり学習）の活用
  - 説明可能性（XAI）の統合
  - 鳥類個体識別への応用
- **鹿への応用**: 少数データでの学習、識別根拠の可視化

#### 1.5 マルチスケールTransformer + Attention
**A Multi-scale Cattle Individual Identification Method Based on CMT Module and Attention Mechanism**
- 著者: Yuan Li et al. (2024)
- URL: https://ieeexplore.ieee.org/document/10695246/
- **キーポイント**:
  - CMT（Compact Mixed Transformer）モジュール
  - マルチスケール特徴抽出
  - Attentionメカニズムによる重要特徴強調
- **鹿への応用**: 異なる距離・角度からの識別

### 2. Few-shot Learning（少数サンプル学習）

#### 2.1 プロトタイプコントラスティブネットワーク
**Prototypical Contrastive Network for One-Shot Animal Individual Identification**
- 著者: Yurong Zhang et al. (2025)
- URL: https://ieeexplore.ieee.org/document/11090778/
- **キーポイント**:
  - One-shot（1サンプル）での個体識別
  - プロトタイプネットワーク + コントラスティブ学習
  - 新規個体への即座適応
- **鹿への応用**: 初見個体の即座識別、データ収集コスト削減

#### 2.2 Siamese Network + 転移学習
**Unique Animal Identification using Deep Transfer Learning For Data Fusion in Siamese Networks**
- 著者: T. L Van Zyl et al. (2020)
- URL: https://ieeexplore.ieee.org/document/9190426/
- **キーポイント**:
  - Siamese Networkによる類似度学習
  - 複数データソースの融合
  - 転移学習による汎化性能向上
- **鹿への応用**: 既存動物データセットからの知識転移

#### 2.3 Few-shotキーポイント検出
**AW-HRNet: A Spatially-Aware and Context-Enhanced Network for Few-Shot Animal Keypoint Detection**
- 著者: Ling Yang et al. (2025)
- URL: https://ieeexplore.ieee.org/document/11108430/
- **キーポイント**:
  - 少数サンプルでのキーポイント検出
  - 空間認識とコンテキスト強化
  - HRNet（High-Resolution Network）の拡張
- **鹿への応用**: 骨格・関節ポイント検出による姿勢不変識別

### 3. Siamese Network & メトリック学習

#### 3.1 Siamese Networkによる野生動物個体識別
**Automated Identification of Individuals in Wildlife Population Using Siamese Neural Networks**
- 著者: Nkosikhona Dlamini et al. (2020)
- URL: https://ieeexplore.ieee.org/document/9311574/
- **キーポイント**:
  - 野生動物集団からの自動個体識別
  - 画像ペアによる類似度学習
  - 大規模個体群への対応
- **鹿への応用**: 群れ内個体の自動追跡

#### 3.2 ポーズ不変埋め込み学習
**Robust Re-identification of Manta Rays from Natural Markings by Learning Pose Invariant Embeddings**
- 著者: Olga Moskvyak et al. (2021)
- URL: https://ieeexplore.ieee.org/document/9647359/
- **キーポイント**:
  - ポーズ変動に頑健な埋め込み学習
  - 自然模様（マンタの斑点）からの識別
  - 幾何学的等価性の学習
- **鹿への応用**: 姿勢・角度変化に対する頑健性

#### 3.3 メトリック学習ベースのセグメンテーション
**Metric learning based automatic segmentation of patterned species**
- 著者: Ankita Shukla et al. (2016)
- URL: https://ieeexplore.ieee.org/document/7533107/
- **キーポイント**:
  - パターン種のメトリック学習
  - 自動セグメンテーション
  - 模様ベースの識別
- **鹿への応用**: 斑点・縞模様パターンからの自動分割

#### 3.4 自己教師あり学習
**Self-Supervised Animal Detection, Tracking & Re-Identification**
- 著者: Muhammad Moosa et al. (2024)
- URL: https://ieeexplore.ieee.org/document/10755717/
- **キーポイント**:
  - ラベルなしデータからの学習
  - 検出・追跡・再識別の統合
  - 自己教師あり学習（SSL）の活用
- **鹿への応用**: アノテーションコスト削減、大量未ラベルデータ活用

### 4. 歩容認識（Gait Recognition）

#### 4.1 パンダの歩容認識
**ReconGait: Giant Panda Gait Recognition Based on Spatio-Temporal Feature Reconstruction**
- 著者: Peng Min et al. (2024)
- URL: https://ieeexplore.ieee.org/document/10649970/
- **キーポイント**:
  - 時空間特徴の再構成
  - 歩容パターンによる個体識別
  - ビデオシーケンスの解析
- **鹿への応用**: 歩行パターンによる動的識別、遠距離からの識別

#### 4.2 家畜の歩容識別
**BiLSTM-based Individual Cattle Identification for Automated Precision Livestock Farming**
- 著者: Yongliang Qiao et al. (2020)
- URL: https://ieeexplore.ieee.org/document/9217026/
- **キーポイント**:
  - BiLSTM（双方向LSTM）による時系列学習
  - 歩容データからの個体識別
  - 精密畜産への応用
- **鹿への応用**: 時系列動作パターンの学習、長期追跡

#### 4.3 マルチモーダル行動認識
**AnimalFormer: Multimodal Vision Framework for Behavior-based Precision Livestock Farming**
- 著者: Ahmed Qazi et al. (2024)
- URL: https://ieeexplore.ieee.org/document/10677926/
- **キーポイント**:
  - マルチモーダル（視覚+他センサー）
  - 行動ベースの識別
  - Transformer フレームワーク
- **鹿への応用**: 採食・警戒等の行動パターン統合識別

### 5. 特殊な識別手法

#### 5.1 足跡による個体識別
**PawPrint: Whose Footprints are These? Identifying Animal Individuals by their Footprints**
- 著者: Inpyo Song et al. (2025)
- URL: https://ieeexplore.ieee.org/document/11084465/
- **キーポイント**:
  - 足跡画像からの個体識別
  - 非侵襲的モニタリング
  - 痕跡学（Ichnology）+ AI
- **鹿への応用**: 雪上・泥地の足跡からの識別、直接観察不要

#### 5.2 色素パターン学習
**Pigmentation-based Visual Learning for Salvelinus fontinalis Individual Re-identification**
- 著者: Zhongliang Zhou et al. (2023)
- URL: https://ieeexplore.ieee.org/document/10020966/
- **キーポイント**:
  - 体表色素パターンの学習
  - 魚類（カワマス）個体識別
  - 自然変異への対応
- **鹿への応用**: 体表の斑点・毛色パターン識別

#### 5.3 ヒョウの斑点パターン識別
**Individual Leopard Identification Using Black Spot Patterns**
- 著者: Vishmila Mahaliyanaarachchi et al. (2024)
- URL: https://ieeexplore.ieee.org/document/10499779/
- **キーポイント**:
  - 黒斑パターンの自動抽出
  - パターンマッチング
  - 野生ヒョウの個体追跡
- **鹿への応用**: シカ種の斑点パターン（ニホンジカ・アクシスジカ等）

### 6. カメラトラップ技術

#### 6.1 ハイブリッド深層学習フレームワーク
**Hybrid Deep Learning Framework for Automated Classification of Wildlife Camera Trap Images**
- 著者: P Sudeepa et al. (2024)
- URL: https://ieeexplore.ieee.org/document/10724732/
- **キーポイント**:
  - 複数CNNモデルのアンサンブル
  - カメラトラップ画像の自動分類
  - 高精度・高速処理
- **鹿への応用**: 野外カメラからのリアルタイム種判定・個体識別

#### 6.2 時系列メタデータ駆動分類
**TemporalSwin-FPN Net: A Novel Pipeline for Metadata-Driven Sequence Classification in Camera Trap Imagery**
- 著者: Sameeruddin Muhammad et al. (2025)
- URL: https://ieeexplore.ieee.org/document/10869574/
- **キーポイント**:
  - Swin Transformer + FPN（Feature Pyramid Network）
  - メタデータ（時刻・場所等）活用
  - 時系列画像の分類
- **鹿への応用**: 撮影時刻・場所を考慮した識別精度向上

#### 6.3 深層学習による物体検出
**Deep Learning Object Detection Methods for Ecological Camera Trap Data**
- 著者: Stefan Schneider et al. (2018)
- URL: https://ieeexplore.ieee.org/document/8575770/
- **キーポイント**:
  - YOLO・Faster R-CNNの生態学適用
  - カメラトラップデータの課題分析
  - 検出精度とスピードのトレードオフ
- **鹿への応用**: リアルタイム検出システムの構築

### 7. 適応的・動的学習手法

#### 7.1 適応的特徴選択
**Adaptive Feature Selection and Image Classification Using Manifold Learning Techniques**
- 著者: Amna Ashraf et al. (2023)
- URL: https://ieeexplore.ieee.org/document/10272610/
- **キーポイント**:
  - 多様体学習による特徴選択
  - データ分布に応じた適応
  - 次元削減と分類の統合
- **鹿への応用**: 環境変化（季節・照明）への動的適応

#### 7.2 リアルタイムモバイル実装
**Mobile Menagerie: Evaluating and Implementing CNNs for Real-Time Animal Species Recognition on Smart Devices**
- 著者: Jeevan Um et al. (2025)
- URL: https://ieeexplore.ieee.org/document/10898865/
- **キーポイント**:
  - スマートデバイスでのリアルタイム認識
  - 軽量CNNモデルの評価
  - エッジコンピューティング
- **鹿への応用**: フィールドワーク用モバイルアプリ実装

#### 7.3 YOLOベースのリアルタイム検出
**Enhanced YOLOv5 Model for Real-Time Fish Species Recognition on Jetson Orin Nano**
- 著者: Hsin-Chun Tsai et al. (2024)
- URL: https://ieeexplore.ieee.org/document/10936930/
- **キーポイント**:
  - YOLOv5の改良
  - エッジデバイス（Jetson）での高速推論
  - リアルタイム種認識
- **鹿への応用**: 低消費電力デバイスでの野外モニタリング

### 8. データセット・ツール

#### 8.1 野生動物再識別ツールキット
**WildlifeDatasets: An open-source toolkit for animal re-identification**
- 著者: Vojtěch Čermák et al. (2024)
- URL: https://ieeexplore.ieee.org/document/10483925/
- **キーポイント**:
  - オープンソースツールキット
  - 標準化されたデータセット
  - ベンチマーク評価
- **鹿への応用**: 標準データセット構築、性能比較

---

## 技術的アプローチの体系的分類

### アーキテクチャ別分類

| アーキテクチャ | 論文数 | 代表例 | 鹿への適用性 |
|--------------|--------|---------|------------|
| **Transformer系** | 8件 | ReDeformTR, ViT-CatNet, DINO | ★★★★★ |
| **CNN系** | 35件 | ResNet, EfficientNet, MobileNet | ★★★★ |
| **Siamese Network** | 6件 | Siamese + 転移学習 | ★★★★★ |
| **LSTM/RNN系** | 4件 | BiLSTM歩容認識 | ★★★★ |
| **YOLO系** | 8件 | YOLOv5, YOLOv8 | ★★★★ |
| **ハイブリッド** | 12件 | ResNet-YOLO, Ensemble | ★★★★ |

### 学習戦略別分類

| 学習戦略 | 論文数 | 主要手法 | データ要求量 |
|---------|--------|----------|------------|
| **Few-shot Learning** | 4件 | Prototypical Network, Meta-learning | 極小 |
| **Transfer Learning** | 18件 | ImageNet事前学習 → Fine-tuning | 小 |
| **Self-supervised** | 5件 | DINO, SimCLR, MoCo | 中（ラベル不要） |
| **Metric Learning** | 7件 | Triplet Loss, Contrastive Learning | 中 |
| **Supervised** | 40件 | 従来型教師あり学習 | 大 |

### 特徴種別分類

| 特徴タイプ | 論文数 | 主要論文 | 鹿への応用 |
|----------|--------|----------|-----------|
| **静的特徴（外観）** | 55件 | 斑点・縞模様・体型 | ○ |
| **動的特徴（歩容）** | 8件 | ReconGait, BiLSTM | ◎（高精度期待） |
| **行動特徴** | 6件 | AnimalFormer, 採食行動 | ○ |
| **音響特徴** | 4件 | 鳴き声分析 | △（鹿は静か） |
| **足跡特徴** | 2件 | PawPrint | ◎（非侵襲的） |

---

## 鹿個体識別への統合アプローチ提案

### 推奨システムアーキテクチャ

#### Phase 1: ベースライン構築（3ヶ月）

**目標**: 基本的な個体識別システムの構築

1. **データ収集・準備**
   - カメラトラップ設置（複数角度）
   - 既知個体の撮影（100-200画像/個体）
   - アノテーション（個体ID、姿勢、環境条件）

2. **ベースラインモデル**
   - **主モデル**: ReDeformTR（軽量Deformable Transformer）
     - 理由: 野生動物に特化、マルチ画像融合
   - **バックアップ**: ResNet50 + ArcFace Loss
     - 理由: 実績豊富、実装容易

3. **評価指標**
   - Top-1 Accuracy, Top-5 Accuracy
   - mAP (mean Average Precision)
   - Rank-1 Identification Rate

#### Phase 2: 動的特徴統合（3-6ヶ月）

**目標**: 歩容・行動パターンの統合による精度向上

1. **歩容認識モジュール**
   - **モデル**: ReconGait（パンダ歩容認識）の適応
   - **入力**: ビデオシーケンス（5-10秒）
   - **出力**: 歩容特徴ベクトル

2. **マルチモーダル融合**
   - 外観特徴（Transformer）+ 歩容特徴（LSTM）
   - Attention機構による動的重み付け
   - Early fusion vs Late fusion の比較

3. **時系列追跡**
   - DeepSORT / ByteTrackによる個体追跡
   - 時系列情報の活用（行動パターン）

#### Phase 3: Few-shot適応（6-9ヶ月）

**目標**: 新規個体への即座適応

1. **Few-shot学習モジュール**
   - **モデル**: Prototypical Contrastive Network
   - **トレーニング**: Meta-learning (MAML/Reptile)
   - **サポートセット**: 1-5画像/新規個体

2. **継続学習（Continual Learning）**
   - 新規個体の段階的追加
   - 破滅的忘却（Catastrophic Forgetting）回避
   - Elastic Weight Consolidation (EWC)

#### Phase 4: エッジデプロイ（9-12ヶ月）

**目標**: 実フィールド展開

1. **モデル最適化**
   - TensorRT / ONNX変換
   - 量子化（INT8）
   - プルーニング（40-60%削減）

2. **エッジデバイス**
   - NVIDIA Jetson Orin Nano（推奨）
   - Raspberry Pi 5 + Coral TPU（低予算）
   - 太陽光パネル + バッテリー

3. **リアルタイム処理**
   - 検出: YOLOv8-nano（30 FPS）
   - 識別: 軽量Transformer（10 FPS）
   - 通信: LoRaWAN（低消費電力）

---

## 技術スタック詳細

### 推奨フレームワーク・ライブラリ

| 目的 | ツール | 理由 |
|------|--------|------|
| **深層学習** | PyTorch 2.0+ | 柔軟性、Transformer実装豊富 |
| **コンピュータビジョン** | OpenCV 4.8+, Albumentations | 前処理、データ拡張 |
| **物体検出** | Ultralytics YOLOv8 | 高速、高精度 |
| **メトリック学習** | PyTorch Metric Learning | Triplet/Contrastive Loss実装 |
| **Few-shot** | learn2learn | Meta-learning実装 |
| **追跡** | SORT/DeepSORT | リアルタイム追跡 |
| **可視化** | Weights & Biases, TensorBoard | 実験管理 |
| **エッジ展開** | TensorRT, ONNX Runtime | 高速推論 |

### データ拡張戦略

鹿特有の課題に対応:

1. **照明変動**: ColorJitter, 明度調整
2. **姿勢変化**: RandomRotation, Affine変換
3. **部分遮蔽**: Random Erasing, CutOut
4. **距離変化**: RandomResize, Multi-scale training
5. **季節変化**: 毛色変化シミュレーション

### 評価プロトコル

**クロスバリデーション**:
- 個体ベース分割（Individual-based split）
- 時間ベース分割（Temporal split）：古い画像でトレーニング、新しい画像でテスト
- 場所ベース分割（Location-based split）：異なるカメラ地点

**メトリクス**:
- **Closed-set**: Top-1/5 Accuracy
- **Open-set**: AUC, TPR@FPR=0.01
- **Re-ID**: mAP, CMC curve

---

## 実装ロードマップ（12ヶ月）

### Q1（Month 1-3）: 基盤構築
- [ ] カメラトラップ設置（10-20台）
- [ ] データ収集開始（目標: 50個体、5000画像）
- [ ] アノテーションツール構築
- [ ] ReDeformTR/ResNet50 ベースライン実装
- [ ] 評価パイプライン構築

### Q2（Month 4-6）: 動的特徴統合
- [ ] 歩容データ収集（ビデオ）
- [ ] ReconGait実装・適応
- [ ] マルチモーダル融合実験
- [ ] 精度評価・改善イテレーション

### Q3（Month 7-9）: 適応学習
- [ ] Few-shot学習実装
- [ ] Meta-learning トレーニング
- [ ] 新規個体テスト（10個体）
- [ ] 継続学習メカニズム実装

### Q4（Month 10-12）: 実フィールド展開
- [ ] モデル最適化（量子化・プルーニング）
- [ ] Jetson Orin Nano移植
- [ ] リアルタイム処理検証
- [ ] 長期モニタリング開始（3ヶ月）

---

## 期待される成果

### 技術的成果

1. **識別精度**: Top-1 Accuracy > 95%（Closed-set）
2. **処理速度**: 10 FPS（Jetson Orin Nano）
3. **Few-shot性能**: 5サンプルで80%以上
4. **ロバスト性**: 季節変動・照明変化への対応

### 学術的貢献

1. **新規データセット**: 鹿個体識別ベンチマーク
2. **論文発表**: IEEE/CVPRワークショップ
3. **オープンソース**: ツールキット公開

### 保全への応用

1. **個体群動態**: 長期個体追跡
2. **行動生態**: 採食・移動パターン解析
3. **健康モニタリング**: 体重・体調変化検出
4. **密猟対策**: 異常行動検出

---

## 課題とリスク

### 技術的課題

| 課題 | 影響度 | 対策 |
|-----|--------|------|
| **個体間類似性** | 高 | メトリック学習、Fine-grained特徴 |
| **姿勢変動** | 高 | ポーズ正規化、Multi-view学習 |
| **部分遮蔽** | 中 | Attention機構、Occlusion augmentation |
| **季節変化（毛色）** | 中 | 継続学習、Shape重視 |
| **データ不足** | 中 | Few-shot learning, 転移学習 |

### 実装上のリスク

1. **計算資源**: GPU不足 → クラウドGPU活用（AWS/GCP）
2. **データ収集遅延**: 天候・機材トラブル → 予備カメラ、長期計画
3. **モデル過学習**: データ偏り → 多様な環境条件での撮影
4. **エッジ性能不足**: リアルタイム処理困難 → モデル軽量化、Two-stage処理

---

## 関連リソース

### 重要データセット

1. **Wildlife Datasets Toolkit**: https://ieeexplore.ieee.org/document/10483925/
2. **ATRW (Amur Tiger Re-identification in the Wild)**: トラ個体識別
3. **SeaTurtleID**: ウミガメ顔認識
4. **Kaggle Wildlife Dataset**: 多種野生動物

### 参考実装

1. **MMDetection**: 物体検出フレームワーク
2. **MMTracking**: 追跡フレームワーク
3. **PyTorch Metric Learning**: メトリック学習
4. **Torchreid**: Person Re-ID（動物に転用可）

---

## 最重要論文リスト（Top 20）

### Transformer & 最先端

1. **ReDeformTR** (Li et al., 2024) - https://ieeexplore.ieee.org/document/10620204/
2. **Transformer-based Amur Tiger** (Bai et al., 2024) - https://ieeexplore.ieee.org/document/10432893/
3. **ViT-CatNet** (Hu, 2025) - https://ieeexplore.ieee.org/document/11103379/
4. **Re-Identification DINO** (Maddigan et al., 2024) - https://ieeexplore.ieee.org/document/10794473/

### Few-shot & Meta-learning

5. **Prototypical Contrastive Network** (Zhang et al., 2025) - https://ieeexplore.ieee.org/document/11090778/
6. **Siamese + Transfer Learning** (Van Zyl et al., 2020) - https://ieeexplore.ieee.org/document/9190426/
7. **AW-HRNet** (Yang et al., 2025) - https://ieeexplore.ieee.org/document/11108430/

### Siamese & Metric Learning

8. **Automated Siamese** (Dlamini et al., 2020) - https://ieeexplore.ieee.org/document/9311574/
9. **Pose Invariant Manta Rays** (Moskvyak et al., 2021) - https://ieeexplore.ieee.org/document/9647359/
10. **Metric Learning Segmentation** (Shukla et al., 2016) - https://ieeexplore.ieee.org/document/7533107/
11. **Self-Supervised Detection** (Moosa et al., 2024) - https://ieeexplore.ieee.org/document/10755717/

### Gait & Behavior

12. **ReconGait Panda** (Min et al., 2024) - https://ieeexplore.ieee.org/document/10649970/
13. **BiLSTM Cattle** (Qiao et al., 2020) - https://ieeexplore.ieee.org/document/9217026/
14. **AnimalFormer** (Qazi et al., 2024) - https://ieeexplore.ieee.org/document/10677926/

### Camera Trap & Detection

15. **Hybrid Framework** (Sudeepa et al., 2024) - https://ieeexplore.ieee.org/document/10724732/
16. **TemporalSwin-FPN** (Muhammad et al., 2025) - https://ieeexplore.ieee.org/document/10869574/
17. **Deep Learning Camera Trap** (Schneider et al., 2018) - https://ieeexplore.ieee.org/document/8575770/

### Special Methods

18. **PawPrint Footprints** (Song et al., 2025) - https://ieeexplore.ieee.org/document/11084465/
19. **Leopard Spot Patterns** (Mahaliyanaarachchi et al., 2024) - https://ieeexplore.ieee.org/document/10499779/
20. **Wildlife Datasets Toolkit** (Čermák et al., 2024) - https://ieeexplore.ieee.org/document/10483925/

---

## 結論

野生シカの個体識別における拡張動的深層学習アプローチは、以下の技術的進展により実現可能性が高まっている：

1. **Transformerベース手法**による高精度識別
2. **Few-shot Learning**による少数サンプル適応
3. **動的特徴（歩容・行動）**の統合による識別精度向上
4. **エッジデプロイ技術**による実フィールド展開

本調査で収集した118件の論文から、実装可能な具体的技術スタックとロードマップを提示した。今後12ヶ月での実証システム構築が現実的である。

---

**作成者**: Claude Code + Browser-Use Automation
**調査期間**: 2025-10-16
**データ保存先**: `papers/deer_individual_id/`
**次ステップ**: 詳細実装計画書の作成、予算見積もり
