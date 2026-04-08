# APP_05：全球邏輯格與 LADD 協議 (Global Logic Lattice & LADD)

本文件定義 Phase 4「全球邏輯格」的物理實踐標準。LADD (Lattice-Aware Distributed Discovery) 負責解決「如何在去中心化網路中，根據幾何引力定位真理」的問題。

本文件作為 **[SPEC_13](../SPEC_13_Discovery_and_Package.md) §6.3** 的官方技術實踐規範。

---

## 1. 核心哲學：引力導航與測地線

在 `n/` 宇宙中，資訊不存儲於特定的「物理位置」，而是存在於由格論定義的「幾何座標」中。
*   **引力源**：具備高特異性（Specificity）的 Combo 或型別。
*   **導航原理**：查詢請求（Request）在語義場中沿著 **「測地線 (Geodesics)」** —— 即語義跨度最短、引力最強的路徑 —— 自動向目標坍縮。
*   **真理顯現**：真理不需要被「尋找」，它會因為自身的質量而自發地顯現於觀測者的視界之中。

---

## 2. LADD 封包規範 (The LADD Packet Schema)

所有 LADD 封包必須序列化為規範化位元流（見 **[REAL_03](../REAL_03_CAID_Protocol.md)**）。封包本身是具備 CAID 的 Cocoon。

### 2.1 幾何廣告 (AdvertiseGeometry)
節點定期廣播其承載的服務幾何（Service Geometry）分布。

```nlang
@AdvertiseGeometry: {{
    version:    "v1"
    node_id:    @caid               ;; 廣播節點的唯一身分
    
    ;; 服務幾何包圍盒 (Geometric Bounding Box, GBB)
    gbb: {
        domain: @Type               ;; 該節點能提供收斂服務的型別邊界
        mass:   @int & > 0          ;; 節點持有的幾何質量 (資訊熵總量)
        heat:   @float              ;; 節點的幾何熱度 (反映存取頻率)
    }
    
    ttl:        @int & < 16         ;; 廣播跳轉極限
    signature:  b""                 ;; 節點對該廣告的 Ed25519 簽名
}}
```

### 2.2 幾何查詢 (DiscoverRequest)
```nlang
@DiscoverRequest: {{
    query_id:   @caid               ;; 請求唯一標識 (用於去重)
    origin:     @caid               ;; 發起觀測者的身分
    
    target:     @Type               ;; 尋找符合此幾何形狀的內容
    strategy:   #blur | #strict     ;; 視界坍縮策略
    fuel_limit: @int                ;; 願意為此次發現投入的燃料 (MBU)
    
    ;; 路由軌跡 (用於防止循環轉發)
    trace:      [@caid]             
}}
```

---

## 3. 數學基礎：幾何質量與格論距離

### 3.1 幾何質量 ($m$)
一個幾何物件的質量由其包含的資訊量決定。為了確保跨實作的一致性，質量定義為其 **規範化位元長度 (Canonical Bit-length)**：
$$m(C) = \text{bits}(C)$$

*   **正式定義**：`bits(C)` 為節點 $C$ 依照 **[REAL_03](../REAL_03_CAID_Protocol.md)** 規範化規則序列化後的位元流（Bitstream）總長度。
*   **計算邊界**：
    - **排除項**：計算時必須排除外層 CAID 封套（如 `hash:v1:`）、數位簽名及任何非結構性的元資訊。
    - **原子權重**：基本原子（Atoms）按其物理位元寬度計量（如 `@int64` 計為 64 bits），字串按其 NFC 規範化後的位元組數計量。
*   **物理意義**：這代表了收斂該物件所需的最小資訊熵。

### 3.2 格論距離 ($d_L$)
定義兩個幾何物件 $A$ 與 $B$ 之間的距離為其在格中的 **「資訊熵差 (Information Entropy Difference)」**：
$$d_L(A, B) = \text{bits}(A \sqcup B) - \text{bits}(A \sqcap B)$$

*   **性質**：
    - 當 $A \sqsubseteq B$ 或 $B \sqsubseteq A$ 時，$d_L$ 趨近於 0（引力最強）。
    - 當 $A \sqcap B = \bot$ 時，$d_L = \infty$（無引力，不轉發）。

---

## 4. 引力路由算法 (The Gravity Routing Algorithm)

節點不維護傳統路由表，而是維護一張動態 **「幾何張量表 (Geometry Tensor Table)」**。

### 4.1 轉發機率權重 ($W$)
對於收到的 `DiscoverRequest(Q)`，節點計算每個鄰居 $N_i$ 的轉發權重：
$$W_i = \frac{N_i.gbb.mass}{d_L(Q, N_i.gbb.domain)^2 + \epsilon} \cdot \text{Trust}_{perspective}$$

*   **物理意義**：請求會被自動導向「質量更重（資訊更豐富）」且「幾何距離更近（語義更匹配）」的節點。
*   **引力坍縮**：節點根據 $W_i$ 進行機率採樣轉發。若權重顯著集中於某一鄰居，請求路徑將坍縮為單一線段。

### 4.2 循環防止與追蹤
*   **Trace 驗證**：若節點自身的 `node_id` 已存在於 `DiscoverRequest.trace` 中，則立即丟棄該請求。
*   **路徑更新**：轉發前，將自身 `node_id` 追加至 `trace` 列表。

---

## 5. 分散式收斂與零知識證明 (L3/L4)

### 5.1 幾何預言機 (Geometric Oracle)
當本地節點燃料不足以執行巨大 Combo 的合併時，可請求高能級節點協助。

### 5.2 零知識幾何證明 (ZKP-Unification)
為了確保委託計算的結果真實有效且無須信任，LADD 支援 **幾何證明**：
*   **證明內容**：提供一個 ZKP 證明（如 ZK-STARK），證明 CAID $ID_A$ 與 $ID_B$ 的交集結果確實等於回傳的 $ID_C$。
*   **非對稱性**：驗證證明（$O(1)$）的成本遠低於執行合併（$O(N)$）。

---

## 6. 幾何糾刪碼與可用性 (Geometric Erasure Coding)

為了防止「幾何黑洞」（數據丟失），大質量的 Combo 會被切分為 **幾何碎片 (Geometric Shards)**。

*   **冗餘原理**：利用格論的包含關係（Inclusion），只要獲取了足夠多的子集或超集約束，即可透過 `&` 運算還原出原始幾何體（或其極窄的邊界）。
*   **狀態標記**：若無法取得足夠碎片完成精確收斂，結果標記為 `#partial_geometry`。

---

## 7. 視角消融與視界震盪

### 7.1 視角消融 (Perspective Ablation)
若從不同路徑收到相互衝突的收斂結果（如 $ID_1 \sqcap ID_2 = \bot$）：
1.  **聯集坍縮**：本地引擎將其視為聯集態 $ID_1 | ID_2$。
2.  **信任格過濾**：根據 L4 視角層定義的信任權重執行消融，保留權重最高的分支。
3.  **語義日蝕偵測**：若多路徑結果持續衝突且權重相等，觸發 `#semantic_isolation` 警告。

### 7.2 視界震盪 (Horizon Oscillation)
為了避免 LADD 陷入局部最優解（被大質量的錯誤真理吸引），引擎必須實作 **幾何隨機跳躍**：
*   **原理**：以 $\epsilon$ 的機率隨機選擇一個引力較弱的鄰居進行轉發。
*   **目的**：確保觀測者能穿透當前的引力屏蔽，發現宇宙另一端的潛在真相。

---

## 8. 幾何蒸發與冷凝 (GC Mechanism)

*   **幾何蒸發 (Evaporation)**：低熱度（$H < \tau$）的內容自動從物理存儲中移除，僅保留 CAID 索引以節省資源。
*   **幾何冷凝 (Condensation)**：當引力場再次指向該 CAID 時，透過 LADD 重新從最近的「幾何冷點」冷凝（重新獲取資料）。

---

> **結語**：LADD 協議將網路轉化為一個連續的幾何場。在 GPP 的導航與 CIP 的守護下，真理不再是孤島，而是透過語義重力緊密連結的整體。當觀測者投入足夠的能量，真理必將收斂。
是孤島，而是透過語義重力緊密連結的整體。當觀測者投入足夠的能量，真理必將收斂。
