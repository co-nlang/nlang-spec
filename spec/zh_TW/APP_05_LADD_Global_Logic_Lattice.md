# APP_05：全球邏輯格與 LADD 協議 (Global Logic Lattice & LADD)

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

    ttl:        @int & < 16
    signature:  b""                 ;; 譜加密簽名
}}
```

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

## 3.5 譜指紋提取與量子化 (Spectral Fingerprint Extraction)

### 3.5.1 v2 複數譜架構

CAID v2（REAL_03 §2.2）引入 `<masa_ref>` 和複數譜。Lattice Sketch 從實數特徵值擴充為複數譜 $[\lambda_1 e^{i\theta_1}, \lambda_2 e^{i\theta_2}, \ldots]$，
其中 $\theta_i$ 是該特徵向量相對於 MASA 參考系的相位角。

### 3.5.2 譜指紋計算流程

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

### 3.5.3 量子化與編碼

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

### 3.5.4 Lattice Sketch 編碼

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

### 3.5.5 跨架構穩定性保障

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

---

## 5. 幾何機率證明 (GPP)

**GPP (Geometric Probability Proof)** 是支撐「氣味搜尋」的零知識證明機制。它如同 **「譜儀量測」**——觀測者無需下載完整數據，僅透過比對譜指紋即可判斷目標的幾何相容性。

### 5.1 譜邊界證明

當節點收到 `DiscoverRequest`，可回傳 GPP 證明：

```nlang
@GPP_Proof: {{
    target_caid:    @caid           ;; 被請求內容的譜指紋
    spectrum_hash:  @hash           ;; 譜摘要的雜湊承諾
    boundary_proof: b""             ;; STARK 證明：此譜特徵位於請求邊界內

    ;; 信心度：基於譜重疊積分的機率估計
    confidence:     @float & [0.0..1.0]
}}
```

*   **物理意義**：GPP 證明 $P_{target}$ 與 $P_{query}$ 的譜重疊積分 $\text{Tr}(P_{target} P_{query}) > \theta$，無需揭露 $P_{target}$ 的完整結構。
    v2 擴充為複數譜：$\text{Re}(\text{Tr}(P_{target}^\dagger P_{query})) > \theta$，其中 $P_{target}^\dagger$ 包含 MASA 相位共軛。

### 5.2 氣味路由決策

節點可根據 GPP 的 `confidence` 決定是否轉發：
*   **高信心度 (>0.8)**：本地可能包含目標，進入嚴格搜尋模式。
*   **中等信心度 (0.3-0.8)**：繼續沿測地線轉發請求。
*   **低信心度 (<0.3)**：譜特徵不相干，返回 `#not_found`。

---

## 6. 因果完整性證明 (CIP) 與幾何預言機

### 6.1 幾何預言機 (Geometric Oracle)

當本地設備算力不足以執行巨大子空間的合併時，可委託給網路上的 **幾何預言機**——具備高計算能力的節點，專門處理複雜的譜收斂運算並生成 CIP 證明。

**譜計算委託流程**：

```
本地節點（低算力）               幾何預言機
    |                               |
    |-- 委託: P_A & P_B --------> |
    |                               |-- 執行投影算子 Meet
    |<-- 結果 P_C + CIP ---------|
    |
    |-- 本地驗證: verify(CIP) --> 確認計算正確
    |-- 接受 P_C 作為本地觀測結果
```

### 6.2 CIP 的譜相位鎖定

**CIP (Causal Integrity Proof)** 如同 **「相位鎖定 (Phase Locking)」**：
*   **證明內容**：利用 STARK 證明 $P_C = P_A \sqcap P_B$ 的運算嚴格遵循正交模格公設。
*   **相位連續性**：證明在精煉路徑（`#refine`）的轉遷過程中，子空間的幾何本質被連續且一致地鎖定在新的 CAID 中。
*   **v2 複數譜**：CIP 現在鎖定的是複數譜（振幅 + 相位），相位資訊來自 CAID 的 `<masa_ref>`。驗證者需檢查 $\text{Re}(\text{Tr}(P_C^\dagger P_A))$ 和 $\text{Re}(\text{Tr}(P_C^\dagger P_B))$ 的相位連續性——跨 MASA 的相位躍遷記錄在 `%cause` 的 `%cocycle` 中。
*   **非對稱性**：驗證者僅需比對複數譜摘要即可確認計算的幾何真實性，驗證成本 $O(1)$ 遠低於執行成本 $O(N)$。

#### 6.2.1 理論基礎：多值古典作用量與密度路徑積分

CIP 的設計深受 Lohmiller & Slotine (2024) 的量子-古典對應理論啟發。該論文證明了精確的量子波函數可以從**有限個古典極值路徑**重建：

$$\psi = \sum_{j \in J} \sqrt{\rho_j} \cdot e^{\frac{i}{\hbar}\phi_j}$$

其中 $\phi_j$ 是第 $j$ 條古典極值路徑的作用量，$\rho_j$ 是沿該路徑計算的古典密度。

**對 CIP 的設計啟示**：

1.  **有限路徑原則**：如同論文取代 Feynman 無窮路徑積分，CIP 不需要傳輸所有中間計算狀態，只需傳遞**極值路徑的最終結果**加上完整性證明。

2.  **密度加權的幾何質量**：論文中的 $\sqrt{\rho_j}$ 對應 LADD 的**幾何質量** $m = \text{Tr}(P_C)$。每個分支的「信任權重」正比於其幾何體積（資訊豐富度）。

3.  **在傳輸中解決**：論文的核心洞見是「波函數計算可以在古典路徑上解析完成」，這正是 CIP 的運作模式——幾何預言機在轉發路徑上執行計算，本地節點只驗證結果。

**相位鎖定的物理類比**：
CIP 確保了在分散式環境中，不同節點對同一子空間的觀測結果具有**相位相干性**——如同論文中多條古典路徑的相位 $e^{i\phi_j/\hbar}$ 在測量時正確干涉，產生精確的量子機率。

**最終洞見**：計算不再發生在某台機器上，而是**在傳輸過程中被解決**。網路成為一個具備格論計算能力的量子流體。每一條 LADD 路由路徑，同時也是一條計算管道。

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
| §5 GPP | **[COSMOLOGY/15](./COSMOLOGY/15_PHYSICS_Semantic_Resonance.md)** 譜諧振 |
| §6 CIP | **[APP_02](./APP_02_Formal_Verification.md)** ZKP、形式化驗證；**[COSMOLOGY/15](./COSMOLOGY/15_PHYSICS_Semantic_Resonance.md)** 相位鎖定；**[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** §4.1.1 `#branching`（多值幾何的判定與處理） |
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
