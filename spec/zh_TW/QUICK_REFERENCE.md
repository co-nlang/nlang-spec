# n/ Language Specification - 快速參考手冊 (Quick Reference)

本文件提供 `n/` 語言的快速查閱指南。
詳細語義請參閱各 **SPEC** 章節；書寫細則見 **SYNTAX** 系列。
（2026-07-07 依 SPEC_14 定稿版全表重生成——語法凍結於 SYNTAX_00–12 全數 `[穩定]`。）

---

## 1. 運算子結合層級 (Operator Levels)

**層級數值越小 = 結合越緊密（優先權越高）**
本表與 **[SPEC_14: 正式語法](./SPEC_14_Formal_Grammar.md)** **§2.3** 完全對齊。
若有歧異，以 **[SPEC_14](./SPEC_14_Formal_Grammar.md)** 為最終權威。

| 層級 | 運算子 | 名稱 | 結合性 |
| :--- | :--- | :--- | :--- |
| 1 | `_`, `_\|_`, `()`, `{}`, `{{}}`, `[]`, `(x,)`, `@{}`, `#{}` | 原子、複合字面量與分組 | N/A |
| 1 | `_.`, `^.`, `..`, `<<expr>>` | **路徑錨點、區間與水晶透視（雙角括號）** | N/A |
| 2 | `.`, `[]` | 成員存取與動態導航 (Lens) | 左至右 |
| 3 | **`@`** | **型別註解 (Annotation)** | 左至右 |
| 4 | `...` | 展開運算子 (Spread) | N/A |
| 5 | `!` | 單元運算（正交補）——**負號屬字面量**（`-5`、`-i` 是原子；W1-1，SYNTAX_02 §4.3） | 右至左 |
| 6 | `f x` | **態射應用 (Apply)**——帶護欄：運算元後的 `-` `*` `/f` 等讓位給中綴層（`a -1` 是減法；SYNTAX_09 §4 #9） | 左至右 |
| 7 | `a /op b` | **中綴邏輯調用 (Infix Logic)**——`/` 與識別碼間**不得**有空白 | 左至右 |
| 8 | `*`, `/`, `%` | 乘法、除法、取餘（`/`/`%` 帶 `!ident` 護欄——`a /f`、`a %len` 非除法/取餘） | 左至右 |
| 9 | `+`, `-` | 加法、減法（`-` 空白規則見 SYNTAX_02 §4.3） | 左至右 |
| 10 | **`&`** | **集合合併 (Merge)**——比比較運算**緊**（與 C 相反；SPEC_14 §2.3、SYNTAX_06 §1） | 左至右 |
| 11 | `<=>`, `<`, `<=`, `=`, `>=`, `>`, `==`, `!=` | 比較運算——**兩家族**：格論/集合 `< <= = >= >`（不塌縮）／原子 `== !=`（塌縮）；`<=>` 方向探測（回傳序位標籤；SYNTAX_10） | **不可鏈式**（單次） |
| 12 | **`\|`, `\`** | **集合聯集 (Union) 與 差集** | 左至右 |
| 13 | **`\|>`** | **演化管道 (Pipe)** | 左至右 |
| 14 | `? :` | **條件收斂 (Ternary)**——分支為管道層級；巢狀三元**必須**括號（SYNTAX_12 §4 #1） | N/A |
| 15 | **`->`** | **態射定義 (Morphism)** | 右至左 |
| 16 | `:` | 定義與綁定 (Binding) | 右至左 |

---

## 2. 命名空間前綴 (Namespace Prefixes)

| 前綴 | 角色 | 範例 | 說明 |
| :--- | :--- | :--- | :--- |
| (無) | **Data** (數據) | `age: 25` | 存有、狀態、數值 |
| `@` | **Type** (型別) | `@nat: 0..` | 邊界、約束、集合 |
| `/` | **Morphism** (態射) | `/add: x y -> x + y` | 變換、規律、映射 |
| `%` | **Meta** (元資訊) | `%len`, `%id` | 元數據、系統自省 |
| `~%` | **System** (系統) | `~%Repl.auto_commit` | 系統物件、標準庫介面 |
| `~` | **Local** (私有) | `~tmp: 123` | 私有空間、詞法作用域 |

**結構化組合（SPEC_14 §2.2）**：合法形式共八種——無前綴、`@`、`/`、`%`、`~%`、`~`、
`~@`（私有型別）、`~/`（私有態射）。自由疊加（如 `%@a`）**非法**。

---

## 3. 元欄位字典 (%Meta)

| 欄位 | 型別 | 說明 |
| :--- | :--- | :--- |
| `%id` | `@str` | 內容定址標識符 (CAID) |
| `%len` | `@int` | 容器、字串或區間的長度 |
| `%branches` | `@int` | 聯集分支的數量（分歧度） |
| `%kind` | `#Tag` | 本體論角色 (`#data`, `#type`, `#logic` 等) |
| `%rank` | `@int` | Poset 序位（引擎衍生屬性；使用者應經 `<=`/`<=>` 讀取，SYNTAX_10 §2.4） |
| `%rules` | `@combo` | 態射的分支規則集，Key 是輸入 Pattern（排序見 REAL_03 §5.2；語義見 SPEC_05 §3.3） |
| `%closure` | `@combo` | 態射捕獲的外部作用域快照（閉包）——承重，不得省略（SPEC_05 §3.3） |
| `%code` | `@any` | 某一分支的被引述本體；引述不是求值（SPEC_05 §3.3） |
| `%builtin` | `@str` | 引擎本地的原生實作名；**使用者資料不得含之**（SPEC_05 §3.3） |
| `%cause` | `@any` | 衝突或發散的因果溯源鏈 |
| `%strategy` | `#Tag` | 視界策略 (`#blur`, `#strict`, `#approximate`) |
| `%fuel` | `@int` | 觀測容許的空間半徑 (燃料 / MBU) |
| `%timeout` | `@int` | 觀測容許的時間半徑 (毫秒) |
| **`~%Engine.mass_map`** | `@combo` | 全域幾何質量 ($m$) 分布反映 |
| **`~%Engine.heat_map`** | `@combo` | CAID 熱度與蒸發能級反映 |
| **`~%Engine.horizons`** | `@combo` | 目前計算光錐與剩餘燃料反映 |
| `%max_branches` | `@int` | 允許的最大聯集分支數（複雜度上限） |
| `%max_unification_depth` | `@int` | 遞迴合併的最大深度（防止堆疊溢位） |
| `%max_pattern_nodes` | `@int` | 模式匹配的最大節點數（防組合爆炸） |
| `%max_lifting_depth` | `@int` | 管道函子升寫的最大深度 |
| `%fmap` | `@morphism` | 函子映射介面 |
| `%fold` | `@morphism` | 可折疊聚合介面 |
| `%empty` | `@any` | 幺半群單位元 |
| `%concat` | `@morphism` | 幺半群合併介面 (映射至 `+`) |
| `%bind` | `@morphism` | 單子鏈結介面 |
| **`%compat`** | `@list \| @str` | 相容性宣告 (舊版 CAID 集合) |
| `%effect` | `#Tag` | 代數效果標記 (如 `#io`, 預設: `#pure`)——tuple 不屏蔽效應，Cocoon 才屏蔽（SYNTAX_04 §2.5）；`.%effect` 可讀（SPEC_08 §4.1），顯示尾註 `;; %effect:` 屬診斷註解層（SPEC_11 §3.4） |
| `%termination_proof` | `#Tag \| @morphism` | 遞迴終止性的形式化證明 |
| `%migration` | `@morphism` | 版本遷移態射 |
| `%privilege_token` | `@str` | 特權模式訪問憑證 |

---

## 4. 因果標籤 (%cause)

| 標籤 | 意義 |
| :--- | :--- |
| `#conflict` | 靜態邏輯不相容 (如 `1 & 2`) |
| `#divergent` | 動態非終止發散 (如 `a: a + 1`) |
| `#recursive_lazy` | 合法的結構遞迴標記 |
| `#fuel_exhausted` | 觀測燃料耗盡 (#incomplete) |
| `#no_context` | 自由 `$` 在無包圍演化下被觀測（SPEC_07 §4.2 P3） |
| `#out_of_horizon` | 路徑上溯超過嵌套層數（`^` 過度穿透；SPEC_07 §4.2.3） |
| `#order_conflict` | Poset 合併出現矛盾序位（SYNTAX_10 §2.5） |
| `#partial_geometry` | 幾何內容缺失（因網路斷線或未發現） |
| `#semantic_isolation` | 語義日蝕警告（幾何不連續性） |
| `#not_found` | 發現機制無法定位該 CAID |
| `#caid_mismatch` | 內容雜湊與請求的 CAID 不符 |
| `#refinement_cycle` | 精煉重定向環 (如 A->B->A) |
| `#missing_key` | 存取 Cocoon 中未定義的欄位（含 tuple × 結構演化加鍵，SYNTAX_12 §4 #7） |
| `#cocoon_isolation_violation` | 態射升寫非法穿透 Cocoon 隔離界限 |
| `#lifting_failed` | 管道演化中的函子升寫失敗 |
| `#compat_conflict` | 版本相容性檢查失敗 |
| `#effect_violation` | 純粹語境中觸發了副作用或 IO |

---

## 5. 法典導航表 (Navigation)

本表彙整法典全卷。**認知負荷評級僅供參考，讀者可視自身背景彈性調整閱讀順序。**

| 章節 | 主題 | 認知負荷 | 核心概念 |
| :--- | :--- | :---: | :--- |
| **[SPEC_00](./SPEC_00_Introduction.md)** | 介紹 | — | 哲學、六層架構、守恆定律 |
| **[SPEC_01](./SPEC_01_Foundation_and_Lattice.md)** | 格論 | ⭐ | Top/Bottom, Meet/Join, 補集 |
| **[SPEC_02](./SPEC_02_Lexical_Structure.md)** | 詞法 | ⭐ | 前綴、原子、運算子層級 |
| **[SPEC_03](./SPEC_03_Combo_System.md)** | Combo | ⭐⭐ | 疊加態預設/本徵態封閉、Cocoon、異質展開 |
| **[SPEC_04](./SPEC_04_Navigation_and_Duality.md)** | 導航 | ⭐⭐ | 詞法作用域 (Lexical Scope)、水晶透視 `<<...>>` (正交投影算子 $P_a$) |
| **[SPEC_05](./SPEC_05_The_Trinity_Isomorphism.md)** | 三位一體 | ⭐⭐⭐ | Data/Type/Logic 同構 |
| **[SPEC_06](./SPEC_06_Unification_Logic.md)** | 統一化 | ⭐⭐⭐⭐ | 合併演算法、極小元素規則 |
| **[SPEC_07](./SPEC_07_Logic_and_Pipe.md)** | 態射與管道 | ⭐⭐⭐ | 態射、管道、`$` P1–P5、遞迴升寫 |
| **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** | 運行時 | ⭐⭐⭐ | 計算視界、狀態機、效果系統 |
| **[SPEC_09](./SPEC_09_Standard_Library.md)** | 標準庫 | ⭐⭐⭐ | 代數憲法、符號態射 |
| **[SPEC_10](./SPEC_10_Evolution_and_Commit.md)** | 演化 | ⭐⭐ | 因果邊界 (Causal Boundary)、核心態射 |
| **[SPEC_11](./SPEC_11_Reflection_and_Synthesis.md)** | 工具 | ⭐⭐⭐ | 規範化、Unicode NFC、反映 |
| **[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** | 遞迴 | ⭐⭐⭐ | 不動點、發散判定 |
| **[SPEC_13](./SPEC_13_Ouroboros_Discovery_Protocol.md)** | 發現 | ⭐⭐⭐⭐ | CAID 封套、快照、精煉共識 |
| **[SPEC_14](./SPEC_14_Formal_Grammar.md)** | 文法 | ⭐⭐⭐ | PEG 定義、Unicode 識別碼（**語法最終權威**） |
| **[SPEC_15](./SPEC_15_Anti_Patterns.md)** | 反模式 | ⭐⭐ | 禁止行為、歧義預防 |
| **[SPEC_16](./SPEC_16_Testing_and_Proof.md)** | 測試 | ⭐⭐ | 空間覆蓋率、證明格式 |
| **[SPEC_17](./SPEC_17_Self_Evolution.md)** | 自我演化 | ⭐⭐⭐⭐⭐ | 創世演算法、N-1 自舉 |
| **[SPEC_18](./SPEC_18_The_Echo.md)** | 餘韻 | ⭐⭐⭐ | 終極對稱 |
| **[SYNTAX_00](./SYNTAX_00_Conventions.md)** | 語法細則總則 | ⭐ | 系列地圖、位階（SPEC 之下）、除名記錄 |
| **[SYNTAX_01](./SYNTAX_01_Lexical_Structure.md)** | 詞法細則 | ⭐ | 空白顯著性、註解、行結構 |
| **[SYNTAX_02](./SYNTAX_02_Literals_and_Atoms.md)** | 字面量 | ⭐ | 負號字面量化（W1-1）、複數、kebab 識別碼 |
| **[SYNTAX_03](./SYNTAX_03_Paths_and_Assignment.md)** | 路徑與賦值 | ⭐ | 三種 `_` 形、賦值即交集、單行鍵 |
| **[SYNTAX_04](./SYNTAX_04_Combo_Construction.md)** | 容器 | ⭐ | `{}`/`{{}}`/`@{}`/`[]`/tuple/range、展開 `...` |
| **[SYNTAX_05](./SYNTAX_05_Prefix_Ontology.md)** | 前綴本體論 | ⭐ | 八種合法前綴、交集即匯入 |
| **[SYNTAX_06](./SYNTAX_06_Comparison_and_Subtyping.md)** | 比較與子型別 | ⭐⭐ | 兩家族分離、吸收律、`&` 反 C 優先序 |
| **[SYNTAX_07](./SYNTAX_07_Observation_Duality.md)** | 觀測對偶 | ⭐⭐ | `x` vs `<<x>>`（坍縮態／結構態） |
| **[SYNTAX_08](./SYNTAX_08_Metadata.md)** | 元數據 | ⭐ | `%` 宣告 vs 派生、寫入協商 |
| **[SYNTAX_09](./SYNTAX_09_Morphism_Application.md)** | 態射應用 | ⭐⭐ | juxtaposition/infix、apply 護欄、算術中綴 |
| **[SYNTAX_10](./SYNTAX_10_Enum_and_Poset.md)** | Enum/Poset | ⭐⭐ | `#{}` 序位鏈、`<=>` 方向探測、`%rank` |
| **[SYNTAX_11](./SYNTAX_11_Morphism_Definition.md)** | 態射定義 | ⭐⭐ | `->`、分派表、匿名態射、柯里化 |
| **[SYNTAX_12](./SYNTAX_12_Pipe_Ternary_and_Context.md)** | 管道與上下文 | ⭐⭐ | `\|>` 三形態、`? :`、`$` P1–P5 |
| **[APP_01](./APP_01_Tropical_Geometry.md)** | 熱帶擴展 | ⭐⭐⭐⭐ | 熱帶幾何與幾何優化 |
| **[APP_02](./APP_02_Formal_Verification.md)** | 形式證明 | ⭐⭐⭐ | 戰略藍圖與機器證明路線圖 |
| **[APP_03](./APP_03_Paradigm_Comparison.md)** | 範式比較 | ⭐ | 傳統語言對照與心態轉變指南 |
| **[APP_04](./APP_04_Mathematical_Foundations.md)** | 數學基礎 | ⭐⭐⭐ | 格論與範疇論的核心應用總結 |
| **[APP_05](./APP_05_LADD_Global_Logic_Lattice.md)** | LADD協議 | ⭐⭐⭐⭐ | 全域邏輯格與引力路由 |
| **[APP_06](./APP_06_Unified_Field_Theory.md)** | 大一統理論 | ⭐⭐⭐⭐⭐ | EML、Solèr 與 Bohrification 的量子化演化 |
| **[APP_07](./APP_07_The_Obstruction_Ladder.md)** | 障礙階梯 | ⭐⭐⭐⭐ | H¹–H⁴ 工程對照字典 |
| **[ORDER_00](./ORDER_00_Interim_Constitution.md)** | 臨時憲法 | ⭐⭐ | 引導期治理與委員會機制 |
| **[ORDER_01](./ORDER_01_Evolution_and_Governance.md)** | 演化治理 | ⭐⭐ | Epoch 0 啟用之去中心化治理 (Draft) |
| **[REAL_01](./REAL_01_Ouroboros_Engineering.md)** | 工程實作 | ⭐⭐⭐ | 工作區結構、自舉與視界清理 |
| **[REAL_02](./REAL_02_Ouroboros_Protocols.md)** | 通訊協定 | ⭐⭐⭐ | JSON-RPC、FFI 與幾何因果鏈協議 |
| **[REAL_03](./REAL_03_CAID_Protocol.md)** | 物理協議 | ⭐⭐ | CAID 計算與序列化細則 |
| **[REAL_04](./REAL_04_Causal_Chain_Protocol.md)** | 因果結構 | ⭐⭐ | `%cause` 標準結構與標籤分類 |
| **[REAL_05](./REAL_05_Compliance_and_MVP.md)** | MVP 子集 | ⭐⭐ | 分階段實作與合規性測試 |
| **[GUIDE_01](./GUIDE_01_Style_and_Formatting.md)** | 排版風格 | ⭐ | 代碼美化與最佳實踐 |
| **[GUIDE_02](./GUIDE_02_Engine_Optimization.md)** | 引擎優化 | ⭐⭐⭐ | 熱帶幾何優化與啟發式搜尋策略 |
| **[GUIDE_03](./GUIDE_03_Incremental_Convergence.md)** | 增量收斂 | ⭐⭐⭐ | DAG 與快取的實作指南 |
| **[GUIDE_04](./GUIDE_04_EML_Execution_Strategy.md)** | EML 執行策略 | ⭐⭐⭐⭐ | 數值穩定性、硬體優化與精度權衡 |

---

## 6. 特殊符號與對偶性

| 符號 | 名稱 | 格論維度 (垂直) | 序位維度 (水平) |
| :--- | :--- | :--- | :--- |
| `_` | Top | 萬有集合 / 任意值 | N/A |
| `_\|_` | Bottom | 空集合 / 衝突 | N/A |
| `#_` | End | N/A | 最大元 / 正無限 |
| `#_\|_` | Start | N/A | 最小元 / 負無限 |

---

## 7. 快速範例

### 型別安全除法（分派表約束第二參數；分支值的 `$` ＝ 被匹配輸入）
```nlang
@NonZero: @int & !0
/safe_div: a -> { @NonZero: a / $ }
```

### 帶有轉換器 Combo 的管道
```nlang
result: data |> {
    val: $.input + 1
    status: (val > 100) ? #overflow : #ok
}
```

### Poset 與方向探測（SYNTAX_10）
```nlang
~Status: #{ #draft <= #review < #publish }
ok:  ~Status.#draft <= ~Status.#publish    ;; #true（格論軌，布林）
dir: ~Status.#draft <=> ~Status.#publish   ;; #lt（方向軌，序位標籤）
```

### Tuple 位置輸入（密封包裹配態射演化；SYNTAX_12 §4 #7）
```nlang
sum: (1, 2) |> (p -> $.0 + $.1)            ;; 3
ext: { ...(1, 2) } |> { s: $.0 + $.1 }     ;; 顯式拆封後才可加欄位
```

### 遞迴階乘與終止證明
```nlang
/fact: {
    0: 1
    n: @int & n * /fact(n - 1)

    %termination_proof: {
        %measure: (n -> n)
        %strategy: #well_founded_induction
    }
}
```
