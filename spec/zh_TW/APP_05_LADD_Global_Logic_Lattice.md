# APP_05：全域邏輯格與 LADD 協議 (Global Logic Lattice & LADD)

本文件定義 **OODP (Ouroboros Discovery Protocol)** **L3-L5 層**的譜幾何優化標準。

LADD (Lattice-Aware Distributed Discovery) 是 OODP 的**譜幾何優化擴充**，負責解決「如何在去中心化網路中，根據投影算子的幾何引力定位真理」的問題。

> **協定定位**：
> - **OODP 基礎**：L1-L3 層的傳輸與基礎發現（見 **[REAL_02](./REAL_02_Ouroboros_Protocols.md)**）
> - **LADD 優化**：L3-L5 層的譜幾何路由、引力算法與視角管理（本文）
>
> LADD 並非替代 OODP，而是在其 L3 收斂層之上提供**熱帶剪枝**、**譜距離計算**與**測地線路由**等優化。

本文件作為 **[SPEC_13: 銜尾蛇發現協定](./SPEC_13_Ouroboros_Discovery_Protocol.md) §6.3** 的官方技術實踐規範。

---

## 1. 核心哲學：引力導航與譜幾何

在量子化的 `n/` 宇宙中，資訊不存儲於特定的物理位置，而是存在於 Hilbert 空間的子空間中。
*   **引力源**：具備高特異性（譜特徵明顯）的子空間投影算子。
*   **導航原理**：查詢請求（Request）在語義場中沿著投影算子間的 **「測地線 (Geodesics)」** 自動向目標坍縮。
*   **氣味搜尋**：透過比對 **CAID (譜幾何指紋)** 的相似性，觀測者能在不下載數據的前提下，感知真理的「氣味」（譜能量分布）。

---

## 2. LADD 封包規範與協議棧

### 2.1 五層譜協議架構 (The Spectral Stack)

類比 OSI 模型，LADD 定義五個邏輯層次，每層對應譜幾何的不同抽象：

| 層次 | 名稱 | 譜幾何對應 | 功能 |
| :--- | :--- | :--- | :--- |
| **L1 物理層 (Carrier)** | 傳輸載體 | 位元流傳輸 | TCP/UDP、libp2p、QUIC（傳輸原始位元） |
| **L2 定址層 (Identity)** | 節點定位 | 譜指紋定位 | CAID 規範化、Kademlia XOR 路由（尋找**節點的物理位置**） |
| **L3 收斂層 (Convergence)** | 譜收斂核心 | 投影算子 Meet | 分散式 `&` 運算、衝突判定、熱帶剪枝 |
| **L4 視角層 (Perspective)** | Bohrification | 交換子代數過濾 | 權威格論、譜消融、主觀真理坍縮 |
| **L5 應用層 (Ouroboros)** | 語義接口 | 觀測者交互 | `~%Discovery./find`、插件發現、全球實體互動 |

**關鍵設計**：L2 使用 Kademlia 尋找**物理節點**（解決「這台機器在哪裡」），L3 以上才是譜感知路由（解決「這個子空間投影由誰服務」）。兩層不衝突，各司其職。

### 2.2 幾何廣告 (AdvertiseGeometry)

節點定期廣播其承載的子空間服務分布。

```nlang
@AdvertiseGeometry: {{
    version:    "v1"
    node_id:    @caid               ;; 廣播節點的身分

    ;; 服務幾何包圍盒 (Geometric Bounding Box, GBB)
    gbb: {
        domain: @Type               ;; 該節點涵蓋的子空間邊界 (投影算子)
        mass:   @float              ;; 幾何質量 (子空間投影之跡 Tr(P))
        spectrum: [@complex]        ;; 譜指紋摘要 (譜空間的主成分)
    }

    ;; Čech 神經位置 (選擇性)
    ;; 記錄此節點在 MASA 交集複形中的位置，幫助路由預測收斂路徑
    nerve_structure: [{
        masa:       @caid           ;; 參與的 MASA 的 CAID
        overlaps:  [@caid]          ;; 與此 MASA 交集非空的鄰居 MASA 列表
    }]

    ttl:        @int & ..15         ;; 格論量,非時長;語義見 REAL_02 §4.2.7
    signature:  b""                 ;; 譜加密簽名
}}
```

> **`ttl` 的語義【2026-07-28】**:它是**格論量**——§4.1 的第一級過濾是 meet,而 meet 沿格序下降;§3.1 的質量是投影的秩(整數)。**沒有單位,因為格論的秩沒有秒或跳這種單位;沒有節點遞減它,數學在遞減它。** 由此它是**自我認證**的(每個節點自內容定址資料重算)。
> **但 L2/線上層算不出它**:$d_L$ 與 GBB 在本文這一側,而 `ttl` 出現在 **[REAL_02](./REAL_02_Ouroboros_Protocols.md)** §4.2 的線上廣告裡,兩者從未相交。該層之規範限於它撐得住者(範圍 `0..=15`、`0` = 不要轉發我、永不修改),見 REAL_02 §4.2.7 與 §4.3.7。

### 2.3 幾何查詢 (DiscoverRequest)

```nlang
@DiscoverRequest: {{
    query_id:   @caid
    target:     @Type               ;; 目標子空間的投影特徵
    strategy:   #blur | #strict
    fuel_limit: @int

    ;; 氣味靈敏度：願意接受的譜距離閾值
    epsilon:    @float
}}
```

> **兩個「discover」同名而不同物【2026-07-28】**
>
> | | 本文 `@DiscoverRequest`(L3–L5) | **[REAL_02](./REAL_02_Ouroboros_Protocols.md)** §4.3 `#discover`(L2–L3) |
> | :-- | :--- | :--- |
> | 問什麼 | `target: @Type` 之**幾何模式** | 一個 **CAID** |
> | 答什麼 | 關於**內容**的證據(§5.1) | **對等點**與其位址(`%peers`) |
> | 有無節點 | **無** | 有 |
> | 規範層級 | 譜幾何優化擴充,**非強制**(SPEC_13 §6.3) | Core Requirement |
>
> 二者**不可互相替代**:前者回答不出「誰服務這個」(§5.1 附註),後者回答不出「什麼東西像這個」。
> 此處明列,是因為同名不同物正是 disc 026 所診斷的病;一份規格若讓讀者靠追溯章節出處
> 才分得出兩個 `discover`,它已經在製造下一個碰撞。

---

## 3. 數學基礎：幾何質量與譜距離

### 3.1 幾何質量 ($m$)

一個幾何物件的質量由其子空間的維度與資訊密度決定，定義為其投影算子的 **跡 (Trace)**：
$$m(C) = \text{Tr}(P_C)$$

*   **物理意義**：這代表了該定義在 Hilbert 空間中佔據的「幾何體積」。質量越大，代表其提供的約束資訊越豐富。

### 3.2 格論距離 (譜距離 $d_L$)

定義兩個幾何物件 $A$ 與 $B$ 之間的距離為其投影算子間的 **量子弦距離 (Chordal Distance)**：
$$d_L(A, B) = \sqrt{\text{Tr}(P_A + P_B - 2P_A \sqcap P_B)}$$

*   **氣味性質**：
    - 當 $A \sqsubseteq B$ 或 $B \sqsubseteq A$ 時，$d_L$ 趨向極小值（引力最強，氣味一致）。
    - 當 $A \perp B$ (正交) 時，$d_L$ 達到極大值（無引力，氣味不相干）。

---

### 3.3 譜指紋提取與量子化 (Spectral Fingerprint Extraction)

#### 3.3.1 v2 複數譜架構

CAID v2（REAL_03 §2.2）引入 `<masa_ref>` 和複數譜。Lattice Sketch 從實數特徵值擴充為複數譜 $[\lambda_1 e^{i\theta_1}, \lambda_2 e^{i\theta_2}, \ldots]$，
其中 $\theta_i$ 是該特徵向量相對於 MASA 參考系的相位角。

#### 3.3.2 譜指紋計算流程

**Lattice Sketch** 是 CAID 的「波動維度」，由投影算子 $P$ 的譜特徵及其 MASA 相位構成。

**步驟 1：特徵值分解**
對於投影算子 $P$（假設維度 $D$）：
$$P = \sum_{i=1}^{r} \mathbf{v}_i \mathbf{v}_i^\dagger$$
其中 $r = \text{Tr}(P)$（質量），$\mathbf{v}_i$ 為標準正交基底向量。

**步驟 2：MASA 相位提取**
從 MASA 參考系 $M$ 計算每個特徵向量的相位：
$$\theta_i = \arg(\langle \mathbf{v}_i | \mathbf{e}_M \rangle)$$
其中 $\mathbf{e}_M$ 是 MASA $M$ 的規範化參考基底向量，定義為按字典序取 MASA $M$ 的 Gelfand 譜中的第一個非零特徵向量。此選取規則確保跨引擎的決定論。

**步驟 3：複數譜建構**
構建複數譜向量：
$$\vec{S}_{\mathbb{C}} = [\lambda_1, \theta_1, \lambda_2, \theta_2, \ldots, \lambda_{16}, \theta_{16}]$$

振幅和相位各自獨立量化。

#### 3.3.3 量子化與編碼

為確保跨 CPU 架構的穩定性，複數譜需進行量子化：

| 處理步驟 | 說明 | 精度 |
| :--- | :--- | :--- |
| **歸一化** | 將特徵值投影至標準基底；相位歸一化到 $[-\pi, \pi]$ | N/A |
| **128-bit 定點化（振幅）** | 使用 REAL_03 §3.1 的定點數格式 | 64-bit 整數 + 64-bit 小數 |
| **128-bit 定點化（相位）** | $\theta_i / \pi$ 歸一化到 $[-1, 1]$，128-bit 定點數 | 64-bit 整數 + 64-bit 小數 |
| **噪聲捨棄** | 捨棄最後 8-bit | 保留 120-bit 有效位 |
| **截斷** | 僅保留前 16 個複數主成分 | 32 × 128-bit |

**量化函數：**
$$\lambda_{q}(v) = \text{round}(v \cdot 2^{64}) \mod 2^{120}$$
$$\theta_{q}(\phi) = \text{round}(\phi / \pi \cdot 2^{64}) \mod 2^{120}$$

**複數譜向量：**
$$\vec{S}_{\mathbb{C}} = [\lambda_{q}(v_1), \theta_{q}(\theta_1), \lambda_{q}(v_2), \theta_{q}(\theta_2), \ldots]$$

#### 3.3.4 Lattice Sketch 編碼

**壓縮流程：**

```
複數譜向量 (32 × 128-bit: 振幅 + 相位交錯)
    ↓
振幅序列 Delta 編碼（相鄰差分）
相位序列 Delta 編碼（相鄰差分）
    ↓
ZigZag 編碼（有符號 → 無符號）
    ↓
LEB128 壓縮（交錯合併：一個振幅後跟一個相位）
    ↓
Base64 輸出
```

**最終格式：**
```
lattice_sketch = base64_encode(compressed_complex_spectrum)
```

v1 相容：若相位全為 $0$（即無 MASA 相位資訊），退化为純實數譜。

#### 3.3.5 跨架構穩定性保障

為防止 IEEE 754 浮點精度差異導致的 CAID 漂移：

- **嚴格計算順序**：複數特徵值按振幅降冪排序後逐個處理；相位跟隨對應特徵向量
- **數值穩定性**：採用 Gram-Schmidt 正交化的穩定版本（Modified Gram-Schmidt）
- **確定性捨入**：統一採用向零捨入（Round-towards-zero）
- **基準測試**：引擎必須通過 `lattice_sketch_test_suite v2` 驗證，確保與參考實作 100% 匹配

**相容性說明：**
- 舊引擎（不支援譜幾何）可僅使用 `content_digest` 部分
- v1 引擎可選擇忽略 `masa_ref` 和複數相位，退化为純實數 Lattice Sketch 匹配
- v2 引擎必須同時驗證 `masa_ref`、`lattice_sketch`（複數）與 `content_digest` 的一致性

---

## 4. 引力路由算法 (The Gravity Routing Algorithm)

### 4.1 MASA 前置過濾

CAID v2 引入 `<masa_ref>` 後，路由的第一級過濾是 MASA 相容性檢查：

```
if MASA_overlap(Q_masa_ref, N_i.gbb.masa_ref) == _|_
    → W_i = 0        (H² obstruction: incompatible contexts, 跳過)
else
    → proceed to §4.2 (可比較，但需校正相位參考系)
```

MASA 重疊計算（同 REAL_03 §4.1 的合併語義）：
$$MASA_{overlap} = MASA_{Q} \sqcap MASA_{N_i}$$

### 4.2 轉發機率權重 ($W$)

對於通過 MASA 過濾的鄰居 $N_i$：

令 $M = MASA_{overlap}$，$\hat{P}_B = \Pi_M P_B \Pi_M^\dagger$ 為 $P_B$ 投影到重疊參考系後的版本。轉發權重為：

$$W_i = \frac{N_i.gbb.mass}{d_L^{\mathbb{C}}(Q_{spectrum}, N_i.gbb.spectrum)^2 + \epsilon}$$

其中 $d_L^{\mathbb{C}}$ 是**複數譜距離**（延伸自實數 Frobenius 距離）：

$$d_L^{\mathbb{C}}(A, B) = \sqrt{\text{Tr}(P_A^\dagger P_A + \hat{P}_B^\dagger \hat{P}_B - 2\,\text{Re}(\text{Tr}(P_A^\dagger \hat{P}_B)))}$$

*   **物理意義**：請求會被自動導向「質量更重（資訊更豐富）」且「譜距離更近（氣味更匹配）」的節點。
*   **$H^1$ 相位校正**：當 $d_L^{\mathbb{C}}$ 的虛部非零時，代表兩個 CAID 來自不同但兼容的 MASA——此相位差記錄在 `%cause` 中供後續路由修正。這是 L-S 框架中 $d_1$ obstruction 的工程表現。

### 4.3 神經感知路由 (Nerve-Aware Routing)

若遠端節點在其 GBB 中提供了 `nerve_structure`（見 §2.2），則路由器可利用 MASA 重疊資訊提前修剪無法收斂的路徑：

```
1. 對每個鄰居 N_i，比較其 nerve_structure 與本地 nerve_structure
2. 僅轉發給至少有一個共通 MASA overlap 的鄰居
3. 若無任何共通 MASA → 使用隨機跳躍（見 §4.4 視界震盪）
```

這將路由複雜度從 $O(n^2)$ 降低到 $O(n \cdot \bar{k})$，其中 $\bar{k}$ 是平均神經維度。
*   **譜校準**：節點利用 **柯西交錯定理 (Interlacing)** 在本機快速過濾掉那些幾何上不可能包含目標的鄰居。

### 4.4 視界震盪 (Horizon Oscillation)

為了避免 LADD 陷入局部最優解（被大質量的錯誤真理吸引），引擎必須實作 **譜隨機跳躍**：
*   **原理**：以 $\epsilon$ 的機率隨機選擇一個引力較弱的鄰居進行轉發。
*   **目的**：確保觀測者能穿透當前的引力屏蔽，發現宇宙另一端的潛在真相。

### 4.5 三個預算,與被放棄的單調性 **[Core Requirement,2026-07-28 新設]**

§4.1 使**每一跳都是一個 meet**,而 meet 沿格序下降。由此,一個沿路由累積的格論量
(§3.1 之秩)**只會下降**——這是 `ttl`(§2.2、**[REAL_02](./REAL_02_Ouroboros_Protocols.md)** §4.2.7)
原本的機制:**沒有人遞減它,數學在遞減它**,故它自我認證,不需信任任何轉發者。

**但本文自己放棄了那個單調性,而且是刻意的。** §4.3 第 3 步:「若無任何共通 MASA → 使用隨機跳躍」;
§4.4:引擎**必須**實作譜隨機跳躍。而無共通 MASA 之鄰居,在 §4.1 已被 $W_i = 0$ 濾除
——**隨機跳躍按構造離開那條下降鏈**。§7.3 說明了代價換來什麼:那是**語義日蝕**的防禦。

> **自我認證的單調預算,與逃出被佔據鄰域的能力,不可兼得。**
> 本規格選擇了逃脫,因而必須另備一個**不單調**的安全網。

於是三個預算並存,且**沒有一個是原來那個**:

| 量 | 出處 | 性質 | 誰持守 |
| :--- | :--- | :--- | :--- |
| `ttl` | §2.2 / REAL_02 §4.2 | 格論量(已簽);本層算得出時自我認證 | 數學(理想);線上層退化為宣告之傳播界 |
| `fuel_limit` | §2.3 `@DiscoverRequest` | 查詢方的執行預算 | 查詢者自己 |
| 硬跳數上限 | 實作(引擎) | 不單調的安全網 | 引擎,無條件 |

**規範**:三者**不得**互相替代,亦**不得**互相比較(它們不是同一個量)。實作**必須**具備第三者
——因為 §4.4 使前二者皆不足以保證終止。此表存在的理由是:**在此之前規格從未說出這個取捨**,
而不說出來的取捨,會在下一次有人問「TTL 是什麼單位」時,再被重新發明一次。

---

## 5. 持有聲明與氣味信心度 **〔2026-07-28 更名,原稱「幾何機率證明 (GPP)」〕**

歷史名 **GPP (Geometric Probability Proof)** 支撐「氣味搜尋」的可信度。**兩軌修訂
（2026-07-11，APP_02 §0）**：其內容拆為兩個不同性質的部件——

| 部件 | 軌 | 內容 |
| :--- | :--- | :--- |
| **持有聲明**〔2026-07-28 更名,原稱「身分證明」〕 | 執行軌 | 節點**聲明**其持有宣告之子空間。得選用附帶 $\omega/q$-Gram 指紋知識證明（電路一律見 APP_02 §6）；協定地位見 REAL_02 §7 |
| **氣味信心度** | 執行軌（$\mathbb{C}$） | 譜重疊的**啟發式估計**——不需要也不再有 ZK 證明；它只影響路由決策，謊報由反模式機制吸收（SPEC_15 §7） |

> **更名理由(2026-07-28)**:APP_02 §6.2 之電路公開輸入不提證明者,所證為**持有**而非
> 「是誰」;而「是誰」已由 REAL_02 §4.1.1 之金鑰對與 §4.2.2 之簽章回答。依 APP_02 §0
> 之命名規則(執行軌不得以「證明」命名),協定面所出示者為**聲明**。判別表見
> **[REAL_01](./REAL_01_Ouroboros_Engineering.md)** §7.6。**兩部件現皆在執行軌**——
> 持有的性格與質量相同:謊報只使查詢者白跑一趟,不影響內容真實性。
>
> **【2026-07-28 補】** 該次更名處理了表格與散文,卻漏掉**本節標題**與 `@GPP_Response`
> 兩處結構名。此即命名規則存在的理由:**名字比它的指涉活得久**,而漏網的名字會在下一位
> 讀者眼裡重新變成一個承諾。GPP 保留為**歷史縮寫**(見 GLOSSARY),**不得**用於新條款。

### 5.1 發現回應結構

當節點收到 `DiscoverRequest`，回傳：

```nlang
@CustodyResponse: {{
    target_caid:            @caid   ;; 被請求內容的 CAID
    fingerprint_commitment: @hash   ;; ω/q 指紋承諾（持有聲明錨，APP_02 §6）
    witness_proof:          b""     ;; F₂ STARK（可選；已驗過且在**驗證快取時效**內可省略）

    ;; 信心度：譜重疊的啟發式估計（執行軌——無證明義務）
    confidence:             @float & [0.0..1.0]
}}
```

> **【2026-07-28 更名】** 原名 `@GPP_Response`。disc 026 已將 GPP 自協定層退出並降為
> **持有聲明**(REAL_02 §7、**[APP_02](./APP_02_Formal_Verification.md)** §0),而此結構名躲過了該次更名——
> 它屬**執行軌**,依 APP_02 §0 之命名規則(執行軌之物不得以「證明」命名)不得叫 GPP。
> 判別表見 **[REAL_01](./REAL_01_Ouroboros_Engineering.md)** §7.6。

*   **信心度的語義**：`confidence` 估計 $P_{target}$ 與 $P_{query}$ 的譜重疊（封套層
    的 Lattice Sketch 比對，§3.3）。它是**導航訊號**：估錯或謊報只浪費路由 fuel，
    不影響內容真實性——最終接受與否由 CAID 內容定址把守。

*   **本結構回答不了「誰服務這個」(2026-07-28)**：它承載的是**關於內容的證據**
    ——`target_caid`、指紋承諾、見證、信心度——**裡面沒有節點,也沒有位址**。
    這與 APP_02 §6 之電路「公開輸入不含節點」是同一件事在回應格式上的顯影
    (disc 026)。「誰服務這個」由 **[REAL_02](./REAL_02_Ouroboros_Protocols.md)** §4.3 的
    `#discover` 回答,其回應攜帶 `%peers`。**兩者同名而不同物**,見 §2.3 附註。

### 5.2 氣味路由決策

節點根據 `confidence` 決定轉發（純執行軌決策）：
*   **高信心度 (>0.8)**：本地可能包含目標，進入嚴格搜尋模式。
*   **中等信心度 (0.3-0.8)**：繼續沿測地線轉發請求。
*   **低信心度 (<0.3)**：譜特徵不相干，返回 `#not_found`。

---

## 6. 因果完整性證明 (CIP) 與幾何預言機

### 6.1 幾何預言機 (Geometric Oracle)

當本地設備算力不足以執行大型觀測（深層 force 級聯、大宇宙合併）時，可委託給網路上
的 **幾何預言機**——高算力節點，代為執行收斂運算並生成 CIP 證明。

**設計出身（正名）**：CIP 是拿 LADD 類比區塊鏈/乙太坊得到的機制，「預言機」之名
即由此而來。這個類比是**結構性的**，不只是取名：

| 乙太坊 | n/ | 為什麼同構 |
| :--- | :--- | :--- |
| gas | `%fuel`／CHS 視界參數 | 讓執行有界、可記帳，因此**可證** |
| receipt / state root | CHS 封套、輸出 CAID | 執行結果的內容定址承諾 |
| block chain | Commit 鏈（SPEC_10） | 離散、不可變的狀態轉移序列 |
| rollup prover / sequencer | 幾何預言機 | 強算力方執行、弱算力方只驗證 |
| rollup validity/fraud proof | **CIP** | 「這段狀態轉移確實照規則算的」 |

**委託流程**：

```
本地節點（低算力）               幾何預言機
    |                               |
    |-- 委託: (輸入 commit CAID, 查詢 q, 視界參數 H) --> |
    |                               |-- 執行觀測收斂（force/unify 級聯）
    |<-- 結果 V + CIP -----------|
    |
    |-- 本地驗證: verify(CIP) --> 確認計算正確
    |-- 接受 V 作為本地觀測結果
```

### 6.2 CIP 的 claim 格式與證明分級

**兩軌修訂（2026-07-11）**：CIP 的證明對象是**離散求值語義**——引擎的 force/unify
運行在 bn_serial 可雜湊的離散資料上，委託完整性本質上是**離散計算證明**；舊版的
「複數譜相位鎖定」框架（對 $\text{Tr}(P_C^\dagger P_A)$ 的相位連續性檢查）退場。

*   **claim 格式（收斂鏈粒度）**——委託方需要的是端到端語句，不是逐步證明
    （委託方連分解都算不動，逐步證明服務不了它）：

    $$\text{CIP claim}: \quad (\text{CAID}_{in},\; q,\; H) \;\longmapsto\; (\text{CAID}_{out},\; \text{fuel}_{consumed})$$

    其中 $\text{CAID}_{in}$ 為輸入 commit、$q$ 為觀測查詢、$H$ 為視界參數（fuel/
    strategy/depth 上限）。**良定義性由視界決定論不變性（SPEC_00 Invariant 4）
    承保**：同輸入＋同 $H$ ⟹ 同輸出——乙太坊靠 gas 讓執行可證，n/ 靠 fuel/CHS
    讓觀測可證。
*   **memo 透明性**：claim 蓋的是語義求值關係，非引擎的快取執行——預言機用不用
    觀測 memo（GUIDE_03 §11）不影響證明對象。
*   **證明分級**（接 REAL_02 §7.3 的分級慣例；規格押注 claim 格式，不押注證明系統）：

| 層級 | 機制 | 乙太坊對應 | 狀態 |
| :--- | :--- | :--- | :--- |
| **Level 1（樂觀）** | 預言機承諾求值 trace 的 Merkle 根；委託方抽查若干步，或於挑戰期內由任意節點提出反證 | optimistic rollup | 先落地（無需遞迴證明系統） |
| **Level 2（有效性）** | 遞迴 STARK 蓋整條收斂鏈，驗證 $O(1)$ | zk-rollup validity proof | 終態（工具鏈成熟後） |

*   **非對稱性**（兩級共通）：驗證成本遠低於執行成本——Level 1 為 $O(\text{抽查數}\cdot\log)$，
    Level 2 為 $O(1)$。
*   **`#refine` 跨接**：精煉路徑（SPEC_10 §2.5）上的委託同格式——輸入輸出換成
    refine 前後的 CAID，單調性判定（$ID_{new}\sqsubseteq ID_{old}$）本身就是一次可委託
    的離散計算。

---

## 7. 視角消融、冗餘與分散式 GC

### 7.1 視角消融 (Perspective Ablation)

若從不同視角收到衝突的收斂結果，本地引擎執行 **Bohrification 疊加**：
1.  將結果視為聯集態 $A \mid B$。
2.  計算兩者的譜能量殘留，保留幾何質量更穩定（低熵）的分支。

### 7.2 部分觀測與幾何冗餘 (Semantic Data Availability)

**問題**：若一個 Combo 的 CAID 由子節點 A、B、C 構成，B 節點的物理機器斷線，這個 CAID 在全域格論中進入什麼狀態？

**譜冗餘（Spectral Redundancy）**：

LADD 不能只靠單純的資料副本（Replication），而是利用 **「語義糾刪碼」**——若 A 且 C 的資訊量足夠大（譜維度足夠高），可以從幾何邊界**限制出 B 的可能範圍**：

```
完整 CAID = P_A & P_B & P_C
當 P_B 不可達時：
  已知資訊 = P_A & P_C
  P_B 的可能範圍 = P_{\top} (萬有投影，任何值皆相容)
  觀測結果 = CAID_blur (標記 #incomplete, %cause: #partial_geometry)
```

系統維持 `#blur` 觀測直到 P_B 重新上線，或其他節點提供 P_B 的 `#refine` 等價物。

**與 Invariant 2 的關係**：這不違反資訊單調性——我們沒有減少已知資訊，而是誠實地標記「我們暫時無法觀測到 P_B」。

### 7.3 語義日蝕攻擊與視界震盪防禦 (Semantic Eclipse Attack)

**問題**：惡意節點提供一套完全自洽但與全域宇宙隔離的「權威格論」，讓目標節點的所有查詢被導向惡意的 `#refine` 路徑。

**防禦機制：多重宇宙交叉觀測（Cross-Universe Observation）**：

引擎必須具備「視界震盪」能力：

1. **隨機跳出**：定期隨機選取不在當前信任格中的節點，抓取相同 CAID 的譜指紋。
2. **譜連續性驗證**：同一個 `ID_old` 在不同信任路徑下，其 `#refine` 結果必須滿足格論序位一致性——若 A 主張 `ID_old \rightarrow ID_{new_A}`，B 主張 `ID_old \rightarrow ID_{new_B}`，則必有 $P_{new_A} \sqcap P_{new_B} \neq P_{\bot}$（兩個精煉必須譜相容），否則觸發警告。
3. **譜不連續警告**：

```nlang
%cause: #semantic_isolation {
    id:               "被質疑的 CAID"
    trusted_refine:   "ID_new_A"
    external_refine:  "ID_new_B"
    conflict:         "P_new_A & P_new_B == _|_"
}
```

### 7.4 幾何蒸發與分散式 GC (Geometric Evaporation)

**問題**：Invariant 2 規定資訊只能增加，但產生了 `_|_` 的 Commit 鏈、被廢棄的實驗性分支，會不會永遠堆積在網路中？

**譜蒸發（Spectral Evaporation）**：

LADD 引入類熱力學機制。每個 CAID 節點維護一個**譜熵（Spectral Entropy）**指標：

$$S(CAID) = -\text{Tr}(P \log P)$$

物理節點在資源壓力下可以優先「遺忘」高熵（低穩定度）的幾何孤島，只保留「真理主幹」。

**關鍵語義保證**：

1. **遺忘不等於刪除**：節點可以丟棄高熵 CAID 的本地副本，但**必須保留 CAID 字串本身及其因果鏈指標**。若未來有其他節點查詢，回傳 `#not_found`，讓查詢者透過 L2 尋找其他副本。
2. **不違反 Invariant 2**：被遺忘的 Commit 在邏輯上仍然存在於宇宙中，只是這個節點暫時無法觀測。這和 `#blur`（視界不足）一樣，是誠實的物理局限，不是語義刪除。
3. **熱力學類比**：低熵（高譜純度）的 CAID 相當於「被更多觀測確認」的態，在網路上自然更穩定。

---

## 8. 開放問題

以下問題是 Phase 4 實作前需要解決的理論難題：

| 問題 | 難度 | 與現有規格的關聯 |
| :--- | :--- | :--- |
| 服務幾何的譜標準化表示 | 高 | **[SPEC_03](./SPEC_03_Combo_System.md)** Combo、**[SPEC_13](./SPEC_13_Ouroboros_Discovery_Protocol.md)** CAID |
| LADD L3 的譜路由演算法 | 極高 | **[GUIDE_02](./GUIDE_02_Engine_Optimization.md)** 熱帶剪枝、**[APP_01](./APP_01_Tropical_Geometry.md)** |
| 譜熵指標的熱力學精確定義 | 中 | **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** `%fuel`、**[REAL_01](./REAL_01_Ouroboros_Engineering.md)** §11 |
| GPP/CIP 的 STARK 可行性 | 極高 | **[APP_02](./APP_02_Formal_Verification.md)** 形式化驗證 |
| 語義日蝕攻擊的譜防禦協議 | 高 | **[SPEC_13](./SPEC_13_Ouroboros_Discovery_Protocol.md)** §7 信任格論 |
| 跨 Epoch 的 LADD 譜相容性 | 中 | **[ORDER_01](./ORDER_01_Evolution_and_Governance.md)** §1.3 跨 Epoch 共存 |

---

## 附錄：與現有規格的對應

| 本章節 | 對應規格 |
| :--- | :--- |
| §2 譜協議架構 | **[SPEC_13](./SPEC_13_Ouroboros_Discovery_Protocol.md)** §6（`~%Discovery`）、**[REAL_02](./REAL_02_Ouroboros_Protocols.md)** |
| §3 數學基礎 | **[APP_04](./APP_04_Mathematical_Foundations.md)** 投影算子、譜幾何 |
| §4 引力路由 | **[GUIDE_03](./GUIDE_03_Incremental_Convergence.md)** §2（路線分析） |
| §5 GPP | **[COSMOLOGY/01 §8](./COSMOLOGY/01_PHYSICS_Unified_Field_Theory.md)** 譜諧振 |
| §6 CIP | **[APP_02](./APP_02_Formal_Verification.md)** ZKP、形式化驗證；**[COSMOLOGY/01 §8](./COSMOLOGY/01_PHYSICS_Unified_Field_Theory.md)** 相位鎖定；**[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** §4.1.1 `#branching`（多值幾何的判定與處理） |
| §7 視角消融 | **[SPEC_13](./SPEC_13_Ouroboros_Discovery_Protocol.md)** §5.3（別名消融） |
| §7.2 部分觀測 | **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** §4.2（`#blur`）、**[SPEC_13](./SPEC_13_Ouroboros_Discovery_Protocol.md)** §5.1 |
| §7.3 日蝕攻擊 | **[SPEC_13](./SPEC_13_Ouroboros_Discovery_Protocol.md)** §5.3（別名消融）、§7（信任格論） |
| §7.4 譜蒸發 | **[REAL_01](./REAL_01_Ouroboros_Engineering.md)** §11（物件生存週期）、**[SPEC_00](./SPEC_00_Introduction.md)** Invariant 2 |

---

> **結語**：LADD 協議將全球網路轉化為一個連續的量子幾何場。在譜指紋的導航下，真理不再是孤島，而是透過語義引力緊密連結的整體。當觀測者釋放足夠的能量，真理必將在 Hilbert 空間中顯現其唯一的截面。

---

## 參考文獻 (References)

1.  **Lohmiller, W., & Slotine, J. J. (2024)**. "On computing quantum waves exactly from classical and relativistic action." *arXiv:2405.06328* [quant-ph]. https://arxiv.org/abs/2405.06328
    *   **核心洞見**：量子波函數可以從有限個古典極值路徑精確重建：$\psi = \sum_j \sqrt{\rho_j} e^{i\phi_j/\hbar}$。這為 LADD 的「有限路徑計算」與「密度加權」提供了物理基礎。
    *   **對 n/ 的影響**：分支點 (branch points) 不是錯誤，而是多值幾何的合法現象——這直接啟發了 SPEC_12 §4.1.1 `#branching` 的設計。
