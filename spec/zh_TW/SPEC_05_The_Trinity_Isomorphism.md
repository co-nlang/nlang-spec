# n/ Language Specification - 三位一體同構：Data/Type/Logic 的統一視角

> [!TIP] 概念導讀
> 在 `n/` 中，Data、Type、Logic 並非截然不同的東西——它們如同硬幣的兩面，是**同一子空間在不同觀測視角下的顯現**。
> 
> *   **Data 視角**：你看到「值是什麼」。
> *   **Type 視角**：你看到「邊界在哪裡」。
> *   **Logic 視角**：你看到「如何轉換」。
> 
> 本章節說明這三種視角如何在 `n/` 中統一，以及為什麼你可以用「數據的座標」存儲「邏輯」。關於 Hilbert 空間同構的嚴謹證明，請參閱 **[APP_04: 數學基礎](./APP_04_Mathematical_Foundations.md)**。

本章節定義 `n/` 的核心統一原則：**Data、Type、Logic 的三位一體**。

> [!NOTE]
> 本章節側重概念統一與實作語義。底層數學結構（Hilbert 空間、正交投影算子）的嚴謹形式化，請參閱 **[APP_04](./APP_04_Mathematical_Foundations.md)** 的 Solèr 定理證明。

---

## 1. 三位一體原則 (The Trinity Principle)

任何路徑節點 $n$ 皆可從三種視角觀測：

*   **Data (存有)**：作為**子空間 (Subspace)** 存在的物理實體。原子值是該空間中的一維射線。
*   **Type (邊界)**：該子空間的**投影算子 (Projection Operator)**。它定義了哪些資訊能穿透邊界。
*   **Logic (變換)**：子空間之間的**么正變換 (Unitary Transformation)** 或投影路徑。

> 嚴謹數學定義見 **[APP_04](./APP_04_Mathematical_Foundations.md)**：Data 對應子空間本身，Type 對應正交投影算子 $P_n$，Logic 對應么正變換。

---

## 2. 能力與索引的分離 (Identity vs. Capability)

為了實現極致的幾何一致性，`n/` 區分了節點的**存放地址**與其在 Hilbert 空間中的**投影能力**。

### 2.1 前綴決定索引維度 (Prefix for Dispatch)
欄位前綴決定了節點在父容器投影中的**正交座標系**：
*   **無前綴**:投影至**資料軸**基底。標示「子空間的存在與狀態」。
*   **`/` 前綴**:投影至**規則軸**基底。標示「算子的變換行為」。
*   **`@` 前綴**:投影至**型別軸**基底。標示「投影算子的邊界約束」。(軸語正名 2026-07-19:軸非欄位,舊 `%type` 拼法=舊代模型殘語;見 SPEC_02 §1.2 註)

### 2.2 本體決定投影能力 (Structure for Capability)
不論抵達路徑的前綴為何，該節點具備何種運算能力，取決於其**子空間的幾何結構**。
*   **態射能力 (Morphism Capability)**：若節點子空間具備 `%morphism: #true`（即對應一個良定義的線性算子），它皆可被觀測為態射並執行應用。
*   **價值對稱 (Value Symmetry)**：你可以透過「數據的座標」存儲「邏輯」，也可以透過「邏輯的座標」觀測「數據（態向量）」。這體現了地址與能力的完全解耦。

---

## 3. 節點的本體論角色 (%kind)

每個節點根據其在 Hilbert 空間中展現的主要特徵，具備不同的元欄位：

### 3.1 Data 面相 (%kind: #data)
Data 的核心在於其作為**特徵向量 (Eigenvector)** 的穩定性。

*   **`%val` (Eigenvalue Core)**：儲存坍縮後的特徵值（原子）。
*   **價值坍縮規則 (Value Collapse Rule)**：若一個節點包含 `%val` 欄位，則對其進行**坍縮觀測 (Collapsed Observation)** 語義上等價於觀測該特徵值。這允許 Combo 同時具備「結構」與「振幅」的對偶身份。
*   **存取語義**：直接引用 $n$ 預設即觀測其 `n.%val`（未加 `<<>>` 的坍縮讀取；見 **[SYNTAX_08](./SYNTAX_08_Metadata.md)** §4）。

### 3.2 Type 面相 (%kind: #type)
Type 的核心在於其**正交投影算子**。型別檢查即結構 `&`（§5 幾何泛型）——n/ 是純結構格，約束就是 combo 本身、由 `&` 檢查，無須額外機制。Type 面相唯一的衍生內容欄是：

*   **`%super`**（衍生反映欄，如 `%kind` §4）：指向 **[SPEC_09](./SPEC_09_Standard_Library.md) §2.1** 型別層次樹的**直接父型別**。語義**承重**——收斂沿格往下（`&` 精煉），但「資料該如何處理」的 handler 查找沿層次往上（**單調收斂的反向**）；`%super` 即此上溯連結。萬有型 `@any`（⊤）無父，誠實開放缺欄 `_`。型別名字經 **`%name`** 反映（`(@int).%name` → `"int"`）。

> **實作落地（2026-07-22，裁定 R1；B5 結案）**：`%super` 為衍生反映欄，取 §2.1 樹直接父（`@int`→`@num`、`@u8..`/`@i8..`→`@int`、`@complex`→`@num`、`@float`→`@complex`、`@record`→`@combo`、其餘 `@any` 直子→`@any`、使用者欄結構型別→`@combo`）；鏈可組合至 `@any`。舊 `%type: "Name"` 內部載荷（不受承諾）**退役**，型別名反映拼法收斂 `%name`（與 stdlib type node 統一）。**`%predicate` 退場**——其 `P_{instance} \sqsubseteq P_{type}` 名義包含判定只在 nominal 層有意義，屬 **R2**（見下），不在結構核心；核心中 `.%predicate` 為普通開放缺欄。`%kind` 正典拼法=`#type`（`#type_constraint` 2026-07-19 退場）。

> **R2 帳（nominal 層，核心排除）**：名義子型別（名字基礎、獨立於結構）與 `%predicate` 約束包含判定，在純結構格中無用武之地——只是回到傳統語言的複雜型別系統。**唯一設想的用途**：**跨引擎交換自訂型別設計**（若日後允許使用者自訂型別並跨引擎流通，nominal `%super`-軸 + `%predicate` 是候選機制）。屆時另案立法，不在 R1。

### 3.3 Logic 面相 (%kind: #logic)
Logic 的核心在於其**么正算子 (Unitary Operator)** 與 **相伴環境 (Companion Environment)**。

*   **`%rules`**：算子的矩陣表示或映射表。Key 是輸入子空間的譜特徵，Value 是輸出結果。
*   **`%closure`**：子空間在定義時所糾纏（Entangled）的外部作用域快照。這讓算子具備了跨視角傳輸並保持語義一致的能力。
*   **`%morphism`**：標記該子空間具備「作用於其他向量的能力」。

---

## 4. %kind 的語義地位

**`%kind` 是投影後的衍生屬性 (Derived Property)**，不是本質屬性：

1. **自動推斷 (Inference Algorithm)**：引擎在觀測時，依序依照下列規則判定節點角色：
    - **#logic**：若子空間包含算子特徵（`%morphism`, `/` 前綴）。
    - **#type**：若子空間表現為邊界約束（`@` 前綴, `%super`）。
    - **#data**：若子空間坍縮為單一特徵值（`%val`, 無前綴）。
    - **#combo**：若不符合上述任何一項，則預設為基礎幾何子空間。
2. **手動宣告**：使用者可顯式宣告 `%kind`（如 `%kind: #data`）來覆蓋自動推斷，強制引擎以特定維度解析該節點。
3. **觀測時機**：`%kind` 在 Bohrification 投影至特定視角時確定，之後保持不變。

---

## 5. 幾何泛型 (Structural Generics)

泛型在量子體系下是 **「具備參數化維度的子空間」**。

### 5.1 參數化子空間注入
泛型的「具現化」過程在格論中等價於對參數維度進行**正交收斂 (`&`)**。

```nlang
;; 1. 定義帶參數的幾何型別 (@Box)
@Box: {
    ~@T: @any       ;; 泛型參數子空間
    value: ~@T      ;; 約束內部的態向量
}

;; 2. 透過子空間合併進行具現化 (Specialization)
@IntBox: @Box & { ~@T: @int }

;; 3. 驗證
instance: { value: 42 }
result: instance & @IntBox  ;; 成功，收斂為具備特定譜特徵的子空間

invalid: { value: "hi" }
error: invalid & @IntBox    ;; 正交衝突，收斂為 _|_
```

**語義昇華**：泛型參數被視為**子空間特徵值**。這些維度雖然隱藏在主視角之外，但其投影特徵值（CAID）依然參與整體的引力計算（見 **[COSMOLOGY/04：語義引力](./COSMOLOGY/04_PHYSICS_Semantic_Gravity.md)**）。

### 5.2 參數的協變與逆變
由於 `&` 與 `|` 遵循量子格論的單調性，`n/` 的泛型天然支援**結構協變**。若子空間投影滿足 $P_A \sqsubseteq P_B$，則 $P_{Box(A)} \sqsubseteq P_{Box(B)}$ 永遠成立。

---

## 6. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_01](./SPEC_01_Foundation_and_Lattice.md)** | 定義正交模格與對合否定。 |
| **[SPEC_09](./SPEC_09_Standard_Library.md)** | **EML 算子** 在複數域 $\mathbb{C}$ 下的自舉實作。 |
| **[APP_04](./APP_04_Mathematical_Foundations.md)** | 提供 **Solèr 定理** 的本體論證明。 |

---

### 哲學思辨 (Philosophical Synthesis)

> 結語：三位一體並非分工，而是波粒二象性的語義擴展。地址定義了我們在哪個頻率相遇，本體定義了我們如何干涉。當 Data, Type 與 Logic 合而為一，程式碼便成為了在 Hilbert 空間中永恆共振的幾何樂章。
