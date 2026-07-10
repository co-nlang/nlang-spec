# n/ Language Specification - 統一化邏輯 (Unification Algorithm)

本章節正式描述 `n/` 收斂引擎 (**銜尾蛇引擎 / Ouroboros Engine**) 的統一化邏輯規則。

---

## 1. 核心規則 (The Unification Algorithm)
當兩個節點 $A$ 與 $B$ 進行合併 $C = A \sqcap B$ 時，遵循下列規則：

### 1.1 原子與型別
1.  **等值合併**：若 $A = B$，則 $C = A$。
2.  **Top 合併**：若 $A = \_$，則 $C = B$。
3.  **Bottom 合併**：若 $A = \bot$ 或 $B = \bot$，則 $C = \bot$。
4.  **互斥原子**：若 $A, B$ 為不同原子，則 $C = \bot$。
5.  **精確度優先與吸收律 (Precision Primacy & Absorption)**：
    *   **定義**：格的深度代表資訊的精確度。`#exact` 節點在格中位於 `#blur` 節點之下 ($Exact \sqsubseteq Blur$)。
    *   **合併行為**：當一個精確值 $v$ 與一個模糊視界 $B$ 合併時，若滿足 $v \in B$，則結果為 $v$。
    *   **模糊合併**：兩個模糊視界 $B_1$ 與 $B_2$ 合併時，結果為兩者交集的模糊邊界 $B_{new} = B_1 \sqcap B_2$。
    *   **衝突判定**：若 $Exact \sqcap Blur = \bot$，則判定該精確值不在該模糊觀測的預期邊界內，引發因果衝突。
6.  **原子同構展開 (Atomic Isomorphic Expansion)**：
    當原子 (Atom) $v$ 與 Combo $C$ 進行合併時，為了維持「萬物皆 Combo」的一致性，原子會自動展開為 `{ %val: v }` 並進行遞迴合併。其細部衝突解決規則如下：

| 合併組合 | 結果 (Result) | 說明 |
| :--- | :--- | :--- |
| **v & {}** (空 Combo) | `{ %val: v }` | 原子被包裹後存入開放容器。 |
| **v & {name: "x"}** | `{ %val: v, name: "x" }` | 原子與不衝突的欄位平行存在。 |
| **v & {%val: v'}** | `{ %val: (v  &  v') }` | 若兩者皆有 `%val`，對其原子值進行格論合併。 |
| **v & {%val: v, ...}** | `{ %val: v, ... }` | 若原子值相同，結果保持該值。 |
| **v & {%val: v', ...}** | `_\|_` | 若 $v \neq v'$，引發原子層級衝突。 |
| **v & {{...}}** (Cocoon) | 依 Cocoon 規則 | 若 Cocoon 未宣告 `%val`，則合併失敗 (`_\|_`)。 |

    *   **案例**：`5 & { %val: 6, name: "x" }` 會收斂為 `{ %val: _|_ , name: "x" }`。
    *   **案例**：`5 & { %kind: #type }` 會收斂為 `{ %val: 5, %kind: #type }`。


### 1.2 Combo 的遞迴收斂
當 $A$ 與 $B$ 皆為 Combo 時，對其所有欄位路徑 $p$ 進行遞迴運算：
1.  **共通欄位**：若 $A.p$ 與 $B.p$ 皆存在，則 $C.p = A.p \sqcap B.p$。
2.  **獨有欄位 (疊加態預設)**：若僅 $A.p$ 存在，且 $B$ 是 Combo `{}`，則 $C.p = A.p$。
3.  **本徵態封閉違規**：若僅 $A.p$ 存在且為非 Top 值，但 $B$ 是 Cocoon `{{}}` 且未定義路徑 $p$，則根據本徵態預設，$B.p$ 隱含為 $\bot$，導致合併結果 $C.p = A.p \sqcap \bot = \bot$。這體現了 Cocoon 對外部非預期擴張的「拒絕權」。


### 1.3 聯集與分支收斂
在正交模格中，全域分配律（Global Distributive Law）並不成立。這意味著合併與聯集的順序會影響結果，反映了不相容觀測量的非交換性。

1.  **局部分配律 (Local Distributivity / Bohrification)**：
    分配律 $A \sqcap (B \sqcup D) = (A \sqcap B) \sqcup (A \sqcap D)$ 僅在 A、B、D 彼此 **「交換 (Commute)」** 時成立。
    *   **語義**：這對應於 Bohrification 中的一個特定「交換視角 (Perspective)」。在同一個觀測視角下，邏輯表現如經典分配格。
2.  **正交模律 (Orthomodular Law)**：
    格結構必須滿足：若 $A \sqsubseteq B$，則 $B = A \sqcup (B \sqcap !A)$。
    *   **物理意義**：這保證了子空間的分解與正交補的一致性。
3.  **分支化簡**：合併後若產生多個重複分支，自動進行冪等化簡。
4.  **空集消除**：若聯集中的某個分支坍縮為 `_|_`，該分支從聯集中移除。若所有分支皆為 `_|_`，則整體結果為 `_|_`。
5.  **保守性原則 (Conservatism)**：在執行極小元素篩選時，若兩個分支 $K_i$ 與 $K_j$ 因視界限制（具備 `#blur` 狀態）導致其子集關係 $K_i \subseteq K_j$ 為 **「不可判定 (Undecidable)」**，則引擎 **必須** 保留兩者，維持聯集態。這確保了在燃料不足時，引擎不會錯誤地丟棄潛在的合法路徑。

#### 1.3.1 障礙度標記 (Obstruction Degree)

當合併產生衝突時，引擎根據障礙等級在 `%cause` 中記錄 `%obstruction_degree`：

| 標籤 | 障礙等級 | 收斂行為 | 代數特徵 |
|:---|:---:|:---|:---|
| `#h1_phase` | $H^1$ | **可補償**，繼續收斂，路徑修正 | 兩 MASA 交集非空，有連續相位 |
| `#h2_sign` | $H^2$ | **不可補償**，必須分支 SPLIT | 四 MASA 交替乘積 $= -I$ |
| `#h3_gerbe` | $H^3$ | **視界擴張**，增加 `%fuel` 後重試 | 三重重疊關聯子失效 |
| `#h4_sybil` | $H^4$ | **信任隔離**，標記為女巫候選 | 神經複形頂點集被污染 |

- `#h1_phase` 時引擎應嘗試相位修正後繼續。修正規則：若兩 MASA 的 meet 非空，計算其幾何相位差 $\theta_{AB}$；若 $\theta_{AB} < \varepsilon_{coherent}$ 則合併，否則分支（詳見 REAL_03 §4.1 相位感知合併）。
- `#h2_sign` 時引擎必須保留所有衝突分支（非嚴格性，見 §1.7）。
- `#h3_gerbe` 和 `#h4_sybil` 為預留標籤，當前引擎可忽略，但必須記錄。

#### 1.3.2 上鏈格式 (Cocycle Format)

`%cause` 中的衝突記錄應遵循以下上鏈結構，使衝突的代數起源可被標準化追溯：

```nlang
%cause: {
  %degree:        <int>                   ;; 上同調維度：1 (H¹) / 2 (H²) / 3 (H³) / 4 (H⁴)
  %obstruction:   #h1_phase | #h2_sign | #h3_gerbe | #h4_sybil
  %cocycle:       [<masa_1>, <masa_2>, ..., <masa_n>]  ;; 形成障礙的 MASA 序列
  %holonomy:      <phase> | <sign>        ;; 累積的相位（H¹）或符號（H²）
  %branches:      <int>                   ;; 衝突產生的分支數（僅 H²/H⁴）
}
```

| 字段 | H¹ 障礙 | H² 障礙 |
|:---|:---|:---|
| `%cocycle` | `[MASA_A, MASA_B]`（二重覆蓋）| `[MASA_A, MASA_B, MASA_C, MASA_D]`（四重循環）|
| `%holonomy` | $e^{i\theta}$（連續相位）| $-I$（$\mathbb{Z}_2$ 符號翻轉）|

範例（Peres-Mermin 方塊衝突）：
```nlang
%cause: {
  %degree:      2
  %obstruction: #h2_sign
  %cocycle:     [@MASA_X, @MASA_Y, @MASA_Z, @MASA_W]
  %holonomy:    -I
  %branches:    2
}
```

對於 `#h3_gerbe` 和 `#h4_sybil`，`%cocycle` 長度分別為 5 和 6，
對應 Čech 神經中 4-重疊和 5-重疊的維度（APP_04 §2.3）。

> 上述障礙等級的 Čech 神經基礎（MASA 交集複形如何決定障礙維度）見 **[APP_04 §2.3](./APP_04_Mathematical_Foundations.md)**。

> [!NOTE]：
> 遞迴的 Combo 合併、差集的德摩根轉換，以及此處的極小元素篩選，在最壞情況下可能導致 **組合爆炸 (Combinatorial Explosion)**，這本質上是一個 NP-hard 問題。
> 1. **靜態預估**：引擎與工具鏈應在 `oo check --strict` 或 `~%Engine./evolve` 階段預先計算複雜度。若預估節點數超過 `%max_pattern_nodes`，驗證器應拒絕該定義並拋出錯誤。
> 2. **格式化解耦**：`oo fmt` 僅負責原始碼的規範化，不強制進行深度複雜度預估。
> 3. **保護機制**：若極小元素篩選過程中觸及 `%max_pattern_nodes`，引擎將根據當前的 `%strategy` 決定行為：
> - **`#blur` (預設)**：終止篩選，返回 `#incomplete` 並標記 `%cause: #max_nodes_exceeded`。
> - **`#strict`**：直接坍縮為 `_|_`，標記 `%cause: #max_nodes_exceeded`。
> - **`#approximate`**：啟動啟發式近似收斂。

### 1.4 合理性與等價性要求 (Soundness & Equivalence)
為了容許不同的引擎實作與優化技術，`n/` 對統一化邏輯採取 **「黑盒等價原則」**：
1.  **語義保全**：不論引擎採用何種內部演算法（如位圖、熱帶幾何或啟發式搜尋），其最終收斂產生的 CAID **必須**與格論 Meet 運算的純數學定義一致。
2.  **物理隔離**：任何實作層的「捷徑」或「近似」若可能導致結果偏離數學真理，引擎**必須**將該結果標記為特定的非穩定狀態（如 `#blur` 或 `#approximate`），嚴禁將其偽裝為穩定原子。
3.  **效能獨立性**：規格不保證效能一致性。引擎的能量消耗與目標幾何體的複雜度成正比，詳見 **[COSMOLOGY/01](./COSMOLOGY/01_PHYSICS_Unified_Field_Theory.md)** 關於質能等價的定義。


### 1.5 極小元素規則 (Minimal Element Rule)

為了嚴格定義模式匹配的優先級，我們定義特異性排序關係 $\subseteq$：

1.  **子集判定 (Specificity)**： $A \subseteq B$ 當且僅當 $A \sqcap B = A$。這代表 A 提供了比 B 更具體、更嚴格的約束。
2.  **真子集**： $A \subset B$ 當且僅當 $A \subseteq B$ 且 $A \neq B$。
3.  **篩選 (Sifting)**：在多重匹配中，若存在分支 $K_j \subset K_i$，則移除 $K_i$（保留更特定的匹配項）。
4.  **極小元素定義**：$K_i$ 是極小元素，若不存在 $K_j$ 使得 $K_j \subset K_i$。
5.  **聯集輸出 (Union)**：將所有剩下的極小元素對應的結果 $V_{minimal}$ 進行聯集運算。若僅有一個極小元素，結果收斂為該單一值。

**範例 A：層級匹配**
```nlang
/func: {
    1: "exact"
    @int: "generic"
}
;; 觀測 /func 1
;; 1 ⊂ @int（因為 1 & @int = 1），所以 1 是極小元素
;; 結果："exact"
```

**範例 B：不可比性與歧義**
```nlang
/func: {
    @{ @int & 4.. }: "A"
    @{ @int & ..6 }: "B"
}
;; {@int & 4..} 與 {@int & ..6} 互不可比（有重疊但互不為子集）
;; 觀測 /func 5：兩者都匹配且皆為極小元素，結果為 "A" | "B"
```

### 1.6 步進式統一化範例 (Worked Example)

**輸入 A**：`{ x: 1, y: @int }`  
**輸入 B**：`{ x: @int, y: 2, z: 3 }`

**觀測過程**：
1.  **欄位對齊**：路徑集為 `{x, y, z}`。
2.  **處理 x**：觀測 `1 & @int`。由於 $1 \in Integer$，結果為 `1`。
3.  **處理 y**：觀測 `@int & 2`。由於 $2 \in Integer$，結果為 `2`。
4.  **處理 z**：由於 A 中不存在 z，但 A 是開放 Combo（隱含 `z: _`），觀測 `_ & 3`，結果為 `3`。
5.  **結構合成**：結果為 `{ x: 1, y: 2, z: 3 }`。

**若 B 為 Cocoon `{{ x: @int, y: 2 }}`**：
- 處理 z 時，由於 B 是封閉的且未定義 z，觀測 `_ & _|_`，結果為 `_|_`。
- 整體收斂為 `_|_` (含 `%cause: #missing_key`)。

---

## 2. 非嚴格性與多重衝突 (Non-strictness & Multiple Conflicts)
`n/` 允許節點局部處於 `_|_` 狀態而不導致全域崩潰。

*   **衝突原子性**：若一個 Combo 中有多個欄位發生衝突（如 `{a: 1&2, b: 3&4}`），引擎應盡可能保留 **所有** 衝突路徑的因果紀錄於 `%cause` 中。這能協助觀測者進行全方位的幾何診斷。
*   **級聯坍縮**：在封閉結構 (Cocoon) 或特定嚴格策略 (`#strict`) 下，任何局部欄位的衝突皆會導致該容器整體坍縮為 `_|_`。
*   **`x <= _|_` 觀測**：允許邏輯在偵測到衝突時進行分支選擇。透過判定節點是否為空集合，建立邏輯防火牆。

---

## 3. 同構合併規則 (Isomorphism Rules)
當使用 `...` 展開運算子時：
1.  **Combo 展開**：將欄位直接混入目標。若展開物件與目標物件皆具備 `%val`，則對兩者的值執行遞迴合併（`target.%val & source.%val`）。
2.  **Cocoon 展開**：將定義混入，展開後的內容在目標容器中不再具備原先的封閉約束。

---

## 4. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_01](./SPEC_01_Foundation_and_Lattice.md)** | 統一化算法基於格論 Meet 運算。 |
| **[SPEC_03](./SPEC_03_Combo_System.md)** | Combo 欄位的遞迴合併遵循統一化規則。 |
| **[SPEC_05](./SPEC_05_The_Trinity_Isomorphism.md)** | 統一化跨越 Data/Type/Logic 三位一體的界限。 |
| **[SPEC_07](./SPEC_07_Logic_and_Pipe.md)** | 態射應用依賴極小元素規則進行模式匹配。 |
| **[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** | 遞迴合併的終止性檢查與發散處理。 |

---

> [!TIP]
> [!NOTE]：對於具備大量聯集分支的複雜型別合併或模式匹配，建議實作者採用熱帶幾何剪枝與啟發式搜尋演算法，詳見 **[GUIDE_02: 引擎優化指南](./GUIDE_02_Engine_Optimization.md)**。

---

### 哲學思辨 (Philosophical Synthesis)

> 結語：統一化是宇宙邁向和諧的本能。它不強求一致，而是尋求交集；在收斂的盡頭，差異消融於共同的真理之中。
