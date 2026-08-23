# n/ 法典：繁體中文正體版 (The n/ Code - zh_TW)

本目錄存放 `n/` 語言的繁體中文規範文件。作為 Epoch 0 的發源語系，本目錄下的文件被視為當前宇宙的「主導規格」。


---

## 1. 📚 目錄索引 (Table of Contents)

### 核心法典 (The Core Spec)
- **[SPEC_00: 緒論 (Introduction)](./SPEC_00_Introduction.md)**
- **[SPEC_01: 格論公設 (Lattice)](./SPEC_01_Foundation_and_Lattice.md)**
- **[SPEC_02: 詞法結構 (Lexical)](./SPEC_02_Lexical_Structure.md)**
- **[SPEC_03: 複合結構 (Combo)](./SPEC_03_Combo_System.md)**
- **[SPEC_04: 導航與詞法作用域 (Lexical Scope) (Navigation)](./SPEC_04_Navigation_and_Duality.md)**
- **[SPEC_05: 三位一體同構 (Trinity)](./SPEC_05_The_Trinity_Isomorphism.md)**
- **[SPEC_06: 統一化邏輯 (Unification)](./SPEC_06_Unification_Logic.md)**
- **[SPEC_07: 態射與管道 (Morphism)](./SPEC_07_Logic_and_Pipe.md)**
- **[SPEC_08: 運行時與計算視界 (Runtime)](./SPEC_08_Meta_and_Runtime.md)**
- **[SPEC_09: 代數憲法與標準庫 (StdLib)](./SPEC_09_Standard_Library.md)**
- **[SPEC_10: 演化與因果邊界 (Causal Boundary) (Commit)](./SPEC_10_Evolution_and_Commit.md)**
- **[SPEC_11: 反映與合成 (Reflection)](./SPEC_11_Reflection_and_Synthesis.md)**
- **[SPEC_12: 遞迴與驗證 (Recursion)](./SPEC_12_Logic_Validation_and_Recursion.md)**
- **[SPEC_13: 銜尾蛇發現協定 (OODP)](./SPEC_13_Ouroboros_Discovery_Protocol.md)**
- **[SPEC_14: 正式語法 (Grammar)](./SPEC_14_Formal_Grammar.md)**
- **[SPEC_15: 反模式 (Anti-Patterns)](./SPEC_15_Anti_Patterns.md)**
- **[SPEC_16: 測試與證明 (Testing)](./SPEC_16_Testing_and_Proof.md)**
- **[SPEC_17: 自我演化 (Self-Evolution)](./SPEC_17_Self_Evolution.md)**
- **[SPEC_18: 餘韻 (Echo)](./SPEC_18_The_Echo.md)**

### 語法細則 (Syntax — 施行細則)
> 規範性，位階在 SPEC 之下。把 `n/` 從邊界（Type）的法帶到紙面（Data）的存在，逐構造釘死寫法與邊界情況、消除未定義行為。文法上位規範見 SPEC_14。
- **[SYNTAX_00: 語法細則總則與慣例](./SYNTAX_00_Conventions.md)** ← 從這裡開始（定位、位階、章節格式、索引）
- SYNTAX_01–12：詞法、字面量、路徑、Combo、前綴本體論、比較與集合運算、觀測對偶、元數據、態射應用與中綴運算、Enum/Poset、態射定義、管道與上下文（**01–12 全數 `[穩定]`**（2026-07-05 定稿）；macro/import 已除名；`$` P1–P5 定案；索引見 SYNTAX_00 §5，引擎同步清單見 meta/ENGINE_SYNC.md）

### 具現標準 (Realization Standards)
- **[REAL_01: Ouroboros 工程實作](./REAL_01_Ouroboros_Engineering.md)**
- **[REAL_02: 通訊協定規範](./REAL_02_Ouroboros_Protocols.md)**
- **[REAL_03: CAID 物理協議](./REAL_03_CAID_Protocol.md)**
- **[REAL_04: %cause 標準結構](./REAL_04_Causal_Chain_Protocol.md)**
- **[REAL_05: 合規測試與 MVP](./REAL_05_Compliance_and_MVP.md)**

### 演化秩序 (Evolutionary Order)
- **[ORDER_00: 臨時治理憲法](./ORDER_00_Interim_Constitution.md)**
- **[ORDER_01: 演化與治理](./ORDER_01_Evolution_and_Governance.md)**

### 附錄 (Appendices)
- **[APP_01: 熱帶幾何擴展](./APP_01_Tropical_Geometry.md)**
- **[APP_02: 形式化驗證戰略](./APP_02_Formal_Verification.md)**
- **[APP_03: 範式比較與遷移](./APP_03_Paradigm_Comparison.md)**
- **[APP_04: 數學基礎](./APP_04_Mathematical_Foundations.md)**
- **[APP_05: 全域邏輯格與 LADD 協議](./APP_05_LADD_Global_Logic_Lattice.md)**
- **[APP_06: 語義大一統理論](./APP_06_Unified_Field_Theory.md)**

### 工程指南 (Engineering Guides)
- **[GUIDE_01: 排版風格指南](./GUIDE_01_Style_and_Formatting.md)**
- **[GUIDE_02: 引擎優化指南](./GUIDE_02_Engine_Optimization.md)**
- **[GUIDE_03: 增量收斂引擎設計](./GUIDE_03_Incremental_Convergence.md)**

### 數位宇宙學 (Digital Cosmology)
> 物理、拓撲與哲學詮釋框架。非規格性，作為理解 n/ 更深層數學意義的導讀。

- **[COSMOLOGY/00: 數位宇宙學總論](./COSMOLOGY/00_COSMOLOGY_Overview.md)** ← 從這裡開始
- **[COSMOLOGY/01: 數位統一場論（質能等價 + 譜諧振）](./COSMOLOGY/01_PHYSICS_Unified_Field_Theory.md)**
- **[COSMOLOGY/02: 內在邏輯與正交模格](./COSMOLOGY/02_TOPOLOGY_Intrinsic_Logic.md)**
- **[COSMOLOGY/03: 數位量子力學](./COSMOLOGY/03_PHYSICS_Digital_Quantum_Mechanics.md)**
- **[COSMOLOGY/04: 語義重力與信任覆蓋](./COSMOLOGY/04_PHYSICS_Semantic_Gravity.md)**
- **[COSMOLOGY/05: 計算視界（ℏ=arity；視界深度=H³）](./COSMOLOGY/05_PHYSICS_Horizons_and_Uncertainty.md)**
- **[COSMOLOGY/06: 全像原理與真理積分](./COSMOLOGY/06_PHYSICS_Holography_and_Action.md)**
- **[COSMOLOGY/07: 觀測者主權與自我表示（n=4）](./COSMOLOGY/07_PHYSICS_Observer_Sovereignty.md)**

> **註（2026-06）：** 本系列已從 16 篇精煉為 7 篇 —— 過時的物理類比（弦論、數位 GR、大爆炸/暗能量）已移除，熱力學、Grothendieck、真理積分、語義諧振各併入相關章節。嚴格數學依據見 **Paper N（白皮書）** 與論文系列 I–XXII。

### 診斷與輔助
- **[GLOSSARY: 術語對照表](./GLOSSARY.md)**
- **[TAG_REGISTRY: 標籤登記簿](./TAG_REGISTRY.md)**
- **[QUICK_REFERENCE: 語法快速參考](./QUICK_REFERENCE.md)**
- **[PREFACE: 序言](./PREFACE.md)**

---

## 2. 閱讀路徑建議

| 讀者類型 | 建議起點 |
| :--- | :--- |
| **語言實作者** | **[SPEC_00](./SPEC_00_Introduction.md)** → **[SPEC_01](./SPEC_01_Foundation_and_Lattice.md)**~18 → REAL 系列 |
| **引擎工程師** | **[REAL_01](./REAL_01_Ouroboros_Engineering.md)** → **[GUIDE_02](./GUIDE_02_Engine_Optimization.md)** → **[GUIDE_03](./GUIDE_03_Incremental_Convergence.md)** → **[APP_05](./APP_05_LADD_Global_Logic_Lattice.md)** |
| **理論研究者** | **[COSMOLOGY/00](./COSMOLOGY/00_COSMOLOGY_Overview.md)** → **[COSMOLOGY/02](./COSMOLOGY/02_TOPOLOGY_Intrinsic_Logic.md)** → **[APP_04](./APP_04_Mathematical_Foundations.md)** |
| **一般開發者** | **[PREFACE](./PREFACE.md)** → **[SPEC_00](./SPEC_00_Introduction.md)** → **[COSMOLOGY/00](./COSMOLOGY/00_COSMOLOGY_Overview.md)** |
| **治理參與者** | **[ORDER_00](./ORDER_00_Interim_Constitution.md)** → **[ORDER_01](./ORDER_01_Evolution_and_Governance.md)** |

## 3. 規格完備性與實作地圖

下表詳細描述各章節的理論完備程度與 `oo` 引擎目前的支援狀態。

| 章節 | 語義完備性 | `oo` 實作狀態 | 關鍵缺口 |
| :--- | :---: | :---: | :--- |
| **[SPEC_01: 格論](./SPEC_01_Foundation_and_Lattice.md)** | 100% | 100% | 無 |
| **[SPEC_04: 導航](./SPEC_04_Navigation_and_Duality.md)** | 100% | 100% | 無 |
| **[SPEC_06: 統一化](./SPEC_06_Unification_Logic.md)** | 100% | 100% | 無 |
| **[SPEC_07: 態射管道](./SPEC_07_Logic_and_Pipe.md)** | 100% | 100% | 遞迴升寫深度限制實作中 |
| **[SPEC_08: 運行時](./SPEC_08_Meta_and_Runtime.md)** | 100% | 80% | 效果標籤的動態傳染驗證 |
| **[SPEC_09: 標準庫](./SPEC_09_Standard_Library.md)** | 100% | 50% | 創世預設值已規範，等待引擎實作 |
| **[SPEC_13: 銜尾蛇發現協定](./SPEC_13_Ouroboros_Discovery_Protocol.md)** | 100% | 10% | LADD 引力路由規範已正式化 |
| **[SPEC_17: 自我演化](./SPEC_17_Self_Evolution.md)** | 100% | 0% | N-1 自舉演算法規範已正式化 |
| **[COSMOLOGY: 宇宙學](./COSMOLOGY/00_COSMOLOGY_Overview.md)** | 100% | N/A | 理論定稿 |

---

## 4. 路線圖 (Roadmap)

完整路線圖移至 **[meta/ROADMAP.md](../../meta/ROADMAP.md)**（2026-07-05；本節舊 TODO 表已過時並歸檔於該處「已完成」節）。快照：

| 狀態 | 項目 |
| :---: | :--- |
| 進行中 | SYNTAX_01–10 語法細則（[SYNTAX_00](./SYNTAX_00_Conventions.md) §5）；oo 引擎 stdlib/協定 phases；claims ledger 後續（[meta/claims_ledger.md](../../meta/claims_ledger.md)） |
| 排隊中 | 規格書 Combo 化；增量收斂引擎（[GUIDE_03](./GUIDE_03_Incremental_Convergence.md)） |
| 門檻制 | 對外宣傳（intro）與 Changelog——等語言完成到一個段落（見 ROADMAP §1） |

> Review agents 請注意：spec↔論文系列的宣稱強度以 **[meta/claims_ledger.md](../../meta/claims_ledger.md)** 為準（R0/R1/R2/R3 分級）。

---

*"如其在頂，如其在底。"*
