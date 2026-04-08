# n/ Language Specification - 快速參考手冊 (Quick Reference)

本文件提供 `n/` 語言的快速查閱指南。
詳細語義請參閱各 **SPEC** 章節。

---

## 1. 運算子結合層級 (Operator Levels)

**層級數值越小 = 結合越緊密（優先權越高）**
本表與 **[SPEC_14: 正式語法](./SPEC_14_Formal_Grammar.md)** **§2.3** 完全對齊。
若有歧異，以 **[SPEC_14](./SPEC_14_Formal_Grammar.md)** 為最終權威。

| 層級 | 運算子 | 名稱 | 結合性 |
| :--- | :--- | :--- | :--- |
| 1 | `_`, `_\|_`, `()`, `{}`, `[]`, `@{}` | 原子、複合字面量與分組 | N/A |
| 1 | `_.`, `^.`, `..`, `<>` | **路徑錨點、區間與水晶透視** | N/A |
| 2 | `.`, `[]` | 成員存取與動態導航 (Lens) | 左至右 |
| 3 | **`@`** | **型別註解 (Annotation)** | 右至左 |
| 4 | `...` | 展開運算子 (Spread) | N/A |
| 5 | `!`, `-` | 單元運算 (補集、負號) | 右至左 |
| 6 | `f x` | **態射應用 (Apply)** | 左至右 |
| 7 | `/op` | **中綴邏輯調用 (Infix Logic)** | 左至右 |
| 8 | `*`, `/`, `%` | 乘法、除法、取餘 | 左至右 |
| 9 | `+`, `-` | 加法、減法 | 左至右 |
| 10 | `<`, `<=`, `>`, `>=`, `==`, `!=` | 比較運算、子型別判定 | 左至右 |
| 11 | **`&`** | **集合合併 (Merge)** | 左至右 |
| 12 | **`\|`, `\`** | **集合聯集 (Union) 與 差集** | 左至右 |
| 13 | **`\|>`** | **演化管道 (Pipe)** | 左至右 |
| 14 | `? :` | **條件收斂 (Ternary)** | N/A |
| 15 | **`->`** | **態射定義 (Morphism)** | 右至左 |
| 16 | `:` | 定義與綁定 (Binding) | 右至左 |

---

## 2. 命名空間前綴 (Namespace Prefixes)

| 前綴 | 角色 | 範例 | 說明 |
| :--- | :--- | :--- | :--- |
| (無) | **Data** (數據) | `age: 25` | 存有、狀態、數值 |
| `@` | **Type** (型別) | `@int: >= 0` | 邊界、約束、集合 |
| `/` | **Morphism** (態射) | `/add: x y -> x + y` | 變換、規律、映射 |
| `%` | **Meta** (元資訊) | `%len`, `%id` | 元數據、系統自省 |
| `~%` | **System** (系統) | `~%repl.auto_commit` | 系統物件、標準庫介面 |
| `~` | **Local** (私有) | `~tmp: 123` | 私有空間、詞法作用域 |

---

## 3. 元欄位字典 (%Meta)

| 欄位 | 型別 | 說明 |
| :--- | :--- | :--- |
| `%id` | `@str` | 內容定址標識符 (CAID) |
| `%len` | `@int` | 容器、字串或區間的長度 |
| `%branches` | `@int` | 聯集分支的數量（分歧度） |
| `%kind` | `#Tag` | 本體論角色 (`#data`, `#type`, `#logic` 等) |
| `%rules` | `@combo` | 態射的座標變換規則集（按 Pattern 規範排序） |
| `%closure` | `@combo` | 態射捕獲的外部作用域快照（閉包） |
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
| `%fmap` | `@morphism` | 函子映射介面 |
| `%fold` | `@morphism` | 可折疊聚合介面 |
| `%empty` | `@any` | 幺半群單位元 |
| `%concat` | `@morphism` | 幺半群合併介面 (映射至 `+`) |
| `%bind` | `@morphism` | 單子鏈結介面 |
| **`%compat`** | `@list \| @str` | 相容性宣告 (舊版 CAID 集合) |
| `%effect` | `#Tag` | 代數效果標記 (如 `#io`, 預設: `#pure`) |
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
| `#partial_geometry` | 幾何內容缺失（因網路斷線或未發現） |
| `#semantic_isolation` | 語義日蝕警告（幾何不連續性） |
| `#not_found` | 發現機制無法定位該 CAID |
| `#caid_mismatch` | 內容雜湊與請求的 CAID 不符 |
| `#refinement_cycle` | 精煉重定向環 (如 A->B->A) |
| `#missing_key` | 存取 Cocoon 中未定義的欄位 |
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
| **[SPEC_03](./SPEC_03_Combo_System.md)** | Combo | ⭐⭐ | 開放/封閉、Cocoon、異質展開 |
| **[SPEC_04](./SPEC_04_Navigation_and_Duality.md)** | 導航 | ⭐⭐ | 詞法作用域 (Lexical Scope)、水晶透視 |
| **[SPEC_05](./SPEC_05_The_Trinity_Isomorphism.md)** | 三位一體 | ⭐⭐⭐ | Data/Type/Logic 同構 |
| **[SPEC_06](./SPEC_06_Unification_Logic.md)** | 統一化 | ⭐⭐⭐⭐ | 合併演算法、極小元素規則 |
| **[SPEC_07](./SPEC_07_Logic_and_Pipe.md)** | 態射與管道 | ⭐⭐⭐ | 態射、管道、遞迴升寫 |
| **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** | 運行時 | ⭐⭐⭐ | 計算視界、狀態機、效果系統 |
| **[SPEC_09](./SPEC_09_Standard_Library.md)** | 標準庫 | ⭐⭐⭐ | 代數憲法、符號態射 |
| **[SPEC_10](./SPEC_10_Evolution_and_Commit.md)** | 演化 | ⭐⭐ | 因果邊界 (Causal Boundary)、核心態射 |
| **[SPEC_11](./SPEC_11_Reflection_and_Synthesis.md)** | 工具 | ⭐⭐⭐ | 規範化、Unicode NFC、反映 |
| **[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** | 遞迴 | ⭐⭐⭐ | 不動點、發散判定 |
| **[SPEC_13](./SPEC_13_Discovery_and_Package.md)** | 發現 | ⭐⭐⭐⭐ | CAID 封套、快照、精煉共識 |
| **[SPEC_14](./SPEC_14_Formal_Grammar.md)** | 文法 | ⭐⭐⭐ | PEG 定義、Unicode 識別碼 |
| **[SPEC_15](./SPEC_15_Anti_Patterns.md)** | 反模式 | ⭐⭐ | 禁止行為、歧義預防 |
| **[SPEC_16](./SPEC_16_Testing_and_Proof.md)** | 測試 | ⭐⭐ | 空間覆蓋率、證明格式 |
| **[SPEC_17](./SPEC_17_Self_Evolution.md)** | 自我演化 | ⭐⭐⭐⭐⭐ | 創世演算法、N-1 自舉 |
| **[SPEC_18](./SPEC_18_The_Echo.md)** | 餘韻 | ⭐⭐⭐ | 終極對稱 |
| **[APP_01](./APP_01_Tropical_Geometry.md)** | 熱帶擴展 | ⭐⭐⭐⭐ | 熱帶幾何與幾何優化（研究草案） |
| **[APP_02](./APP_02_Formal_Verification.md)** | 形式證明 | ⭐⭐⭐ | 戰略藍圖與機器證明路線圖 |
| **[APP_03](./APP_03_Paradigm_Comparison.md)** | 範式比較 | ⭐ | 傳統語言對照與心態轉變指南 |
| **[APP_04](./APP_04_Mathematical_Foundations.md)** | 數學基礎 | ⭐⭐⭐ | 格論與範疇論的核心應用總結 |
| **[ORDER_00](./ORDER_00_Interim_Constitution.md)** | 臨時憲法 | ⭐⭐ | 引導期治理與委員會機制 |
| **[ORDER_01](./ORDER_01_Evolution_and_Governance.md)** | 演化治理 | ⭐⭐ | Epoch 0 啟用之去中心化治理 (Draft) |
| **[REAL_01](./REAL_01_Ouroboros_Engineering.md)** | 工程實作 | ⭐⭐⭐ | 工作區結構、自舉與視界清理 |
| **[REAL_02](./REAL_02_Ouroboros_Protocols.md)** | 通訊協定 | ⭐⭐⭐ | JSON-RPC、FFI 與幾何因果鏈協議 |
| **[REAL_03](./REAL_03_CAID_Protocol.md)** | 物理協議 | ⭐⭐ | CAID 計算與序列化細則 |
| **[REAL_04](./REAL_04_Causal_Chain_Protocol.md)** | 因果結構 | ⭐⭐ | `%cause` 標準結構與標籤分類 |
| **[REAL_05](./REAL_05_Compliance_and_MVP.md)** | MVP 子集 | ⭐⭐ | 分階段實作與合規性測試 |
| **[GUIDE_01](./GUIDE_01_Style_and_Formatting.md)** | 排版風格 | ⭐ | 代碼美化與最佳實踐 |
| **[GUIDE_02](./GUIDE_02_Engine_Optimization.md)** | 引擎優化 | ⭐⭐⭐ | 熱帶幾何優化與啟發式搜尋策略 |

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

### 型別安全除法
```nlang
@NonZero: @int & !0
/safe_div: (a: @int, b: @NonZero) -> a / b
```

### 帶有轉換器 Combo 的管道
```nlang
result: data |> {
    val: $.input + 1
    status: (val > 100) ? #overflow : #ok
}
```

### 遞迴階乘與終止證明
```nlang
/fact: {
    0: 1
    n@int: n * /fact(n - 1)
    
    %termination_proof: {
        %measure: (n -> n)
        %strategy: #well_founded_induction
    }
}
```
