# n/ Language Specification - 代數憲法與標準庫 (Algebraic Constitution)
本章節定義 `n/` 預設提供的代數結構、型別、標籤與元資訊行為。
`n/` 的標準庫並非隨意的態射集合，而是建立在 **範疇論 (Category Theory)** 之上的純粹模型。

---

## 1. 核心代數公設 (Core Algebraic Axioms)

任何 Combo 或型別，只要實作了對應的 `%meta` 欄位，即視為具備該代數結構。引擎在觀測管道演化（`|>`）時，會優先利用這些結構進行態射升寫。

### 1.1 函子 (Functor - `%fmap`)
*   **語義**：「結構保全的態射」。
*   **實作範例 (@Box)**：
    ```nlang
    ;; 定義一個具備函子特性的容器
    @Box: {
        %val: @any
        
        ;; 實作標準 fmap 介面
        %fmap: (f: @morphism) -> { 
            %val: f $.%val    ;; 將態射應用於內部原子
            %kind: #data      ;; 保留數據面相
        }
    }
    
    ;; 範例：處理嵌套 Box
    nested: @Box: @Box: 10
    result: nested |> (x -> x + 1)  ;; 自動遞迴升寫
    ;; 結果: { %val: { %val: 11 } }
    ```

### 1.2 可折疊 (Foldable - `%fold`)
*   **語義**：「結構的聚合」。
*   **介面**：`(accumulator, morphism) -> result`
*   **在 n/ 中的表現**：將容器內的元素依序與累加器合併。

### 1.3 幺半群 (Monoid - `%empty` + `%concat`)
*   **語義**：「可合併的結構」。
*   **介面**：`%empty` 為單位元，`%concat` 為結合律運算。
*   **在 n/ 中的表現**：對於 Combo，`%concat` 預設同構於格論合併 `&`。

### 1.4 單子 (Monad - `%bind`)
*   **語義**：「可鏈式組合的計算」。
*   **實作範例 (@Box)**：
    ```nlang
    @Box: {
        %val: @any
        %bind: (f: @morphism) -> f $.%val
    }
    ;; 使用：(Box 10) |> (x -> Box(x+1)) -> { %val: 11 } (自動攤平)
    ```

### 1.5 符號與代數介面態射 (Symbol Mapping)

為了保證語法的穩定性與使用者擴充性的平衡，核心符號運算子預設態射至對應的 `%meta` 介面。

| 運算子 | 維度 | 代數介面 | 說明 |
| :--- | :---: | :--- | :--- |
| **`+`** | 二元 | **`%concat`** | 優先調用幺半群合併。 |
| **`\`** | 二元 | **`%diff`** | 集合差集。 |
| **`-`** | 二元 | **`%sub`** | 數值或代數減法。 |
| **`-`** | 單元 | **`%neg`** | **負號**：數值取負。 |
| **`!`** | 單元 | **`%compl`** | **補集**：格論補集或邏輯否定。 |
| **`*`** | 二元 | **`%mul`** | 數值乘法或結構笛卡兒積。 |
| **`/`** | 二元 | **`%div`** | 數值除法。 |

---

## 2. 預設效果標籤 (#Effect)
`n/` 使用代數效果標籤來追蹤系統的非決定性與外部依賴。

| 標籤 | 語義 |
| :--- | :--- |
| **`#pure`** | 預設狀態。絕對決定論，無外部副作用。 |
| **`#io`** | 包含外部輸入/輸出（如網路、檔案系統）。 |
| **`#nondet`** | 包含非決定性運算（如隨機數、當前時間）。 |
| **`#state`** | 依賴或修改可變的環境狀態（如 `~%repl`）。 |
| **`#cached`** | 曾經的 `#io` 結果已被固化為穩定的 CAID 快照，可視為純粹數據。 |

---

## 3. 標準型別與代數實作

核心規格預定義了一組標準型別，所有符合規格的引擎必須內建其定義並對齊其 CAID。

| 型別 | 核心幾何結構 (同構展開) | 創世 CAID (Placeholder) |
| :--- | :--- | :--- |
| **`@list`** | `{ %kind: #type, %fmap: /~%List./map, %fold: /~%List./fold, ... }` | `hash:sha256:v1:0001...` |
| **`@option`** | `@{ @Some \| #none }` | `hash:sha256:v1:0002...` |
| **`@result`** | `@{ @Ok \| @Err }` | `hash:sha256:v1:0003...` |
| **`@morphism`** | `{ %kind: #type, %morphism: #true }` | `hash:sha256:v1:0004...` |

### 3.1 容器型別：列表 (`@list`)
*   **`%fmap`**：態射所有元素，保持順序與長度。
*   **`%concat`**：列表串接。
*   **`%bind`**：即 `~%List./flatMap`。

### 3.2 標籤結構：選項 (`@option`)
*   **定義**：`@Some: { %val: @any } | #none`。
*   **用途**：在不觸發 `_|_` 的情況下處理空值。

### 3.3 邏輯結構：結果 (`@result`)
*   **定義**：`@Ok: { %val: @any } | @Err: { %cause: @any }`。

---

## 4. 純量型別與格論行為

### 4.1 數字 (`@int`, `@float`, `@num`)
*   **格論性質**：支援數值比較與區間收斂。
*   **算術 Monoid**：加法 (`%empty: 0`) 與 乘法 (`%empty: 1`)。

### 4.2 字串 (`@str`)
*   **格論性質**：支援與正則表達式 `@regex` 的交集運算。

---

## 5. 系統工具與態射 (`~%System`)

這些工具是為了讓外部世界更方便地操作代數結構。
為了減少開發者的認知負擔，標準庫態射名稱應與其對應的元欄位（%Meta）保持術語對照。

| 代數介面 (Meta) | 標準庫態射 (Morphism) | 說明 |
| :--- | :--- | :--- |
| **`%fmap`** | **`/map`** | 函子映射。`x \| /map(f)` 同義於 `x.%fmap(f)`。 |
| **`%bind`** | **`/flatMap`** 或 **`/bind`** | 單子鏈式組合。 |
| **`%fold`** | **`/fold`** | 容器聚合。 |
| **`%concat`** | **`/concat`** | 結構串接或幺半群合併。 |

### 5.1 核心系統組件清單

| 工具 | 說明 |
| :--- | :--- |
| **`~%List`** | 列表處理（map, filter, fold, flatMap 等）。 |
| **`~%Str`** | 字串處理（split, join, matches 等）。 |
| **`~%Option`** | 選項處理。 |
| **`~%Result`** | 結果處理。 |

---

## 6. 外部函數介面 (Foreign Function Interface)

為了支援與現實世界的互操作性，`n/` 允許態射由外部程式（如 C, Rust, JS）實作。詳見 **[REAL_01](./REAL_01_Ouroboros_Engineering.md)**。

---

## 7. 系統元資訊索引 (%Meta)

這些欄位是 Ouroboros 引擎自省宇宙的標準字典。

| 欄位 | 型別 | 說明 |
| :--- | :--- | :--- |
| **`%id`** | `@str` | 節點的內容雜湊（Content Identity）。 |
| **`%external`** | `@bool` | 標示態射是否由外部程式實作。 |
| **`%len`** | `@int` | 容器長度或字串字元數。 |
| **`%branches`** | `@int` | 聯集中的分支數量。 |
| **`%kind`** | `#Tag` | 本體論角色（`#data`, `#type`, `#logic` 等）。 |
| **`%cause`** | `#Tag` | 收斂至 `_\|_` 時的因果標籤。詳見 **[REAL_04](./REAL_04_Causal_Chain_Protocol.md)**。 |
| **`%strategy`** | `#Tag` | 計算視界邊緣的收斂策略（`#blur`, `#strict`）。 |
| **`%fuel`** | `@int` | 觀測視界的空間配額。 |
| **`%timeout`** | `@int` | 單次收斂允許的最大時間（預設為 CPU 時間）。 |
| **`%max_branches`** | `@int` | 單一節點允許的最大聯集分支數（預設 `64`）。 |
| **`%max_unification_depth`** | `@int` | 限制遞迴 Combo 合併的最大深度（預設 `256`）。 |
| **`%max_pattern_nodes`** | `@int` | 限制模式匹配涉及的最大節點數（預設 `1024`）。 |
| **`%fmap`** | `@morphism` | 函子態射介面。 |
| **`%fold`** | `@morphism` | 容器折疊介面。 |
| **`%empty`** | `@any` | 幺半群單位元。 |
| **`%concat`** | `@morphism` | 幺半群合併操作。 |
| **`%bind`** | `@morphism` | 單子鏈式組合介面。 |
| **`%compat`** | `@list \| @str` | 語言規格或套件的相容性宣告。 |
| **`%effect`** | `#Tag` | 標示運算或態射的副作用型別（如 `#io`），預設為 `#pure`。 |
| **`%termination_proof`** | `#Tag \| @morphism` | 手動提供遞迴終止證明。詳見 **[APP_02](./APP_02_Formal_Verification.md)**。 |
| **`%migration`** | `@morphism` | 結構演化時的自動遷移態射。 |
| **`%privilege_token`** | `@str` | 特權模式訪問令牌。 |

## 8. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_01](./SPEC_01_Foundation_and_Lattice.md)** | 格論基礎。 |
| **[SPEC_07](./SPEC_07_Logic_and_Pipe.md)** | 演化管道與升寫。 |
| **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** | 運行時物理參數。 |
| **[SPEC_10](./SPEC_10_Evolution_and_Commit.md)** | 演化與 Commit。 |
| **[SPEC_17](./SPEC_17_Self_Evolution.md)** | 自我演化保證。 |

---

### 哲學思辨 (Philosophical Synthesis)

> 結語：代數是宇宙的憲法。它不規定具體的行為，只約束抽象的秩序；在規律的守護下，萬物皆能自由地演化。
