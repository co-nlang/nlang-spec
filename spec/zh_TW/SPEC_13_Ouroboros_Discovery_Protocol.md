# n/ Language Specification - 銜尾蛇發現協定 (OODP)

> **OODP (Ouroboros Discovery Protocol)**：Ouroboros 引擎間進行內容定址、發現與信任管理的**語言層協定規範**。

本章節定義 `n/` 宇宙透過子空間投影特徵定位節點，並將其轉化為**宇宙發現機制**。
發現（Discovery）是語言層的本體論概念，與部署方式或傳輸協定無關。

---

## 0. 協定架構：五層譜模型與混合設計

OODP 採用**混合架構**：L2 定址層基於傳統 DHT（如 Kademlia），L3 以上導入譜幾何優化。這是一個**工程妥協**——純粹的格論路由在實作上存在根本性限制。

### 為何需要混合架構？

**純粹譜路由的困難**（OODP 的理想）：
- 譜指紋（Lattice Sketch）是高維連續向量，不像 160-bit 節點 ID 離散且可預測
- 譜距離 $d_L$ 難以建立確定性的路由表（無法像 XOR 距離那樣進行桶分區）
- 物理節點需要穩定標識（IP + Port），譜指紋會隨內容變化

**工程妥協的設計**：

| 層次 | 名稱 | 譜幾何對應 | 功能 | 實作參考 |
| :--- | :--- | :--- | :--- | :--- |
| **L1 物理層** | 傳輸載體 | 位元流傳輸 | TCP/UDP、libp2p、QUIC（傳輸原始位元） | **[REAL_02](./REAL_02_Ouroboros_Protocols.md)** |
| **L2 定址層** | 節點定位 | 譜指紋定位 | **Kademlia XOR 路由**（尋找**節點的物理位置**） | **[REAL_03](./REAL_03_CAID_Protocol.md)** |
| **L3 收斂層** | 譜收斂核心 | 投影算子 Meet | 分散式 `&` 運算、衝突判定 | **[REAL_02](./REAL_02_Ouroboros_Protocols.md)** |
| **L4 視角層** | Bohrification | 交換子代數過濾 | 權威格論、譜消融、主觀真理坍縮 | **本章 §7** |
| **L5 應用層** | 語義接口 | 觀測者交互 | `~%Discovery./find`、插件發現、全球實體互動 | **本章 §6** |

**關鍵設計**：L2 使用傳統 DHT 尋找**物理節點**（解決「這台機器在哪裡」），L3 以上才是譜感知路由（解決「這個子空間投影由誰服務」）。兩層各司其職，LADD 作為 L3-L5 的**譜幾何優化擴充**。

---

## 1. 核心哲學：Yoneda 視角下的身分

在 `n/` 宇宙中，一個子空間的身分不由它的名字決定，而是由它在 Hilbert 空間中展現的投影特徵決定。

### 1.1 內容定址標識符 (CAID)
**CAID (Content Addressable Identifier)** 是子空間結構的內在標識符，反映了其投影算子 $P_A$ 的譜幾何指紋。
*   **波粒二象性**：CAID 既具備抗碰撞的粒子指紋（Digest），也具備散發引力的波動譜摘要（Sketch）。
*   **Yoneda 原理**：物件由其關係決定。CAID 封裝了子空間投影算子與宇宙中其他算子間的干涉特徵。

### 1.2 觀測別名 (Observation Alias)
「名字」是人類觀測者建立的投影標籤。
*   **別名是相對的**：路徑 `_.deps.ui` 是一個觀測視角。
*   **CAID 是絕對的**：它定義了子空間在全域格論中的幾何座標。

### 1.3 CAID 的 symplectic 刻畫 (char-2 影子；Papers VII–XXII)

§1.1 的 CAID（Yoneda 關係指紋 = 投影算子 $P_A$ 的譜指紋）是 Paper I–VI 視角的概念定義。
理論論文系列 VII–XXII 為它補上了精確的代數刻畫：在 stabilizer / Pauli 的特徵二影子裡，觀測代數
降到有限 symplectic 空間 $V=\mathbb{F}_2^{2n}$，而一個子空間的「關係指紋」就是它與其他算子的
**$\omega$（交換性）與 $q$（quadratic refinement，相位/符號）資料**，即 $\omega/q$-Gram。

*   **相位/符號的來源**：CAID v2 複數譜（REAL_03 §3.2）所編碼的 sign/phase，其代數本質是
    $\beta$ / quadratic refinement（Paper XI：$s(C)=(-1)^{\beta/2}$，$\beta_{\text{sum}}\equiv2\pmod4$）。
*   **投影算子的載體**：3-qubit 下，Bohrification 的投影算子由 $\mathrm{Sp}(6,\mathbb{F}_2)$ 在
    $\mathbb{C}^8$ 上的 **Weil 表示**具體實現（Paper XV）。
*   **跨 context 關係**：不同 context 間的 $\omega$ 關係由 cross-context anticommutation 定理刻畫
    （Paper XVII）。

**一致性**：§1.1（概念）與本節（代數）是同一物的兩層 —— Yoneda 關係指紋的特徵二影子 $=\omega/q$-Gram。
本節為 §1.1 的延伸而非取代；CAID 物理封套（REAL_03）暫仍以複數譜實作，symplectic 指紋是其數學本體。

---

## 2. 發現機制：對萬有子空間的約束

在 `n/` 中，所有可能的子空間投影早已存在於萬有集合 `_` 之中。

### 2.1 發現即引力坍縮 (Discovery as Gravity Collapse)
當宣告一個依賴時，是在施加幾何定位約束。引擎透過 **LADD 協議**（L3-L5 優化層）感受譜引力，將路徑坍縮至符合特定 CAID 特徵的子空間。

### 2.2 內容驗證與譜合約 (Spectral Contract)
發現本質上是 **`&` (合併)** 運算，可對發現結果施加額外約束：
```nlang
deps: {
    @db.driver: "hash:blake3:v1:7f8a..." & {
        /connect: @morphism     ;; 驗證投影算子具備連線能力
    }
}
```

---

## 3. 發現與自舉 (Bootstrapping: The Big Bang)

CAID 系統依賴「內容已被發現」的假設。為了打破「雞生蛋、蛋生雞」的循環，`n/` 定義了**種子節點 (Seed Nodes)** 機制。

### 3.1 引擎內建種子 (Hardcoded Seeds)

Ouroboros 引擎在編譯時會內建一組核心規格的 CAID 及其對應內容。以下為創世必須包含的**核心種子清單**：

| 種子路徑 | 角色 | 創世 CAID (Placeholder) |
| :--- | :--- | :--- |
| **`~%List`** | 列表處理原語 | `hash:sha256:v1:seed01...` |
| **`~%Math`** | 算術與數學運算 | `hash:sha256:v1:seed02...` |
| **`~%Logic`** | 態射與柯里化控制 | `hash:sha256:v1:seed03...` |
| **`~%Engine`** | 觀測與演化原語 | `hash:sha256:v1:seed04...` |
| **`~%Discovery`** | 發現與 CAID 解析 | `hash:sha256:v1:seed05...` |

*   **規範化實作保證**：標準庫的 CAID 由其**規範化後的 `n/` 原始碼內容**決定。所有符合規格的引擎，其內建標準庫源碼的 CAID 必須與官方規格書提供的種子完全一致。

### 3.2 創世 Commit (Genesis Commit)

宇宙的第一個 Commit $C_0$ 包含了所有標準庫的根路徑映射。
*   **全域唯一性**：所有符合規格的引擎在初始化時，其 `_` 路徑下的標準庫節點之 `%id` 必須完全一致。
*   **譜凍結保證**：標準庫的 CAID 由其規範化後的譜特徵決定，全宇宙絕對一致。

---

## 4. CAID 格式與封套協議

規格書定義 CAID 的邏輯結構，具體的演算法實作由 **[REAL_03](./REAL_03_CAID_Protocol.md)**（L2 定址層）決定。

### 4.1 標準格式 (CAID Envelope)

CAID 字串是一個**自描述的幾何封套 (Self-describing Envelope)**。其格式確保了在不進行雜湊運算前，引擎即可獲取必要的物理元資訊。

#### 4.1.1 物理協議與編碼 (Physical Protocol)

為了保證全域宇宙的一致性，CAID 的物理表現形式（如 BNF 語法、摘要編碼方式、雜湊演算法清單）由 **OODP L2 定址層**統一定義（詳見 **[REAL_03: CAID 物理協議](./REAL_03_CAID_Protocol.md)**）。

#### 4.1.2 規格義務 (Specification Obligations)

1.  **內容唯一性**：相同的內容在相同的格式版本 (`fmt_version`) 下，產生的 CAID **必須** 全宇宙唯一且決定。
2.  **版本語義隔離**：
    - **格式版本 (`fmt_version`)**：定義 AST 規範化的物理規則。
    - **語言版本 (Spec Version)**：定義語言語義。
    - 兩者為多對一映射關係。

### 4.2 跨版本精煉 (Cross-version Refinement)

當 `fmt_version` 升級導致 CAID 變更時，必須透過 **`#refine` (精煉 Commit)** 建立新舊 CAID 的因果連結（詳見 **[SPEC_10](./SPEC_10_Evolution_and_Commit.md)**）。這允許宇宙在物理格式演進的同時，保持邏輯上的身分連續性。

### 4.3 CAID 等價性判定規則

判定不同演算法或版本的 CAID 是否等價（幾何一致）的程序如下：

1.  **讀取封套**：從 CAID 字串直接提取 `fmt_version` 與 `algo`。
2.  **解析 (Parse)**：使用該版本規則將內容還原為 AST。
3.  **重規範化 (Re-normalize)**：使用當前引擎預設的最新版本規則對 AST 進行重排。
4.  **重雜湊 (Re-hash)**：使用預設演算法重新計算。若結果一致，則判定兩者等價。

---

## 5. 漸進式真理與精煉共識

真理不是一次性的坍縮，而是沿著格不斷深化的過程。

### 5.1 身份分類與生命週期
*   **`CAID_exact` (#exact)**：本質身分。由子空間本體決定。
*   **`CAID_blur` (#blur)**：局部截面快照。標識「在特定能量限制下的觀測事實」。
    *   **固化原則**：一旦寫入 Commit，`CAID_blur` 即代表當時的認識狀態。

### 5.2 精煉語義與自動重定向 (Refinement)

當一個模糊節點被證實符合某個精確節點時，發生**精煉 (Refinement)**。

1.  **精煉宣告**：透過 **[SPEC_10](./SPEC_10_Evolution_and_Commit.md)** 定義的 `#refine` 操作，發布一個精煉 Commit。
2.  **格論序位約束**：$E \sqsubseteq B$。精煉是資訊增加的過程。精煉成立的充要條件是 $E$ 位於 $B$ 定義的幾何邊界內。
3.  **自動重定向演算法 (Auto-Redirect)**：
    - **索引維護**：引擎應維護一個精煉映射表 `RefineMap: BlurCAID -> Set<ExactCAID>`。
    - **重定向邊界 (Redirection Boundary)**：
        - **允許範圍**：引擎僅能在 **「觀測視窗 (Live Observation)」** 或 **「暫存演化 (Staged Area)」** 中觀測自動重定向（將 $B$ 靜默替換為 $E$）。這加速了開發時的真理收斂。
        - **嚴禁範圍**：對於已固化的 **歷史 Commit**，引擎 **嚴禁** 觀測隱性重定向。已寫入歷史的 `CAID_blur` 必須保持其原始語義，以防止「歷史回溯性坍縮」與內容定址漂移。

#### 5.2.1 跨演算法透明度 (Cross-Algorithm Transparency)

精煉機制支援**跨雜湊演算法**與**跨格式版本**的自動重定向：

1.  **不透明目標**：當 `CAID_source` 指向 `CAID_target` 且兩者使用不同雜湊演算法時：
    - 引擎只需驗證 `CAID_source` 的計算正確性。
    - `CAID_target` 被視為**不透明字串**，其正確性由 #refine Commit 的簽署權威背書。
2.  **格式版本隔離**：
    - 若 `CAID_source` 使用 `fmt_version: v1`，`CAID_target` 使用 `fmt_version: v2`：
    - 舊引擎（僅支援 v1）仍可解析 #refine Commit，因為其外層封套使用 v1 語法。
    - 新引擎（支援 v2）可進一步驗證 `CAID_target` 的內容正確性。
3.  **信任鏈傳遞**：
    - 若 A #refine 到 B，且 B #refine 到 C，則 A 自動重定向到 C。
    - 信任鏈的有效性取決於所有中間 #refine Commit 的簽署權威。
4.  **循環阻斷 (Cycle Prevention)**：
    - 引擎必須確保 `#refine` 重定向鏈不形成循環（如 A->B->A）。
    - **重定向深度限制**：為了防止分散式環境下的無限查詢，引擎在追蹤重定向鏈時，必須設定 **「最大跳轉次數 (Max Redirection Hops)」**（創世預設值：16 次）。
    - 若偵測到循環或超過深度限制，受影響的重定向路徑自動失效，觀測該 CAID 將返回 `_|_` (%cause: #refinement_cycle)。
5.  **目標多重性 (Target Multiplicity)**：
    - `target_caids` 允許定義為聯集態（如 `ID_new_A | ID_new_B`）。這支援了規格演化中的「幾何拆分」（Splitting）或「多重等價表示」。
    - **消融規則**：引擎在解析重定向時，應嘗試對所有目標分支進行觀測。若多個目標中僅有一個能與當前**計算視界 (Computational Horizon)** 的約束收斂，引擎應自動坍縮至該分支；若仍具備歧義，則維持聯集態。
6.  **影子精煉 (Shadow Refinement)**：
    當歷史 Commit $C$ 引用了已被精煉的 $B$ 時，引擎可選地在背景觀測「影子測試」：
    - **資源限制**：影子測試受 `~%Engine.shadow_fuel` 物理限制，且嚴禁阻塞主觀測路徑。
    - 若 $E$ 與 $C$ 的現有約束不衝突，則向觀測者發出 **「演化建議 (Evolution Hint)」**。
    - 若 $E$ 會導致 $C$ 坍縮為 `_|_`，則標記為 **「真相衝突 (Refinement Conflict)」**，要求人工或代理發起顯式的遷移 Commit。

### 5.3 別名疊加與消融 (Alias Superposition & Ablation)

當多個發現來源（Registries）對同一個別名提供不同的 CAID 映射時，`n/` 遵循格論的**疊加原理 (Superposition Principle)**：

1.  **聯集坍縮 (Union Collapse)**：
    若來源 A 提供 `pkg: ID_1`，來源 B 提供 `pkg: ID_2`，且兩者互不相容 ($ID_1 \sqcap ID_2 = \bot$)，則該別名的觀測結果為 **`ID_1 | ID_2` (聯集態)**。
2.  **精煉優先 (Refinement Overrule)**：
    若疊加態中的 `ID_1` 具備有效的 `#refine` 證明指向 `ID_2`（或其後繼者），引擎應自動坍縮至 `ID_2` 並移除 `ID_1` 的影子。精煉證明具備「邏輯時間優先性」。
3.  **自動消融 (Auto-Ablation)**：
    當疊加態的別名參與後續的格論運算（如 `pkg & @SpecificType`）時，不符合型別約束的分支會自動收斂至 `_|_` 並從聯集中移除。
    *   **語義效果**：這實現了「基於需求的衝突解決」。宇宙不需要知道哪個 `pkg` 是「正確」的，它只需要知道哪個 `pkg` 能滿足當前的幾何約束。
4.  **歧義殘留 (#ambiguous_alias)**：
    若經過所有約束運算後仍保留多個分支，引擎必須將其標記為 `#ambiguous_alias`。觀測者此時必須透過 **[§7 權威格論]** 顯式選擇一個偏好的觀測視點。

---

## 6. 系統發現介面 (`~%Discovery`)

這些態射定義了語言層如何驅動發現行為（L5 應用層）。

### 6.1 基礎原語 (Basic Primitives)

| 態射 | 說明 |
| :--- | :--- |
| **`./fetch <caid>`** | 在萬有集合中定位並坍縮該 CAID 的子空間。 |
| **`./alias <path>`** | 將指定路徑的內容合成為別名映射表。 |
| **`./identify <node>`** | 獲取指定節點的內在 CAID（即其 `%id`）。 |

### 6.2 幾何發現原語 (Geometric Discovery Primitives)

不同於傳統的名稱查詢，`n/` 支援基於「幾何特徵」的搜尋。這本質上是在語義空間中進行 **幾何場導航 (Geometric Field Navigation)**。

#### 6.2.1. 服務幾何 (Service Geometry)
節點可向網路宣告其具備的 **服務幾何**（一個 Combo），代表其能提供的幾何約束承諾。

#### 6.2.2. `./find <pattern>` (引力導航)
*   **輸入**：一個型別約束 `@Type` 或幾何模式。
*   **語義**：在全域邏輯格中，沿著幾何重力（型別交集路徑）導航至所有滿足 $Node \sqsubseteq Pattern$ 的節點。
*   **結果**：回傳一個包含所有匹配節點的聯集態。
*   **用途**：插件系統發現。例如 `~%Discovery./find @Plugin./Interface` 尋找所有實作了特定邊界的擴充功能。

### 6.3 LADD 協議規範

全域規模的發現行為可透過 **LADD (Lattice-Aware Distributed Discovery)** 協議進行譜幾何優化（詳見 **[APP_05](./APP_05_LADD_Global_Logic_Lattice.md)**）。

*   **物理實踐**：LADD 將發現過程定義為「幾何精煉路徑的自動選擇」。查詢請求天然向幾何質量重、約束具體的節點坍縮。
*   **效能保證**：[APP_05](./APP_05_LADD_Global_Logic_Lattice.md)** 是全域邏輯格進行收斂的物理實踐標準，優化後的引擎應確保其路由行為與格論距離 $d_L$ 一致。
*   **協定定位**：LADD 是 OODP L3-L5 層的**譜幾何優化擴充**，非強制基礎設施。

---

## 7. 權威與信任格論 (Authority & Trust Lattice)

在去中心化的發現中（L4 視角層），「信任」不是二元的（Yes/No），而是**觀測權重 (Observation Weight)**。

### 7.1 信任即約束 (Trust as Constraint)

信任來源（Trust Roots）被視為對萬有集合的**優先級標記**。

1.  **信任排序**：觀測者維護一個偏序集 $T$。當別名衝突發生時，引擎依照 $T$ 中的順序進行篩選。
2.  **極小元素優先**：若 $T$ 中定義了 `official > community`，則引擎優先坍縮至 `official` 提供的 CAID。
3.  **權威隔離**：不同的**觀測視域 (Observational Perspective)** 可以具備不同的信任格。這允許在同一個宇宙中，局部地使用未經社群審核的實驗性分支，而不影響全域的穩定性。

### 7.2 視界震盪與交叉觀測 (Horizon Oscillation)

為了防禦 **語義日蝕攻擊 (Semantic Eclipse Attack)** —— 即惡意節點群組提供一組自洽但與全域格論隔離的偽造權威與內容 —— 引擎 **必須** 實作視界震盪防禦機制：

1.  **隨機跳出 (Stochastic Jump)**：引擎在進行 `./fetch` 或引力導航時，必須以一定比例（創世預設值：1/64 MBU 觀測量）在當前「信任格」之外隨機選取節點進行交叉觀測。
2.  **幾何連續性驗證**：若不同信任路徑下的精煉結果在同一座標產生絕對衝突（`_|_`），引擎必須計算兩者的 **「幾何張力 (Geometric Tension)」**。
3.  **語義隔離警告 (#semantic_isolation)**：若偵測到系統性的幾何不連續（即多個不相關座標同時發生跨信任衝突），引擎必須向觀測者發出 `#semantic_isolation` 警告，並強制暫停自動重定向功能，直至觀測者手動進行視域校準。
4.  **因果溯源**：在警告狀態下，引擎應優先顯示引發衝突的鄰居節點 `node_id`，協助定位潛在的攻擊來源。

---

## 8. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_01](./SPEC_01_Foundation_and_Lattice.md)** | 萬有集合 `_` 是發現機制的源頭。正交模格公設。 |
| **[SPEC_06](./SPEC_06_Unification_Logic.md)** | 發現行為中的 CAID 匹配遵循統一化演算法的極小元素規則。 |
| **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** | 定義了影響 `CAID_blur` 的計算視界參數。 |
| **[SPEC_10](./SPEC_10_Evolution_and_Commit.md)** | 定義了驅動精煉變遷的 `#refine` 操作。 |
| **[APP_05](./APP_05_LADD_Global_Logic_Lattice.md)** | LADD 協議：OODP L3-L5 的譜幾何優化擴充。 |
| **[REAL_02](./REAL_02_Ouroboros_Protocols.md)** | OODP L1-L3 的傳輸層與基礎收斂協定實作。 |
| **[REAL_03](./REAL_03_CAID_Protocol.md)** | OODP L2 定址層：CAID 的物理編碼與雜湊規範。 |
| **[REAL_04](./REAL_04_Causal_Chain_Protocol.md)** | OODP 因果鏈協議：`%cause` 結構與錯誤傳播。 |
| **[COSMOLOGY/04](./COSMOLOGY/04_PHYSICS_Semantic_Gravity.md)** | 發現機制的數位物理學基礎：語義重力場。 |
| **[COSMOLOGY/01 §8](./COSMOLOGY/01_PHYSICS_Unified_Field_Theory.md)** | 諧振身分的物理詮釋（譜諧振，原第 15 章已併入）。 |

---

### 哲學思辨 (Philosophical Synthesis)

> 結語：內容即定址，發現即存在。在 Yoneda 的觀測下，宇宙不再有孤島，萬物皆透過其本質的特徵相互連結。
>
> 然觀測有限，而真理無窮。**精煉不是對過往的推翻，而是對幾何細節的細化；模糊的真理並非謊言，而是等待更多觀測與能量投入的莊嚴邀請。** 衝突在 `n/` 中不是錯誤，而是疊加的選擇；當約束降臨時，歧義消融，真理自顯。
