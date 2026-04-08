# GUIDE_03：增量收斂引擎設計 (Incremental Convergence Engine)

> **Authority**: [Recommendation / 非規範性建議]
> **Phase Target**: Phase 3 / 4
> **Status**: Draft

本指南整理 Phase 3/4 推進時面臨的核心工程挑戰，並評估三種架構路線的取捨，最終提出建議的混合策略。

---

## 1. 問題根源：為什麼全量合併行不通

Phase 1/2 的引擎採用「靜態 Genesis 模式」：

```
讀取所有定義 → 執行全量 Unify → 回傳觀測結果
```

這在小規模時沒問題。但進入 Phase 3/4 後，一個 Combo 可能引用來自全球各地的數千個 CAID。每次修改一行代碼就重新計算數百萬個節點的交集，效能是災難性的。

**核心矛盾**：n/ 的格論語義要求「資訊單調增加」（Invariant 2），但增量計算的本質是「只重算變動的部分」。如何在不違反單調性的前提下做增量，是這個問題的根本張力。

---

## 2. 三種架構路線的分析

### 路線 A：語義快取層 (Semantic CAID Cache)

**原理**：利用 CAID 的不變性。`A & B` 的結果恆等，可建立全域快取：

```
(CAID_A, CAID_B) → CAID_Result
```

子結構的 CAID 若未變動，合併結果可直接查表跳過計算。

**與現有規格的對應**：
- **[REAL_01](./REAL_01_Ouroboros_Engineering.md)** §3.3 的「增量依賴追蹤」已為此預留空間
- **[REAL_01](./REAL_01_Ouroboros_Engineering.md)** §10.2「計費不變性」規定 MBU 是邏輯步數，快取命中可合法跳過計費

**適合場景**：
- 靜態 Combo 的大量重複合併（如標準庫 `~%Math`）
- 態射的純函數部分（`#pure` 效果標記）

**問題**：
- 態射的動態執行（Pattern Matching、Functor Lifting）難以有效快取
- 內存壓力大時的 Cache Eviction 策略複雜
- 聯集態（`A | B`）的中間結果快取語義不穩定

---

### 路線 B：響應式幾何圖 (Reactive Dependency DAG)

**原理**：每個節點追蹤其依賴座標，定義變動時只有依賴它的節點標記為 `Dirty`，在下次觀測時重新收斂。類似 Excel 的響應式計算網路。

**與現有規格的對應**：
- **[REAL_01](./REAL_01_Ouroboros_Engineering.md)** §3.3 §3 已明確：「僅對 DAG 中受影響的節點標註為髒（Dirty）」
- **[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** §1.1「靜止循環」（`a: b, b: a` 收斂為 Top）需要特別處理，否則 Dirty 傳播進入 SCC 後永無終止

**適合場景**：
- 頻繁局部修改的開發工作流
- REPL 模式下的增量收斂

**問題**：
- **[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** 的循環依賴（強連通分量/SCC）需要在 Dirty 傳播前先偵測處理
- 資訊單調性（Invariant 2）在每層展開的驗證成本高
- 維護支援「資訊單調增加」的響應式圖，需要參考 Differential Dataflow 演算法

---

### 路線 C：原子斷言流 (Atomic Assertion Stream)

**原理**：宇宙不存儲為巨樹，而是一串原子斷言：

```
path.a: 1, path.b: 2, path.c: @int, ...
```

新定義追加到流的末尾，引擎只計算「新斷言」與「當前坍縮態」的交集。

**與現有規格的對應**：
- **[SPEC_10](./SPEC_10_Evolution_and_Commit.md)** 的 Commit 模型天然對應「斷言流的快照」
- **[REAL_02](./REAL_02_Ouroboros_Protocols.md)** 的分散式協定可直接將 Commit 作為斷言流交換

**適合場景**：
- Phase 4 的分散式同步（多節點的宇宙合併）
- Append-only 的演化日誌

**問題**：
- 態射分派（極小元素規則，**[SPEC_06](./SPEC_06_Unification_Logic.md)** §1.4）在扁平結構下搜尋困難，需額外索引
- `~` 私有欄位的幾何隔離（**[SPEC_04](./SPEC_04_Navigation_and_Duality.md)** §3）在扁平化後邊界模糊

---

## 3. 三路線對照表

| 維度 | 路線 A：CAID 快取 | 路線 B：響應式 DAG | 路線 C：斷言流 |
| :--- | :--- | :--- | :--- |
| **靜態合併效能** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **動態態射效能** | ⭐ | ⭐⭐⭐ | ⭐⭐ |
| **分散式適配** | ⭐⭐ | ⭐ | ⭐⭐⭐ |
| **循環依賴處理** | ⭐⭐ | ⭐（需 SCC 特殊處理） | ⭐⭐ |
| **實作複雜度** | 低 | 高 | 中 |
| **規格符合度** | 高 | 中（需擴充） | 高 |

---

## 4. 建議：A + B 混合的結構化記憶化

對 Phase 3 而言，**路線 A 作為底層、路線 B 作為上層**的混合體最為務實。

### 4.1 分層策略

```
觀測請求
    ↓
[Layer B] 響應式 DAG — 局部 Dirty 判定
    ↓ (僅 Dirty 節點)
[Layer A] CAID 快取 — 合併結果查表
    ↓ (Cache Miss)
[底層] 真正的 Unification 計算
```

### 4.2 關鍵實作點

**節點級穩定身份（Lazy CAID）**

每個 Value 內部存儲 `lazy_id`，合併後若未觀測則不急於計算 CAID：

```rust
fn unify(a: Value, b: Value) -> Value {
    let key = (a.id(), b.id());  // lazy 計算
    if let Some(res) = GLOBAL_MEMO.get(&key) {
        return res.clone();
    }
    let result = do_unify(a, b);
    GLOBAL_MEMO.insert(key, result.clone());
    result
}
```

**按需收斂（On-demand Convergence）**

觀測 `user.name` 時，不應連帶收斂 `user.address`，除非兩者有邏輯依賴。這需要 DAG 的依賴邊在「首次觀測時」才建立（Lazy Edge Construction）。

**循環依賴的安全處理**

**[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** §1.1 已定義語義：純路徑循環（`a: b, b: a`）收斂為 `_`。引擎需在 DAG 的 Dirty 傳播前先做 SCC 偵測，對靜止循環節點跳過 Dirty 傳播，防止無限循環。

---

## 5. Phase 4 的前瞻：斷言流的嵌入

路線 C 不應被拋棄，而是作為 Phase 4 分散式同步的傳輸層：

```
本地引擎（A+B 混合）← 接收 → 遠端斷言流（路線 C）
                              ↕ 轉換
                         本地 Commit 快照
```

遠端節點以斷言流推送新的 Commit，本地引擎接收後轉換為 DAG 的局部 Dirty 更新，再透過 CAID 快取加速合併。三條路線各司其職。

---

## 6. 核心技術決策點

### 選項 1：純粹路徑（維持樹狀結構）

維持樹狀 Combo 結構，實作深度遞迴的記憶化。

- ✅ 最符合格論直覺，與 **[SPEC_03](./SPEC_03_Combo_System.md)** 的 Combo 語義一致
- ✅ 天然對接 **[GUIDE_02](./GUIDE_02_Engine_Optimization.md)** 的熱帶幾何剪枝優化
- ✅ `~` 私有視界的幾何隔離（**[SPEC_04](./SPEC_04_Navigation_and_Duality.md)** §3）自然維持
- ⚠️ 海量數據時可能遇到遞迴深度或內存碎片問題
- **建議**：Phase 3 的主力策略

### 選項 2：數據流路徑（扁平 KV 存儲）

將宇宙扁平化為 Key-Value 存儲，所有合併為資料庫更新操作。

- ✅ 能處理海量數據，存儲引擎技術成熟
- ❌ 態射執行（極小元素匹配，**[SPEC_06](./SPEC_06_Unification_Logic.md)** §1.4）在扁平結構下需要額外索引
- ❌ 幾何隔離（`~` 私有視界）在扁平化後邊界模糊
- **建議**：作為 Phase 4 的分散式存儲後端，不應作為主引擎邏輯層

**結論**：Phase 3 選擇選項 1，配合 **[GUIDE_02](./GUIDE_02_Engine_Optimization.md)** §1.2 的熱帶剪枝。Phase 4 在存儲後端引入選項 2，但引擎邏輯層仍保持選項 1 的樹狀語義。

---

## 7. 三個待解決的核心難題

### 難題 1：格論語義下的終止度量

**問題**：如何為運算遞迴定義通用的「遞迴下降度量（Termination Metric）」？

**[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** §3 已區分兩類遞迴：
- **結構遞迴**（`@List: { head: @any, next: @List | #none }`）：惰性展開，天然不觸發停機問題
- **運算遞迴**（`/fib: x -> /fib (x-1) + /fib (x-2)`）：需要終止度量

對運算遞迴，建議用**格論高度（Lattice Height）**作為度量：

$$h(x) = \text{distance from } x \text{ to } \bot \text{ in the lattice}$$

每次展開後若輸入的格論高度嚴格遞減，靜態分析器可給出「保證終止」標記（**[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** §4.2 的 `%termination_proof`）。

**仍未解決**：非數值型結構（如異質 Combo）的高度定義，以及多參數遞迴的聯合度量。

---

### 難題 2：發散的早期偵測

**問題**：如何在不耗盡 `%fuel` 的前提下提早判定 `#divergent`？

建議的演算法——**狀態指紋（State Fingerprint）**：

引擎在每次遞迴展開時記錄三元組 `(path, input_CAID, depth)`：
- 若相同三元組出現兩次 → **靜止循環** → 立即回傳 `_`
- 若同一 path 的 input_CAID 連續 $k$ 次都是新的，且格論高度無下降趨勢 → **疑似發散** → 判定 `#divergent`

整體在 $O(k \cdot n)$ 時間內完成，可配合 **[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** §4.2 的 `%termination_proof: #safe` 作為逃生門。

**仍未解決**：最佳 $k$ 值選取，以及跨路徑的發散傳播偵測（一個發散的態射呼叫另一個本身正常的態射）。

---

### 難題 3：資訊單調性驗證的成本

**問題**：遞迴每層是否都需要 $O(\text{Merge})$ 的單調性驗證？在深層遞迴中這會導致指數級開銷。

**三個降本策略**：

1. **靜態保證跳過驗證**：若靜態分析器已給出「保證終止」標記（**[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** §3.1），該路徑天然保證單調，無需運行時驗證。

2. **以 CAID 版本號代替完整合併**：比較前後兩層的 input_CAID——相同則靜止循環（不需驗證）；不同則只做方向判斷（是否往 Bottom 方向走），而非完整的 $O(\text{Merge})$ 計算。

3. **跳躍式驗證（Checkpoint）**：每消耗 16 MBU（見 **[REAL_01](./REAL_01_Ouroboros_Engineering.md)** §10）做一次 Checkpoint，驗證累積單調性，而非每步都驗。

這將最壞情況從 $O(depth \times \text{Merge})$ 降為 $O(\frac{depth}{k} \times \text{Merge})$。

**仍未解決**：如何選取 Checkpoint 間距，以及在 `#approximate` 策略（**[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** §4.2）下如何放寬驗證頻率而不違反 Invariant 2。

---

## 9. 漸進式觀測體驗 (User Experience & Feedback)

由於真理積分（**[COSMOLOGY/10](./COSMOLOGY/10_TOPOLOGY_The_Truth_Integral.md)**）是一個過程，引擎實作者應提供對應的漸進式反饋機制。

### 9.1 漸進式 UI 渲染 (Progressive Rendering)
利用 `#blur` 狀態實現「先模糊，後精確」的互動體感：
*   **模糊佔位**：當觀測觸及視界邊緣時，引擎立即返回帶有 `%strategy: #blur` 的 CAID。UI 層應顯示為半透明或動畫狀態，代表「真理正在坍縮中」。
*   **斷點續傳**：利用 **[REAL_01 §10](./REAL_01_Ouroboros_Engineering.md)** 的 MBU 累積特性，使用者增加 `%fuel` 後，UI 應從上次的中斷點（截面）直接繼續渲染，避免畫面閃爍。

### 9.2 視界震盪實務 (Horizon Oscillation)
在 LADD 導航中，為了避免被語義黑洞（**[COSMOLOGY/05](./COSMOLOGY/05_PHYSICS_Semantic_Gravity.md)**）遮蔽，引擎應實作震盪機制：
*   **隨機跳躍 (Stochastic Jump)**：每隔一定數量的 MBU，引擎應強行隨機選取一個非引力中心的鄰居節點進行交叉觀測。
*   **指令實現**：建議實作 `oo horizon-oscillate` 指令，允許使用者手動觸發「邏輯躍遷」，跳出當前的信任格邊界。

---

## 10. 與現有規格及附錄的對應索引

| 本指南章節 | 對應規格文件 |
| :--- | :--- |
| §2 路線 A（CAID 快取） | **[REAL_01](./REAL_01_Ouroboros_Engineering.md)** §3.3、**[REAL_01](./REAL_01_Ouroboros_Engineering.md)** §10 |
| §2 路線 B（響應式 DAG） | **[REAL_01](./REAL_01_Ouroboros_Engineering.md)** §3.3、**[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** §1 |
| §2 路線 C（斷言流） | **[SPEC_10](./SPEC_10_Evolution_and_Commit.md)** Commit 模型、**[REAL_02](./REAL_02_Ouroboros_Protocols.md)** |
| §4 結構化記憶化 | **[SPEC_06](./SPEC_06_Unification_Logic.md)** §1.4、**[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** §3 |
| §7 難題 1（終止度量） | **[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** §3.1、COSMOLOGY/01 ($m$) |
| §9 漸進式渲染 | COSMOLOGY/06 (測不準原理) |
| §9 視界震盪 | **[SPEC_13](./SPEC_13_Discovery_and_Package.md)** §7.2、COSMOLOGY/05 (引力) |
| 熱帶幾何剪枝 | **[GUIDE_02](./GUIDE_02_Engine_Optimization.md)** §1、**[APP_01](./APP_01_Tropical_Geometry.md)** |

---

*Phase 3 的核心目標：讓引擎在不失去格論語義的前提下，把「全量合併」的計算模型升級為「增量精煉」的計算模型。*

