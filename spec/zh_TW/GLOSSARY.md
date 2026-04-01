# n/ Language Specification - Glossary (術語表)

This document defines the standard translation of key terms in the n/ language specification.
All SPEC documents should use these translations consistently.

---

## 1. Core Concepts (核心概念)

| English | Traditional Chinese | Japanese (參考) | Notes |
| :--- | :--- | :--- | :--- |
| Convergence | 收斂 | 収束 | Core computation model |
| Collapse | 坍縮 | 崩壊 | State after observation |
| Merge | 合併 | 合併 | Meet operation `&` |
| Union | 聯集 | 和集合 | Join operation `\|` |
| Complement | 補集 | 補集合 | `!A` |
| Difference | 差集 | 差集合 | `A \ B` |
| Unification | 統一化 | 統一 | Unification algorithm |
| Observation | 觀測 | 観測 | Accessing a value |

---

## 2. Structure (結構)

| English | Traditional Chinese | Japanese (參考) | Notes |
| :--- | :--- | :--- | :--- |
| Combo | Combo | コンボ | Core data structure `{}` |
| Cocoon | Cocoon (繭) | 繭 | `{{}}` closed combo |
| List | List | リスト | `[...]` |
| Tuple | Tuple | タプル | `(...)` |
| Atom | 原子 | 原子 | Indivisible value |
| Tag | 標籤 | タグ | `#label` |
| Path | 路徑 | パス | Navigation expression |
| Scope | 作用域 | スコープ | Lexical scope |
| Horizon | 視界 | 視界 | 觀測與解析的邊界。依語境分為三類：<br>1. **Lexical Horizon (詞法視界)**: 詳見 **[SPEC_04](./SPEC_04_Navigation_and_Duality.md)**，符號解析與名稱查找的範圍（由 `$` 與 `^` 定位）。<br>2. **Computational Horizon (計算視界)**: 詳見 **[SPEC_08](./SPEC_08_Meta_and_Runtime.md) §4**，物理資源的限制邊界（由 `%fuel` 與 `%timeout` 決定）。<br>3. **Observation Horizon (觀測視界)**: 詳見 **[SPEC_13](./SPEC_13_Discovery_and_Package.md) §5**，資訊坍縮的狀態範圍（由 `#blur` 與 `#exact` 標識）。 |

---

## 3. Ouroboros System (體系)

| English | Traditional Chinese | Meaning |
| :--- | :--- | :--- |
| **Ouroboros Model** | **銜尾蛇模型** | `n/` 的核心理論體系（格論、三位一體、自舉演化）。 |
| **Ouroboros Engine** | **銜尾蛇引擎** | 實現收斂與演化邏輯的具體計算核心實作（如 `oo`）。 |
| **Ouroboros Protocol** | **銜尾蛇協定** | 節點間發現、交換 CAID 與特權管理的工作協議（NDP）。 |
| **Ouroboros Symbol** | **銜尾蛇符號** | 專指 `%` 元資訊前綴，象徵系統的自我意識與自省。 |

---

## 4. Type System (型別系統)

| English | Traditional Chinese | Japanese (參考) | Notes |
| :--- | :--- | :--- | :--- |
| Type | 型別 | 型 | `@type` |
| Data | 數據 | データ | Existence/value |
| Logic | 邏輯 | 論理 | `/logic` |
| Meta | 元資訊 | メタ情報 | `%meta` |
| System | 系統 | システム | `~%system` |
| Local | 私有 | ローカル | `~local` |
| Functor | 函子 | 関手 | `%fmap` |
| Monad | 單子 | モナド | `%bind` |
| Monoid | 幺半群 | モノイド | `%empty` + `%concat` |
| Foldable | 可折疊 | 畳み込み可能 | `%fold` |

---

## 5. Logic & Computation (邏輯與計算)

| English | Traditional Chinese | Japanese (參考) | Notes |
| :--- | :--- | :--- | :--- |
| Morphism | 態射 | 射 | `/function` |
| Pipe | 管道 | パイプ | `\|>` operator |
| Lifting | 升寫 | 持ち上げ | Functor lifting |
| Application | 應用 | 適用 | Function call |
| Currying | 柯里化 | カリー化 | Auto-currying |
| Pattern Matching | 模式匹配 | パターンマッチ | |
| Recursion | 遞迴 | 再帰 | |
| Cycle | 循環 | 循環 | Circular dependency |
| Divergent | 發散 | 発散 | Non-terminating |
| Static | 靜止 | 静止 | No computation |

---

## 6. System & Tooling (系統與工具)

| English | Traditional Chinese | Japanese (參考) | Notes |
| :--- | :--- | :--- | :--- |
| Ouroboros | 銜尾蛇 | ウロボロス | Engine name |
| Engine | 引擎 | エンジン | Runtime |
| CLI | 命令列 | CLI | Command line |
| REPL | 互動式環境 | REPL | Read-eval-print loop |
| Commit | Commit | コミット | Version snapshot |
| Staged | 暫存 | ステージ | Pending changes |
| HEAD | HEAD | HEAD | Current commit |
| Discovery | 發現 | 発見 | Package discovery |
| CAID | CAID | CAID | Content-addressable ID |
| Format | 格式化 | フォーマット | `oo fmt` |
| Canonical | 規範化 | 標準化 | Normalized form |

---

## 7. Observation States (觀測狀態)

| English | Traditional Chinese | Tag | Notes |
| :--- | :--- | :--- | :--- |
| Lazy | 未觀測 | `#lazy` | Defined but not yet accessed |
| Incomplete | 不完全 | `#incomplete` | Halted by horizon limits |
| Blur | 模糊 | `#blur` | Deterministic incomplete state with CAID |
| Exact | 精確 | `#exact` | Fully converged stable state |
| Conflict | 衝突 | `_\|_` | Lattice inconsistency |

---

## 8. Mathematics (數學)

| English | Traditional Chinese | Japanese (參考) | Notes |
| :--- | :--- | :--- | :--- |
| Lattice | 格論 | 束論 | Lattice theory |
| Top | Top | 頂 | Top element `_` |
| Bottom | Bottom | 底 | Bottom element `_\|_` |
| Poset | 偏序集 | 半順序集合 | Partially ordered set |
| Supremum | 上确界 | 上限 | Least upper bound |
| Infimum | 下确界 | 下限 | Greatest lower bound |
| Isomorphism | 同構 | 同型 | Trinity isomorphism |
| Duality | 對偶性 | 双対性 | Observation duality |
| Specificity | 特異性 | 特異性 | Matching priority |
| Minimal Element | 極小元素 | 極小元 | Most specific match |

---

## 9. Philosophy (哲學)

| English | Traditional Chinese | Japanese (參考) | Notes |
| :--- | :--- | :--- | :--- |
| Trinity | 三位一體 | 三位一体 | Data/Type/Logic |
| Ontology | 本體論 | 存在論 | Ontological role |
| Epistemology | 認識論 | 認識論 | Observation theory |
| Self-Evolution | 自我演化 | 自己進化 | Language bootstrapping |
| Self-Reference | 自指 | 自己言及 | Self-description |
| Bootstrapping | 自舉 | ブートストラップ | Pulling up by own straps |

---

## 10. Translation Principles (翻譯原則)

1. **保留英文**：對於已廣泛使用的技術術語（如 Combo, CAID, Commit），保留英文不翻譯。

2. **數學術語**：遵循台灣數學界標準翻譯（如 幺半群 Monoid、格論 Lattice）。

3. **哲學概念**：使用哲學領域標準譯名（如 本體論 Ontology、認識論 Epistemology）。

4. **一致性**：同一英文術語在整個規格書中應使用相同的中文翻譯。

5. **雙語並列**：首次出現時，使用「中文 (English)」格式，後續可直接使用中文。

---

## 11. Revision History

| Date | Change | Author |
| :--- | :--- | :--- |
| 2026-03-25 | Initial glossary creation | Gali |
| | - Added translation principles | |
