# REAL_05：合規測試與 MVP (Compliance & MVP)

> **Authority**: [Standard / 物理合規性標準]  

## 1. 為什麼需要 MVP？

`n/` 的完整規格涵蓋了從格論到內容定址、再到形式化證明的龐大體系。為了確保跨引擎實作的幾何一致性，本章定義了 **「最小可用子集 (Minimum Viable n/)」** 與對應的合規等級（Compliance Tiers）。

根據 **[ORDER_01](./ORDER_01_Evolution_and_Governance.md)**，任何實作引擎必須明確聲明其符合的等級，方可參與對應語義 Epoch 的分發。

---

## 2. 三階合規等級 (Compliance Tiers)

### Level 1：結構驗證級 (Static Lattice)
**核心目標**：實現比 JSON/YAML 更強大的數據描述與靜態驗證能力。

*   **包含語法**：
    *   **格論標記**：萬有集合 `_`、衝突底 `_|_`。
    *   **基礎算子**：合併 `&`、聯集 `|`、補集 `!`、差集 `\`。
    *   **比較兩家族**(SYNTAX_06):原子 `==`/`!=`(吸收律)與集合 `=`/`<`/`<=`/`>`/`>=`(乾淨布林)——比較是靜態格論關係,屬本級。
    *   **容器結構**：組合體 `{}`、繭 `{{}}`（封閉性）、列表 `[]`、序位枚舉與區間 `..`。
    *   **導航**：路徑存取 `a.b`、視界符號 `$`。
*   **物理義務**：
    1.  **收斂決定論**：相同的靜態定義合併，必須產生一致的坍縮。
    2.  **單調性保全**：任何合併運算嚴禁減少既有的資訊量。

### Level 2：語義演化級 (Dynamic Evolution) —— [核心 MVP]
**核心目標**：實現 `n/` 的動態計算特質，展現「三位一體同構」的價值。

*   **包含能力 (Level 1 +)**：
    *   **態射 (`->`)**：Lambda 定義與柯里化應用。
    *   **管道 (`|>`)**：演化管道與自動升寫 (Lifting)。
    *   **動態鍵 (`@{}`)**：基於型別匹配的幾何搜尋。
    *   **前綴體系**：`@` (Type)、`/` (Logic)、`~` (Local)。
    *   **Nominal 型別引用**:使用者 `@Name` 定義參與合併執法(內建型別名保留);密封 `{{}}` 模板 = 窮盡 schema(SPEC_03)。
*   **物理義務**：
    1.  **視界隔離**：嚴格實作 `~` 私有欄位的幾何不可達性。
    2.  **邊界斷言**：實作 `!field_start` 以確保表達式解析的正確性。
    3.  **計算視界**：具備基礎的 `%fuel` 限制與循環偵測（防範 `#divergent`）。

### Level 3：銜尾蛇級 (The Ouroboros)
**核心目標**：實現完整的內容定址宇宙與自我演化能力。

*   **包含能力 (Level 2 +)**：
    *   **內容定址**：CAID (`%id`) 計算與 `oo fmt` 規範化。
    *   **時間演化**：Commit 模型、Staged 區、`history` 鏈。
    *   **反映與合成**：系統物件 (`~%`)、虛擬元欄位 (`%`)。
    *   **外部邊界**：代數效果系統 (`%effect`)、FFI。
*   **物理義務**：
    1.  **CAID 全域唯一性**：不同平台、不同引擎對相同內容計算出的 `%id` 必須 100% 一致。
    2.  **事務性提交**：`#commit` 必須保證原子性與因果一致性。

---

## 3. 實作者測試矩陣 (Compliance Matrix)

引擎必須 **100% 通過**宣稱等級的全部向量方可宣稱合規(v0.2.0 起;向量的
**可執行形式**存於 repo 根 **`conformance/L1|L2/`**,本節為規範性索引——
兩者同源,修改任一 = 規格變更,走 changelog 紀律)。

依 `meta/VERSIONING.md` §3:**引擎裸核版號(無 pre-release 標)= 通過
Level 2 全數向量**;Level 3 義務自 v1.0.0 起。

### 3.1 Level 1 向量(靜態格論,39 條)

| ID | 向量(語料檔) | 語義 | 期望 | 出處 |
| :-- | :-- | :-- | :-- | :-- |
| **L1-01** | `01-int-refine` | 內建型別精化 | `1` | SPEC_01/SYNTAX_05 |
| **L1-02** | `02-open-conflict` | 同欄位原子衝突 | `_\|_` `#conflict` | SPEC_03 |
| **L1-03** | `03-sealed-no-grow` | 密封不得增欄 | `_\|_` | SPEC_03 §2 |
| **L1-04** | `04-union-select` | 聯集分配選擇 | `1` | SPEC_01/SPEC_07 §4 |
| **L1-05** | `05-marker-range-member` | 型別精化區間成員 | `10` | SYNTAX_04/SPEC_02 §3 |
| **L1-06** | `06-top-identity` | ⊤ 為 & 么元 | `1` | SPEC_01 |
| **L1-07** | `07-bottom-absorb` | ⊥ 為 & 吸收元 | `_\|_` | SPEC_01 |
| **L1-08** | `08-top-meet-bottom` | ⊤ & ⊥ = ⊥ | `_\|_` | SPEC_01 |
| **L1-09** | `09-open-merge` | 開放合併聯合欄位 | `{   a: 1   b: 2 }` | SPEC_03 |
| **L1-10** | `10-list-identity` | 等列表冪等 | `[1, 2]` | SYNTAX_04 |
| **L1-11** | `11-range-member` | 區間成員 | `10` | SPEC_02 §3 |
| **L1-12** | `12-range-nonmember` | 區間非成員 | `_\|_` | SPEC_02 §3 |
| **L1-13** | `13-range-intersect` | 區間交集 | `2..3` | SPEC_02 §3 |
| **L1-14** | `14-union-range-distribute` | 聯集對區間分配 | `1` | SPEC_07 §4 |
| **L1-15** | `15-range-empty-intersect` | 空交集 → ⊥ | `_\|_` | SPEC_02 §3 |
| **L1-16** | `16-range-complement-meet` | 嚴格正性(補集×區間) | `5` | SPEC_07 §5 |
| **L1-17** | `17-complement-tag` | 正交補選擇 | `#false` | SPEC_01 §2.5 |
| **L1-18** | `18-anonset-empty` | @{} ≡ ⊥ | `_\|_` | SYNTAX_04 §4.7 |
| **L1-19** | `19-anonset-transparent` | @{e} ≡ e | `5` | SYNTAX_04 §4.7 |
| **L1-20** | `20-cmp-subset-int` | 子集序(相異單集不互含;數值偏差退役) | `#false` | SYNTAX_06 §4 #10(2026-07-20 正法) |
| **L1-21** | `21-cmp-clean-bottom` | 集合家族乾淨布林 | `#false` | SYNTAX_06 §4.2 |
| **L1-22** | `22-cmp-bottom-self` | 空集=空集 | `#true` | SYNTAX_06 §4.2 |
| **L1-23** | `23-cmp-computed-bottom` | 計算得 ⊥ = 空集 ⊆ 任何 | `#true` | SYNTAX_06 §4.2 |
| **L1-24** | `24-cmp-atomic-absorb` | 原子家族吸收律 | `_\|_` | SYNTAX_06 §4.1 |
| **L1-25** | `25-path-navigation` | 巢狀路徑導航 | `42` | SYNTAX_03 |
| **L1-26** | `26-forward-ref` | 前向引用(欄位同時性) | `5` | SPEC_03(交換律) |
| **L1-27** | `27-forward-chain` | 前向引用鏈 | `1` | SPEC_03(交換律) |
| **L1-28** | `28-union-idempotent` | 聯集冪等(x∨x=x) | `1 \| 2` | SPEC_01 |
| **L1-29** | `29-multiparam-curry` | 多參自動柯里(`x y ->` ≡ 巢狀) | `35` | SYNTAX_11 §2 |
| **L1-30** | `30-slash-def-apply` | `/` 定義之裸名應用 | `8` | SYNTAX_05/09 |
| **L1-31** | `31-tuple-destructure` | tuple 參數位置解構 | `8` | SYNTAX_11 §2 規則 4 |
| **L1-32** | `32-union-navigation` | Union 路徑導航(逐支投影) | `1 \| 2` | SPEC_07(平等演化) |
| **L1-33** | `33-combo-literal-equality` | combo `=` 外延結構等值(字面量) | `#true` | SYNTAX_06 §4 #11 |
| **L1-34** | `34-combo-bound-equality` | combo `=` span 盲測(綁定名) | `#true` | SYNTAX_06 §4 #11/#13 |
| **L1-35** | `35-combo-eqeq-conflict` | combo 遇 `==` 家族誤用大聲失敗 | `_\|_ #conflict` | SYNTAX_06 §4 #12 |
| **L1-36** | `36-hybrid-collapse-eqeq` | 混血塌縮後照原子家族比 | `#true` | SYNTAX_06 §4 #6/#12 |
| **L1-37** | `37-hybrid-observe-val` | 混血坍縮態觀測讀 `%val` | `1` | SYNTAX_06 §4 #6(統一律) |
| **L1-38** | `38-hybrid-math-operand` | 混血算術運算元剝殼 | `2` | SYNTAX_06 §4 #6(統一律) |
| **L1-39** | `39-hybrid-pipe-arg` | 混血管道引數(體內 math 衍生) | `2` | SYNTAX_06 §4 #6(統一律) |

### 3.2 Level 2 向量(語義演化/裸核閘門,123 條)

| ID | 向量(語料檔) | 語義 | 期望 | 出處 |
| :-- | :-- | :-- | :-- | :-- |
| **L2-01** | `01-pipe-list-lift` | 函子升寫 | `[2, 3]` | SPEC_07/SYNTAX_12 |
| **L2-02** | `02-morphism-apply` | 態射定義與應用 | `10` | SYNTAX_09/11 |
| **L2-03** | `03-pipe-context` | 管道語境 $(演化=合併,單調保全) | `{   name: "A"   res: …` | SYNTAX_12 |
| **L2-04** | `04-tuple-morphism-pipe` | tuple 配態射演化 | `3` | SYNTAX_12 §4/ENGINE_SYNC #16 |
| **L2-05** | `05-tuple-struct-blocked` | tuple 結構演化拒絕(密封 Cocoon) | `_\|_` | SYNTAX_12 §4 |
| **L2-06** | `06-currying` | 柯里化 | `7` | SYNTAX_09 |
| **L2-07** | `07-dispatch-minimal` | 子集模式唯一極小 | `"C"` | SPEC_07 §5 |
| **L2-08** | `08-dispatch-incomparable` | 不可比模式保疊加 | `"A" \| "B"` | SPEC_06 §/SPEC_07 |
| **L2-09** | `09-dispatch-tag-key` | tag 鍵分派 | `1` | SYNTAX_03 §10 |
| **L2-10** | `10-ternary` | 三元條件(條件改拼 `~%Math./gt`,序波 W2) | `"big"` | SYNTAX_12 |
| **L2-11** | `11-union-evolves-equally` | 疊加態平等演化 | `2 \| 3` | SPEC_07(Kleisli) |
| **L2-12** | `12-nominal-enforce` | nominal 型別執法(通過) | `{   age: 25   name: "…` | SPEC_05/SPEC_03 |
| **L2-13** | `13-nominal-violate` | nominal 型別執法(違規) | `_\|_` | SPEC_05/SPEC_03 |
| **L2-14** | `14-sealed-exhaustive` | 密封窮盡 schema | `_\|_` | SPEC_03 §2 |
| **L2-15** | `15-builtin-reserved` | 內建型別名保留 | `10` | SYNTAX_05 |
| **L2-16** | `16-free-context-bottom` | 自由 $ 觀測 → ⊥ | `_\|_` `#no_context` | SYNTAX_12 §4($ P3) |
| **L2-17** | `17-divergence` | 自指發散偵測 | `_\|_` `#divergent` | SPEC_12/REAL_05 §2 |
| **L2-18** | `18-float-projection` | int→float 投影 | `1` | SYNTAX_02 |
| **L2-19** | `19-range-anchor-default` | 缺界錨點+型別精化 | `6..#_` | SPEC_02 §3 |
| **L2-20** | `20-deep-recursion-type` | 遞迴型別終止 | `1` | SPEC_05(E4) |
| **L2-21** | `21-runaway-cause-honest` | runaway 態射 cause 誠實 | `#fuel_exhausted` | SPEC_08 §3.2.2 |
| **L2-22** | `22-flat-exhaustion-cause` | 平場燃料耗盡 %cause(視界傳播) | `#fuel_exhausted` | SPEC_08 §3.2.2 |
| **L2-23** | `23-config-home-fuel` | `~%Config.fuel` 裸名觀測(視界參數之家) | `10000` | SPEC_08 §3.1 |
| **L2-24** | `24-nav-blur-absorb` | 導航遇 `#blur` 吸收(座標語境) | `#fuel_exhausted` | SPEC_08 §3.2.2 #5 |
| **L2-25** | `25-eq-blur-self-true` | `=` 同 CAID 快照 → `#true`(決定論) | `#true` | SPEC_08 §3.2.2 #6 |
| **L2-26** | `26-eq-blur-twin-absorb` | `=` 異快照吸收(不得 `#false`) | `#fuel_exhausted` | SPEC_08 §3.2.2 #6 |
| **L2-27** | `27-caid-meta-total` | `%caid` meta 可導航、全可判比較 | `#true` | SPEC_08 §3.2.2 #4 |
| **L2-28** | `28-bottom-nav-compositional` | ⊥ 導航合成性(內聯 meta 讀) | `#conflict` | SYNTAX_08 §4 #3 |
| **L2-29** | `29-cause-collapses-tag` | `%cause` 對偶坍縮為標籤 | `#conflict` | REAL_04 §1 |
| **L2-30** | `30-no-cause-open` | 未坍縮節點無因可溯 → 開放 | `_` | SYNTAX_08 §4 #2 |
| **L2-31** | `31-atom-nav-open` | 原子座標缺失 = 開放(#invalid_path 廢止) | `_` | TAG_REGISTRY 廢止注記 |
| **L2-32** | `32-private-outward-blocked` | 外部點路徑 → 違規坍縮 | `#private_access_violation` | SPEC_04 §3.1 #3/#5 |
| **L2-33** | `33-private-inward-spec-example` | 向內可見(規格 factory 範例) | `43` | SPEC_04 §3.1 #1/§3.2 |
| **L2-34** | `34-private-morphism-capture` | 態射值捕獲(閉包 scope) | `8` | SPEC_04 §3.3 |
| **L2-35** | `35-private-display-strip` | 觀測投影剝除 local 軸 | `{ pub: 2 }` | SPEC_04 §3.1 #4 |
| **L2-36** | `36-spread-no-exfiltration` | 外部展開排除私有欄 | `_` | SPEC_03 §3.1 |
| **L2-37** | `37-spread-public-only-eq` | 外部展開結果僅公有軸 | `#true` | SPEC_03 §3.1 |
| **L2-38** | `38-spread-insider-keeps` | 內部展開保全(語料形) | `1` | SPEC_03 §3.1 |
| **L2-39** | `39-spread-collision-intersect` | 展開碰撞交集合併(非覆寫) | `#conflict` | SPEC_03 §3.1/§3.1.1 |
| **L2-40** | `40-literal-repeated-key-merge` | 字面量重複鍵合併(平行定義退化形) | `#conflict` | SPEC_03 §1.1 |
| **L2-41** | `41-atom-spread-val` | 原子展開同構 `{%val: v}` | `#ok` | SPEC_03 §3.1 |
| **L2-42** | `42-circular-spread-divergent` | 循環展開保護 | `#divergent` | SPEC_03 §3.1 |
| **L2-43** | `43-lexical-sibling-thunk` | 兄弟欄裸名解析(詞法鏈) | `6` | SPEC_04 §2.1 |
| **L2-44** | `44-lexical-holder-morphism` | 態射體讀 holder 兄弟欄 | `6` | SPEC_04 §2.1/§3.3 |
| **L2-45** | `45-lexical-shadowing-inner-first` | 內層遮蔽外層(先到先得) | `8` | SPEC_04 §2.1 |
| **L2-46** | `46-lexical-grandparent-lifting` | 非根祖先作用域提升 | `6` | SPEC_04 §2.1 |
| **L2-47** | `47-lexical-three-hop-chain` | ≥3 跳兄弟鏈(全遞迴) | `12` | SPEC_04 §2.1 |
| **L2-48** | `48-cocoon-sibling-lexical` | cocoon 兄弟欄裸名解析 | `6` | SPEC_04 §2.1+SPEC_03 §1.2 |
| **L2-49** | `49-cocoon-shadowing-inner-first` | cocoon 內層遮蔽外層 | `8` | SPEC_04 §2.1 |
| **L2-50** | `50-cocoon-eigenstate-access` | 本徵態預設:未定義鍵 ⊥ | `#missing_key` | SPEC_03 §1.2/§1.3 |
| **L2-51** | `51-cocoon-merge-top-field-allowed` | 合併拒絕限非 Top 欄 | `1` | SPEC_03 §1.2 #2 |
| **L2-52** | `52-cocoon-union-missing-cull` | 聯集導航剔 ⊥ 支(cocoon 缺鍵) | `2` | SPEC_03 §1.3+REAL_04 §4 |
| **L2-53** | `53-static-cycle-top` | 靜止循環 → Top(root/combo 同律) | `_` | SPEC_12 §1.1 |
| **L2-54** | `54-combo-transform-divergent` | 變換循環 → ⊥(combo 層同律) | `#divergent` | SPEC_12 §2.2/§1.1 #3 |
| **L2-55** | `55-static-cycle-cause` | 帶因 Top:`%cause` 讀 `#static_cycle` | `#static_cycle` | SPEC_12 §1.1/SYNTAX_08 §4 #2 |
| **L2-56** | `56-plain-top-no-cause` | **裸** Top 無因(`_` 字面量;開放缺欄帶因見 L2-91) | `_` | SYNTAX_08 §4 #2 + SPEC_01 §2.4.2 |
| **L2-57** | `57-blur-spread-absorb` | Blur 展開源吸收(快照傳出) | `#fuel_exhausted` | SPEC_03 §3.1+SPEC_08 §3.2.2 |
| **L2-58** | `58-blur-spread-nested` | 巢內 Blur 展開逐節點吸收 | `#fuel_exhausted` | SPEC_03 §3.1 |
| **L2-59** | `59-top-spread-noop` | Top 展開 no-op(分界綠釘) | `1` | SPEC_03 §3.1 |
| **L2-60** | `60-system-key-reserved` | combo 內 `~%` 定義鍵 ⊥ | `#system_reserved` | SPEC_09 所有權+TAG_REGISTRY §1.4 |
| **L2-61** | `61-system-novel-reserved` | novel `~%` 名同違法 | `#system_reserved` | SPEC_09 所有權 |
| **L2-62** | `62-system-rhs-import` | RHS 別名/匯入合法(分界綠釘) | `2` | SPEC_09 所有權+SYNTAX_05 |
| **L2-63** | `63-two-source-bottom-blur` | 二源展開 ⊥×blur 序盲(摺疊律) | `#conflict` | SPEC_03 §3.1+SPEC_06 |
| **L2-64** | `64-system-effect-clean` | 效果預測誠實(~%Math 純) | `3` | SPEC_09 §4 |
| **L2-65** | `65-blur-merge-caid-verbatim` | `&`×blur 快照原樣(綠釘) | `#true` | SPEC_08 §3.2.2 #1 |
| **L2-66** | `66-caret-parent-shadowing` | `^` 上溯父容器(遮蔽決定形) | `1` | SYNTAX_03 §4.4 #4 |
| **L2-67** | `67-caret-reaches-root` | 容器鏈含根宇宙(`^^` 達 root) | `42` | SYNTAX_03 §4.4 #4(a) |
| **L2-68** | `68-caret-overshoot-cause` | overshoot 觀測 ⊥(綠釘) | `#out_of_horizon` | SPEC_07 §4.2.3 |
| **L2-69** | `69-union-thunk-bottom-cull` | 聯集導航 thunk ⊥ 支剔除 | `1` | SPEC_08 §3.2.2 #5 |
| **L2-70** | `70-union-all-bottom-primary` | 聯集全 ⊥ 主因果(`#divergent` 優先) | `#divergent` | REAL_04 §4 |
| **L2-71** | `71-union-field-join-cull` | 觀測出口 `\|` ⊥ 成員剔除 | `5` | SPEC_08 §3.2.2 #5 |
| **L2-72** | `72-union-static-member-survives` | 靜止環聯集支存活(帶因 Top=診斷成員,吸收豁免) | `9 \| _` | SPEC_12 §1.1 + SPEC_01 §2.4.2 |
| **L2-73** | `73-union-transform-member-culled` | 變換環聯集支依法剔(綠釘) | `1` | SPEC_12 §1.1 + SPEC_08 §3.2.2 #5 |
| **L2-74** | `74-math-union-distributes` | math 對聯集分配 | `3 \| 10` | SPEC_07 §4 平等演化 |
| **L2-75** | `75-math-union-top-branch` | Top 支經 math 存活開放 | `10 \| _` | SPEC_07 §4 + F4a 開放律 + SPEC_01 §2.4.1 |
| **L2-76** | `76-union-canonical-display` | 拼法=值的函數(先存者拼法獲勝違法) | `2 \| 9` | SPEC_01 §2.4.1 |
| **L2-77** | `77-union-display-type-rank` | 顯示型別族階排序 | `1 \| 3 \| "b" \| #t` | SPEC_01 §2.4.1 |
| **L2-78** | `78-type-alias-retired` | `.%type` 化石讀法退役(⊥ 原樣傳出) | `_\|_` `#conflict` | REAL_04 §1(2026-07-19 調和) |
| **L2-79** | `79-body-caret-definition-side` | 態射體 `^` 尾鏈=定義側(勿洩呼叫鏈) | `5` | SPEC_07 §4.2.3(2026-07-19) |
| **L2-80** | `80-body-caret-root-def` | root 持有態射 `^`=root(勿呼叫點動態) | `5` | SPEC_07 §4.2.3(2026-07-19) |
| **L2-81** | `81-forward-spread-basic` | 前向源展開(交換律,收斂時擴張) | `7` | SPEC_03 §3.1(2026-07-19) |
| **L2-82** | `82-forward-spread-bottom` | 前向 ⊥ 源傳因(位置無關) | `#conflict` | SPEC_03 §3.1 + REAL_04 |
| **L2-83** | `83-effect-meta-read-io` | `.%effect` 元讀(io 原子) | `#io` | SPEC_08 §4.1(2026-07-20) |
| **L2-84** | `84-effect-cocoon-shield` | Cocoon 效果屏蔽(`.%effect`=`#pure`) | `#pure` | SPEC_08 §4.2.1 |
| **L2-85** | `85-combo-subtype-order` | combo 子型別序(`(A&B)=A` 歸約) | `#true` | SYNTAX_06 §2.1/§3(2026-07-20) |
| **L2-86** | `86-union-inclusion-order` | 聯集支集合包含序 | `#true` | SYNTAX_06 §2.1(2026-07-20) |
| **L2-87** | `87-union-absorb-type` | 吸收正規化(型別蓋原子) | `#true` | SPEC_01 §2.4.2(2026-07-20) |
| **L2-88** | `88-union-coverage-order` | 開放 combo 支覆蓋序(吸收自癒) | `#true` | SPEC_01 §2.4.2 + SYNTAX_06 §2.1 |
| **L2-89** | `89-union-top-absorb` | **裸** Top 支塌縮 | `_` | SPEC_01 §2.4.2 |
| **L2-90** | `90-union-static-cycle-order-blind` | 靜止環聯集支序盲 | `#true` | SPEC_12 §1.1 + SPEC_01 §2.4.2 |
| **L2-91** | `91-open-miss-cause` | 開放缺欄帶因 Top(`#no_coordinate`) | `#no_coordinate` | TAG_REGISTRY §1.1(2026-07-20) |
| **L2-92** | `92-union-nav-open-miss-survives` | 聯集導航:開放缺欄支存活(不被吸收) | `1 \| _` | SPEC_01 §2.4.2 |
| **L2-93** | `93-type-super-int-num` | `%super` 反映欄取型別樹直接父 | `#true` | SPEC_05 §3.2(裁定 R1) + SPEC_09 §2.1 |
| **L2-94** | `94-type-super-fixed-width` | 定寬整數之直接父為 `@int` | `#true` | SPEC_05 §3.2(裁定 R1) + SPEC_09 §2.1 |
| **L2-95** | `95-type-name-reflection` | 型別名經 `%name` 反映 | `"int"` | SPEC_05 §3.2(裁定 R1) |
| **L2-96** | `96-type-top-no-super` | 萬有型 `@any`(⊤)無父,誠實開放缺欄 | `_` | SPEC_05 §3.2(裁定 R1) |
| **L2-97** | `97-effect-compose-union` | 效果組合＝標籤集聯集(兩支) | `#io \| #nondet` | SPEC_08 §4.1 |
| **L2-98** | `98-effect-compose-three` | 效果組合＝標籤集聯集(三支) | `#io \| #nondet \| #state` | SPEC_08 §4.1 |
| **L2-99** | `99-effect-compose-unify` | 合一(`&`)亦取效果聯集 | `#io \| #nondet` | SPEC_08 §4.1 + §4.2 |
| **L2-100** | `100-effect-violation-declared-pure` | 宣告 `#pure` 被實際活動效應反證 | `_\|_` `#effect_violation` | SPEC_08 §4.3(靜態守護,裁定 A) + TAG_REGISTRY |
| **L2-101** | `101-effect-pure-honest` | 誠實的 `#pure` 宣告照常成立 | `#pure` | SPEC_08 §4.3 |
| **L2-102** | `102-effect-pure-cocoon-escape` | 繭 `{{ }}` 屏蔽副作用(非特權逃生門) | `#pure` | SPEC_08 §4.3 |
| **L2-103** | `103-effect-runpure-unprivileged` | 非特權視界呼叫 `runPure` 遭拒 | `_\|_` `#privileged_required` | SPEC_08 §4.3 + §6.1.2(裁定 P1) |
| **L2-104** | `104-project-down-named-params` | `project_down` 具名參數與 `#blur` 截面 | `#blur` 截面 | SPEC_08 §3.5 |
| **L2-105** | `105-import-is-spread` | 匯入＝頂層展開;展開後裸名解析得到 | `"yes"` | SYNTAX_05 §4 邊界 #6 + SPEC_03 §3.1(O72) |
| **L2-106** | `106-spread-opens-a-cocoon` | 展開卸下封閉外殼(解封特性) | `#false` | SPEC_03 §3.1(解封特性) |
| **L2-107** | `107-spread-commutes` | 展開可交換——書寫順序不改變結果 | `#true` | SPEC_03 §3.1(碰撞合併) + §1 重複鍵合併 |
| **L2-108** | `108-spread-keeps-field-effect` | 展開逐欄位保留效果標籤(非純者) | `#nondet` | SPEC_03 §16.4 + SPEC_08 §4.1 |
| **L2-109** | `109-underscore-is-the-default-branch` | `_:` 作為鍵＝預設分支(Combo 施用) | `99` | SPEC_07 §1.1.1(O72 ⑥) |
| **L2-110** | `110-spread-keeps-a-pure-field-pure` | 展開不憑空製造效果(純者仍純) | `#pure` | SPEC_03 §16.4 + SPEC_08 §4.1 |
| **L2-111** | `111-meet-of-two-spreads-keeps-both` | 兩個展開結果相 meet,兩邊的鍵都在 | `["a", "b"]` | REAL_03 §6.9 + SPEC_03 §3.1 |
| **L2-112** | `112-meet-of-two-spreads-commutes` | 該 meet 可交換——換邊不換答案 | `#true` | REAL_03 §6.9 + SPEC_03 §1(欄位同時性/交換律) |
| **L2-113** | `113-meet-of-two-spreads-keeps-a-conflict` | 被丟掉的運算元不得把「不同意」一起帶走 | `_\|_` `#conflict` | REAL_03 §6.9 + SPEC_03 §3.1(碰撞合併) |
| **L2-114** | `114-meet-of-two-modules-keeps-both-names` | 兩個標準模組相 meet,兩邊的名字都解析得到 | `3` | REAL_03 §6.9 + SPEC_09 §3(`~%Math`) + §5.2(`~%Cond`) |
| **L2-115** | `115-declared-pure-survives-no-application` | 一層態射應用不得洗白 `#pure` 宣告 | `_\|_` `#effect_violation` | SPEC_08 §4.3(宣告守護,O74 ①) |
| **L2-116** | `116-a-discarded-boolean-keeps-its-obstruction` | 謂詞的布林被丟掉,障礙仍在 | `_\|_` `#effect_violation` | SPEC_08 §4.3(施用即觀測,O74 ①) |
| **L2-117** | `117-an-honest-pure-predicate-is-writable` | 誠實的純謂詞必須寫得出來(保守宣告不是替代品) | `1` | SPEC_08 §4.3(O74 ④) |
| **L2-118** | `118-a-cocoon-discharges-the-obstruction` | 繭 discharge 障礙——**綠圍籬向量,兩版皆通**,收錄以防日後把逃生門當漏洞關掉 | `#pure` | SPEC_08 §4.3(繭是 discharge) + TAG_REGISTRY |
| **L2-119** | `119-durable-keys-are-not-a-backdoor` | **耐久形自己的鍵不是後門**——`~%__nlang_effect` 作為 combo 定義鍵仍 ⊥。L2-61 釘的是任意新名(`~%Mine`);本條釘的是**引擎在耐久形裡自己用的那些鍵**,若有實作為了讓耐久形能被一般源碼寫出而開放它們,L2-61 不會抓到 | `#system_reserved` | REAL_03 §6.8.3(字面僅於耐久形內合法,表層不得改變) + SPEC_09 所有權 |
| **L2-120** | `120-a-declared-list-shape-answers` | `~%List./count` 宣告的形（謂詞在前、資料在後）答對 | `3` | SPEC_09 §5.1.1 + SYNTAX_09 §2 #1(O76／O78) |
| **L2-121** | `121-an-undeclared-list-shape-does-not-silently-answer` | 未宣告的鍵形不得給出一個像是在數三個元素的答案（繭仍帶 `%builtin`，不是 `0`／`3`） | `"list.count"` | SPEC_09 §5.1.1 + SYNTAX_09 §2 #1(O76) |
| **L2-122** | `122-a-collapsed-predicate-is-not-a-false-one` | 塌陷的謂詞與誠實的 `#false` 必須可分辨（塌陷交 `_|_`，不是 `0`） | `_\|_` `#conflict` | SPEC_08 §4.3(O77) + SPEC_09 §5.1.1 |
| **L2-123** | `123-truth-is-the-atom-not-anything-not-false` | **真＝原子 `#true`，不是「非 `#false`」**——本弧之前 `~%Query./where`／`/take_while`／`/drop_while` 走寬鬆判準，謂詞回 `#none` 會**保留**該元素；三個真值判準統一後為 `0`。規格此前從未定義「謂詞為真」 | `0` | SPEC_09 §5.1.1(2026-08-26 補) |

### 3.3 Level 3(銜尾蛇級)

CAID 全域一致性、事務性提交、反映系統之向量**待 v1.0.0 前另波補齊**
(依 ORDER_00 時程;屆時 `%cause` 比對升為 MUST)。

### 3.4 Runner 契約

見 **`conformance/README.md`**(規範性):觀測欄位 `out`、canonical print
逐字元比對、⊥ 之雙通道判定、`%cause` 行於 L1/L2 為 SHOULD、L3 起 MUST。**（2026-09-12 釐清，D65）該行是 `.%cause` 這條通道的投影，不是值本體的一部分**——語料以獨立一行寫它，正是因為值本體是裸 `_|_`；引擎側對應的載體是診斷註解層的 `;; %cause: <tag>`（`SPEC_11` §3.4）。**⟹ 升為 MUST 時要求的是「成因說得出來」，不是「成因印在值裡」。**
參考實作:`scripts/run-conformance.py`。

### 3.5 現況記錄(資訊性,2026-07-12)

參考引擎 nlang-tools **v0.2.0(首個裸核版,2026-07-12 定版)**:**45/45**
——Level 2 矩陣全綠(於 tag 所在 commit 實測),L2-17 發散偵測補齊
(`a: a + 1` → `_|_ (%cause: #divergent)`),⊥ 顯示帶 `%cause` 標籤
(runner 之 cause 比對於 L1/L2 已可實測,L3 起 MUST 不變)。
裸核門檻(VERSIONING §3:去 pre-release 標)達成並已行使。
2026-07-12 增 L1-26/27(前向引用,SPEC_03 交換律的可執行化),同日引擎側
結案:dev `f9dd657` 起 47/47,**v0.2.1 定版於 47/47 實測 commit**。
同日再增 L1-28(聯集冪等)並於同日結案:dev 起 **48/48**
(`normalize_union`:結構等值、首現保序、單倖存坍縮)。
2026-07-12 語料清理後 G2 重新診斷,增 L1-29(多參自動柯里,SYNTAX_11
既有裁定的可執行化;**開單時紅**,引擎追法)與 L1-30(`/` 定義應用,
開單時即綠、入法看守)。同日 G2 三件結案(零代修;parser 去糖 +
root 影蓋 evolve 邊界攔截 + 原子×態射 ⊥):**50/50**;
**引擎 v0.2.3 同日定版**(tag 於 50/50 實測 commit)。
同日增 L1-31(tuple 參數位置解構,SYNTAX_11 規則 4 可執行化;
開單時紅 = G5 工單門)並同日結案(零代修;`%params` 打包 + 分派側
位置解構):**51/51**;**引擎 v0.2.4 同日定版**(tag 於實測 commit)。
同日增 L1-32(Union 路徑導航,SPEC_07 平等演化之觀測投影;開單時紅
= G4 工單門)並同日結案(零代修;navigate_segments Union 臂逐支投影):
**52/52**;**引擎 v0.2.5 同日定版**(tag 於實測 commit)。
2026-07-13 G1 combo 等值裁定入法(SYNTAX_06 §4 #11–13:`=` 固化後
外延結構等值、`==` 家族誤用 → ⊥ #conflict、固化防火牆 span 盲),
增 L1-33~36(**開單時四紅** = G1 工單門,引擎追法);矩陣 52→**56**;同日結案(零代修;固化 + 家族邊界):**56/56**;**引擎 v0.2.6 同日定版**(tag 於實測 commit)。
同日 G6 值語境統一律入法(SYNTAX_06 §4 #6 + SYNTAX_07 §4 #6 對偶),
增 L1-37~39(**開單時三紅** = G6 工單門);矩陣 56→**59**;同日結案(一件代修:結構標記導航透明化):**59/59**;**引擎 v0.2.7 同日定版**(tag 於實測 commit;`oo --version` 自此綁 git tag)。
2026-07-13 G3 重診斷(真相 = 視界抹除:預設策略 Blur 之一等 #blur
快照被值語境 catch-all 鑄成 ⊥ #conflict,通用於一切燃料耗盡)+
視界傳播律入法(SPEC_08 §3.2.2:值語境吸收/引數載體/cause 誠實/
meta 回 BlurCause),增 L2-21/22(**開單時兩紅** = G3 工單門);
矩陣 59→**61**;同日結案(零代修):**61/61**;**引擎 v0.2.8 同日定版**(tag 於實測 commit)。
同日視界參數劃家入法後增 L2-23(`~%Config.fuel` 裸名觀測;開單時紅
= config 收斂單門);矩陣 61→**62**;翌日結案 2026-07-14(零代修
第九例):**62/62**(workspace 887/0/3、語料 74/0);**引擎 v0.2.9
同日定版**(tag 於實測 commit)。
Blur 邊界律入法後增 L2-24~27(座標吸收/`=` 二段律/`%caid` meta;
L2-25 開單時即綠=法釘,餘三紅 = 工單門);矩陣 62→**66**;
同日結案(一件代修:導航合成性):**66/66**(workspace 907/0/3、
語料 74/0)。
⊥ meta 觀測整流 + #invalid_path 廢止入法後增 L2-28~31(合成性/
%cause 坍縮/無因開放/原子開放;開單時四紅 = 工單門);矩陣 66→**70**;
同日結案(一件代修:聯集交換律=多重集等值):**70/70**(workspace
930/0/3、語料 74/0);**引擎 v0.2.10 同日定版**(tag 於實測 commit)。
私有軸實施+`~.` 錨廢止入法後增 L2-32~35(外阻/內通/捕獲/顯示剝除;
開單時四紅 = 工單門);矩陣 70→**74**;同日結案(零代修):**74/74**
(workspace 948/0/3、語料 74/0);**引擎 v0.2.11 同日定版**(tag 於
實測 commit)。
spread 私有保全開單後增 L2-36~38(外部排除/等值僅公有/內部保全
=開單時即綠法釘);矩陣 74→**77**;同日結案(零代修):**77/77**
(workspace 959/0/3、語料 74/0);**引擎 v0.2.12 同日定版**(tag 於
實測 commit)。
展開碰撞交集合併弧開單後增 L2-39~42(碰撞交集/重複鍵合併/原子
展開/循環保護;開單時四紅 = 工單門);矩陣 77→**81**;同日結案
(零代修):**81/81**(workspace 984/0/3、語料非 pending 78/0,
口徑漂移註記見 ENGINE_SYNC);**引擎 v0.2.13 同日定版**(tag 於
實測 commit)。
詞法作用域弧開單後增 L2-43~46(兄弟欄/holder 態射/遮蔽/祖先提升;
開單時四紅 = 工單門);矩陣 81→**85**;同日結案(一件代修:跨層
%id 分裂):**85/85**(workspace 1005/0/3、語料零敗;≥3 跳鏈/
cocoon 兄弟=既有債另案)。
詞法鏈補完弧開單後增 L2-47~49(≥3 跳鏈/cocoon 兄弟/cocoon 遮蔽;
開單時三紅 = 工單門);矩陣 85→**88**;同日結案(零代修):
**88/88**(workspace 1022/0/3、語料零敗;語料耗時淨改善);
**引擎 v0.2.14 同日定版**(tag 於實測 commit)。
cocoon 本徵態預設弧開單後增 L2-50~52(未定義鍵 ⊥/Top 欄合併
放行/聯集剔支;開單時三紅 = 工單門);矩陣 88→**91**;同日結案(零代修):**91/91**(workspace 1038/0/3、語料零敗;釘衝突停報=協議首次正確觸發,遷移由驗收方補辦);**引擎 v0.2.15 同日定版**(tag 於實測 commit)。
互指/自指裁定入法後增 L2-53~56(靜止循環 Top/變換循環 ⊥ 同律/
帶因 Top %cause/普通 Top 無因=開單即綠法釘;開單時三紅 = 工單
門);矩陣 91→**95**;同日結案(一件代修:環成員未含全環):**95/95**(workspace 1051/0/3、語料零敗);**引擎 v0.2.16 同日定版**(tag 於實測 commit)。
Blur 展開源裁定入法後增 L2-57~59(展開吸收快照傳出/巢內逐節點/
Top no-op 分界=開單即綠法釘;開單時兩紅 = 工單門);矩陣 95→**98**;
同日結案(零代修):**98/98**(workspace 1064/0/3、語料零敗;新曝光
另案:二源 ⊥×blur 序依賴)。
系統軸所有權裁定入法後增 L2-60~62(combo `~%` 鍵 ⊥/novel 名同/
RHS 匯入=開單即綠法釘;開單時兩紅 = 工單門;root 大聲死面留探針);
矩陣 98→**101**。同日結案(一件代修:路徑鍵拼法穿透——中間節
點物化還魂無聲影蓋,整欄塌首段):**101/101**(workspace 1078/0/3、
語料零敗;幻影 #io RHS 面=既有債反事實歸因另案)。
**引擎 v0.2.17 同日定版**(tag 於實測 commit)。
cause 正典審計裁定入法後增 L2-63~65(二源摺疊/效果誠實/`&`×blur
CAID 原樣=開單即綠法釘;開單時兩紅 = 工單門);REAL_04 §2 類別法
重寫+§4 優先級重立法+TAG_REGISTRY 正典地位;矩陣 101→**104**。同日
結案(零代修):**104/104**(workspace 1087/0/3、語料零敗;
`#invalid_path` 活鑄點歸零=F4 承諾兌現;幻影 #io 根治)。
**引擎 v0.2.18 同日定版**(tag 於實測 commit)。
`^` 解析裁定入法後增 L2-66~68(上溯遮蔽/root 可達/overshoot 綠法
釘;開單時兩紅 = 工單門;LHS `^` 定義鍵廢止=文法面留探針);
矩陣 104→**107**。同日結案(零代修):**107/107**(workspace
1122/0/3、語料零敗;新曝光另案:態射體內 `^` 綁呼叫點容器=
動態綁定風味,裁定候選)。
**引擎 v0.2.19 同日定版**(tag 於實測 commit)。
2026-07-17 G4 惰性 ⊥ 收帳開單(零新裁定,SPEC_08 §3.2.2 #5「僅
`_|_` 支剔除」+REAL_04 §4 主因果引擎追法):量測=剔除律無單一居所
——僅 unify 分配臂(root evolve 路徑)與導航臂即時 Bottom 比對持有,
導航投影不 force(thunk ⊥ 全漏、`%cause` 投影成因果聯集、`= 1` 謊
#false),force/observe 出口全不剔(欄內直接 `|` ⊥ 成員裸曬=比帳載
更寬之新面);全 ⊥ 鑄造丟成員誠實訊息(「empty union after
normalize」行話)。增 L2-69~71(**開單時三紅 = 工單門**);矩陣
107→**110**。校準曝光另案:靜止環×聯集投影語境分歧(CLI evolve
固化=`9 | _` vs harness 惰性投影=`9 | ⊥ #divergent`,SPEC_12 家族)。
同日結案(零代修第十九例):**110/110**(workspace 1137/0/3、語料
74/0;blur/Top 支存活對抗全正;靜止環另案升級=誤判成員如今被依法
剔除,`_` 支靜默消失,兩語境皆 `9`)。
同日靜止環染色作用域弧開單(零新裁定,SPEC_12 Q2 環自身跳+Q4 不
傳播引擎追法;**帳載修正第九次**:「CLI vs harness 語境分歧」框架
=量測誤差,真變因=同觀測內先行 force 之非純引用兄弟毒染
`chain_transform_taint`〔儀器直讀:字面量 `9` 觸發 TAINT_SET〕+
分類時點;twin-eq `#false` 等值謊入紅門);增 L2-72(**開單時紅
=工單門**)/73(綠法釘);矩陣 110→**112**。同日結案(零代修第
二十例):**112/112**(workspace 1151/0/3、語料 74/0;taint 向上
寫回拆除單點修;跨欄變換環兩拼法對抗保 #divergent;twin-eq 謊癒)。
**引擎 v0.2.20 同日定版**(tag 於實測 commit,條件閘一次成功)。
同日 math×聯集分配弧開單(零新裁定,SPEC_07 §4 疊加態平等演化引擎
追法;重診斷:裸 Top math 全健康,帳載「math×Top」實為 eval_math
無 Union 臂之投影——全 math 族對聯集 ⊥ #conflict 僭稱,管道/應用
已分配;⊥ 支剔+全 ⊥ 原樣沿剔除弧、Top/blur 支單值臂存活、左主序
決定性);增 L2-74/75(**開單時兩紅 = 工單門**);矩陣 112→**114**。同日
結案(零代修第二十一例):**114/114**(workspace 1168/0/3、語料
74/0;越單變更審核通過=整除除零 ⊥ #numerical_error 引擎追法
TAG_REGISTRY 明文;全 ⊥ 同位階取最左原樣平手律對抗驗證)。
**引擎 v0.2.21 同日定版**(tag 於實測 commit,條件閘一次成功)。
2026-07-18 正典顯示序弧開單(裁定 A 案=SPEC_01 §2.4.1 新法:聯集
顯示為正典排序拼法,型別族階+族內序、穩定、只動顯示層、禁 digest
鍵;病灶=CAID 序無關而顯示依演化史,先存者拼法全域獲勝/無關欄位
隔空改寫拼法);L2-75 期望依法遷移 `10 | _`,增 L2-76(拼法無關)
/77(型別族階)(**開單時三紅 = 工單門**);矩陣 114→**116**。
同日結案(代碼零修;協議代修一筆=交付方單方遷移兩相遇序舊釘,
內容追認、G3 預告條款兌現;共責=開單漏遷×2):**116/116**
(workspace 1185/0/3、語料 74/0;對抗含 combo 內嵌/nav 合成/
TopCaused 殿後全正)。曝光另案:雙 blur 聯集顯示序跨行程非決定
(%caid 鹽經顯示字串滲入排序鍵;修法候選=blur 族內鍵改
(%cause, 視界參數))。同日 blur 鍵去鹽弧結案(零代修第二十二例:
§2.4.1 #5 修訂鍵=(cause,fuel,strategy) 排鹽;雙 blur 8 次 CLI 序
證鹽已非鍵)。**引擎 v0.2.22 同日定版**(tag 於實測 commit,條件閘
一次成功)。
2026-07-19 cause cocoon 調和弧開單(裁定 A 案+設計考古:REAL_04 §1
重寫=%val 唯一核+%-前綴診斷欄依類變形;%type 化石廢止、`.%type`
退役;鷹架不可見;二源 ⊥×blur 已癒照記);8 條向量 `.%type`→
`.%cause` 改拼、增 L2-78(**開單時紅=門**);矩陣 116→**117**。
超級衝突另案開帳:SPEC_02 §1.2/SPEC_05 §2.1 舊 %type 語 vs
SPEC_03 §4 %kind 模型(nominal 機構+REAL_03 序列化面,裁定候選)。
同日結案(代碼零修;協議代修一筆第二連=交付方單方遷移 probe/語料
`.%type` 期望,忠實改寫追認;共責=開單掃描漏全樹):**117/117**
(workspace 1206/0/3、語料 74/0;繭類變形淨、鷹架隱、用戶 `_:5`
保全;cause 繭 CAID 一次性合法位移)。
2026-07-19 續:%kind 超級衝突裁定 B 全套並全數落地(B1 軸語正名/
B2 內部表示宣告/B3 引擎 #type 統一 L2 矩陣不動/B4 REAL_03 範例
實態化;B5 掛帳);態射體 `^` 定義側全鏈裁定+結案(L2-79/80,
矩陣 117→**119**;三通道各一法);前向引用×spread 收斂時序收帳
+結案(L2-81/82,矩陣 119→**121**;一件代修=驗收抓漏 cocoon
目標面,in_evolve 相位旗標+重建保 pending;CAID 前向/實心孿生
收斂 #true;容器雙形({}/{{}})教訓入紅線;evolve 期急切計算×
pending 開放 combo=既有債另案)。

## 4. 通過標準 (Compliance Criteria)

1.  **語義正確性**：必須 100% 通過上述測試矩陣。
2.  **診斷品質**：發生 `_|_` 時，必須提供符合 **[REAL_04](./REAL_04_Causal_Chain_Protocol.md)** 的最低限度 `%cause` 標籤。
3.  **效能獨立性**：規格不強制效能指標，但 Level 2 以上引擎必須提供合理的預設燃料限制。

---

## 5. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_00](./SPEC_00_Introduction.md)** | 定義了六層架構，與本章分級對應。 |
| **[ORDER_01](./ORDER_01_Evolution_and_Governance.md)** | 定義了宣稱合規的治理義務與流程。 |
| **[REAL_01](./REAL_01_Ouroboros_Engineering.md)** | 提供針對各合規等級的具體工程實作指引。 |
