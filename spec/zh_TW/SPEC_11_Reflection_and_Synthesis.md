# n/ Language Specification - 反映與合成 (Reflection & Synthesis)
本章節定義 `n/` 語言如何感知環境狀態，以及如何將外部世界（如檔案系統）對齊為 `n/` 的路徑結構。
遵循「萬物皆 Combo」原則，環境本身被視為宇宙中的一組特殊節點。

---

## 1. 系統物件反映 (Reflection)

**反映 (Reflection)** 是指宇宙對自身當前運行狀態的自省觀測。這不是透過特殊的「指令」，而是透過標準的系統物件（System Objects）實現。

### 1.1 `~%repl`：工作階段反映
`~%repl` 是一個會話層級（Session-level）的系統物件。它不進入 Commit 歷史，但它能觀測並驅動當前工作階段的演化行為。詳細欄位定義請參閱 **[SPEC_09](./SPEC_09_Standard_Library.md)**。

---

## 2. 合成與環境對齊 (Synthesis)

**合成 (Synthesis)** 是將非 `n/` 結構（如檔案系統中的 `.n` 檔案）對齊為 `n/` 宇宙中路徑節點的過程。

### 2.1 指導文件 (Instruction File)
合成邏輯由指導文件定義。它規定了宇宙根節點 `_` 與外部資源的態射關係。
- **`%import` 語義**：將外部路徑的內容（由引擎負責解析）掛載至指定的 Combo 節點。
- **遞迴掛載**：若 `%import` 對象為目錄，引擎自動將其下的檔案合成為 Combo 的欄位。

### 2.2 多維來源 (Multi-dimensional Sources)
宇宙的根節點 `_` 可以是多個物理來源的交集。這些不同來源的定義最終在 `_` 之下進行格論收斂。

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

---

## 4. 語法與工具的邊界

工具（如 `oo`）是實作語言規格的手段。

### 4.1 LSP 最小功能集 (LSP Minimum Requirements)
為了保證開發觀測體驗，符合規格的 LSP 實作應支援前往定義、懸停觀測與即時診斷。

### 4.2 語義一致性
對同一個 Hash 的觀測，在不同工具中產生的坍縮態必須一致。

---

## 5. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** | 元資訊欄位（%）與系統物件（~%）共同構成運行時的自省介面。 |
| **[SPEC_10](./SPEC_10_Evolution_and_Commit.md)** | 演化操作透過 `~%repl` 介面暴露給觀測者。 |
| **[SPEC_13](./SPEC_13_Discovery_and_Package.md)** | 發現機制是環境合成的分散式實作。 |
| **[REAL_03](./REAL_03_CAID_Protocol.md)** | 定義 CAID 計算的物理位元流細則。 |
| **[GUIDE_01](./GUIDE_01_Style_and_Formatting.md)** | 定義程式碼的美化與排版風格建議。 |

---

### 哲學思辨 (Philosophical Synthesis)

> 結語：反映讓系統看見自己，合成讓宇宙擁抱外部。在對齊的瞬間，混亂的現實轉化為和諧的幾何路徑。
