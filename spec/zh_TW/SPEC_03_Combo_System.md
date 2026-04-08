# n/ Language Specification - 複合結構 (Combo System)
## 1. Combo 與 Cocoon

### 1.1 Combo (開放的組合 `{}`)
**Combo** (源自 Combination，即開放容器) 是 `n/` 最核心的結構。它遵循「開放世界」假設。
*   **特性**：未被提及的欄位預設為 `_` (Top)。這意味著一個 Combo 永遠可以被後續的平行定義擴張。
*   **平行定義**：同一個 Key 可以分散在不同檔案定義，最終結果是所有定義的**合併 (`&`)** (詳見 **[SPEC_06](./SPEC_06_Unification_Logic.md)**)。

### 1.2 Cocoon (繭 `{{}}`)
**Cocoon** (繭) 用於需要絕對嚴謹邊界、封閉且不可擴張的場景。
*   **特性**：遵循「封閉世界」假設。
*   **封閉語義 (Sealed Boundary)**：
    1.  **存取限制**：讀取未定義的欄位 $k$ 立即返回 `_|_`。
    2.  **合併拒絕 (Merge Rejection)**：當 Cocoon $C$ 參與合併運算 $C \sqcap X$ 時，若 $X$ 包含 $C$ 未定義的任何**非 Top 欄位**，則合併結果立即坍縮為 `_|_`。
    3.  **效果隔離 (Effect Isolation)**：Cocoon 是一個副作用隔離艙。內部欄位的效果標籤（如 `#io`）**不會**自動向上傳染給 Cocoon 容器本身。外部觀測者看見的 Cocoon 標籤預設為 `#pure`（詳見 **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)**）。
    4.  **與展開的區別**：合併 (`&`) 是「幾何疊加」，受限於封閉性與效果隔離；展開 (`...`) 是「顯式解封 (Unboxing)」，它搬運定義、丟棄封閉外殼，並**釋放**內部的副作用標籤。

### 1.2.1 封閉性衝突 (Cocoon Conflict)

當一個 Cocoon 與另一個包含「Cocoon 未定義欄位」的結構進行交集（`&`）時，將觸發封閉性衝突。

*   **案例**：
    ```nlang
    ;; 定義一個封閉的個人數據
    @StrictUser: {{ name: @str }}

    ;; 嘗試併入額外欄位 age
    result: @StrictUser & { name: "Alice", age: 30 }

    ;; 結果：_|_ (Bottom)
    ;; %cause: #missing_key (在 @StrictUser 中找不到 age)
    ```

*   **設計理由**：封閉結構是進行靜態分析與「開世界（Open-world）轉閉世界（Closed-world）」推導的重要邊界。它允許編譯器在確定的集合內進行窮舉與優化。

**範例對比：**
```nlang
~c: {{ b: 2 }}
~o: { a: 1 }

;; 1. 直接合併 (幾何衝突)
result_merge: ~o & ~c    ;; 結果: _|_ (%cause: #missing_key)

;; 2. 展開合併 (顯式解封)
result_spread: { a: 1, ...~c }  ;; 結果: { a: 1, b: 2 } (開放)
```

### 1.3 欄位存在性與預設值
在 `n/` 中，欄位的「不存在」並非一種狀態，而是對萬有集合 `_` (Top) 的一種觀測。
*   **開放預設**：在 Combo 中，任何未定義的 Key $k$ 滿足 $Combo.k = \top$。
*   **封閉預設**：在 Cocoon 中，任何未定義的 Key $k$ 滿足 $Cocoon.k = \bot$。
*   **同構性**：這種設計確保了「存取」操作本身是安全的，錯誤僅發生在合併衝突之時。

---

## 2. 封裝與作用域
Combo 內部的欄位可視性與路徑解析規則（由內而外的詞法溯源）詳見 **[SPEC_04](./SPEC_04_Navigation_and_Duality.md)**。

---

## 3. Combo 運算與動態鍵
*   **合併 `&`**：遞迴地合併兩個 Combo 的欄位。
*   **差集 `\` 與 補集 `!`**：對 Combo 進行差集或補集運算時，引擎會將其轉化為對特定欄位的「負向約束」。例如 `{a: @int} \ {a: 1}` 等價於對 `a` 欄位施加 `@int & !1` 的約束。
*   **展開運算子 `...`**：
    *   將目標 Combo 或 Cocoon 的所有欄位「攤平」至當前 Combo 中。
    *   **安全邊界規則 (Spread Isolation)**：展開運算子**僅能搬運**在當前「詞法作用域 (Lexical Scope) (Lexical Scope)」中**具備觀測權限**的欄位。
        - **私有保全**：若展開操作位於目標 Combo 外部，則目標中的 `~` 私有欄位將**不會**被包含在展開結果中。這防止了透過 `...` 運算子非法導出（Leak）內部私有狀態。
        - **顯式覆蓋例外**：若需「破繭（Break the cocoon）」獲取全部定義（含私有），觀測者必須位於目標的詞法內部，或具備特權模式。
    *   **碰撞合併 (Collision Merge)**：當展開的欄位與目標容器中已有的欄位發生重疊（Key 碰撞）時，其行為必須是**交集合併 (`&`)**，而非覆寫。這確保了「資訊單調性」。例如：`{ a: 1, ...{a: @int} }` 等價於 `{ a: 1 & @int }`。
    *   **解封特性 (Unboxing)**：若展開對象為 **Cocoon `{{}}`**，被搬運的欄位集合在進入目標容器後不再受到其原先的「封閉世界」約束。
    *   **目標屬性保全 (Target Attribute Preservation)**：展開操作僅搬運欄位定義，**嚴禁修改目標容器本身的屬性**。
        *   若展開至 Combo `{}`，目標維持開放。
        *   若展開至 Cocoon `{{}}`，目標維持封閉。
    *   **語義轉變**：展開 `{{a: 1}}` 至 `{}` 後，`a` 欄位變回「開放」狀態；展開 `{{a: 1}}` 至 `{{}}` 後，`a` 欄位依然處於一個封閉世界中（即該目標 Cocoon 依然拒絕未宣告的額外欄位）。
    *   **異質展開規則 (Heterogeneous Spread)**：當展開對象非標準 Combo 時，遵循以下同構規則：
        - **List `[]`**：將其數字索引欄位攤平至目標（例如 `{...[10, 20]}` 產生 `{0: 10, 1: 20}`）。
        - **原子 (Atom)**：將其視為 `{ %val: v }` 展開（例如 `{...#ok}` 產生 `{%val: #ok}`）。
        - **Top `_`**：無效操作，不對目標增加任何欄位或約束。
        - **Bottom `_|_`**：強制坍縮。目標容器立即變為 `_|_`，標記 `%cause: #conflict`。
    *   **循環展開保護 (Circular Spread Protection)**：嚴禁一個 Combo 展開其自身或其祖先節點（例如 `A: { ...A }`）。
        *   **語義**：此類定義被視為邏輯發散，引擎將其判定為 `_|_`，標記 `%cause: #divergent`。這防止了在收斂過程中產生無限展開的黑洞。

    #### 3.1 碰撞合併與衝突解決
開發者習慣於傳統語言的「後者覆寫」直覺，但在 `n/` 中，`...` 始終遵循格論合併。
*   **視覺化範例**：
    ```nlang
    ~base: { status: #ok, priority: 1 }
    ~patch: { status: #error }
    
    ;; 結果不是 { status: #error, priority: 1 }
    ;; 而是 { status: #ok & #error, priority: 1 } -> { status: _|_ }
    result: { ...~base, ...~patch }
    ```
*   **解決策略**：若需覆寫效果，必須使用特權模式的 `#pin` 或在工程層調用 `oo merge --strategy favor_incoming`（詳見 **[REAL_02](./REAL_02_Ouroboros_Protocols.md)**）。

### 3.2 動態鍵 (Dynamic Keys)
在定義 Combo 時，可以使用匿名集合 `@{}` 作為鍵，這稱為動態鍵。動態鍵本質上是對輸入或查詢的「模式匹配條件」。
```nlang
{
    @{ @int & > 3 }: #true
    @{ @int & <= 3 }: #false
}
```
這在構建複雜的邏輯態射（Logic Isomorphism）時非常強大。

---

## 4. 同構原理 (Isomorphism)
在 `n/` 中，「萬物皆 Combo」。所有的複合字面量都可以被觀測為特定約束下的 Combo 結構。

| 觀測對象 | 等價的 Combo 展開 |
| :--- | :--- |
| **Data `x: v`** | `{ %val: v, %kind: #data }` |
| **Type `@T`** | `{ %super: @B, %predicate: [...], %kind: #type }` |
| **Logic `/f`** | `{ %rules: { ... }, %morphism: #true, %kind: #logic }` |
| **Tuple `(A, B)`** | `{ 0: A, 1: B, %len: 2, %kind: #tuple, %closed: #true }` |
| **List `[1, 2]`** | `{ 0: 1, 1: 2, %kind: #list, %state: #total_ordered }` |
| **Enum `#X`** | `{ #X: (), %kind: #enum, %state: #unordered, %order: {...} }` |
| **Cocoon `{{A}}`** | `{ A, %closed: #true }` |

*註：**`%kind`** 標示了該 Combo 的主要本體論角色（如 `#data`, `#type`, `#logic` 等），其自動推斷規則詳見 **[SPEC_05: 三位一體同構](./SPEC_05_The_Trinity_Isomorphism.md#4-kind-的語義地位)**。*

---

## 5. 順序與數值 Combo (Ordered & Numeric)

在 `n/` 中，順序（Order）是結構的一種維度。List、Tuple 與 Enum 均透過 `~%Enum` 與 `~%List` 提供的語義進行同構。

### 5.1 Enum (偏序枚舉)
Enum 是對一組標籤（Tags）施加偏序關係的 Combo。
*   **定義**：`workflow: { #draft < #review < #publish }`。
*   **比較運算 `<=>`**：用於判定兩個標籤的先後關係，回傳 `#lt | #gt | #eq | #un` (Unordered)。
*   **錨點**：序位預設受 `#_|_` (Start) 與 `#_` (End) 約束。

#### 元資訊與收斂
*   **`%rank`**：該標籤在序位中的整數權重。若序位尚未完全決定，其值為一組可能的聯集或區間。
*   **`%state`**：反映序位的決定程度：
    *   `#unordered`：標籤間無關係。
    *   `#partially_ordered`：部分標籤有先後關係。
    *   `#total_ordered`：任意兩標籤均可比較，此時 `%rank` 坍縮為單一原子。

### 5.2 List (鬆散的數值 Combo `[]`)
List 是以非負整數為 Key 且預設為 `#total_ordered` 的 Combo。
*   **預設值**：所有非負整數索引預設皆為 `_` (Top)。
*   **邊界觀測**：存取大於等於 `%len` 的索引將返回 **`_` (Top)**。這反映了 List 作為開放集合的本質：未定義的座標僅代表尚未觀測的可能性。

### 5.3 Tuple (嚴謹的數值 Combo `()`)
Tuple 語法 `(A, B)` 是對 List 施加「長度與封閉性」約束後的產物。
*   **特性**：具備固定 `%len`，且預設為 `%closed: #true` 與 `%state: #total_ordered`。
*   **邊界觀測**：由於 Tuple 等價於以數字為 Key 的 Cocoon，存取大於等於 `%len` 的索引將立即觸發 **`_|_` (Bottom)**，並標記 `%cause: #missing_key`。


### 5.4 投影與轉換 (Projection)
*   **隱性投影**：當 Enum 處於 `#total_ordered` 狀態時，可直接透過數字索引存取（如 `workflow[0]` 返回 `#draft`）。
*   **顯性轉換**：利用 `~%` 系統邏輯進行結構投影。
    *   `workflow |> ~%Enum./toList` $\rightarrow$ 產生一個對應的 List。
    *   `myList |> ~%List./toEnum` $\rightarrow$ 產生一個對應的 Enum 順序關係。

### 5.5 元資訊：長度 `%len`
對於數值 Combo，`%len` 是一個虛擬欄位，由引擎動態計算：
*   **計算公式**：`%len = max(index | Combo[index] != _|_) + 1`。
*   **語義**：它代表了當前 Combo 中「非衝突邊界」的範圍。若 List 為空，則 `%len: 0`。

---

## 6. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_01](./SPEC_01_Foundation_and_Lattice.md)** | 合併（&）與聯集（\|）是 Combo 演化的基礎算子。 |
| **[SPEC_05](./SPEC_05_The_Trinity_Isomorphism.md)** | 「萬物皆 Combo」是三位一體同構的基石。 |
| **[SPEC_06](./SPEC_06_Unification_Logic.md)** | 統一化算法定義了 Combo 欄位的遞迴收斂規則。 |
| **[SPEC_13](./SPEC_13_Discovery_and_Package.md)** | CAID 標識了 Combo 的內在幾何指紋。 |

---

### 哲學思辨 (Philosophical Synthesis)

> 結語：Combo 是開放的宇宙，Cocoon 是封閉的繭。成繭以錨定收斂之果，破繭以重尋演化之源——兩者的辯證法，構成了 n/ 幾何的完整邊界。
