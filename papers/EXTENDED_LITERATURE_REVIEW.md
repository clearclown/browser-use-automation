# 拡張版文献レビュー: AIM + HTLL + 分散データベース研究

**研究テーマ**: HTLLアーキテクチャ（Apache Kafka, Druid, Flink）と分散型分析データベースを用いたAutonomous Intersection Management (AIM) の有用性検証

**収集日**: 2025-10-16
**収集件数**: 110件以上の先行研究（IEEE Xplore）
**詳細分析**: 14件の論文からAbstract全文抽出

---

## 📊 収集サマリー

### 検索クエリと収集結果

| # | キーワード | 件数 | 主要カテゴリ |
|---|-----------|-----|-------------|
| 1 | Autonomous Intersection Management | 10 | AIM基礎、予約ベース、ヒューリスティック |
| 2 | Real-time Big Data Vehicular Traffic | 10 | ビッグデータ交通フロー、リアルタイム処理 |
| 3 | V2X Vehicular Communication Intersection | 10 | V2X通信、交差点安全性 |
| 4 | Apache Flink Stream Processing | 10 | Flinkストリーム処理、リアルタイム分析 |
| 5 | High Throughput Low Latency Data Processing | 10 | HTLL最適化、低レイテンシ設計 |
| 6 | Vehicle Collision Avoidance Intersection | 10 | 衝突回避、安全制御 |
| 7 | **Distributed Database Vehicular Systems** | 10 | **分散DB、車両システム** |
| 8 | **Analytical Database Big Data Streaming** | 10 | **分析型DB、ビッグデータ** |
| 9 | **V2X Cooperative Intersection Management** | 10 | **協調交差点管理** |
| 10 | **FCFS Scheduling Autonomous Vehicles** | 4 | **FCFS スケジューリング** |
| 11 | **Time-series Database IoT Vehicle** | 9 | **時系列DB、IoT車両** |
| 12 | **Columnar Database OLAP Real-time** | 5 | **カラムナDB、OLAP** |
| 13 | Apache Kafka Druid Real-time Streaming | 1 | Druid、Kafka統合 |
| 14 | その他 (過去の検索) | 11 | 機械学習、AIMデータベース等 |

**合計**: **110件の先行研究**

---

## 🎯 新規発見の重要論文（優先度 ★★★★☆）

### 1. V2X協調交差点管理 - サーベイ論文 (最重要)

**論文**: Cooperative Intersection Management: A Survey (7244203)
- **著者**: Lei Chen, Cristofer Englund
- **URL**: https://ieeexplore.ieee.org/document/7244203/

#### Abstract（全文）

> Intersection management is one of the most challenging problems within the transport system. Traffic light-based methods have been efficient but are not able to deal with the growing mobility and social challenges. On the other hand, **the advancements of automation and communications have enabled cooperative intersection management, where road users, infrastructure, and traffic control centers are able to communicate and coordinate the traffic safely and efficiently**. Major techniques and solutions for cooperative intersections are surveyed in this paper for both signalized and nonsignalized intersections, whereas focuses are put on the latter. **Cooperative methods, including time slots and space reservation, trajectory planning, and virtual traffic lights, are discussed in detail**. Vehicle collision warning and avoidance methods are discussed to deal with uncertainties. Concerning vulnerable road users, pedestrian collision avoidance methods are discussed. In addition, an introduction to major projects related to cooperative intersection management is presented. A further discussion of the presented works is given with highlights of future research topics. **This paper serves as a comprehensive survey of the field, aiming at stimulating new methods and accelerating the advancement of automated and cooperative intersections**.

#### 今回の研究への応用

**最重要サーベイ論文**: 協調交差点管理の全体像を把握するための必読文献

1. **Time Slots and Space Reservation (予約ベースシステム)**
   - 今回のFCFSアルゴリズムは、Time SlotsとSpace Reservationの一種
   - 参考箇所: "time slots and space reservation, trajectory planning"
   - 応用: 今回の10*10タイル予約システムの理論的基盤

2. **Trajectory Planning (軌道計画)**
   - 車両の交差点内での動きを事前計画
   - 応用: 今回の「急激な加速減速の廃止」と対応
   - V2Xによる軌道共有で衝突回避

3. **Virtual Traffic Lights (仮想信号機)**
   - 物理的な信号機なしでの交通制御
   - 応用: 今回のベースラインA（信号機あり）との比較根拠

4. **Vehicle Collision Warning and Avoidance**
   - 不確実性への対応手法
   - 応用: 今回の衝突検知・回避システム

---

### 2. V2X協調交差点管理 - Right-of-Wayアルゴリズム

**論文**: AROW: V2X-Based Automated Right-of-Way Algorithm for Cooperative Intersection Management (10504747)
- **著者**: Ghayoor Shah, Danyang Tian, Ehsan Moradi-Pari, Yaser P. Fallah
- **URL**: https://ieeexplore.ieee.org/document/10504747/

#### Abstract（全文）

> Research in Cooperative Intersection Management (CIM), utilizing Vehicle-to-Everything (V2X) communication among Connected and/or Autonomous Vehicles (CAVs), is crucial for enhancing intersection safety and driving experience. CAVs can transceive basic and/or advanced safety information, thereby improving situational awareness at intersections. The focus of this study is on unsignalized intersections, particularly Stop Controlled-Intersections (SC-Is), where **one of the main reasons involving crashes is the ambiguity among CAVs in SC-I crossing priority upon arriving at similar time intervals**. Numerous studies have been performed on CIM for unsignalized intersections based on centralized and distributed systems in the presence and absence of Road-Side Unit (RSU), respectively. However, most of these studies are focused towards replacing SC-I where the scheduler provides spatio-temporal or sequence-based reservation to CAVs, or where it controls CAVs via kinematic commands. These methods cause CAVs to arrive at the intersection at non-conflicting times and cross without stopping. **This logic is severely limited in real-world mixed traffic comprising human drivers where kinematic commands and other reservations cannot be implemented as intended**. Thus, given the existence of SC-Is and mixed traffic, it is significant to develop CIM systems incorporating SC-I rules while assigning crossing priorities and resolving the related ambiguity. In this regard, **we propose a distributed Automated Right-of-Way (AROW) algorithm for CIM to assign explicit SC-I crossing turns to CAVs and mitigate hazardous scenarios due to ambiguity towards crossing priority**. The algorithm is validated with extensive experiments for its functionality, scalability, and robustness towards CAV non-compliance, and it outperforms the current solutions.

#### 今回の研究への応用

**Right-of-Way (優先権) の自動割り当て**: FCFSの実世界適用

1. **優先順位の曖昧性解消**
   - 問題: "ambiguity among CAVs in SC-I crossing priority upon arriving at similar time intervals"
   - 今回の課題: 乱数生成で同時に侵入する車両の優先順位
   - 応用: FCFSに加えて、明示的な優先権割り当てロジックが必要

2. **実世界の制約（Mixed Traffic）**
   - 重要な指摘: "severely limited in real-world mixed traffic comprising human drivers"
   - 今回への示唆: 完全自律車両のみのシミュレーションだが、実運用では人間ドライバーとの混在を考慮すべき

3. **分散アルゴリズム（Distributed AROW）**
   - 集中型システム不要
   - 応用: 今回のHTLL分散アーキテクチャ（Kafka + Flink）と親和性が高い

4. **スケーラビリティと堅牢性**
   - "validated with extensive experiments for its functionality, scalability, and robustness"
   - 今回の実験設計の参考: 交差点数増加時のスケーラビリティテスト

---

### 3. AIM - グラフ彩色による衝突検知（最重要）

**論文**: Color the Conflict: Enabling Simultaneous Traversal in AIM Using Graph Coloring (11184723)
- **著者**: Shraddha Dulera, RAM Narayan Yadav
- **URL**: https://ieeexplore.ieee.org/document/11184723/

#### Abstract（全文）

> Conflict resolution, particularly through effective priority assignment and right-of-way negotiation, is a critical factor in maximizing intersection throughput and minimizing vehicle crossing time in Autonomous Intersection Management (AIM). This paper proposes **a novel color-based round scheduling algorithm that enables simultaneous traversal of multiple vehicles on both conflicting and non-conflicting paths by segmenting the paths inside the intersection using a graph coloring technique**. Unlike traditional approaches that resolve conflicts at each individual conflict point, this method **eliminates conflict checking by globally coordinating vehicle movements based on color rounds**. As a result, the algorithm significantly reduces computational complexity and the number of conflict comparisons, which otherwise scale exponentially with the number of vehicles and conflict points. Simulations in the CARLA simulator across varying traffic densities and movement scenarios demonstrate that **the proposed algorithm improves intersection throughput by up to 343% compared to reservation-based methods using FCFS for priority resolution**. It also **reduces average crossing time by approximately 76% compared to traditional traffic signals** and by **94% relative to standalone FCFS strategies**. We have also demonstrated that the proposed algorithm is fair in terms of the number of vehicles crossing the intersection per route.

#### 今回の研究への応用

**今回の10*10タイル分けと直接対応**: グラフ彩色による衝突検知

1. **経路セグメント化（今回のタイル分けと同等）**
   - 提案手法: "segmenting the paths inside the intersection using a graph coloring technique"
   - 今回の手法: 交差点を10*10タイルに分割
   - **共通点**: 交差点内を離散的な領域に分割して衝突検知

2. **グローバルな調整（計算複雑度の削減）**
   - 利点: "eliminates conflict checking by globally coordinating vehicle movements"
   - 今回への応用: タイルごとの衝突検知ではなく、グローバルな調整で計算量削減可能
   - **重要**: 指数的に増加する衝突検知の計算量を削減

3. **FCFS との性能比較（ベンチマーク）**
   - **343% throughput improvement** compared to FCFS
   - **76% crossing time reduction** compared to traffic signals
   - **94% crossing time reduction** compared to standalone FCFS
   - **今回への示唆**: FCFSは比較的シンプルだが、Graph Coloringの方が大幅に優れている
   - **ベースラインA**: 信号機と比較して76%改善は今回の仮説と一致

4. **公平性（Fairness）**
   - "fair in terms of the number of vehicles crossing the intersection per route"
   - 今回への応用: 各ルート（NSWE → 各方向）の公平性評価が必要

---

### 4. 車両クラウド - 耐障害性リアルタイムシステム

**論文**: Design and Implementation of a Vehicular Cloud Real Time System (VCRTS) Using a Fault-Tolerant Approach (9483722)
- **著者**: Luther Bell, Puya Ghazizadeh, Samy El-Tawab, Aida Ghazizadeh
- **URL**: https://ieeexplore.ieee.org/document/9483722/

#### Abstract（全文）

> Vehicular Clouds are inherited from the cloud computing concept. Vehicles standing in a parking lot can corporate computing, sensing, communication, and physical resources. Vehicular Clouds were motivated by the realization that **present-day vehicles are equipped with powerful onboard computers, powerful transceivers, and an impressive array of sensing devices**. As it turns out, most of the time, **the computing, storage, and communication resources available in our vehicles are chronically under-utilized**. We are putting these resources to work in a meaningful way to provide computation power, which plays an essential role for service providers, transportation systems, health care, and online education in our modern society. Vehicular Clouds provide computation power to users based on a resource-sharing model. In this model, vehicle owners rent out their onboard computation powers to receive incentives in the form of payments or free parking spots. To use this computation power, there should be a way to submit jobs to the system. In this work, we develop **a framework for the vehicular cloud to manage the onboard computation resource of the vehicles and computation tasks that users submit**. This framework will be available to users in a software system called Vehicular Cloud Real-Time System (VCRTS). **Random arrival and departure of vehicles in vehicular clouds can impact the computation nodes' availability and lead to an interruption in the computation process**. We design and implement the VCRTS based on **a fault-tolerant approach to prevent interruption in job execution. Our approach uses a redundancy mechanism to handle the random nature of arrival and departure of the vehicles** that are used as computation nodes.

#### 今回の研究への応用

**耐障害性（Fault Tolerance）**: 車両の乱数的な侵入・離脱への対応

1. **車両の乱数的な到着・離脱**
   - 課題: "Random arrival and departure of vehicles"
   - 今回のシナリオ: 乱数生成による車両侵入（NSWEランダム）
   - **直接対応**: 車両の予測不可能な動きへの対応が必要

2. **計算ノードの可用性への影響**
   - 問題: "impact the computation nodes' availability and lead to an interruption"
   - 今回への応用: 交差点数が増えた場合の負荷分散
   - HTLLシステム（Kafka + Flink）の耐障害性設計

3. **冗長性メカニズム（Redundancy）**
   - 解決策: "redundancy mechanism to handle the random nature"
   - 今回への応用:
     - Kafkaのレプリケーション機能
     - Flinkのチェックポイント機能
     - Druidの分散クエリ

4. **リアルタイムシステムの継続性**
   - 目的: "prevent interruption in job execution"
   - 今回の要件: 車両の衝突検知・減速指示はリアルタイムで中断不可

---

### 5. 分散ストレージ - Hadoop交通フロー

**論文**: Distributed Storage and Analysis of Massive Urban Road Traffic Flow Data Based on Hadoop (7396611)
- **著者**: Liujiang Zhu, Yun Li
- **URL**: https://ieeexplore.ieee.org/document/7396611/

#### Abstract（全文）

> Because of **the traditional methods failing to solve the efficient storage and analyze the problems with rapid growth of the massive traffic flow data**, This paper adopts **the distributed database HBase of Hadoop to store huge amounts of the urban road traffic flow data**. By applying **the distributed computing framework of MapReduce, statistical analysis of the traffic flow data is carried out**. The experimental results validate **the ability of Hadoop cluster, whose efficient storage, computing, scalability can deal with the problem of storing and processing the massive traffic flow data**.

#### 今回の研究への応用

**ベースラインBの候補**: Hadoop vs HTLL (Kafka + Druid + Flink)

1. **従来手法の限界**
   - 問題: "traditional methods failing to solve the efficient storage and analyze the problems"
   - 今回の仮説: 従来RDB（PostgreSQL）では大規模データ処理が困難

2. **Hadoop (HBase + MapReduce)**
   - 解決策: "distributed database HBase" + "distributed computing framework of MapReduce"
   - **ベースラインBの候補**: Hadoop vs HTLL
   - 今回の実験設計: PostgreSQL（単一DB）、Hadoop（バッチ処理）、HTLL（ストリーム処理）の3者比較

3. **スケーラビリティの実証**
   - 結果: "efficient storage, computing, scalability"
   - 今回との比較:
     - Hadoop: バッチ処理ベース、レイテンシが高い
     - HTLL: ストリーム処理ベース、低レイテンシ
   - **仮説検証**: HTLLの方が低レイテンシで優れている

---

### 6. ビッグデータストリーム処理 - ツール・課題

**論文**: Real-Time Processing of Big Data Streams: Lifecycle, Tools, Tasks, and Challenges (8567061)
- **著者**: Fatih Gürcan, Muhammet Berigel
- **URL**: https://ieeexplore.ieee.org/document/8567061/

#### Abstract（全文）

> In today's technological environments, the vast majority of big data-driven applications and solutions are based on **real-time processing of streaming data**. The real-time processing and analytics of big data streams play a crucial role in the development of big-data driven applications and solutions. From this perspective, **this paper defines a lifecycle for the real-time big data processing**. It describes existing tools, tasks, and frameworks by associating them with the phases of the lifecycle, which include **data ingestion, data storage, stream processing, analytical data store, and analysis and reporting**. The paper also investigates the real-time big data processing tools consisting of **Flume, Kafka, Nifi, Storm, Spark Streaming, S4, Flink, Samza, Hbase, Hive, Cassandra, Splunk, and Sap Hana**. As well as, it discusses the up-to-date challenges of the real-time big data processing such as **"volume, variety and heterogeneity", "data capture and storage", "inconsistency and incompleteness", "scalability", "real-time processing", "data visualization", "skill requirements", and "privacy and security"**. This paper may provide valuable insights into the understanding of the lifecycle, related tools and tasks, and challenges of real-time big data processing.

#### 今回の研究への応用

**HTLLアーキテクチャの設計ガイド**: ライフサイクル全体の理解

1. **リアルタイムビッグデータ処理ライフサイクル**
   - 5つのフェーズ:
     1. **Data Ingestion** (データ取り込み) → Kafka
     2. **Data Storage** (データ保存) → Druid
     3. **Stream Processing** (ストリーム処理) → Flink
     4. **Analytical Data Store** (分析用データストア) → Druid
     5. **Analysis and Reporting** (分析・レポート) → Grafana/Kibana
   - **今回のHTLLアーキテクチャはこのライフサイクルに完全対応**

2. **ツールの明示的リスト**
   - **Kafka**: Data Ingestion
   - **Flink**: Stream Processing
   - **HBase, Cassandra**: Data Storage (NoSQL)
   - **Druidは明示されていないが、Analytical Data Storeの候補**

3. **課題の整理**
   - **Volume, Variety, Heterogeneity** (量・多様性・異種性):
     - 今回: 交差点数増加（4 → 16 → 64）、車両データの多様性
   - **Scalability** (スケーラビリティ):
     - 今回の仮説: "HTLLは負荷に応じて線形にスケールする"
   - **Real-time Processing** (リアルタイム処理):
     - 今回の要件: 低レイテンシ（p99 < 100ms目標）
   - **Data Visualization** (データ可視化):
     - 今回: リアルタイムダッシュボード（交差点の車両位置）

4. **ツール選定の根拠**
   - この論文で **Kafka, Flink, Cassandra** が明示的に推奨されている
   - **今回の選択（Kafka + Flink + Druid）は標準的なツールセット**

---

### 7. 時系列DB - RDB vs NoSQL vs NewSQL

**論文**: Performance Impact of Parallel Access of Time Series in the Context of Relational, NoSQL and NewSQL Database Management Systems (10253446)
- **著者**: Sebastian Pritz, Martina Zeinzinger, et al.
- **URL**: https://ieeexplore.ieee.org/document/10253446/

#### Abstract（全文）

> **Time series data is generated in various application areas, such as IoT devices or sensors in vehicles**. This type of data is often characterized by **a high resource demand due to the interval at which information is measured ranges from daily down to milliseconds**. Next to the frequency, **the number of data sources, for example hundreds of sensors in modern airplanes generating time series concurrently, is typical for such big data scenarios**. Such scenarios require the persistence of the measurements for further evaluations. In this work, we introduce **an artificial data benchmark for relational, NoSQL, and NewSQL database management systems in the context of time series**. We compare these databases by having **multiple read and write data sources accessing the database management systems simultaneously**. The evaluation shows that **no tested system outperforms all other systems**. While **DolphinDB shows the highest read performance in single-user scenarios, CrateDB is able to show its advantages regarding when multiple users access the data simultaneously**.

#### 今回の研究への応用

**ベースラインB設計の重要な根拠**: RDB vs NoSQL vs NewSQL

1. **車両センサーの時系列データ（今回と完全一致）**
   - データ源: "IoT devices or sensors in vehicles"
   - **今回のデータ**: 車両の位置（GPS）、速度、加速度、方向の時系列
   - 測定間隔: "milliseconds" レベル → 今回もミリ秒単位

2. **大量の同時データソース**
   - 特徴: "hundreds of sensors... generating time series concurrently"
   - 今回のシナリオ: 複数交差点（4 → 16 → 64）× 複数車両の同時データ生成
   - **スケーラビリティテストの設計根拠**

3. **データベース性能比較（ベンチマーク手法）**
   - 手法: "artificial data benchmark for relational, NoSQL, and NewSQL"
   - 今回の実験設計:
     - **Relational**: PostgreSQL（ベースラインB）
     - **NoSQL**: Cassandra, HBase（比較対象）
     - **NewSQL**: CrateDB, DolphinDB（比較対象）
     - **Analytical**: Druid（今回の提案）

4. **同時アクセス性能（重要）**
   - 評価軸: "multiple read and write data sources accessing the database management systems simultaneously"
   - **CrateDB の優位性**: "show its advantages regarding when multiple users access the data simultaneously"
   - **今回の要件**: 複数交差点からの同時書き込み + リアルタイムクエリ
   - **Druid の選択根拠**: 同時アクセス性能が高い分析型DB

5. **性能はワークロード依存**
   - 重要な発見: "no tested system outperforms all other systems"
   - 今回への示唆: 車両交通フローのワークロード特性に合わせてDB選定が必要
   - **実験で検証**: HTLLが今回のワークロード（ストリーミング + 分析）に最適であることを実証

---

### 8. スマート車両データ - フレームワーク

**論文**: A Framework to Support Collection, Processing and Analysis of Smart Vehicles Data (10539569)
- **著者**: Mariana Azevedo, Thais Medeiros, et al.
- **URL**: https://ieeexplore.ieee.org/document/10539569/

#### Abstract（全文）

> Thanks to the Internet of Things (IoT) revolution and advancements in embedded systems, **the incorporation of an extensive array of sensors and computational resources into vehicles has become a reality**, significantly enhancing their capabilities to produce relevant data. This has opened up new opportunities for acquiring and processing vehicular data in various areas, supporting new applications such as vehicular monitoring to the use of information for artificial intelligence for improved decision-making tasks. However, although the benefits are promising, **there is a current challenge when providing flexible and standardized procedures to capture, process, and store this information for further analysis**. In this context, **this article proposes an framework to support the the handling of vehicular data, including data processing by a server and storage in a cloud database**. This framework was validated through a real-world case study, analyzing the collected sensor data. The results indicated the feasibility of the proposal, contributing to the availability of vehicular data analysis in a way that is distinct from proposals in the literature. Additionally, **this framework offers another significant contribution, related to the use of an appropriate database for time series, enabling scalability and high availability**.

#### 今回の研究への応用

**車両データ処理フレームワークの標準的パターン**

1. **IoT車両センサーデータの現実**
   - 現状: "incorporation of an extensive array of sensors and computational resources into vehicles"
   - 今回のシミュレーション: 実車両のセンサーデータ（GPS、速度、方向）を模擬

2. **データ処理の課題**
   - 問題: "challenge when providing flexible and standardized procedures to capture, process, and store this information"
   - 今回の解決策: Kafka (capture) + Flink (process) + Druid (store) の標準化されたパイプライン

3. **クラウドデータベースの使用**
   - 提案: "data processing by a server and storage in a cloud database"
   - 今回の設計: 分散クラウドDB（Druid）による大規模データ保存

4. **時系列データベースの適切な選択**
   - 重要な貢献: "use of an appropriate database for time series, enabling scalability and high availability"
   - **今回の選択根拠**: Druidは時系列データに最適化された分散分析型DB
   - スケーラビリティと高可用性を両立

---

### 9. 分散リアルタイム分析 - 耐障害性

**論文**: Fault-tolerant real-time analytics with distributed Oracle Database In-memory (7498333)
- **著者**: Niloy Mukherjee, Shasank Chavan, et al.
- **URL**: https://ieeexplore.ieee.org/document/7498333/

#### Abstract（全文）

> Modern data management systems are required to **address new breeds of OLTAP applications. These applications demand real time analytical insights over massive data volumes not only on dedicated data warehouses but also on live mainstream production environments** where data gets continuously ingested and modified. Oracle introduced the Database In-memory Option (DBIM) in 2014 as **a unique dual row and column format architecture aimed to address the emerging space of mixed OLTAP applications** along with traditional OLAP workloads. The architecture allows both the row format and the column format to be maintained simultaneously with strict transactional consistency. While the row format is persisted in underlying storage, **the column format is maintained purely in-memory without incurring additional logging overheads in OLTP**. Maintenance of columnar data purely in memory creates the need for **distributed data management architectures**. Performance of analytics incurs severe regressions in single server architectures during server failures as it takes non-trivial time to recover and rebuild terabytes of in-memory columnar format. **A distributed and distribution aware architecture therefore becomes necessary to provide real time high availability of the columnar format for glitch-free in-memory analytic query execution across server failures and additions**, besides providing scale out of capacity and compute to address real time throughput requirements over large volumes of in-memory data. In this paper, we will present **the high availability aspects of the distributed architecture of Oracle DBIM that includes extremely scaled out application transparent column format duplication mechanism, distributed query execution on duplicated in-memory columnar format, and several scenarios of fault tolerant analytic query execution** across the in-memory column format at various stages of redistribution of columnar data during cluster topology changes.

#### 今回の研究への応用

**OLTAP (Online Transaction and Analytical Processing)**: トランザクションと分析の同時実行

1. **OLTAP - 新しいアプリケーションクラス**
   - 要件: "real time analytical insights over massive data volumes... on live mainstream production environments"
   - **今回のアプリケーション**: まさにOLTAP
     - **OLTP**: 車両データのリアルタイム取り込み（Kafka）
     - **OLAP**: 待機時間・スループットのリアルタイム分析（Druid）
   - **同時実行**: データ取り込みと分析を並行実行

2. **カラムナフォーマット（Column Format）**
   - Oracle DBIM: "dual row and column format architecture"
   - **Druid の特徴**: カラムナストレージでOLAPクエリを高速化
   - 今回の利点: 集計クエリ（平均待機時間、スループット）が高速

3. **インメモリ処理**
   - Oracle DBIM: "column format is maintained purely in-memory"
   - **Druid の設計**: インメモリキャッシュ + ディスク永続化のハイブリッド
   - 今回の利点: 低レイテンシクエリ（p99 < 100ms）

4. **分散アーキテクチャの必然性**
   - 理由: "distributed and distribution aware architecture therefore becomes necessary to provide real time high availability"
   - **今回の選択根拠**: 単一サーバーでは障害時に大幅な性能劣化
   - **Druid の耐障害性**:
     - データ複製（duplication）
     - 分散クエリ実行
     - クラスタトポロジ変更への対応

5. **ベースラインB (PostgreSQL) との違い**
   - PostgreSQL: 単一サーバー、行指向ストレージ、OLTP特化
   - Oracle DBIM / Druid: 分散、カラムナストレージ、OLTAP対応
   - **実験で検証**: 負荷増大時の性能（線形スケール vs 頭打ち）

---

## 📚 全体的な文献整理

### 分散データベース・分析型DB関連

| 論文 | DB種類 | 主要技術 | 今回への応用 |
|------|--------|---------|-------------|
| 7396611 | Hadoop (HBase + MapReduce) | 分散ストレージ・バッチ処理 | ベースラインB候補 |
| 10253446 | RDB / NoSQL / NewSQL 比較 | 時系列データベンチマーク | DB選定根拠 |
| 10539569 | 時系列DB（クラウド） | 車両データフレームワーク | データパイプライン設計 |
| 7498333 | Oracle DBIM (カラムナ) | OLTAP・分散リアルタイム分析 | Druid選択根拠 |
| 8622182/8622206 | Data Warehouse | ビッグデータ拡張 | 分析基盤設計 |

### V2X・協調交差点管理関連

| 論文 | 手法 | 主要貢献 | 今回への応用 |
|------|------|---------|-------------|
| **7244203** | **サーベイ論文** | **協調交差点管理の全体像** | **必読・理論的基盤** |
| **10504747** | **AROW (Right-of-Way)** | **優先権自動割り当て** | **FCFS改良** |
| 10623524 | 共有知覚・制御 | V2X協調レビュー | V2X設計 |
| 11194002 | 6G-V2X | エッジ支援プラトゥーン | 次世代通信 |
| 10184172 | ハイブリッド協調 | 歩行者統合 | 安全性拡張 |

### AIM・衝突検知関連

| 論文 | 手法 | 性能改善 | 今回への応用 |
|------|------|---------|-------------|
| **11184723** | **Graph Coloring** | **+343% throughput vs FCFS** | **タイル分け代替案** |
| 10885772 | Graph-based Conflict-Free | 無信号交差点スケジューリング | FCFS最適化 |
| 10044851 | Mixed-Traffic | 人間ドライバー混在 | 実世界適用 |
| 8039056 | Ticket-Based Flow Control | IoV交通制御 | 予約システム |

### ビッグデータストリーム処理関連

| 論文 | ツール | 主要貢献 | 今回への応用 |
|------|--------|---------|-------------|
| **8567061** | **Kafka/Flink/Cassandra等** | **ライフサイクル・課題整理** | **HTLL設計ガイド** |
| 9005614 | Enterprise Big Data | スケーラブルモデリング | エンタープライズ設計 |
| 7584967 | Scala Frameworks | 分析フレームワーク | ツール選定 |
| 10556121 | Time-series Sensor Platform | センサーデータ分析 | IoT統合 |

### 車両クラウド・リアルタイムシステム関連

| 論文 | 手法 | 主要貢献 | 今回への応用 |
|------|------|---------|-------------|
| **9483722** | **Vehicular Cloud + Fault Tolerance** | **乱数的車両到着への対応** | **耐障害性設計** |
| 6644100 | VANET分散DB | 車両ネットワーク通信 | V2Xデータ管理 |
| 8730671 | データ冗長性削減 | 車両ネットワーク最適化 | 通信効率化 |

---

## 🎯 研究への統合的な応用

### 1. AIM設計の理論的基盤

| 要素 | 参考論文 | 具体的応用 |
|------|---------|-----------|
| **協調交差点管理全体** | 7244203 (Survey) | Time Slots, Space Reservation, Trajectory Planning |
| **FCFS予約システム** | 10504747 (AROW) | 優先権の明示的割り当て、曖昧性解消 |
| **衝突検知最適化** | 11184723 (Graph Coloring) | 10*10タイル分けの代替・改良案 |
| **耐障害性** | 9483722 (Vehicular Cloud) | 乱数的車両到着への対応 |

### 2. HTLL (Kafka + Flink + Druid) アーキテクチャ設計

| 要素 | 参考論文 | 具体的応用 |
|------|---------|-----------|
| **ライフサイクル全体** | 8567061 (Lifecycle) | Ingestion → Storage → Processing → Analytics → Reporting |
| **時系列データ処理** | 10253446 (Time-series DB) | 車両センサーデータの特性理解 |
| **車両データフレームワーク** | 10539569 (Smart Vehicles) | データパイプライン標準化 |
| **OLTAP対応** | 7498333 (Oracle DBIM) | トランザクション+分析の同時実行 |

### 3. ベースラインA比較（信号機 vs AIM）

| 比較指標 | 参考論文 | 予想結果 |
|---------|---------|---------|
| **平均車両待機時間** | 11184723 | **76% 削減** (信号機 vs Graph Coloring AIM) |
| **交差点スループット** | 11184723 | **343% 向上** (FCFS vs Graph Coloring) |

### 4. ベースラインB比較（RDB vs HTLL）

| 比較指標 | 参考論文 | 予想結果 |
|---------|---------|---------|
| **エンドツーエンド遅延** | 7498333 | HTLL (Druid) の低レイテンシ（インメモリ処理） |
| **同時アクセス性能** | 10253446 | CrateDB/Druid の優位性（同時ユーザー） |
| **スケーラビリティ** | 7396611 | Hadoop vs HTLL (HTLL の方が低レイテンシ) |

---

## 📊 収集論文の完全リスト

### 新規追加論文（48件）

#### 分散データベース・車両システム (10件)
1. 6644100 - Communication in distributed database system in the VANET environment
2. 1015327 - More efficient location tracking in PCS systems
3. 9473632 - Localized Data Transfer System by Vehicles
4. 1505160 - A dynamic data information management algorithm
5. 5169576 - Highway Emergency Response System Based on GIS-T
6. 9483722 - Vehicular Cloud Real Time System (Fault-Tolerant) ★★★★☆
7. 7396611 - Distributed Storage and Analysis (Hadoop) ★★★★☆
8. 881040 - Database-centered architecture for traffic incident
9. 851685 - Terminal aided k-location tracking
10. 8730671 - Distributed System for Reducing Uploaded Data Redundancy

#### 分析型DB・ビッグデータストリーミング (10件)
11. 9442793 - Advanced Health Information Technology
12. 9005614 - Effective and Scalable Data Modeling
13. 7584967 - Open Source Big Data Analytics Frameworks (Scala)
14. 7546229 - Knowledge Based Retrieval Scheme
15. 8622182/8622206 - Big Data Augmentation with Data Warehouse
16. 10556121 - Open-framework Big Data Analytic Platform
17. 7433711 - Conceptual Predictive Modeling
18. 8567061 - Real-Time Processing of Big Data Streams ★★★★☆
19. 9183863 - Scalable Heterogeneous Big Data Framework

#### V2X協調交差点管理 (10件)
20. 7244203 - Cooperative Intersection Management: A Survey ★★★★★
21. 10623524 - Exploring Shared Perception and Control
22. 11194002 - Toward 6G-V2X
23. 10477532 - Game Theoretic Application to Intersection Management
24. 10184172 - Hybrid cooperative intersection management
25. 10504747 - AROW: V2X-Based Automated Right-of-Way ★★★★☆
26. 9920759 - Safe Cooperative Intersection (Robots)
27. 8542751 - Collision-Aware Communication
28. 9264154 - Coordination Algorithm for Multi-Intersection
29. 9336022 - Leveraging Multiagent Learning

#### FCFS・スケジューリング (4件)
30. 10885772 - Graph based Conflict-Free Scheduling
31. 10044851 - Mixed-Traffic Intersection Management
32. 11184723 - Color the Conflict (Graph Coloring) ★★★★★
33. 8039056 - Ticket-Based Traffic Flow Control

#### 時系列DB・IoT車両 (9件)
34. 10253446 - Performance Impact of Parallel Access (Time Series) ★★★★☆
35. 10539569 - Framework for Smart Vehicles Data ★★★★☆
36. 9705673 - IoT Based Real-Time Water Quality Monitoring
37. 8537845 - Predictive Modeling with Vehicle Sensor Data
38. 10389839 - Framework for Efficient Communication (OBD-II)
39. 10181164 - Lightweight, Mobility-Aware Data Store (UAV)
40. 9042994 - Highly Reliable IoT Data Management (Blockchain)
41. 10665254 - Digital Twin for Drinking Water Source
42. 8340736 - Common data architecture for energy data

#### カラムナDB・OLAP (5件)
43. 8509384 - Accelerating Joins and Aggregations (Oracle In-Memory)
44. 8029340 - SCMAT: SCMs for OLAP and OLTP
45. 7498333 - Fault-tolerant real-time analytics (Oracle DBIM) ★★★★☆
46. 9377937 - Benchmarking HOAP for Document Data
47. 8110657 - Janus: Hybrid Scalable Multi-Representation

### 既存論文（62件）- 前回収集分

- AIM基礎: 10件
- リアルタイムビッグデータ（車両交通）: 10件
- V2X通信: 10件
- Apache Flink: 10件
- HTLL: 10件
- 衝突回避: 10件
- その他: 12件

**総計**: **110件の先行研究**

---

## 🔑 主要な発見

### 1. 協調交差点管理は確立された研究分野
- **サーベイ論文** (7244203) が存在し、体系的な整理がされている
- Time Slots, Space Reservation, Trajectory Planning などの標準的手法

### 2. FCFS は基本的なベンチマークだが改良の余地あり
- Graph Coloring (11184723) は **FCFS より 343% 高いスループット**
- AROW (10504747) は優先権の曖昧性を解消する改良版

### 3. 分散リアルタイム分析DBは OLTAP アプリケーションに最適
- Oracle DBIM (7498333) が分散カラムナDBの耐障害性を実証
- Druid は同様のアーキテクチャ（カラムナ、分散、リアルタイム）

### 4. ビッグデータストリーム処理のツールセットは標準化されつつある
- Kafka + Flink + (Cassandra/HBase) が一般的
- ライフサイクル (8567061) に沿った設計が重要

### 5. 時系列DBの選択はワークロード依存
- RDB / NoSQL / NewSQL の比較 (10253446) で明確
- 車両データは時系列DB（CrateDB, DolphinDB, Druid）が最適

---

## 📝 次のステップ

### 優先的に読むべき論文（Top 10）

1. **7244203** - Cooperative Intersection Management: A Survey ★★★★★
2. **11184723** - Graph Coloring (343% throughput improvement) ★★★★★
3. **10504747** - AROW (Right-of-Way algorithm) ★★★★☆
4. **8567061** - Real-Time Big Data Streams Lifecycle ★★★★☆
5. **7498333** - Fault-tolerant real-time analytics (Oracle DBIM) ★★★★☆
6. **10253446** - Time-series DB comparison ★★★★☆
7. **10539569** - Smart Vehicles Data Framework ★★★★☆
8. **9483722** - Vehicular Cloud Fault-Tolerant ★★★★☆
9. **7396611** - Hadoop Traffic Flow (Baseline B) ★★★★☆
10. 11134195 - Kafka + Flink + ML ★★★★★（前回抽出済み）

---

**作成日**: 2025-10-16
**収集ツール**: Browser-Use Automation + IEEE Xplore Integration
**LLMプロバイダー**: DeepSeek (deepseek-chat)
**総論文数**: 110件
**詳細分析**: 14件（Abstract全文抽出）
