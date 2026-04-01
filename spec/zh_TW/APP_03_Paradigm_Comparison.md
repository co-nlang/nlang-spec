# APP_03：範式比較與遷移指南 (Paradigm Comparison & Migration)
## 1. 範式大對抗：n/ 定位何處？

`n/` 是一門**數據中心 (Data-centric)** 的**格論收斂 (Lattice Convergence)** 語言。它不屬於傳統的命令式、物件導向或單純的函數式範疇。

| 特性 | 命令式 (Python/Rust) | 邏輯式 (Prolog) | 依賴型別 (Agda/Lean) | **n/ (n-slash)** |
| :--- | :--- | :--- | :--- | :--- |
| **核心單元** | 指令 (Statement) | 關係 (Relation) | 證明 (Proof) | **Combo (幾何體)** |
| **運算機制** | 狀態變遷 | 搜尋/回溯 | 型別檢查 | **收斂 (Convergence)** |
| **第一公民** | 函數/對象 | 謂詞 (Predicate) | 型別 (Type) | **數據 (Data)** |
| **錯誤處理** | 異常/Result | 失敗 (Fail) | 靜態證明 | **Bottom (`_\|_`)** |
| **演化路徑** | 修改記憶體 | 填充事實 | 遞增證明 | **Commit 序列** |

---

## 2. 核心對比解析

### 2.1 n/ vs. 邏輯編程 (Logic Programming)
*   **相似點**：兩者都使用 **Unification (統一化)** 作為核心運算。
*   **差異點**：
    *   Prolog 追求的是「滿足條件的所有解」，會產生回溯（Backtracking）。
    *   `n/` 追求的是「滿足約束的唯一收斂點」。`n/` 的 Unification 發生在格論空間，目的是尋找極小元素，且具備強大的**內容定址 (CAID)** 穩定性。

### 2.2 n/ vs. 依賴型別 (Dependent Types)
*   **相似點**：兩者都允許「型別依賴於值」（例如：長度為 n 的列表）。
*   **差異點**：
    *   依賴型別語言（如 Lean, Idris）通常有嚴格的層級區分（Term vs. Type），驗證過程是複雜的證明搜索。
    *   `n/` 透過 **三位一體同構**，將值與型別在幾何上完全等價。驗證被簡化為格論的 **合併 (`&`)** 運算。`n/` 犧牲了部分極端靈活的證明能力，換取了極高的執行期收斂效率。

---

## 3. 常用模式遷移表 (Pattern Migration)

### 3.1 條件判斷 (Conditionals)
*   **傳統 (Python/JS)**: `if (age >= 18) { return "Adult"; }`
*   **n/ 方式**: 使用 **動態鍵匹配** 或 **條件收斂 (`? :`)**。
*   **遷移範例**:
    ```nlang
    ;; n/ 風格：模式即匹配
    /status: {
        @{ @int & >= 18 }: #adult
        @{ @int & < 18 }: #minor
    }
    ```

### 3.2 迴圈與迭代 (Loops)
*   **傳統 (Rust/Go)**: `list.map(|x| x + 1)`
*   **n/ 方式**: 使用 **態射升寫 (Lifting)** 或 **遞迴**。
*   **遷移範例**:
    ```nlang
    ;; 在 n/ 中，管道會自動對函子執行升寫
    result: [1, 2, 3] |> (x -> x + 1)  ;; 輸出 [2, 3, 4]
    ```

### 3.3 數據驗證 (Validation)
*   **傳統 (Pydantic/Zod)**: `Schema.parse(data)`
*   **n/ 方式**: 使用 **Cocoon 合併 (`&`)**。
*   **遷移範例**:
    ```nlang
    @User: {{ name: @str, age: @int }}
    valid_data: raw_input & @User  ;; 若不合規，自動收斂為 _|_ 並記錄 %cause
    ```

### 3.4 錯誤處理 (Error Handling)
*   **傳統**: `try-catch` 或 `Result<T, E>`
*   **n/ 方式**: **觀測 Bottom (`_|_`)**。
*   **遷移範例**:
    ```nlang
    ;; 偵測衝突並提供預設值
    safe_val: (risky_op <= _|_) ? default_val : risky_op
    ```

---

## 4. 實用觀念轉變 (Mindset Shift)

1.  **不要寫「動作」，要寫「形狀」**：
    *   別想著「我要怎麼過濾列表」，要寫「這個列表合併一個型別約束後剩下的部分」。
2.  **變數不是「盒子」，是「座標」**：
    *   `x: 1` 並非將 1 放入名為 x 的盒子，而是宣告 `x` 這個座標在宇宙中的位置就是 `1`。
3.  **沒有「版本」，只有「內容」**：
    *   忘記語義化版本 (SemVer)。在 `n/` 中，如果內容變了，CAID 就會變。如果你需要相容性，使用 `%compat` 標籤在格論層級進行宣告。

---

## 5. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_05](./SPEC_05_The_Trinity_Isomorphism.md)** | 數據、型別、邏輯合一的理論基礎。 |
| **[SPEC_06](./SPEC_06_Unification_Logic.md)** | 遷移表中「合併即驗證」的數學實現。 |
| **[SPEC_01](./SPEC_01_Foundation_and_Lattice.md)** | 格論作為所有範式轉換的底層規律。 |
| **[REAL_04](./REAL_04_Causal_Chain_Protocol.md)** | 遷移表中「觀測 Bottom」後的因果診斷。 |
