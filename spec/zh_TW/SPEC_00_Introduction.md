# n/ Language Specification - Introduction

---

## 1. 核心哲學：格論與收斂

`n/` (n-slash 或 n-lang) 是一個以「數據為中心 (Data-centric)」的幾何宣告式語言。它的設計並非基於傳統的指令執行，而是基於 **格論 (Lattice Theory)** 的收斂規律。

*   **收斂性 (Convergence)**：所有的運算皆是集合的合併，直到坍縮成唯一的原子。
*   **同構性 (Isomorphism)**：Data, Type, Logic 在幾何結構上是統一的 Combo。
*   **演化觀 (Evolution)**：宇宙是 Commit 的離散序列，觀測引發坍縮，演化推進時間。

---

## 2. 核心概念：銜尾蛇體系 (Ouroboros System)

**Ouroboros** 是 `n/` 語言體系的總稱。為了確保規格的嚴謹性，本法典在不同維度下精確使用以下指稱：

*   **銜尾蛇模型 (Ouroboros Model)**：指 `n/` 的核心理論，包含格論模型、三位一體同構與自我演化機制。
*   **銜尾蛇引擎 (Ouroboros Engine)**：指實作上述模型的計算核心（如官方實作 `oo`）。它負責處理增量收斂、內容存儲與視界管理。
*   **銜尾蛇協定 (Ouroboros Protocol)**：指引擎間進行通訊與發現（NDP）的標準規範。
*   **銜尾蛇符號 (Ouroboros Symbol)**：專指元資訊前綴 `%`，象徵系統的自我意識與自省。

---

## 3. 三位一體視界 (The Trinity Horizons)

為了精確描述觀測行為的邊界，法典區分以下三種「視界」範疇：

1.  **詞法視界 (Lexical Horizon)**：由 Combo 嵌套結構定義的名稱可見性空間。決定「當前座標能看見哪些欄位」。詳見 **[SPEC_04](./SPEC_04_Navigation_and_Duality.md)**。
2.  **計算視界 (Computational Horizon)**：由資源限制（燃料與時間）定義的收斂深度。決定「觀測者能透視多深的真理」。詳見 **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)**。
3.  **時間視界 (Temporal Horizon)**：由 Commit 序列定義的狀態變遷邊界。決定「哪些事實已固化，哪些仍處於疊加態」。詳見 **[SPEC_10](./SPEC_10_Evolution_and_Commit.md)**。

---

## 4. 系統架構與權威等級

`n/` 不僅是一門程式語言，其本體是一個 **Semantic OS Kernel (語義作業系統核心)**。實作者必須嚴格區分「理想的數學模型」與「現實的物理具現」。

### 4.1 六層法典架構 (The 6-Layer Architecture)

為了確保這套系統在未來的演化中不產生「範疇混淆」，全域架構定義為以下六個層次：

*   **Layer 0 — 數學基礎層**：不可動搖的公理（格論、收斂）。永久凍結。
*   **Layer 1 — 語言系統層**：幾何規律（詞法、態射、三位一體）。5 年凍結。
*   **Layer 2 — 系統法度層**：標準宇宙行為（視界、標準庫、遞迴）。穩定演進。
*   **Layer 3 — 執行與環境層**：引擎運作方式（Commit 模型、反映、合成）。
*   **Layer 4 — 網路與發現層**：全球共識（CAID、發現協定、NDP）。
*   **Layer 5 — 社會與信任層**：人類協作（別名映射、信任鏈）。

### 4.2 規格與格式版本映射 (Version Mapping)

為了確保內容定址 (CAID) 的穩定性，語言版本與物理格式版本的映射關係如下：

| 語言版本 (Spec) | 預設格式版本 (fmt) | 支援範圍 | 變更說明 |
| :--- | :---: | :--- | :--- |
| **`v1.0.0`** | **`v1`** | `v1` | 創世規格 (SHA-256) |

*註：任何對規範化演算法的修改均會導致 `fmt_version` 提升。詳見 **[REAL_03](./REAL_03_CAID_Protocol.md)**。*

### 4.3 規範體系與法律效力 (Hierarchy of Authority)

本法典之文件依照其性質具備不同的法律效力：

1.  **法典 (SPEC 系列)**：**絕對規範性 (Normative)**。定義語言的數學公理與幾何。違反 SPEC 即視為非 `n/` 語言。
2.  **具現標準 (REAL 系列)**：**物理規範性 (Normative)**。定義引擎互操作協議。違反標準將無法參與全域 Hash 宇宙。
3.  **演化秩序 (ORDER 系列)**：**秩序規範性 (Normative)**。定義社群治理與規格遷移義務。包含：
    - **[ORDER_00：臨時憲法](./ORDER_00_Interim_Constitution.md)** (引導期適用)。
    - **[ORDER_01：演化與治理](./ORDER_01_Evolution_and_Governance.md)** (Epoch 0 啟用)。
4.  **建議指南 (GUIDE 系列)**：**參考性 (Informative)**。提供風格與最佳實踐建議。
5.  **附錄 (APP 系列)**：**參考性 (Informative)**。提供背景知識與理論擴展。

---

## 5. 語義不變性 (Semantic Invariants)

以下公設定義了 `n/` 宇宙的「物理定律」。任何實作若違反下列不變性，即被視為邏輯崩潰。

### 🔒 Invariant 1 — 收斂決定論 (Convergence Determinism)
*   **意義**：這是 **CAID (內容定址)** 的物理基礎。
*   **規範化要求**：計算雜湊前必須進行語義等價的格式化處理（見 **[REAL_03](./REAL_03_CAID_Protocol.md)**）。

### 🔒 Invariant 2 — 資訊單調性 (Monotonic Knowledge)
*   **意義**：宇宙的資訊量隨時間單調遞增。任何修改在本質上都是新的「精煉」。

### 🔒 Invariant 3 — 觀測純粹性 (Observation Purity)
*   **意義**：確保了平行觀測的安全性與等價性。

### 🔒 Invariant 4 — 複合封閉性 (Combo Closure)
*   **意義**：貫徹「萬物皆 Combo」的幾何統一性。

### 🔒 Invariant 5 — 邊界一致性 (Top/Bottom Consistency)
*   **意義**：界定了宇宙的邏輯極限。

---

## 6. 規格書導航 (The Code of n/)

本法典分為五卷，描述了宇宙從格論到網路的完整規律。關於各章節的 **當前狀態與開發目標**，請參閱 **[法典狀態追蹤表 (SPEC_STATUS)](./SPEC_STATUS.md)**。

### 卷一：公設 (The Axioms) —— 宇宙的理
1.  **[SPEC_01: 格論公設](./SPEC_01_Foundation_and_Lattice.md)**
2.  **[SPEC_02: 詞法結構](./SPEC_02_Lexical_Structure.md)**
3.  **[SPEC_03: 複合結構](./SPEC_03_Combo_System.md)**

### 卷二：流轉 (The Dynamics) —— 宇宙的氣
4.  **[SPEC_04: 導航與詞法視界](./SPEC_04_Navigation_and_Duality.md)**
5.  **[SPEC_05: 三位一體同構](./SPEC_05_The_Trinity_Isomorphism.md)**
6.  **[SPEC_06: 統一化邏輯](./SPEC_06_Unification_Logic.md)**
7.  **[SPEC_07: 態射與管道](./SPEC_07_Logic_and_Pipe.md)**

### 卷三：法度 (The System) —— 宇宙的格論
8.  **[SPEC_08: 運行時與計算視界](./SPEC_08_Meta_and_Runtime.md)**
9.  **[SPEC_09: 代數憲法與標準庫](./SPEC_09_Standard_Library.md)**
10. **[SPEC_10: 演化與時間視界](./SPEC_10_Evolution_and_Commit.md)**
11. **[SPEC_11: 反映與合成](./SPEC_11_Reflection_and_Synthesis.md)**

### 卷四：體系 (The Architecture) —— 宇宙的網
12. **[SPEC_12: 遞迴與驗證](./SPEC_12_Logic_Validation_and_Recursion.md)**
13. **[SPEC_13: 發現與內容幾何](./SPEC_13_Discovery_and_Package.md)**
14. **[SPEC_14: 正式語法](./SPEC_14_Formal_Grammar.md)**
15. **[SPEC_15: 反模式](./SPEC_15_Anti_Patterns.md)**

### 卷五：循環與餘韻 (The Eternal Echo) —— 宇宙的悟
16. **[SPEC_16: 測試與證明](./SPEC_16_Testing_and_Proof.md)**
17. **[SPEC_17: 自我演化](./SPEC_17_Self_Evolution.md)**
18. **[SPEC_18: 餘韻](./SPEC_18_The_Echo.md)**

---

### 具現、秩序與附錄 (Realization, Order & Apps)
- **[REAL_01: 銜尾蛇工程](./REAL_01_Ouroboros_Engineering.md)**
- **[REAL_02: 銜尾蛇協定](./REAL_02_Ouroboros_Protocols.md)**
- **[REAL_03: CAID 物理協議](./REAL_03_CAID_Protocol.md)**
- **[REAL_04: 因果鏈協議](./REAL_04_Causal_Chain_Protocol.md)**
- **[REAL_05: 合規測試與 MVP](./REAL_05_Compliance_and_MVP.md)**
- **[ORDER_00: 臨時治理憲法](./ORDER_00_Interim_Constitution.md)**
- **[ORDER_01: 演化與治理](./ORDER_01_Evolution_and_Governance.md)**
- **[APP_01: 熱帶幾何擴展](./APP_01_Tropical_Geometry.md)**
- **[APP_02: 形式化驗證](./APP_02_Formal_Verification.md)**
- **[APP_03: 範式比較與遷移](./APP_03_Paradigm_Comparison.md)**
- **[GUIDE_01: 排版風格指南](./GUIDE_01_Style_and_Formatting.md)**
