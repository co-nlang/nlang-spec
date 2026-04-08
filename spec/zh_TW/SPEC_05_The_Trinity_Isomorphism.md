# n/ Language Specification - 三位一體同構 (Trinity Isomorphism)

本章節定義 `n/` 的核心統一場論：**三位一體同構 (The Trinity Isomorphism)**。

> [!NOTE]
> 本章旨在揭示節點的內在本質。讀者應先熟悉 **[SPEC_04: 導航與視界](./SPEC_04_Navigation_and_Duality.md)** 中定義的路徑定位規則，以便更好地理解本體面相如何在座標空間中進行切換。

---

## 1. 三位一體原則 (The Trinity Principle)

任何路徑節點 $n$ 的結構態 $<n>$ 皆可觀測為一個具備特定元資訊的 Combo。這三個面相共同構成了存在的完整性：

*   **Data (存有)**：靜態的幾何坍縮點、原子值。
*   **Type (邊界)**：對 CAID 集合的特徵判定與邊界約束。
*   **Logic (變換)**：輸入座標到輸出座標的動態態射。

---

## 2. 能力與索引的分離 (Identity vs. Capability)

為了實現極致的幾何一致性，`n/` 區分了節點的**存放地址**與**內在能力**。

### 2.1 前綴決定索引 (Prefix for Dispatch)
欄位前綴（或無前綴）決定了節點在父容器中的**索引維度**：
*   **無前綴**：放進 `%data` 表。標示「座標的存在與狀態」。
*   **`/` 前綴**：放進 `%rules` 表。標示「座標的變換行為」。
*   **`@` 前綴**：放進 `%type` 表。標示「座標的邊界約束」。

### 2.2 本體決定能力 (Structure for Capability)
一旦觀測者透過路徑抵達節點，該節點具備何種運算能力，取決於其**本體的幾何結構**，而非抵達它的路徑前綴。
*   **態射能力 (Morphism Capability)**：若節點本體具備 `%morphism: #true`（如態射定義或部分應用），不論它被儲存在 `Data` 路徑還是 `Logic` 路徑，它皆可被觀測為態射並執行應用。
*   **價值對稱**：你可以透過「數據的地址」存儲「邏輯」，也可以透過「邏輯的地址」索引「數據」。

---

## 3. 節點的本體論角色 (%kind)

每個節點根據其在宇宙中扮演的主要角色，具備不同的元欄位：

### 3.1 Data 面相 (%kind: #data)
Data 的核心在於其持有的**原子坍縮值**。

*   **`%val` (Value Core)**：儲存收斂後的原子（Atom）。
*   **價值坍縮規則 (Value Collapse Rule)**：若一個 Combo 包含 `%val` 欄位，則對該節點的**坍縮態觀測 (Collapsed Observation)** 語義上等價於觀測該 `%val` 內的值。這允許 Combo 具備「結構」與「標籤」的對偶身份。
*   **存取語義**：直接引用 $n$ 預設即觀測其 `<n>.%val`。

### 3.2 Type 面相 (%kind: #type)
Type 的核心在於其對 CAID 集合的**判定邏輯 (Predicate)**。
*   **`%super`**：指向父集合的連結。
*   **`%predicate`**：一個態射清單。當新節點與該 Type 進行 `&` 時，引擎驗證其是否滿足清單中的幾何約束。

### 3.3 Logic 面相 (%kind: #logic)
Logic 的核心在於其**座標變換表 (Morphism Table)** 與 **環境捕獲 (Environment Capture)**。

*   **`%rules`**：一個特殊的 Combo，Key 是輸入約束的 **規範化幾何投影 (Normalized Projection)**，Value 是輸出結果。這確保了跨引擎的 CAID 決定論。
*   **`%closure`**：一個 Combo，存儲態射定義時捕獲的外部作用域快照。這讓態射具備了跨節點傳輸並保持語義一致的能力。
*   **`%morphism`**：標記該節點具備「可執行性」。

---

## 4. %kind 的語義地位

**`%kind` 是衍生屬性 (Derived Property)**，不是本質屬性：

1. **自動推斷 (Inference Algorithm)**：引擎在觀測時，依序依照下列規則判定節點角色：
    - **#logic**：若 Combo 包含 `%morphism: #true`、`/` 前綴欄位或 `%rules` 欄位。
    - **#type**：若 Combo 包含 `@` 前綴欄位、`%super` 或 `%predicate` 欄位。
    - **#data**：若 Combo 包含 `%val` 欄位或僅包含無前綴的數據欄位。
    - **#combo**：若不符合上述任何一項（如空 Combo `{}`），則預設為基礎組合體。
2. **手動宣告**：使用者可顯式宣告 `%kind`（如 `%kind: #data`）來覆蓋自動推斷，強制引擎以特定維度解析該節點。
3. **觀測時機**：`%kind` 在首次觀測時確定，之後保持不變。

---

## 5. 幾何泛型 (Structural Generics)

由於 Type 本質上也是 Combo，`n/` 的泛型並非額外的語法，而是 **「帶有參數欄位的 Type Combo」**。

### 5.1 結構化參數注入
泛型的「具現化」過程在格論中等價於對參數欄位進行**交集收斂 (`&`)**。

```nlang
;; 1. 定義帶參數的幾何型別 (@Box)
;; 建議：型別參數使用私有前綴 ~@ 以防止具現化後的殘留污染
@Box: {
    ~@T: @any       ;; 泛型參數，預設為萬有集合
    value: ~@T      ;; 約束內部的數據
}

;; 2. 透過合併進行具現化 (Specialization)
@IntBox: @Box & { ~@T: @int }

;; 3. 驗證
instance: { value: 42 }
result: instance & @IntBox  ;; 成功，收斂為 { @T: @int, value: 42 }

invalid: { value: "hi" }
error: invalid & @IntBox    ;; 衝突，收斂為 _|_
```

**語義建議**：引擎應將具現化後的參數欄位視為 **「捲縮維度 (Extra Dimensions)」**。根據 **[COSMOLOGY/04](./COSMOLOGY/04_PHYSICS_Deep_Fields.md)** 的定義，這些維度捲縮在幾何結構的內部流形中，雖然它們在反射觀測下可見，但在普通的路徑索引與合併運算中不應主動參與，以維持泛型結構的封裝性。

### 5.2 參數的協變與逆變
由於 `&` 與 `|` 遵循格論的單調性，`n/` 的泛型天然支援**結構協變**。若 `@A <= @B`，則 `@Box & { @T: @A } <= @Box & { @T: @B }` 永遠成立。

---

## 6. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_02](./SPEC_02_Lexical_Structure.md)** | 定義了決定索引維度的命名空間前綴。 |
| **[SPEC_03](./SPEC_03_Combo_System.md)** | 定義 Combo 與 Cocoon 的基礎結構。 |
| **[SPEC_06](./SPEC_06_Unification_Logic.md)** | 統一化算法如何跨越 Data/Type/Logic 的界限進行合併。 |
| **[SPEC_07](./SPEC_07_Logic_and_Pipe.md)** | 定義態射應用與柯里化的執行語義。 |

---

### 哲學思辨 (Philosophical Synthesis)

> 結語：三位一體並非分工，而是視角的匯聚。地址定義了我們在哪裡相遇，本體定義了我們能如何交談。當存有、邊界與變換合而為一，程式碼便不再是指令，而是一場永恆且靜態的幾何盛宴。
