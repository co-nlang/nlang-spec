# n/ Language Specification - Introduction

---

## 1. 核心哲學：觀測、收斂與語義作業系統

`n/` (n-slash 或 n-lang) 是一個**以觀測為中心的語義作業系統 (Observation-Centric Semantic OS)**，建立在宣告式的幾何格論（Lattice-based）核心之上。

不同於傳統語言將程式視為「指令序列」，在 `n/` 中：**程式碼是子空間，執行是觀測，真理是收斂**。

> [!TIP] 一句話理解 n/
> 寫程式像是在 Hilbert 空間中劃分子空間——當你「觀測」`user.name`，你是在請求引擎從潛在的可能性中坍縮出確定的答案。

### 1.1 從數據到觀測

傳統語言問：「這個變數的值是什麼？」  
`n/` 問：「在當前約束下，這個子空間會收斂到什麼？」

*   **收斂 (Convergence)**：從模糊的可能性（`#blur`）到確定的答案（`#exact`）。
*   **觀測 (Observation)**：引擎執行的不是指令，而是「投影」——從萬有集合 `_` 中提取特定子空間。
*   **內容定址 (Content-Addressed)**：一切皆有唯一幾何指紋（CAID）。相同內容在任何宇宙角落都是同一個實體。

### 1.2 三位一體：Data / Type / Logic

在 `n/` 中，這三者不是分離的概念，而是**同一子空間在不同觀測視角下的顯現**：

*   **Data 視角**：「這裡有個值」
*   **Type 視角**：「只能是這些值」
*   **Logic 視角**：「如何轉換成新值」

它們統一於 **Combo** —— `n/` 中唯一的結構原語。

> **靜與動（2026-07-20 補充）**：三位一體看的是**靜態結構**——同一子空間的三種
> 投影，本身不含時間。`n/` 的動態只有兩個來源：**觀測**（路徑投影在視界內收斂，
> 疊加坍縮為定值）與**演化**（欄位演化與管道 `|>`，把新幾何疊加進宇宙；成功即
> 提交，SPEC_07 §4.3）。Logic 視角的「如何轉換」是靜態的藍圖描述——態射是轉換
> 的**算子**，應用／管道才是轉換的**行為**（SPEC_07 卷首註）。二者的關係：
> **演化改變宇宙但不決定事實；觀測決定事實但不改變宇宙**——「尚未定義」與
> 「就是沒有」的分界，就是這兩個相位的分界（引擎相位旗標即其機械化）。

### 1.3 語義作業系統

`n/` 不僅是程式語言，更是一個**語義作業系統的核心**：

*   **OODP/LADD 作為預設**：分散式發現不是外掛，是內建。你的程式天然活在全域邏輯格中。
*   **Commit 作為版本**：沒有「儲存檔案」，只有「固化觀測」。每次 Commit 是宇宙狀態的離散快照。
*   **視界作為資源**：`%fuel` 不是效能限制，是觀測精度的物理對價。

> [!NOTE]
> 以上概念的嚴謹數學定義（正交模格、投影算子、Bohrification）見 **[APP_04](./APP_04_Mathematical_Foundations.md)**。

---

## 2. 核心概念：銜尾蛇體系 (Ouroboros System)

**Ouroboros** 是 `n/` 語言體系的總稱。為了確保規格的嚴謹性，本法典在不同維度下精確使用以下指稱：

*   **銜尾蛇模型 (Ouroboros Model)**：指 `n/` 的核心理論，包含格論模型、三位一體同構與自我演化機制。
*   **銜尾蛇引擎 (Ouroboros Engine)**：指實作上述模型的計算核心（如官方實作 `oo`）。它負責處理增量收斂、內容存儲與視界管理等，也實作銜尾蛇協定。
*   **銜尾蛇協定 (Ouroboros Protocol)**：指引擎間進行通訊與發現（OODP）的標準規範。
*   **銜尾蛇符號 (Ouroboros Symbol)**：專指元資訊前綴 `%`，象徵系統的自我意識與自省。

---

## 3. 三位一體邊界 (The Trinity Boundaries)

為了精確描述觀測行為的極限，法典區分以下三種「邊界」範疇：

1.  **詞法作用域 (Lexical Scope)**：由 Combo 嵌套結構定義的名稱可見性空間。決定「當前座標能看見哪些欄位」。詳見 **[SPEC_04](./SPEC_04_Navigation_and_Duality.md)**。
2.  **計算視界 (Computational Horizon)**：由資源限制（燃料與能量測度）定義的收斂深度。決定「觀測者能透視多深的真理」。詳見 **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)**。
3.  **因果邊界 (Causal Boundary)**：由 Commit 序列定義的狀態固化邊界。決定「哪些事實已進入歷史，哪些仍處於疊加態」。詳見 **[SPEC_10](./SPEC_10_Evolution_and_Commit.md)**。

---

## 4. 系統架構與權威等級

實作者必須嚴格區分「理想的數學模型」與「現實的物理具現」。

### 4.1 六層法典架構 (The 6-Layer Architecture)

為了確保這套系統在未來的演化中不產生「範疇混淆」，全域架構定義為以下六個層次：

*   **Layer 0 — 數學基礎層**：不可動搖的公理（格論、收斂）。永久凍結。
*   **Layer 1 — 語言系統層**：幾何規律（詞法、態射、三位一體）。5 年凍結。
*   **Layer 2 — 系統法度層**：標準宇宙行為（視界、標準庫、遞迴）。穩定演進。
*   **Layer 3 — 執行與環境層**：引擎運作方式（Commit 模型、反映、合成）。
*   **Layer 4 — 網路與發現層**：全球共識（CAID、發現協定、OODP）。
*   **Layer 5 — 社會與信任層**：人類協作（別名映射、信任鏈）。

### 4.2 上同調障礙矩陣

六層架構（$L_0$–$L_5$）和譜序列頁（$E_1$–$E_\infty$）是兩個獨立的分類軸。
每個 $L_r$ 層在每個 $E_r$ 頁都有一個投影，形成以下二維矩陣：

| Layer \ Page | $E_1$（局部分配） | $E_2$（$H^1$ 相位） | $E_3$（$d_2$ / $H^2$） | $E_\infty$（完全收斂） |
|---|---|---|---|---|
| **L0 數學** | `&` meet / `\|` join | 非分配性（$H^1$） | KS 定理（$H^2$） | Atom / $\bot$ |
| **L1 語言** | BNF 文法 | Type（子空間投影） | Cocoon `{{}}` 密封性 | CAID 格式 |
| **L2 標準庫** | StdLib 原語 | `#blur` 局部截面 | 分支（`%cause` 保留）| `#exact` |
| **L3 執行** | `%fuel` 資源邊界 | 視界邊界 | 16-cell 關聯子 | 完全收斂 |
| **L4 網路** | LADD 引力路由 | 網路分區 / CAP（$H^1$） | FLP 不可能性（$H^2$） | 全域共識 |
| **L5 信任** | ORDER 投票 | 信任相位差 | 治理矛盾 | 最終權威 |

**意義：**
- 每個工程決策同時指定它位於哪個 $L_r$ 層和哪個 $E_r$ 頁。
- 同一 $H^2$ obstruction 在 L2 表現為型別衝突，在 L4 表現為 FLP 不可能性——它們的代數形式相同但物理語境不同。
- 本表（欄＝degree）只展開到 $E_3$／$H^2$。各層更深的特徵障礙——L3 計算視界 / 16-cell（$H^3$）、L4 拜占庭 BFT（$H^3$）、L5 女巫攻擊（$H^4$）——出現在 $E_4$／$E_5$ 頁；完整的 CAP / FLP / 拜占庭 / 女巫 $=H^1$/$H^2$/$H^3$/$H^4$ 分散式階梯見 **[APP_07](./APP_07_The_Obstruction_Ladder.md) §4**。
- 上同調障礙（$H^1$–$H^4$）的完整定義和證明見 **[系列論文](https://github.com/co-nlang/research)** 。$H^2$ 障礙（KS 互文性）的無枚舉代數證明見 **[Papers XVI–XVII](https://github.com/co-nlang/research)** ；$H^3$ 障礙於 $n=4$ 消滅、$n \geq 5$ 開啟，並截斷於 $H^3$（不延伸至 $H^4$）現已為定理，見 **[Papers XX–XXII](https://github.com/co-nlang/research)**。

### 4.3 規格根架構 (@n_spec)

為了實現規格的自我驗證（Self-hosting），`n/` 定義了標準的規格根結構。任何符合規格的引擎，其內建的 `@n_spec` 節點必須滿足下列幾何約束：

```nlang
@n_spec: {
    %kind: #type
    version: r"v\d+\.\d+\.\d+(-[a-z0-9.]+)?$"

    ;; 規格分層
    layers: {
        @L0: @Combo, @L1: @Combo, @L2: @Combo,
        @L3: @Combo, @L4: @Combo, @L5: @Combo
    }

    ;; 法典索引：標示各 SPEC 文件的權威 CAID
    codex: {
        @SPEC: [@hash]  ;; 18 個核心章節
        @REAL: [@hash]  ;; 物理具現標準
        @ORDER: [@hash] ;; 治理秩序
    }

    ;; 語義校驗態射
    /validate: (instance: @Combo) -> @bool | _|_
}
```

### 4.4 規格演化與格式版本映射 (Version Mapping)
為了確保內容定址 (CAID) 的穩定性，語言版本與物理格式版本的映射關係如下：

| 語言版本 (Spec) | 預設格式版本 (fmt) | 支援範圍 | 變更說明 |
| :--- | :--- | :---: | :--- |
| **`v0.1.0-genesis`** | **`v1`** | `v1` | 物理創世 |
| **`v0.1.0-alpha.1`** | **`v1`** | `v1` | 引入 LADD 概念 |
| **`v0.1.0-alpha.2`** | **`v2`** | `v1`~`v2` | 引入 CAID v2 |
| **`v0.1.0-alpha.3`** | **`v2`** | `v1`~`v2` | 阻礙階梯定理, COSMOLOGY 重構 |
| **`v0.2.0`** (分水嶺) | **`v2`**（凍結） | `v1`~`v2` | 規格穩定宣告：SYNTAX_01–12 定稿、`$` P1–P5、惰性/增量收斂語義、快照與 Range 裁決。Changelog 自本版起筆（`spec/CHANGELOG.md`）；版號政策見 `meta/VERSIONING.md` |
| **`v0.3.0-draft.1`** | **`v2`**（凍結） | `v1`~`v2` | OODP 上線期之累積：節點與操作者身分分家、廣告與 `#discover`/`#find_node` 落地、耐久對等目錄、本地 GC、線上非成功回應一律說出為什麼。**破壞性 #7「x 的 CAID 就是 x 的 CAID」**。與 `meta/VERSIONING.md` §6.2 同時記錄：規格自 v0.2.0 起停號 334 個提交，本版為其修正 |
| **`v0.4.0-draft.1`** | **`v2`**（凍結） | `v1`~`v2` | 歸屬聲明（REAL_02 §4.2.8）：操作者對「某節點屬於我」之簽署；撤銷即到期（30 日上限），不設撤銷清單。REAL_01 §7.6 身分族判別表由五問增為**六問** |
| **`v0.5.0-draft.1`** | **`v2`**（凍結） | `v1`~`v2` | 哪八個（REAL_02 §4.3.5.1）：`#discover` 溢出時每次查詢抽一次均勻樣本，而非任何排序——**決定性的規則是攻擊者也能離線算的規則**；`#find_node` 維持決定性，因其答案提問者可查證 |
| **`v0.6.0-draft.1`** | **`v2`**（凍結） | `v1`~`v2` | 撥號需要同意（REAL_02 §4.2.6.1）：以遠端位址建立取物來源須出示能力，且**閘先於效果**；SPEC_08 §6.1.4 能力格**軸一擴充第三類**（使引擎主動對外連線者）。**破壞性 #8** |
| **`v0.7.0-draft.1`** | **`v2`**（凍結） | `v1`~`v2` | 歸屬信任根（REAL_02 §4.2.8.1）：工作區以閉合資料 `.oo/discovery.n` 宣告哪些操作者之歸屬聲明得於未來構成准入同意；只建立根、不自動准入，且與服務令牌、治理、套件三份權威清單分離 |
| **`v0.8.0-draft.1`** (目前) | **`v2`**（凍結） | `v1`~`v2` | 直接觀察來源性（REAL_02 §4.2.5、§4.2.6、§4.3.3–§4.3.4、§5.1.2）：區分 `direct`、`relayed`、`unknown`，以 exact signed advertisement 合併觀測半邊；對等點目錄仍與取物來源集合分離，本版不自動准入；fmt v2 與 `.oo/format 1` 不變 |
| **`v1.0.0`** (預計) | **`v2`** | `v1`~`v2` | Epoch 0（ORDER_00 §5） |

*註 1：任何對規範化演算法的修改均會導致 `fmt_version` 提升。詳見 **[REAL_03](./REAL_03_CAID_Protocol.md)**。*
*註 2（誠實聲明）：`fmt v2` 的位元佈局在穩定化期間（alpha.2 → v0.2.0）曾有未版本化變更（值正規化 `Atom(Top/Bottom)`、thunk 序列化之 canonical 列印正規化、`TAG_RANGE` 新增），豁免依據＝無既存宇宙依賴。**自 v0.2.0 起 v2 凍結**：任何影響 CAID 位元的變更一律提升 `fmt_version` 並走 SPEC_10 `#refine` 遷移。*

### 4.5 規範體系與法律效力 (Hierarchy of Authority)

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
*   **意義**：這是 **CAID (內容定址)** 的物理基礎。確保了相同幾何結構在宇宙任何角落皆具備唯一且永恆的身分。
*   **規範化要求**：計算雜湊前必須進行語義等價的格式化處理（見 **[REAL_03](./REAL_03_CAID_Protocol.md)**）。

### 🔒 Invariant 2 — 資訊單調性 (Monotonic Knowledge)
*   **意義**：宇宙的資訊量隨時間單調遞增。知識一旦坍縮即不可逆，演化本質上是幾何空間的持續精煉。

### 🔒 Invariant 3 — 觀測純粹性 (Observation Purity)
*   **意義**：確保了平行觀測的安全性與等價性。

### 🔒 Invariant 4 — 複合封閉性 (Combo Closure)
*   **意義**：貫徹「萬物皆 Combo」的幾何統一性。

### 🔒 Invariant 5 — 邊界一致性 (Top/Bottom Consistency)
*   **意義**：界定了宇宙的邏輯極限。

---

## 6. 規格書導航 (The Code of n/)

本法典分為五卷，描述了宇宙從格論到網路的完整規律。關於各章節的 **當前狀態與開發目標**，請參閱 **[README §4：待辦事項與優先順序](./README.md)**。

### 卷一：公設 (The Axioms) —— 宇宙的理
1.  **[SPEC_01: 格論公設](./SPEC_01_Foundation_and_Lattice.md)**
2.  **[SPEC_02: 詞法結構](./SPEC_02_Lexical_Structure.md)**
3.  **[SPEC_03: 複合結構](./SPEC_03_Combo_System.md)**

### 卷二：流轉 (The Dynamics) —— 宇宙的氣
4.  **[SPEC_04: 導航與詞法作用域](./SPEC_04_Navigation_and_Duality.md)**
5.  **[SPEC_05: 三位一體同構](./SPEC_05_The_Trinity_Isomorphism.md)**
6.  **[SPEC_06: 統一化邏輯](./SPEC_06_Unification_Logic.md)**
7.  **[SPEC_07: 態射與管道](./SPEC_07_Logic_and_Pipe.md)**

### 卷三：法度 (The System) —— 宇宙的格論
8.  **[SPEC_08: 運行時與計算視界](./SPEC_08_Meta_and_Runtime.md)**
9.  **[SPEC_09: 代數憲法與標準庫](./SPEC_09_Standard_Library.md)**
10. **[SPEC_10: 演化與因果邊界](./SPEC_10_Evolution_and_Commit.md)**
11. **[SPEC_11: 反映與合成](./SPEC_11_Reflection_and_Synthesis.md)**

### 卷四：體系 (The Architecture) —— 宇宙的網
12. **[SPEC_12: 遞迴與驗證](./SPEC_12_Logic_Validation_and_Recursion.md)**
13. **[SPEC_13: 銜尾蛇發現協定 (OODP)](./SPEC_13_Ouroboros_Discovery_Protocol.md)**
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
- **[APP_04: 數學基礎](./APP_04_Mathematical_Foundations.md)**
- **[APP_05: 全域邏輯格與 LADD](./APP_05_LADD_Global_Logic_Lattice.md)**
- **[APP_06: 語義大一統理論](./APP_06_Unified_Field_Theory.md)**
- **[GUIDE_01: 排版風格指南](./GUIDE_01_Style_and_Formatting.md)**
- **[GUIDE_02: 引擎優化指南](./GUIDE_02_Engine_Optimization.md)**
- **[GUIDE_03: 增量收斂引擎設計](./GUIDE_03_Incremental_Convergence.md)**
- **[COSMOLOGY: 數位宇宙學 (附錄系列)](./COSMOLOGY/00_COSMOLOGY_Overview.md)**
