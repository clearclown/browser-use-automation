# 事実ベース文献レビュー: AIM + HTLL + 分散データベース

**収集日**: 2025-10-16
**データソース**: IEEE Xplore
**収集方法**: Browser-Use Automation（自動検索・Abstract抽出）
**詳細分析論文数**: 14件（Abstract全文）

---

## 📌 注記

本レビューは、IEEE Xploreから実際に取得したデータのみを記載しています。
- **Abstract**: IEEE Xploreの原文をそのまま引用
- **要約**: Abstract内の事実のみを抽出（著者の主張・実験結果）
- **推測・解釈**: 最小限に抑制

---

## 1. AIM基礎論文

### 1.1 Reservation-based Autonomous Intersection Management Considering Vehicle Failures

**IEEE Document**: 9016469
**URL**: https://ieeexplore.ieee.org/document/9016469/
**カテゴリ**: AIM基礎 - FCFSベース予約システム

#### Abstract（原文）

> In the reservation-based intersection management system proposed in [1], vehicles can travel across the intersection efficiently and collision-free under a constraint that the vehicles travel at a speed within a predefined speed range. As an extension from that work, we propose a scheme wherein collision can still be avoided among vehicles in the intersection when any of the vehicle fails to follow the speed requirement and travels at a slower speed than the allowed minimum speed in the intersection. As a solution to this problem, all cars in the intersection are instructed to stop and we show how to determine the values of the scheduling input parameters to be used to allow the vehicles to stop safely.

#### 要約（事実のみ）

**システム**: Reservation-based intersection management
**前提条件**: 車両が事前定義された速度範囲内で走行
**提案内容**: 車両が最低速度要件を満たさない場合でも衝突回避可能なスキーム
**解決策**: 交差点内の全車両に停止を指示し、安全停止のためのスケジューリングパラメータを決定

---

## 2. HTLL - Kafka + Flink 統合

### 2.1 Real-Time and Offline Analytics for E-Commerce: Kafka + Flink + ML

**IEEE Document**: 11134195
**URL**: https://ieeexplore.ieee.org/document/11134195/
**カテゴリ**: HTLL - Kafka+Flink統合

#### Abstract（原文）

> In the rapidly evolving digital landscape, optimizing user engagement on e-commerce platforms is crucial for success. This paper presents a hybrid analytics system integrating real-time and offline analysis to enhance the functionality and user experience of a hypothetical furniture website. Utilizing Apache Kafka for data streaming, Apache Flink for real-time processing, and MongoDB for offline storage, the system analyzes user interactions and preferences. Machine learning models, including Random Forest and XGBoost, are employed for predictive analytics, with differential privacy ensuring data security. The system also incorporates Explainable AI for transparency. Real-time visual analytics via Elasticsearch and Kibana empower stakeholders with actionable insights, fostering strategic decision making and improved customer satisfaction. This work demonstrates the transformative potential of combining real-time data processing with in-depth offline analysis in the e-commerce sector.

#### 要約（事実のみ）

**システム**: Hybrid analytics (real-time + offline)
**技術スタック**:
- Apache Kafka: data streaming
- Apache Flink: real-time processing
- MongoDB: offline storage
- Elasticsearch + Kibana: real-time visual analytics

**機械学習**: Random Forest, XGBoost
**セキュリティ**: Differential privacy
**適用分野**: E-commerce (furniture website)

---

### 2.2 Automobile Brand Analysis: Kafka + Flink + Vehicle Data

**IEEE Document**: 11138357
**URL**: https://ieeexplore.ieee.org/document/11138357/
**カテゴリ**: HTLL - 車両データ処理

#### Abstract（原文）

> With the rapid development of the automotive industry and the explosive growth of data, how to efficiently process and analyze automotive-related data to gain insights into automotive product trends has become an important issue. This paper presents an automotive brand analysis system based on feature engineering and the Apache Kafka + Flink stream data processing framework. Firstly, vehicle production and sales data, media data, and vehicle sensor data are collected to form a collection of multi-source heterogeneous data; secondly, through data cleansing, feature extraction, and feature transformation, feature engineering is constructed to create a standard, uniform, and norm-compliant data collection; then, based on the advantages and characteristics of Apache Kafka and Apache Flink, a stream data processing framework of Apache Kafka Flink is constructed, which can collect real-time data and efficiently process and transmit time-series data. Finally, by comparing traditional systems and single system architectures, it is concluded that the comprehensive performance of the system architecture presented in this paper is superior.

#### 要約（事実のみ）

**データソース**:
- Vehicle production and sales data
- Media data
- Vehicle sensor data

**処理手順**:
1. Multi-source heterogeneous data collection
2. Data cleansing, feature extraction, feature transformation
3. Apache Kafka + Flink stream processing framework

**性能**: Traditional systems と single system architectures より comprehensive performance が superior（著者主張）

---

### 2.3 Real-Time Data Pipeline Optimization for Autonomous Control Systems

**IEEE Document**: 11077491
**URL**: https://ieeexplore.ieee.org/document/11077491/
**カテゴリ**: HTLL - 自律制御パイプライン

#### Abstract（原文）

> Real-time data pipeline optimization plays a critical role in the efficiency and reliability of autonomous control systems, particularly in dynamic environments that demand low latency and high throughput. This paper explores the latest advancements in optimizing real-time data pipelines, focusing on the integration of sensor data, computational models, and decision-making algorithms used in autonomous systems. The discussion includes challenges related to data collection, preprocessing, and transmission, as well as techniques for enhancing the scalability, fault tolerance, and real-time capabilities of data pipelines. Furthermore, the paper reviews key optimization strategies, such as stream processing, distributed computing, and edge processing, and assesses their applicability to real-time decision-making in autonomous control systems. By analyzing recent research and practical applications, this paper aims to provide insights into the future development of efficient data pipelines that support the autonomous systems of tomorrow.

#### 要約（事実のみ）

**対象**: Autonomous control systems
**要件**: Low latency, high throughput
**焦点**: Sensor data, computational models, decision-making algorithms の統合
**課題**: Data collection, preprocessing, transmission
**最適化戦略**:
- Stream processing
- Distributed computing
- Edge processing

---

### 2.4 Big Data Framework for Monitoring Real-Time Vehicular Traffic Flow

**IEEE Document**: 10347303
**URL**: https://ieeexplore.ieee.org/document/10347303/
**カテゴリ**: ビッグデータ - 車両交通フロー

#### Abstract（原文）

> The relatively high rate of traffic accidents in Iraq shows the necessity of working on the driver's actions monitoring through the use of vehicle flow data to improve the road safety. Based on this situation, many tools and technologies such as sensors, cameras, and data management can be utilized to monitor traffic conditions and provide real-time information to drivers and transportation authorities. The primary challenges are collecting, processing, analyzing, and visualizing the huge volume of data produced by vehicles and devices. To address these challenges, we proposed and implemented a big data framework for monitoring the data flows generated by vehicles in the city environment. Among the various data generated by vehicles, our framework monitors the latitude and longitude values of the global positioning system (GPS) and speed. The framework's architecture is scalable and fault-tolerant which makes it suitable for handling large-scale data flows generated by many connected vehicles. The results show that it allows for increased throughput, high availability, and fault tolerance and provides full-text search. This framework has been implemented using several big data platforms and tools such as Apache Kafka and Elasticsearch. In addition, the framework's services have been packaged in the container-based virtualization environment to support the reusability and portability of the framework.

#### 要約（事実のみ）

**目的**: 車両フローデータによる道路安全性向上（イラク）
**監視データ**: GPS latitude/longitude, speed
**技術スタック**:
- Apache Kafka
- Elasticsearch
- Container-based virtualization

**特性**: Scalable, fault-tolerant
**実験結果（著者主張）**: Increased throughput, high availability, fault tolerance

---

## 3. V2X 協調交差点管理

### 3.1 Cooperative Intersection Management: A Survey

**IEEE Document**: 7244203
**URL**: https://ieeexplore.ieee.org/document/7244203/
**著者**: Lei Chen, Cristofer Englund
**カテゴリ**: V2X協調交差点管理 - サーベイ論文

#### Abstract（原文）

> Intersection management is one of the most challenging problems within the transport system. Traffic light-based methods have been efficient but are not able to deal with the growing mobility and social challenges. On the other hand, the advancements of automation and communications have enabled cooperative intersection management, where road users, infrastructure, and traffic control centers are able to communicate and coordinate the traffic safely and efficiently. Major techniques and solutions for cooperative intersections are surveyed in this paper for both signalized and nonsignalized intersections, whereas focuses are put on the latter. Cooperative methods, including time slots and space reservation, trajectory planning, and virtual traffic lights, are discussed in detail. Vehicle collision warning and avoidance methods are discussed to deal with uncertainties. Concerning vulnerable road users, pedestrian collision avoidance methods are discussed. In addition, an introduction to major projects related to cooperative intersection management is presented. A further discussion of the presented works is given with highlights of future research topics. This paper serves as a comprehensive survey of the field, aiming at stimulating new methods and accelerating the advancement of automated and cooperative intersections.

#### 要約（事実のみ）

**論文種別**: Survey（サーベイ論文）
**対象**: Signalized and nonsignalized intersections（焦点: nonsignalized）
**Cooperative methods**:
- Time slots and space reservation
- Trajectory planning
- Virtual traffic lights

**安全対策**:
- Vehicle collision warning and avoidance
- Pedestrian collision avoidance

**目的**: Comprehensive survey, 新手法の刺激, automated and cooperative intersections の進展加速

---

### 3.2 AROW: V2X-Based Automated Right-of-Way Algorithm

**IEEE Document**: 10504747
**URL**: https://ieeexplore.ieee.org/document/10504747/
**著者**: Ghayoor Shah, Danyang Tian, Ehsan Moradi-Pari, Yaser P. Fallah
**カテゴリ**: V2X協調交差点管理 - Right-of-Wayアルゴリズム

#### Abstract（原文）

> Research in Cooperative Intersection Management (CIM), utilizing Vehicle-to-Everything (V2X) communication among Connected and/or Autonomous Vehicles (CAVs), is crucial for enhancing intersection safety and driving experience. CAVs can transceive basic and/or advanced safety information, thereby improving situational awareness at intersections. The focus of this study is on unsignalized intersections, particularly Stop Controlled-Intersections (SC-Is), where one of the main reasons involving crashes is the ambiguity among CAVs in SC-I crossing priority upon arriving at similar time intervals. Numerous studies have been performed on CIM for unsignalized intersections based on centralized and distributed systems in the presence and absence of Road-Side Unit (RSU), respectively. However, most of these studies are focused towards replacing SC-I where the scheduler provides spatio-temporal or sequence-based reservation to CAVs, or where it controls CAVs via kinematic commands. These methods cause CAVs to arrive at the intersection at non-conflicting times and cross without stopping. This logic is severely limited in real-world mixed traffic comprising human drivers where kinematic commands and other reservations cannot be implemented as intended. Thus, given the existence of SC-Is and mixed traffic, it is significant to develop CIM systems incorporating SC-I rules while assigning crossing priorities and resolving the related ambiguity. In this regard, we propose a distributed Automated Right-of-Way (AROW) algorithm for CIM to assign explicit SC-I crossing turns to CAVs and mitigate hazardous scenarios due to ambiguity towards crossing priority. The algorithm is validated with extensive experiments for its functionality, scalability, and robustness towards CAV non-compliance, and it outperforms the current solutions.

#### 要約（事実のみ）

**対象**: Unsignalized intersections, Stop Controlled-Intersections (SC-Is)
**課題**: Ambiguity in crossing priority when CAVs arrive at similar time intervals
**既存研究の限界**: Real-world mixed traffic（人間ドライバー混在）では実装困難
**提案**: Distributed Automated Right-of-Way (AROW) algorithm
**検証**: Extensive experiments (functionality, scalability, robustness)
**性能（著者主張）**: Outperforms current solutions

---

### 3.3 Color the Conflict: Graph Coloring for AIM

**IEEE Document**: 11184723
**URL**: https://ieeexplore.ieee.org/document/11184723/
**著者**: Shraddha Dulera, RAM Narayan Yadav
**カテゴリ**: AIM - グラフ彩色による衝突検知

#### Abstract（原文）

> Conflict resolution, particularly through effective priority assignment and right-of-way negotiation, is a critical factor in maximizing intersection throughput and minimizing vehicle crossing time in Autonomous Intersection Management (AIM). This paper proposes a novel color-based round scheduling algorithm that enables simultaneous traversal of multiple vehicles on both conflicting and non-conflicting paths by segmenting the paths inside the intersection using a graph coloring technique. Unlike traditional approaches that resolve conflicts at each individual conflict point, this method eliminates conflict checking by globally coordinating vehicle movements based on color rounds. As a result, the algorithm significantly reduces computational complexity and the number of conflict comparisons, which otherwise scale exponentially with the number of vehicles and conflict points. Simulations in the CARLA simulator across varying traffic densities and movement scenarios demonstrate that the proposed algorithm improves intersection throughput by up to 343% compared to reservation-based methods using FCFS for priority resolution. It also reduces average crossing time by approximately 76% compared to traditional traffic signals and by 94% relative to standalone FCFS strategies. We have also demonstrated that the proposed algorithm is fair in terms of the number of vehicles crossing the intersection per route.

#### 要約（事実のみ）

**提案**: Color-based round scheduling algorithm using graph coloring
**手法**: Path segmentation inside intersection
**利点**: Eliminates conflict checking, reduces computational complexity
**シミュレータ**: CARLA simulator
**実験結果（著者主張）**:
- **+343% throughput** vs reservation-based FCFS
- **-76% crossing time** vs traditional traffic signals
- **-94% crossing time** vs standalone FCFS

**公平性**: Fair in terms of vehicles crossing per route

---

## 4. 分散データベース・リアルタイム分析

### 4.1 Vehicular Cloud Real Time System (Fault-Tolerant)

**IEEE Document**: 9483722
**URL**: https://ieeexplore.ieee.org/document/9483722/
**著者**: Luther Bell, Puya Ghazizadeh, Samy El-Tawab, Aida Ghazizadeh
**カテゴリ**: 車両クラウド - 耐障害性リアルタイムシステム

#### Abstract（原文）

> Vehicular Clouds are inherited from the cloud computing concept. Vehicles standing in a parking lot can corporate computing, sensing, communication, and physical resources. Vehicular Clouds were motivated by the realization that present-day vehicles are equipped with powerful onboard computers, powerful transceivers, and an impressive array of sensing devices. As it turns out, most of the time, the computing, storage, and communication resources available in our vehicles are chronically under-utilized. We are putting these resources to work in a meaningful way to provide computation power, which plays an essential role for service providers, transportation systems, health care, and online education in our modern society. Vehicular Clouds provide computation power to users based on a resource-sharing model. In this model, vehicle owners rent out their onboard computation powers to receive incentives in the form of payments or free parking spots. To use this computation power, there should be a way to submit jobs to the system. In this work, we develop a framework for the vehicular cloud to manage the onboard computation resource of the vehicles and computation tasks that users submit. This framework will be available to users in a software system called Vehicular Cloud Real-Time System (VCRTS). Random arrival and departure of vehicles in vehicular clouds can impact the computation nodes' availability and lead to an interruption in the computation process. We design and implement the VCRTS based on a fault-tolerant approach to prevent interruption in job execution. Our approach uses a redundancy mechanism to handle the random nature of arrival and departure of the vehicles that are used as computation nodes.

#### 要約（事実のみ）

**システム**: Vehicular Cloud Real-Time System (VCRTS)
**課題**: Random arrival and departure of vehicles → computation interruption
**解決策**: Fault-tolerant approach using redundancy mechanism
**応用分野**: Service providers, transportation systems, health care, online education

---

### 4.2 Distributed Storage and Analysis of Traffic Flow Data (Hadoop)

**IEEE Document**: 7396611
**URL**: https://ieeexplore.ieee.org/document/7396611/
**著者**: Liujiang Zhu, Yun Li
**カテゴリ**: 分散ストレージ - Hadoop交通フロー

#### Abstract（原文）

> Because of the traditional methods failing to solve the efficient storage and analyze the problems with rapid growth of the massive traffic flow data, This paper adopts the distributed database HBase of Hadoop to store huge amounts of the urban road traffic flow data. By applying the distributed computing framework of MapReduce, statistical analysis of the traffic flow data is carried out. The experimental results validate the ability of Hadoop cluster, whose efficient storage, computing, scalability can deal with the problem of storing and processing the massive traffic flow data.

#### 要約（事実のみ）

**課題**: Traditional methods の限界（massive traffic flow data）
**技術**: Hadoop HBase (distributed database) + MapReduce (distributed computing)
**実験結果（著者主張）**: Hadoop cluster の efficient storage, computing, scalability を検証

---

### 4.3 Real-Time Processing of Big Data Streams: Lifecycle, Tools, Challenges

**IEEE Document**: 8567061
**URL**: https://ieeexplore.ieee.org/document/8567061/
**著者**: Fatih Gürcan, Muhammet Berigel
**カテゴリ**: ビッグデータストリーム処理 - ツール・課題

#### Abstract（原文）

> In today's technological environments, the vast majority of big data-driven applications and solutions are based on real-time processing of streaming data. The real-time processing and analytics of big data streams play a crucial role in the development of big-data driven applications and solutions. From this perspective, this paper defines a lifecycle for the real-time big data processing. It describes existing tools, tasks, and frameworks by associating them with the phases of the lifecycle, which include data ingestion, data storage, stream processing, analytical data store, and analysis and reporting. The paper also investigates the real-time big data processing tools consisting of Flume, Kafka, Nifi, Storm, Spark Streaming, S4, Flink, Samza, Hbase, Hive, Cassandra, Splunk, and Sap Hana. As well as, it discusses the up-to-date challenges of the real-time big data processing such as "volume, variety and heterogeneity", "data capture and storage", "inconsistency and incompleteness", "scalability", "real-time processing", "data visualization", "skill requirements", and "privacy and security". This paper may provide valuable insights into the understanding of the lifecycle, related tools and tasks, and challenges of real-time big data processing.

#### 要約（事実のみ）

**Lifecycle phases**:
1. Data ingestion
2. Data storage
3. Stream processing
4. Analytical data store
5. Analysis and reporting

**Tools**: Flume, Kafka, Nifi, Storm, Spark Streaming, S4, Flink, Samza, Hbase, Hive, Cassandra, Splunk, Sap Hana

**Challenges**:
- Volume, variety, heterogeneity
- Data capture and storage
- Inconsistency and incompleteness
- Scalability
- Real-time processing
- Data visualization
- Skill requirements
- Privacy and security

---

### 4.4 Time-Series Database Performance: RDB vs NoSQL vs NewSQL

**IEEE Document**: 10253446
**URL**: https://ieeexplore.ieee.org/document/10253446/
**著者**: Sebastian Pritz, Martina Zeinzinger, et al.
**カテゴリ**: 時系列DB - RDB vs NoSQL vs NewSQL

#### Abstract（原文）

> Time series data is generated in various application areas, such as IoT devices or sensors in vehicles. This type of data is often characterized by a high resource demand due to the interval at which information is measured ranges from daily down to milliseconds. Next to the frequency, the number of data sources, for example hundreds of sensors in modern airplanes generating time series concurrently, is typical for such big data scenarios. Such scenarios require the persistence of the measurements for further evaluations. In this work, we introduce an artificial data benchmark for relational, NoSQL, and NewSQL database management systems in the context of time series. We compare these databases by having multiple read and write data sources accessing the database management systems simultaneously. The evaluation shows that no tested system outperforms all other systems. While DolphinDB shows the highest read performance in single-user scenarios, CrateDB is able to show its advantages regarding when multiple users access the data simultaneously.

#### 要約（事実のみ）

**データソース例**: IoT devices, sensors in vehicles
**測定間隔**: Daily down to milliseconds
**ベンチマーク**: Artificial data benchmark for relational, NoSQL, NewSQL
**テスト条件**: Multiple read and write data sources simultaneously
**実験結果（著者主張）**:
- DolphinDB: Highest read performance (single-user)
- CrateDB: Advantages in multiple users access

**結論**: No tested system outperforms all other systems

---

### 4.5 Smart Vehicles Data Framework

**IEEE Document**: 10539569
**URL**: https://ieeexplore.ieee.org/document/10539569/
**著者**: Mariana Azevedo, Thais Medeiros, et al.
**カテゴリ**: スマート車両データ - フレームワーク

#### Abstract（原文）

> Thanks to the Internet of Things (IoT) revolution and advancements in embedded systems, the incorporation of an extensive array of sensors and computational resources into vehicles has become a reality, significantly enhancing their capabilities to produce relevant data. This has opened up new opportunities for acquiring and processing vehicular data in various areas, supporting new applications such as vehicular monitoring to the use of information for artificial intelligence for improved decision-making tasks. However, although the benefits are promising, there is a current challenge when providing flexible and standardized procedures to capture, process, and store this information for further analysis. In this context, this article proposes an framework to support the the handling of vehicular data, including data processing by a server and storage in a cloud database. This framework was validated through a real-world case study, analyzing the collected sensor data. The results indicated the feasibility of the proposal, contributing to the availability of vehicular data analysis in a way that is distinct from proposals in the literature. Additionally, this framework offers another significant contribution, related to the use of an appropriate database for time series, enabling scalability and high availability.

#### 要約（事実のみ）

**背景**: IoT revolution, embedded systems → vehicles with sensors
**課題**: Flexible and standardized procedures の欠如
**提案**: Framework for vehicular data handling (server processing + cloud database storage)
**検証**: Real-world case study
**データベース**: Appropriate database for time series (scalability + high availability)

---

### 4.6 Fault-Tolerant Real-Time Analytics (Oracle DBIM)

**IEEE Document**: 7498333
**URL**: https://ieeexplore.ieee.org/document/7498333/
**著者**: Niloy Mukherjee, Shasank Chavan, et al.
**カテゴリ**: 分散リアルタイム分析 - 耐障害性

#### Abstract（原文）

> Modern data management systems are required to address new breeds of OLTAP applications. These applications demand real time analytical insights over massive data volumes not only on dedicated data warehouses but also on live mainstream production environments where data gets continuously ingested and modified. Oracle introduced the Database In-memory Option (DBIM) in 2014 as a unique dual row and column format architecture aimed to address the emerging space of mixed OLTAP applications along with traditional OLAP workloads. The architecture allows both the row format and the column format to be maintained simultaneously with strict transactional consistency. While the row format is persisted in underlying storage, the column format is maintained purely in-memory without incurring additional logging overheads in OLTP. Maintenance of columnar data purely in memory creates the need for distributed data management architectures. Performance of analytics incurs severe regressions in single server architectures during server failures as it takes non-trivial time to recover and rebuild terabytes of in-memory columnar format. A distributed and distribution aware architecture therefore becomes necessary to provide real time high availability of the columnar format for glitch-free in-memory analytic query execution across server failures and additions, besides providing scale out of capacity and compute to address real time throughput requirements over large volumes of in-memory data. In this paper, we will present the high availability aspects of the distributed architecture of Oracle DBIM that includes extremely scaled out application transparent column format duplication mechanism, distributed query execution on duplicated in-memory columnar format, and several scenarios of fault tolerant analytic query execution across the in-memory column format at various stages of redistribution of columnar data during cluster topology changes.

#### 要約（事実のみ）

**対象アプリケーション**: OLTAP (Online Transaction and Analytical Processing)
**システム**: Oracle Database In-memory Option (DBIM, 2014)
**アーキテクチャ**: Dual row and column format (transactional consistency)
**特徴**:
- Row format: Persisted in storage
- Column format: In-memory (no additional logging overheads)

**課題**: Single server architecture → severe regressions during failures
**解決**: Distributed and distribution aware architecture
**機能**: Column format duplication, distributed query execution, fault tolerant query execution

---

## 📊 収集論文の統計

### Abstract全文抽出: 14件

| カテゴリ | 件数 |
|---------|-----|
| AIM基礎 | 1 |
| HTLL (Kafka + Flink) | 4 |
| V2X協調交差点管理 | 3 |
| 分散データベース・リアルタイム分析 | 6 |

### 検索結果（タイトル・著者・URL）: 110件以上

| 検索クエリ | 件数 |
|-----------|-----|
| Autonomous Intersection Management | 10 |
| Real-time Big Data Vehicular Traffic | 10 |
| V2X Vehicular Communication Intersection | 10 |
| Apache Flink Stream Processing | 10 |
| High Throughput Low Latency | 10 |
| Vehicle Collision Avoidance | 10 |
| Distributed Database Vehicular Systems | 10 |
| Analytical Database Big Data Streaming | 10 |
| V2X Cooperative Intersection Management | 10 |
| FCFS Scheduling Autonomous Vehicles | 4 |
| Time-series Database IoT Vehicle | 9 |
| Columnar Database OLAP Real-time | 5 |
| Apache Kafka Druid | 1 |
| その他 | 11 |

**総計**: 110件

---

## 📌 主要な事実（著者の実験結果・主張）

### 性能改善の数値（Graph Coloring - 11184723）

- **Throughput**: +343% vs reservation-based FCFS
- **Crossing time**: -76% vs traditional traffic signals
- **Crossing time**: -94% vs standalone FCFS

### データベース性能（10253446）

- **DolphinDB**: Highest read performance (single-user)
- **CrateDB**: Advantages in multiple users access
- **結論**: No tested system outperforms all others

### 技術スタック（実際に使用されているツール）

**Kafka + Flink 統合事例**:
- E-Commerce (11134195): Kafka + Flink + MongoDB + Elasticsearch
- Automobile Analysis (11138357): Kafka + Flink + feature engineering
- Vehicular Traffic (10347303): Kafka + Elasticsearch

**ビッグデータストリーム処理ツール（8567061）**:
- Flume, Kafka, Nifi, Storm, Spark Streaming, S4, Flink, Samza
- HBase, Hive, Cassandra, Splunk, SAP HANA

---

## ⚠️ 注意事項

1. **性能数値は著者の主張**: 実験条件・環境が異なる可能性
2. **比較対象は各論文で異なる**: 直接比較は困難
3. **技術の適用分野**: E-commerce, automobile, traffic flow など多様
4. **データベースの性能**: Workload dependent（ワークロード依存）

---

**データ取得日**: 2025-10-16
**収集ツール**: Browser-Use Automation
**データソース**: IEEE Xplore (https://ieeexplore.ieee.org/)
