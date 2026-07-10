# n/ Language Specification - 反映與合成 (Reflection & Synthesis)

本章節定義 `n/` 語言如何感知環境狀態，以及如何將外部世界（如檔案系統）對齊為 `n/` 的路徑結構。
遵循「萬物皆 Combo」原則，環境本身被視為宇宙中的一組特殊節點。

---

## 1. 系統物件反映 (Reflection)

**反映 (Reflection)** 是指宇宙對自身當前運行狀態的自省觀測。

### 1.1 幾何場反映 (Field Reflection)
除了對具體節點的觀測，Ouroboros 引擎透過 `~%Engine` 物件向觀測者反映全域幾何場的分布狀態：
*   **質量場 (`~%Engine.mass_map`)**：反映當前視界內各區域的幾何質量（$m$）分布。
*   **熱度場 (`~%Engine.heat_map`)**：反映 CAID 的活動能級與蒸發優先權（見 **[COSMOLOGY/05 §7](./COSMOLOGY/05_PHYSICS_Horizons_and_Uncertainty.md)**）。
*   **視界反映 (`~%Engine.horizons`)**：反映目前剩餘的燃料（$E$）與計算光錐的邊界。

### 1.2 `~%repl`：工作階段反映
`~%repl` 是一個會話層級（Session-level）的系統物件。它不進入 Commit 歷史，但它能觀測並驅動當前工作階段的演化行為。詳細欄位定義請參閱 **[SPEC_09](./SPEC_09_Standard_Library.md)**。

---

## 2. 合成與環境對齊 (Synthesis)

**合成 (Synthesis)** 是觀測（Observation）的對偶過程。

### 2.1 環境合成：對齊外部世界
將非 `n/` 結構（如檔案系統）對齊為路徑節點。
- **`%import` 語義**：將外部資源掛載至 Combo 節點。
- **遞迴掛載**：引擎自動將目錄結構合成為 Combo 的欄位。

### 2.3 結構化合成：$n/^{op}$ 運算
結構化合成是將記憶體中的「動態幾何場」重新固化為「靜態代碼」的過程。
*   **對偶性**：若觀測是 $\text{Code} \rightarrow \text{Geometry}$，則合成是 $\text{Geometry} \rightarrow \text{Code}$。
*   **智能生成**：當 AI 或引擎透過自觀測循環（銜尾蛇效應）產生新的幾何結構時，必須透過合成運算將其轉化為可持久化、具備 CAID 的代碼實體。

---

## 3. 雙重物理表示 (The Dual Representations)

為了平衡「機器的絕對決定論」與「人類的可讀性」，`n/` 區分了兩種物理表示狀態：

### 3.1 規範化形式 (Canonical Form)
此形式是宇宙的「幾何真身」，**專用於計算 CAID (%id)**。
*   **版本鎖定 (Edition Locking)**：工作區必須明確鎖定 `fmt_version` 以確保雜湊穩定性。
*   **物理義務**：引擎必須保證語義等價的 AST 產生唯一的、極小化的物理位元流。
*   **詳細規格**：參閱 **[REAL_03](./REAL_03_CAID_Protocol.md)**。

### 3.2 美化形式 (Pretty Form)
此形式是為了讓人類觀測者能舒適地閱讀與編輯程式碼。
*   **資訊保全**：必須保留註解並維持良好的排版。
*   **冪等性**：多次格式化應產生相同的結果。
*   **風格約定**：參閱 **[GUIDE_01](./GUIDE_01_Style_and_Formatting.md)**。

### 3.3 合成的一致性義務 (Synthesis Invariant)
引擎實作合成演算法時，必須遵守 **「無損迴路」** 原則：
*   **決定論**：給定相同的幾何物件，合成產出的規範化代碼必須唯一。
*   **CAID 守恆**：合成後的代碼重新被引擎觀測所產生的 `%id`，**必須** 與原始幾何物件的 `%id` 完全一致。這確保了數位宇宙在「波（邏輯）」與「粒子（數據）」轉換過程中的能量守恆。

---

## 4. 語義與工具的邊界

工具（如 `oo`）是實作語言規格的手段。

### 4.1 LSP 最小功能集 (LSP Minimum Requirements)
為了保證開發觀測體驗，符合規格的 LSP 實作應支援前往定義、懸停觀測與即時診斷。

### 4.2 語義一致性
對同一個 Hash 的觀測，在不同工具中產生的坍縮態必須一致。

---

## 5. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_05](./SPEC_05_The_Trinity_Isomorphism.md)** | 三位一體同構是反映與合成的哲學前提。 |
| **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** | 運行時參數透過 `~%Engine` 進行動態反映。 |
| **[REAL_03](./REAL_03_CAID_Protocol.md)** | 規範化形式是合成運算的物理目標。 |
| **[COSMOLOGY/01](./COSMOLOGY/01_PHYSICS_Unified_Field_Theory.md)** | 合成運算（$n/^{op}$）的能量消耗與質能轉換。 |
| **[COSMOLOGY/05 §7](./COSMOLOGY/05_PHYSICS_Horizons_and_Uncertainty.md)** | 幾何熱度場（退相干蒸發）的拓撲反映基礎。 |

---

### 哲學思辨 (Philosophical Synthesis)

> 結語：反映讓系統看見自己，合成讓宇宙擁抱外部。在對齊的瞬間，混亂的現實轉化為和諧的幾何路徑。
