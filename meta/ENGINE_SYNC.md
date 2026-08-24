# ENGINE_SYNC — 參考引擎符合性與交付紀錄

> **文件角色（2026-08-13 釐清）**：本檔起於 n.pest／SPEC_14 同步清單，後來成為
> 參考引擎的 append-only 交付史。它回答「哪一版做到了什麼、當時量到什麼」，
> **不回答下一弧做什麼**。現行施工排序只在 [`WORK_QUEUE.md`](WORK_QUEUE.md)。
>
> 文中的「掛帳／殘留／下一弧」是**當時的發現紀錄**，可能已被後續版本修掉或改變
> 前提；搜尋命中不得直接升為待辦。每次新結案仍追加在本檔，但新發現必須另進
> `WORK_QUEUE` Inbox，經現版重現與依賴判定後才取得排序權。

> 2026-07-05，SYNTAX 全系列定稿 pass 的產物；同日引擎同步（RECONSTRUCTION 15），
> 2026-07-06 #16 收尾——**#1–#16 急切引擎範圍全數完成**。SPEC_14 為權威；
> `nlang-tools` 全套測試綠（89 suites，rustc 1.96.1）。殘留＝memo Stage 4+／快照語法另案（F2 已結案 2026-07-07）。
> 引擎側提交於 nlang-tools `local` 分支，待使用者 merge review。

## 完成狀態（2026-07-05／06）

| # | 項目 | 狀態 |
|---|---|---|
| 1 | meet/cmp 優先序（& 比 cmp 緊，反 C） | ✅ `join{cmp{meet{add}}}` |
| 2 | cmp_op 加 `<=>`（最前）與 `=`（`!=`後） | ✅ 文法＋AST（`Probe`／`LatticeEq`）＋最小求值（見下） |
| 3 | structural 雙角 `<<expr>>` | ✅ 含 `to_nlang` 列印同步 |
| 4 | 結構化前綴（八種合法；`%@a` 拒收） | ✅ |
| 5 | tuple ＋ `list_sep`（`,`/`;`、尾隨可省） | ✅ `ExprKind::Tuple`；求值＝**定長密封**數字鍵 Combo——密封只及 arity，`%effect` = 元素**聯集**（原 max；effect_union 弧 2026-07-23 遷集合半格；效應屏蔽為 Cocoon 專屬，2026-07-06 裁決；SYNTAX_04 §2.5） |
| 6 | L7 infix logic（`a /f b`） | ✅ desugar 為 `Apply(Apply(/f, a), b)` |
| 7 | ternary 分支 `pipe ? pipe : pipe` | ✅ 裸鏈式三元已拒收 |
| 8 | unary_op 僅 `!`（W1-1） | ✅（前次已完成） |
| 9 | multiline `\"""` 跳脫 | ✅ |
| 10 | field_key 移除 interp_str（tag 鍵保留） | ✅ |
| 11 | path 清理（anchor_current／meta_key 移除） | ✅ |
| 12 | order_relation 移出 `{}`／`{{}}` | ✅ 裸序位鏈只住 `#{}`；語料已遷移（見下） |
| 13 | poset_lit `#{}`／order_op／`=` 同序位 | ✅ `ExprKind::Poset`；求值產 ValRelation＋`%rank` |
| 14 | apply 護欄 !add/!mul/!cmp | ✅（權威反向採納，前次） |
| 15 | mul_op !ident 護欄 | ✅（前次） |
| 16 | **`$` 語義（interpreter 層）P1–P5** | ✅ **急切引擎範圍內完成（2026-07-06）**——P1/P2/P4/P5 經稽核為結構上已成立（`context_value` 僅在 pipe／dispatch 設定；`sub_context` 隔離＝管道不透明）；P3 補上：自由 `$` 無綁定觀測 → `_\|_` `%cause: #no_context`（新 `BottomCause::NoContext`，原為靜默 `Top`）。測試 `tests/context_dollar_test.rs`（13 項，含 tuple 效應透明與 `{...t}` 顯式拆封）。**殘留＝惰性半邊**：急切引擎在 evolve 期即坍縮開放項，銜尾蛇向量 `v: <<_.>> \|> <<_.>>`／`v.w.x.a` 待 call-by-observation 引擎（GUIDE_03 工作流；Thunk 機制已存在但主要欄位路徑走急切 `FieldKey::Path` 臂） |
| 16a | **惰性引擎半邊 Stage 1+2**（call-by-observation） | ✅ **完成（2026-07-07）**——Stage 1 機械刀（略）。Stage 2 語義刀（略）。**殘留＝Stage 3 綁定傳播**：... |
| 16b | **惰性引擎半邊 Stage 3**（綁定傳播，C 案活引用晚綁定） | ✅ **完成（2026-07-07）**——交付 `705bfb1` + 驗收修 `db83eb8` + 整治 `272b180`。**F1 ✅**（deref 再入供 `$` 框架：`resolve_path_internal`／`force_recursive` 在 Ref 解引用處 scope `ctx.context_value`，`probe_v_w_x_a_yields_logic` unignore 後綠）。**F2 ✅ 結案（2026-07-07，`97a0bcd`）——但根因與整治回函所稱不同（量測定案）**：OOM 真兇是驗收探針自身的 `contains_horizon` 助手（`all_fields_iter()` 產擁有權克隆，對視界深度嵌套鏈遞迴＝O(depth×size)，峰值 15.6GB）；引擎側（含 pre-Arc）本就正確——視界 ~253 deref／depth 251 觸發、observe 快速返回有界鏈（實測 1.2s／峰值 ~440MB）。`sub_context` 深拷貝之說**未經量測、經 stash 對照實驗證偽**。`Arc<ComboVal>` root 改造仍保留＝真實效能收益（每次 thunk force 免一次全宇宙深拷貝；「測試 mutate root 受阻」實為 path_test 4 行 `Arc::make_mut`）。599 綠。新驗收探針 `probe_v_full_stdlib_root_hits_horizon_no_oom`（stdlib 重根）。**F3 衛生筆記**（Ref×非 Top 具體值 unify 走 force 路徑＝A 案快照；現行語法不觸發，延遲或規格裁決留白）。全 workspace 89 suites 綠（Stage 3 6 acceptance + 3 probe 全過）。**惰性化完成定義（`v.w.x.a → "Logic"`）達成 ✓**。殘留＝memo Stage 4+／快照語法。 |
| 16c | **觀測 memo Stage 4**（force 層 memo，019 tier 策略） | ✅ **完成（2026-07-08，驗收含代修）**——交付（`8a00b4d`＋`2b2e524`）：4a tier 分類器（`Tier`/`RhsForm`/`classify_tier`/`has_free_dollar`）搬家 `nlang-parser::tier`、`oo::nlint` 改 re-export；4b `Ouroboros.force_memo`，key＝(expr CAID, frame CAID, context CAID|#open, root CAID)，C/M memo、Q/U 旁路，Route A 三守衛同款，`force(Ref)` 永不 memo；4c 三探針（fuel 命中遞減／Q 不跨觀測／Bottom 不入）。**驗收（2026-07-08，`8229676`）：工單 4c 開四支探針、交付缺兩支紅線，其一揪出 soundness bug 並代修**——memo key 的 context 分量僅取 thunk 自身槽，漏觀測方動態綁定（F1 deref 框架恰走此分量）：`v.w.x.a`（框架綁定 "Logic"）之後直接 `w.x` 命中同 key，框架結果被端給開放觀測（應 `#no_context`）。修法：**有效綁定**（`thunk.context ∨ ctx.context_value`，§11.2 同式）一次計算、key 與 call_ctx 共用。另代修：root CAID 每 force 深拷貝全宇宙重算 → `EvalContext.root_caid()` 惰性快取；還原被刪的 P1/P3 註解；GUIDE_03 §11.3 實作註記（工單預裁決 5，交付未做）補上。evolve 失效紅線交付即過。`stage4_redline_test.rs` 入永久套件。604 綠。殘留＝Stage 5（C₀ 永久化＋KV、Route B dirty-DAG、Q 單觀測局部快取）。（附註：交付側 spec 提交 `7c2b1db` 為**空提交**，記錄僅存在於 commit message——16c 列由驗收方補建。） |
| 16d | **觀測 memo Stage 5**（Route B 每座標失效） | ✅ **完成（2026-07-08，驗收含代修）**——交付（`13f6464`）：5-pre staged 閘門；5a `dep_collector`（root/staged 讀取記錄＋`force(Ref)`＝`"*"` 萬用依賴＋巢狀傳播）；5b `MemoEntry{value,deps}`＋反向索引＋`invalidate_coords`（evolve 逐座標）＋commit/load/refine 全清；C₀＝空依賴天然永久。**預置紅線 R1/R2/R3（`019c40c`）un-ignore 全綠——探針預置制度首戰生效。****驗收（`fe4522b`）**：儀器化量測揪出一個實測洞——engine 內部語境（`eval_context`：unify 合併）以純淨系統根＋無收集器參與 memo，插入 deps=∅ 偽永久條目（refine 期條目擾動 4→6 實測；閘門後純移除 4→3）。修：`EvalContext.memo_enabled`，`eval_context()` 關閉。另兩項縱深防禦（誠實標注）：HIT 時 entry.deps 上浮外層收集器（架構必需；三次對抗構造皆無法武裝失效——快取值內嵌未 force thunk、其條目獨立失效，固化窗比模型窄）；Named-prefix evolve 雙形式推座標（實測 `/name:` 走 Quoted/Path 臂，本臂為防禦）。p1/p2 探針入永久套件（迴歸守衛；反事實不武裝已註記於檔內）。609 綠。**Route B 核心經 dep-trace 驗證**：transformer thunk 收集 {t}→反向索引→失效→重算新鮮。（附註：交付側 spec 提交 `e6c8e7d` **再次為空提交**——工單明文要求非空自查後仍違反；16d 列由驗收方補建。） |
| 17 | **元素位 spread splice**（`[...xs, y]`／`(...xs, y)`） | ✅ **完成（2026-07-06）**——parser 修根因：`"..."` 字面量不產 pest pair，舊 builder 的 `=="..."` 檢查永不成立、三點被靜默丟棄（`ExprKind::Spread` 在元素位從未被建出；欄位位走 `FieldKey::Quoted("...")` 標記別路故倖免）。求值：splice＝取來源數字鍵公開欄位按序重編；效應釋放（SPEC_03 §3.1）；無殼值（原子≅`{%val: x}`）貢獻零元素；底（runtime／字面量兩種表示）坍縮整容器；tuple 結果保持密封。測試 `spread_splice_test.rs`（9）＋ parser 迴歸 |
| 18 | **管道代數律**（`|>` ＝ 疊加 monad 的 Kleisli bind；docs/discussion/018） | ✅ **完成（2026-07-06）**——範疇論拆解 session 的定律表對引擎驗證，抓到兩處違規並修復：(a) **可加性破口**——態射形態 × 疊加輸入 → `_|_`；轉換器形態 `$` 綁整個疊加非逐支；combo 疊加 × 轉換器 → `_|_`（SPEC_07 §4「疊加態平等演化」明文）。修法：Pipe 頂層對 Union 逐支走完整右值處理（各自綁 `$`）、`apply_morphism` 入口同樣分配、⊥ 支剪枝／全 ⊥ 坍縮／單支解包；(b) **原子形態 passthrough**——`5 |> #ok` 回傳 `#ok` 而非 `_|_`（form 3 應為強制交集）。修法：else 臂改走 unify。測試 `pipe_laws_test.rs`（10 項定律：可加性×4、零、單位×2、合成、原子交集×2） |
| 19 | **Parser fuzz／golden-AST 掃描** | ✅ **完成（2026-07-09 交付、2026-07-10 驗收通過）**——交付（`08c0fd5`＋`2885ed7`，第三方模型）：`golden_ast.rs`（SYNTAX_01–12 §4 全向量＋拒絕類，形狀指紋 `shape()`）；`fuzz_roundtrip.rs`（xorshift 種子固定 800×depth3，AST→to_nlang→re-parse 等值）；`roundtrip.rs` 語料＋印表機冪等；`strip_spans`／優先級感知 `to_nlang_prec`。**修蟲 8 隻**：`Rule::range` 未建 AST（文法收、parser 吐 Unexpected rule）；`@{}` 空 anon_set（SYNTAX_02 §8 prose 早已裁 ≡`_|_`，文法未跟上）；`expr_toplevel=SOI~expr~EOI` 堵尾隨靜默丟棄（`a <=> b <=> c` 舊為靜默截斷）；印表機 TypeAnnotation 左右顛倒＋印 `:` 非 `@`、Float 去小數（`1.0`→`"1"` 再 parse 成 Int）、Apply 負參缺括號、Parent 路徑缺 `.`、Lens 點形式坍 Path。**驗收（重跑＋diff-read＋量測）**：102 套 640 綠 0 敗（3 ignored 皆既存已知議題）；Stage 4/5＋Atom(Top) 紅線原樣；交付方**無空提交、自帶 ROADMAP 記帳兩筆**（三個交付模型中紀錄紀律最佳）。**CAID 注意（驗收補帳）**：Thunk bn_serial 序列化走 `expr.to_nlang(0)`（`bn_serial.rs:78`／`lib.rs:952`）——印表機正規化＝**含 Float／純虛複數／TypeAnn／新括號策略之表達式，其 thunk 舊 CAID 已變（一次性合法差異）**；force-memo `expr_caid` 冷啟（無害，行程內快取）。**衍生案**：Atom(Bottom) 吸收律 ✅ 結案（見下「`Atom(Bottom)` 吸收律修正」；探針 `e7d2fcb`→unignore）。殘留：Range／`@{expr}` 無求值臂 → 萬用臂 ⊥Conflict 靜默（需語義裁決）。Spec 側文法行 `anon_set = "@{" ~ expr? ~ "}"` 同步 SPEC_14 §2.4＋SYNTAX_04 §1。 |

## 同步時發現的權威修正（已寫回 SPEC_14）

1. **apply 護欄不足（SPEC_14 §2.3）**：原 `!add_op !mul_op !cmp_op` 擋不住 `a /f b` 的
   `/f` 被 juxtaposition 吞為運算元（apply L6 比 infix L7 緊）。補 `!logic_infix`。
   代價已註記：以態射為 apply 運算元須括號 `f (/g)`。
2. **裸錨定路徑**：SPEC_14 §2.4 的 `path` 本就允許零段的 `_.`（根宇宙）；引擎原要求至少
   一段導致 `<<_.>>` 不可解析。引擎拆出 `anchored_path`（錨定＋可選段），置於 primary 的
   `atom` 之前——順帶讓 `_.x` 正確解析為 Root 路徑（原為 `Lens(Top, x)`）。權威無需改。
3. **complex_lit 缺右邊界護欄（2026-07-06）**：`"-"? ~ "i"` 分支無守衛，任何 `i` 起首的
   識別碼（`io`／`it`／`input`）在值位被拆成「複數 `i` ＋ apply」→ `_|_`。三分支尾端補
   `!(XID_CONTINUE | "-")`（含 `-` 與 kebab 一致：`i-1` 是識別碼）。SPEC_14／SYNTAX_02
   §4.10 同步。由 tuple 效應測試（鍵名 `io_thing`）意外挖出——語料此前無 `i` 起首值位識別碼。

## 引擎側附帶事項

- **解析深度**：16 層優先權遞歸下降在 debug 測試執行緒（2 MiB）對深巢程式（如
  `test_enum_auto_number.n`）臨界溢位；`parse_program`／`parse_expr_only` 已改在專用
  64 MiB scoped thread 執行（API 不變）。
- **求值層最小語義（部分實作，待 SPEC 完整化）**：
  - `<=>`：數值／字串直接比；tag 依 `%rank` 比（poset 無錨點時隱式封箱：source 種秩 1，
    SYNTAX_10 §4.7）；同 poset 無序資訊 → `#un`。**未實作**非嚴格聯集態（`#lt | #eq`）
    與跨容器 `_|_` 判定（需容器歸屬追蹤）。
  - `=`：暫為非塌縮結構等值（原子比 kind、忽略 rank/effect）；真格論相等（互 `<=`）待做。
  - poset `=` 同序位：`compute_ranks` 以等式傳播已知秩（不進 BFS 邊）。
- **列印修正**（`to_nlang`）：AnonSet 原誤印 `#{…}`（與 poset 撞名）→ 改 `@{…}`；
  Structural 單角 → 雙角。**CAID 注意**：若有舊 canonical 輸出留存，含 `@{}`／`<<>>`
  的程式其 canonical 字串已變。
- **語料遷移**：`tests/unit/test_enum.n`、`tests/unit/test_enum_auto_number.n`、
  `tests/pending/test_enum_auto_number.n` —— `{ #a < #b }` → `#{ #a < #b }`；
  鏈式三元加括號（SYNTAX_12 §4.1）。
- **新測試**：`crates/parser/tests/spec14_sync.rs`（12 項：反 C 優先序、兩家族比較、
  `<<>>`、前綴、tuple 四方、infix、三元、跳脫、鍵規則、poset、釘死邊界、深巢迴歸）。
- **`Atom(Top)` 么元修正**（2026-07-08，`nlang-tools` 引擎側，commit 見下）：字面量 `_`
  原求值為 `Value::Atom(AtomKind::Top,…)`，而 unify 的么元臂只匹配 `Value::Top` 變體 →
  `_ & x`、`t:{flag:_}` 後 refine 皆 `_|_ Conflict`（Top＝meet 么元格律被破）。修法＝
  **求值端正規化**：`eval.rs` 的 `ExprKind::Atom(Top)` 與 `lib.rs` `resolve_path` 的 `_` 臂
  一律回 `Value::Top`；`unify_internal` 另加 `Atom(Top)` 別名臂（縱深防禦，手構形態仍存），
  該臂**重入 `Value::Top`**而非 `other.clone()`，以保 `Atom(Top) & Union` 與 `Value::Top`
  同走 do_unify 的 sort/cap 正規化（忠實別名）。**CAID 注意**：`_` 的表面回印不變（兩拼寫
  都印 `"_"`），但 bn_serial 位元由 Atom 路徑改為 `Value::Top → 0xFF`——**含 `_` 的程式其
  舊 CAID 已變（合法差異）**。工單：`meta/`外部 `docs/atom_top_unify_handover.md`；探針
  `crates/interpreter/tests/atom_top_unify_probe_test.rs`（3 支，驗收後 unignore 全綠）。
  非目標：Top/Bottom 雙拼寫的*全面*正規化仍未做（complement 等路徑仍可產 `Atom(Bottom)`，
  靠 unify 別名臂；見下）。
- **`Atom(Bottom)` 吸收律修正**（2026-07-10，`nlang-tools`，對偶 `Atom(Top)`／04df5c4）：
  字面量 `_|_` 原求值為 `Value::Atom(AtomKind::Bottom,…)`，而 `eval_binary_cmp` 的吸收早退
  只匹配 `Value::Bottom` → `_|_ == _|_`→`#true`、`_ == _|_`→`_`（違 SYNTAX_06 §4.1 黑洞／
  「與無比較皆衝突」）。發現路徑：parser `@{}` 經萬用臂恰回 `Value::Bottom(Conflict)`，
  同一位置的 `_|_` 卻不吸收。修法＝**求值端正規化**（`eval.rs` `AtomKind::Bottom` →
  `BottomCause::Conflict.into()`；`resolve_path` 的 `_|_` 臂同）＋ unify 別名臂重入
  `Value::Bottom(Conflict)`（忠實別名，同 5b501e5 模式）。宣告空底因選 Conflict，與
  `@{}`／萬用臂同物，content_hash 對齊。探針 `bottom_spelling_probe_test.rs`（`e7d2fcb`
  預置 2 活＋4 紅）unignore 6/6 綠；workspace 0 敗。**CAID 注意**：`_|_` 表面回印不變，
  bn_serial 由 Atom 路徑改走 `Value::Bottom`（含 cause 位元）——**含字面 `_|_` 的程式舊
  CAID 已變（合法差異）**。
  **驗收（2026-07-10，含代修 `26b31fb`）**：修法本體照預裁決、探針一字未弱化 ✓。但對抗
  量測抓到**回歸**——正規化讓 `Value::Bottom` 抵達 `LatticeEq` 的吸收早退，而 `=` 是
  **不塌縮不吸收**家族（SYNTAX_06 §4.1）：`_|_ = 3` 基線 `#false`（worktree 對照量測）→
  修後 ⊥；`_|_ = _|_` `#true` → ⊥（基線的正確靠的正是同一隻 Atom 漏洞——修好吸收側就
  拆了誤打誤撞的另一側）。代修＝`LatticeEq` 臂 ⊥ 作運算元（空集）：(⊥,⊥)→`#true`、
  (⊥,x)→`#false`，stash 反事實武裝確認。順帶立案：`<=` 極值端（`_|_ <= x` 恆 `#true` 等，
  SYNTAX_06 §4.2）**基線與修後皆違反**＝從未實作（`<=` 與 `==` 共用 `eval_binary_cmp`
  的 ⊥/⊤ 政策，兩家族需拆），非本輪回歸——3 紅線探針預置（`26b31fb`，見 ROADMAP §3）。
  終態：workspace **103 套 648 綠 0 敗 6 ignored**（3 既存＋3 新紅線）；活護欄 8 支
  （含 `=` 家族 2 支新無回歸線）。**協議教訓入檔：修法移動兩家族邊界時，探針須同時釘
  住邊界兩側**——本案預置探針只釘了吸收側，非吸收側的無回歸線是驗收期才補的。
- **Range／`@{e}` 求值**（2026-07-10，工單 `docs/range_eval_handover.md`；裁決 nlang-spec
  `c3c7cdd`）：`a..b`＝閉閉區間集合（非迴圈）；`Value::Range`＋eval 臂（界 force 於觀測期，
  變數界免費）；`@{e}` 透明 eval；`@{}` 仍 ≡⊥。unify：原子∈區間（含閉端／步進）＋無步進
  交集（空⊥、單點→原子）；步進∩步進→⊥（CRT 另案）。parser 缺界預設 `#_|_`/`#_`（TagStart/
  TagEnd，修正 Top 撞規格）。bn_serial `TAG_RANGE = 0x18`（合法新增，先前全 ⊥ 無 CAID）。
  探針 `range_eval_probe_test` 7＋`range_bounds_probe` 3 unignore 全綠。workspace **666/0/3**。
  防火牆：`~%List./range` 半開、吸收／cmp 套件不動。
  **驗收（2026-07-10，含代修 `b3f9316`）**：探針斷言等同、golden 改動恰為授權三條、
  memo_soundness/reflection 各 +1 為窮舉 match 機械臂（非弱化）、核心真值表與 BigInt
  步進（含負差）手驗正確。**對抗量測抓到一洞並代修**：`range_unify` 的 `(Range, _) →
  Conflict` catch-all（L168）搶在 Union 分配（L213）之前——`(1|7) & 1..3` 實測 Conflict，
  應為 `1`（SPEC_07 §4 疊加態平等演化）；`5b501e5` 同族（早臂搶走下游正規化的運算元）。
  代修＝catch-all 改讓位（decline → None）：Union 分配、Thunk 強制、Combo 錯配交回既有
  機制；修後 `(1|7)&1..3`→`1`、`(1|2)&1..3` 保疊加、`1..10 & {a:1}` 仍誠實 Conflict。
  stash 反事實武裝確認；分配護欄入永久套件。終態 **667/0/3**。**臂序教訓（第二次同款）**：
  unify 加早臂時，必查 Union/Thunk/Ref 等「由下游機制服務」的運算元類是否被搶——
  catch-all 預設應為 decline 而非 Conflict。角落註記：`..10..2`（錨點起點＋步進）交付
  採稠密射線語義（無網格原點則步進不設限），未在裁決內，暫收（重開條件＝真實使用）。
- **集合家族 cmp 極值端（SYNTAX_06 §4.2）**（2026-07-10，工單 `docs/cmp_extremes_handover.md`）：
  `<`/`<=`/`>`/`>=` 與 `==`/`!=` 共用 `eval_binary_cmp` 的 ⊥/⊤ 吸收早退 → 極值端從未
  實作（`_|_ <= 5`→⊥、`5 <= _`→`_` 等）。修法＝按 `CmpOp` 分流：Eq/Ne 吸收一字不動；
  集合家族先 force 兩側、collapse 後走極值表（Lte 真值表；Gte≡Lte 鏡像；Lt＝嚴格子集；
  Gt 鏡像），有限值路徑不變。回傳一律 `#true`/`#false`，永不吸收。`Atom(Top/Bottom)`
  殘形若抵達此處視同極值（complement 等路徑；不擴修）。探針 `cmp_extremes_probe_test.rs`
  （`09ec048` 預置 5 紅＋3 活）unignore 8/8 綠。workspace **656 過 0 敗 3 ignored**
  （工單目標吻合）。**非目標防火牆**：`3 <= 5` 仍 `#true`（§4.10 子集語義另案）。
  **驗收（2026-07-10，重跑＋diff-read＋量測）：通過，零代修**——症狀表 10/10、防火牆
  全守、對抗加測含**計算得 ⊥**（`(1 & 2) <= 5`→`#true`——極值判定在 collapse 後，
  非僅字面量）與 `_ < 5`/`5 > _`→`#false` 一致性。探針斷言逐條比對等同（頭註被壓縮，
  斷言未動）。**驗收附註（交付未記）**：家族拆分後 `==`/`!=` 兩側必求值——不再於
  LHS=⊥ 時短路 RHS（結果值不變，fuel 成本變；n/ 無短路語義承諾，屬合法差異）。
  五案模式註記：紅線釘目標側＋活護欄釘不動側＋預裁決含鏡像禁抄——首次零代修交付。

**#16 實作時發現的規格角落（2026-07-06，已釘入 SYNTAX_12 §4）**：
`tuple |> {結構轉換器}` 正確坍縮 `_|_ #missing_key`——tuple 是密封數值 Cocoon，結構演化
的合併語義不得對其新增欄位；`$.0`／`$.1` 位置輸入因此**配態射演化**（`(1,2) |> (p -> $.0 + $.1)`）。
兩條規則各自成立，交點行為此前無家。

**文件側遺留**：~~QUICK_REFERENCE 重生成~~ ✅（2026-07-07 依 SPEC_14 定稿版全表重生成：
運算子表 16 層全同步（`<=>`/`=`、負號移除、雙角 `<<>>`、tuple/poset 字面量、護欄註記、
cmp 不可鏈式、`@` 結合性修正）；前綴八式；`%rank`/`%max_lifting_depth` 補入元欄位；
`#no_context`/`#out_of_horizon`/`#order_conflict` 補入因果標籤；導航表補 SYNTAX_00–12
與 APP_07；範例更新（safe_div 改分派表式、新增 poset/tuple 範例））。

## Range 語義補完(2026-07-11)

比較節遷移驗證曝光四缺口;E1–E3 已結案(工單 `docs/range_gaps_handover.md`),
E4 另單。

- **✅ E1 型別標記 × Range**:`validate_value` 對 Range 驗非錨點界(錨點 TagStart/
  TagEnd 放行);界不改寫(PassWithProjection 仍回原 Range)。`@int & 6..`→`6..#_`。
  **驗收代修 `2991096`**:交付版 unify 早臂為 marker×ANY,搶佔 Union 分配——
  `(10|20) & @int` 基線 `10 | 20` → 交付後 ⊥(worktree 反事實 da6c05c 證實;
  **5b501e5 臂序蟲族第四例**,工單明文預裁 DECLINE 仍被違反)。修:早臂只擁有
  marker×Range,其餘 DECLINE 落回既有下游臂;永久護欄
  `guard_union_x_type_marker_distributes` 追加。
- **✅ E2 分派鍵含 Range**:(1) `apply_single_rule` 認 `%val` 常值(態射則再 apply);
  (2) `resolve_pattern` 對含 `..` 鍵 `parse_expr_only`→Range;(3) `filter_minimal`
  比 **pattern** 精化(`p_i & p_j == p_i`⇒j 非極小);(4) `apply_morphism` 對
  pattern 表(`%morphism` 且有非數字非 meta 鍵、無 `%builtin`/`%rules`)走
  `dispatch_morphism`——排除 curry 數字鍵(防 `math.add` 部分套用被盜)。
- **✅ E3 Range 正交補(meet 語境)**:`try_meet_not_range` 辨 AST `!(e)` 且 e→Range
  →成員否定(Union 分配);standalone `!(range)` 仍 ⊥(無閉形式,fmt v2 凍結)。
- **✅ E4 `@Name` nominal 引用(2026-07-11 結案,零代修——第二例)**:交付
  `9db9090`+驗收 `52353d1`。解析順序改:內建保留集(from_name≠Unknown)→標記
  (不可遮蔽,活釘);其餘 `@Name` 走正常查找鏈(lazy/record_dep;prefix-alternates
  之故,裸名定義亦可被 `@Name` 引用——既有跨前綴機制);查無→Unknown 標記直通。
  deref 即值:密封 `{{}}` 經 deref 保 SPEC_03 窮盡 schema;`@float` 投影穿透模板;
  遞迴型別頂層 force+欄位 thunk 可終止。**README 門面範例端到端首次通過**
  (README 容器已修 `{{}}`→`{}`,spec `3e7773f`)。觀測面 CAID 位移(標記→定義值,
  合法);bn_serial 未動。校準附帶收穫:`10&(@X|@Y)` 舊為 `10|10` 直通不去重,
  今經分配收斂為 `10`(通用 Union 去重仍另案)。**遺留**:use-before-def 靜默直通
  (演化時序語義+Unknown 直通疊加;「引用永不定義之 @Name」lint → 想法 D Tier 1)。

**驗收(2026-07-11,驗收方;交付方 5355ef7 曾自我宣告結案——結案權在驗收方,
本節為修正版)**:通過,一件代修(`2991096`,上述臂序回歸+revert 非目標區
假前提編輯:`strip_plain_quotes` 系列——註解宣稱 to_string_plain 加了引號但
該函數從未被改,開發殘留)。探針 26/26(25+1 驗收護欄)、workspace
**693 過 0 敗 3 ignored**、`dispatch_test` 原樣綠、CLI 對抗掃全對。
已知角落(不修):`try_meet_not_range` 對 `!(非Range) & x` 雙重求值 inner
(fuel 重複計費;spec 無 fuel/次序承諾,合法差異)。探針軸修正一處
(`assert_union_plain` plain→to_nlang)= 開單方校準 bug,交付方忠實修復。
E4 記錄補回:README 門面範例 `~payload & @Adult` 因此不 enforce;裸名模板
`T: {…}` 則正確坍縮——nominal 解析未接線,件級大,獨立工單。

**引擎 v0.2.0-beta.2 定版(2026-07-11)**:nlang-tools top `1bbe4b6`,tag
`v0.2.0-beta.2`(squash dev;tie-back 照拓撲)。內容 = E1–E4 弧線全量
(708/0/3、108 套);REAL_05 L1-05 合規向量自此可執行、SPEC_03/06/07 分派
範例與 README 門面範例全部落地。積極 commit 方針:引擎側今後每完成一個
語義弧線即 squash 定版(user 裁示 2026-07-11)。

## 合規矩陣曝光之引擎缺口(2026-07-11;已結——見下方 L2-17 結案條)

- **L2-17 發散偵測缺席**:`a: a + 1` 觀測 `a` 現得 **`_`**(自指查無 → 開放項
  → Top)——應 ⊥ `#divergent`(REAL_05 §2 L2 義務「循環偵測」)。`_` 屬
  **宣稱萬有的靜默錯**類(同 5b501e5 家族的嚴重度,不同機制)。修法方向:
  thunk force 週期偵測(觀測中 thunk 重入 = 自指)。
- **⊥ 印出 `%cause` 標籤**(nit):現以人話註解印因果(如 free-$ P3 註解),
  conformance runner 的 cause 比對因此暫為 SHOULD。統一印 `%cause: #tag`
  後可升 MUST(L3 前必須)。
- 兩件可併一張小工單;探針即 conformance 語料(L2-17 已在庫,#divergent
  斷言待引擎)。

- **✅ L2-17 發散偵測 + ⊥ %cause 列印(2026-07-12 結案,零代修——第三例)**:
  交付 `3db91f1`,驗收全套重跑 **718/0/3**、探針 10/10、conformance **45/45**
  ——**裸核門檻(REAL_05 Level 2)首次全綠**。機制三層:`in_flight`
  (thunk content-hash 重入)+ `force_coord`/`computing`(公開座標重入;
  `~` 私有與固態值不設閘,HOF 免誤殺)+ evolve 期欄位座標標記;open-miss
  Top(非字面 `_`)具體化為 Thunk,互指環才活得到 force 期偵測。⊥ 顯示
  `_|_ (%cause: #<tag>)`(to_nlang + to_string_plain 對齊 `#tag`);
  bn_serial 未動(Bottom hash 走 cause 判別字,查證屬實)。`#divergent`
  可入 force memo(工單預授權)。
  **行為變更(有意,配套)**:`unify_combo` 對 Top&⊥ 存單欄 ⊥ 綁定——
  欄內衝突(`a: 1 & ""`)從 evolve 期報錯改為演化成功、觀測該座標得
  `_|_ (%cause: #conflict)`;雙邊真衝突(staged 與 incoming 皆非 Top)
  仍中止演化。座標級 ⊥ ∈ 格,裁為誠實化;conformance 雙通道判定兩式皆容。
  **宣稱修正(記錄,非代修)**:交付訊息稱「forward refs survive」——
  bare 前向引用(`out: a` 先於 `a: 5`)交付前後皆 `_`,無迴歸亦無改善;
  具體化只服務環偵測。前向引用解析(演化序不敏感)另案。
  驗收加測五向量全綠:發散 memo 兩次觀測穩定、發散不污染鄰座標、
  同 content-hash thunk 順序使用不誤觸、線性鏈、菱形共享依賴。
  活釘邊界全數保持:factorial 120、未定義名 `_`、`#fuel_exhausted` 不改判、
  free-$ `#no_context`、環×Union `_ | 1`(Top 分支維持開放)。

**引擎 v0.2.0 定版(2026-07-12)——首個裸核版**:nlang-tools top `bde3025`,
tag `v0.2.0`(squash dev;tie-back 照拓撲)。內容 = L2-17 弧線(發散偵測
三層 + ⊥ %cause 顯示 + Top&⊥ 單欄綁定)。**定版驗證於 tag 所在 commit
實測**:718/0/3(109 套)+ conformance 45/45 + `oo --version` = 0.2.0。
VERSIONING §3 之「無 pre-release 標 = 通過 REAL_05 矩陣」自此有第一個實例;
規格 v0.2.0 ↔ 引擎 v0.2.0 對位完成。(定版過程一則環境註記:WSL2 對
/mnt/d 的 target/ 寫入曾連續 I/O error 5,`cargo clean -p` 後復原——
非程式碼問題,重驗全綠後才上 tag。)

- **✅ bare 前向引用解析(2026-07-12 結案,零代修——第四例)**:交付
  `f9dd657`,驗收 736/0/3、conformance **47/47**(L1-26/27 前向引用
  = SPEC_03 交換律可執行化)。兩層修:(1) 引擎——L2-17 的 path 環守衛
  不再把 thunk **指向**的路徑標進 `computing`(淨刪除;保留檢查的語義
  轉為「引用正在 force 中的祖先座標」=真環,自環由 in_flight
  content-hash 收口)——bare-path 引用鏈(`out: mid`/`mid: base`/`base: 1`)
  誤殺 #divergent 根除;(2) CLI——`run_one_shot` 改為全檔全欄 evolve 完
  → 統一 store-put(CAID 目的保留)→ observe,逐欄過早固化根除,跨檔
  前向引用同修。對抗矩陣:欄位重排等價、鏈入環/鏈旁環/三跳環/裸自指
  判定全對。REPL 與 `oo evolve` 逐步語義明文不動。真環 ⊥ 側活釘
  (`a: b`/`b: a`)全程未鬆。

**引擎 v0.2.1 定版(2026-07-12)**:nlang-tools top `d654fdb`,tag `v0.2.1`
(前向引用弧線;736/0/3 + conformance 47/47 於 tag 所在 commit 實測)。

## 開單中(2026-07-12):Union 冪等去重 + R4 use-without-def lint

雙子單(nlang-tools `docs/union_dedupe_lint_handover.md`,探針 10 紅+15 活):
A. SPEC_01 join 冪等律落地——結構等值去重、保首次出現序、不動既有排序、
   bn_serial 不動(觀測面位移合法);L1-28 已入語料,收案 = **48/48**。
B. R4 lint(oo/nlint 零引擎變更):檔內永不定義之名(裸名/`& @Name`)Warn;
   前向引用已合法化不得誤報;保守寧漏勿誤,8 支活釘即法律。
開單校準附帶收穫:**float 顯示怪癖**——`1.0` 之 to_nlang 印 `1`
(`1 | 1.0` 印 `1 | 1`);遺留隊列,另案。

- **✅ Union 冪等去重 + R4 lint(2026-07-12 結案,一件代修)**:交付
  `0b0a788` + 驗收代修(nlang-tools dev:多參態射誤報修 + 護欄)。
  A:`value::normalize_union`(平坦化=結合律 + 結構等值首現保留 + 單倖存
  坍縮)接上七個建構出口;unify 分配改先去重後 cap;排序未動;
  `PartialEq` 含效果標記,同值異效果不併;oml De Morgan 單欄包裝人工物
  一併修正(列帳)。conformance **48/48**(L1-28)。
  B:R4 use-without-def Warn(nlint 零引擎變更)。**代修**:多參態射
  `x y -> …`(Apply 形參數位)第二參數誤報——`collect_param_names` 增
  Apply 臂;開單方共責(活釘只釘單參)。全語料掃:conformance 48 檔
  零 R4;examples/tests 僅真陽性(`/add`、`/set_y`——舊 fixture 類,
  R4 反哺為語料清理清單工具)。驗收終態 **762/0/3**(761+護欄)。

**引擎 v0.2.2 定版(2026-07-12)**:nlang-tools top `c063db1`,tag `v0.2.2`
(Union 冪等 + R4 lint 弧線;762/0/3 + conformance 48/48 於 tag 所在
commit 實測)。單日三定版(v0.2.0 裸核 → v0.2.1 → v0.2.2),每弧線
一版的節奏成立。

## 語料清理曝光之引擎缺口(2026-07-12;已量測,待裁決/派單)

.n 語料清理(11 件舊期望歸零,unit 65/0、integration 7/0;R4 掃描歸零)
過程中曝光三個新缺口 + 一個既有隊列項的量測補充:

- **G1 combo 等值破損(兩家族)**:綁定後完全相同的 combo,`x == y` 與
  `x = y` **皆 `#false`**(`x: {a:1}` / `y: {a:1}`;重排亦同;原子/列表
  正常)。而 `normalize_union` 對相同 combo 正確去重(`{a:1}|{a:1}` →
  單支)——洩漏在 **cmp 求值路徑**,非 `ComboVal::PartialEq` 本身。
  疑向:cmp 之 collapse 拿到的 combo 內欄仍為帶 span 之 Thunk / 或身分軸
  欄位滲入。**需裁決 + 派單**(SYNTAX_06 對 combo 等值的預期行為順帶釘死)。
- **G2 `/` 前綴柯里定義全滅** → **已重新診斷並解體(2026-07-12,見下
  「G2 重診斷」節)**。原帳範圍錯誤:`/` 從來不是變因;真因 = G2-M
  多參糖未去糖 + G2-S root 內建 `/add` 撞名毒宇宙 兩蟲疊影。不撞名
  `/` 定義(`/myadd`、`/assert_eq` 顯式柯里)全形態正常。原「內層態射
  被吞為鍵 `y`」證據為誤讀——那是柯里吃掉一參後的**正確**剩餘態射。
- **G4 union 去重 × 導航**(去重案後續件,不翻案):meet 後全支存活並
  去重為單 combo 時,display(force_recursive,已掛 normalize)見單支,
  **路徑導航拿到去重前 Union** → `#invalid_path`。單支存活(衝突殺支)
  之導航正常。修向:導航/force 路徑補 normalize 掛點。
- **G3 補量測**(既有隊列:runaway cause 精化):`(/recursive 1).%type`
  → `#conflict`(期 `#divergent` 或 `#fuel_exhausted`)。

語料側全部以繞道處理並逐檔標注(欄位斷言繞 G1、裸名定義繞 G2、
衝突殺支繞 G4);test_canonical 移 pending 等 G1/G3。

## G2 重診斷 + 工單開出(2026-07-12)

開單前偵察推翻原 G2 帳載。逐項量測後 G2 解體為三個獨立缺陷:

- **G2-M 多參糖未去糖**:`x y -> body`(SYNTAX_11 §表格明釘「柯里化
  多參數(空白分隔,自動柯里化)」= 合法)解析為 `Morphism{param:
  Apply(x,y)}`,eval 打包規則鍵退化 → 分派永不命中。**裸名與 `/` 同壞**
  (`aeq 5 5` → `_`;`5 |> aeq 5` 默默回傳 `5`)。裁定:AST 建構期摺疊
  為巢狀 Morphism(僅葉子全裸單段路徑之 Apply 鏈)。
- **G2-S root 內建影蓋毒宇宙**:root 頂層規則軸**恰有一個**內建座標
  `/add`(math.add 閉繭)。使用者 `/add:` 定義 evolve 靜默成功,毒發於
  observe 入口 `unify(root, staged)`(閉繭缺 `%rules` → MissingKey ⊥)
  → **全宇宙觀測皆 ⊥ #conflict、無路徑、exit 0**(對照:資料軸衝突
  於 evolve 即死、帶名、exit 1)。裁定:root 座標單調演化,unify = ⊥
  即於 evolve 邊界帶名報錯。
- **G2-C 原子×態射繭之 `%val` 吸收**:do_unify Atom×Combo 臂無條件塞
  `%val`,`/add: 7` 令閉繭長新鍵無衝突。裁定:combo 為態射
  (`is_morphism`)時 → ⊥ #conflict;非態射 combo 吸收行為保留(已釘)。
- **G5(新缺口,本單範圍外)**:tuple 參數 `((x, y) -> …)` 解析正確
  (`Morphism(Tuple[…])`)但引擎分派側解構**未實作**——全應用形態 `_`
  (juxta / pipe / inline 皆試)。SYNTAX_11 規則 4 明釘其合法。另擇期派單。

語料當時全滅真相:斷言庫用多參糖(G2-M)+ 範例慣用 `add` 這唯一撞名字
(G2-S),兩蟲疊影誤判為「`/` 全滅」。教訓:**最小重現須做變因隔離
(裸名對照組 + 換名對照組),單一例證不得概括成類**。

工單:tools `docs/g2_shadow_multiparam_handover.md`;預先提交探針
11 紅門(interpreter 10 + CLI 1,今日全紅實測)+ 12 釘(今日全綠)。
conformance 增 **L1-29**(多參柯里,開單時紅 = 工單門)、**L1-30**
(`/` 定義應用,即綠入法):現況 49/50。

**G2 三件結案(2026-07-12,零代修第四例)**:模型 #3 交付 `05e62ca`,
驗收 `60cdf44`。G2-M = parser `fold_multiparam`(僅摺裸單段 Path 之
Apply 鏈,tuple/多段葉不摺,AST 反例實測);G2-S = `universe.evolve`
寫入座標對 **root** 值 unify=⊥ 即 Err(大聲 Evolution Conflict,
staged×staged 舊路徑不動);G2-C = do_unify Atom×Combo 加 morphism
guard(非態射 `%val` 吸收保留,已釘)。量測:探針 23/23、workspace
**785/0/3**、語料 72/0、conformance **50/50**。對抗邊界(混合鏈柯里、
行內部分應用、參數遮蔽、`~%Math` 影蓋不變、R4 掃描零旗)全淨。
觀察在案:`~x y ->` 亦摺(pk 抽取本剝前綴,行為等價);G2-C guard
整顆 clone 判定(低效非錯,perf 波再收)。遺留:G5 tuple 解構、
G1、G4、`~%` 系統軸影蓋靜默(本次量測確認交付前後一致,另議)。

**引擎 v0.2.3 定版(2026-07-12)**:top `8d97c4f`(squash G2 弧 + 語料
清理),tag 於實測 commit(workspace 785/0/3、語料 72/0、conformance
50/50 皆於 tag 目標重測)。tie-back `1d9e184`。

## G5 工單開出(2026-07-12):tuple 參數位置解構

現況量測:`((x, y) -> …)` 解析正確(`Morphism(Tuple[…])`),eval 打包
pk 抽取對 Tuple 落 `_` fallback,`apply_single_rule` 只綁 `it`/`0`/鍵名
→ `x`/`y` 從未入 scope → 全應用形態回 Top。柯里×tuple 嚴格對偶
(SYNTAX_09 §2)今日已健康(`(x y -> x) (3,5)` 整包綁 x,雙面已釘)。
裁定:R-P 打包(全裸單段 Path 之 Tuple 參數 → 規則附 `%params` 元資料;
巢狀/混形不動)+ R-B 綁定(tuple 形 combo、arity 精確,敗 → ⊥
#conflict;`it`/`$` 整包綁定保留)。工單 tools
`docs/tuple_destructure_handover.md`;探針 8 紅門 + 7 釘(已校準)。
conformance 增 **L1-31**(開單時紅 = 工單門):現況 50/51。

**G5 結案(2026-07-12,零代修第五例)**:模型 #3 交付 `8de3144`,驗收
`27d84fe`。eval 打包 Tuple 臂(規則鍵 `"(x, y)"` + `%params` 閉繭)+
apply_single_rule 解構(force 後驗 data 軸恰 `0..k-1`、精確 arity,敗
→ ⊥)。量測:探針 15/15、workspace **800/0/3**、語料 72/0、conformance
**51/51**。對抗邊界:巢狀 tuple 守門未偷跑、**Union 引數分配先於分派
→ 逐支解構**(`((1,2)|(3,4)) |> tf` → `3 | 7`)、Unit 拒絕、重複參名
後者勝(=柯里遮蔽對偶)、`it` 參名顯式勝。觀察在案:tuple 形判定僅
驗 data 軸(帶他軸而 data 吻合亦過,罕見形,不改);參名 `it` 遮蔽
整包(規格未著墨,留跡)。

**引擎 v0.2.4 定版(2026-07-12)**:top `09ef211`(squash G5 弧),tag
於實測 commit(800/0/3、72/0、51/51 皆於 tag 目標重測)。tie-back
`d897002`。

## G4 重診斷 + 工單開出(2026-07-12):Union 路徑導航

原帳「去重 × 導航」**範圍錯誤**(臂序蟲族之外的第三次帳載修正——變因
隔離教訓再驗)。反事實:同向量於 v0.2.2 行為與今日全同,去重是紅鯡魚
(衝突殺支縮成單倖存才「能導航」)。真相:**任何真多支 Union 的路徑
導航皆 ⊥ #invalid_path**——`navigate_segments`(lib.rs:1380)只有
Combo 臂,Union 落 catch-all。從未實作。
裁定(SPEC_07 平等演化、觀測投影逐支泛函):逐支導航(單值基準已釘:
開放缺欄 → `_`、原子 → ⊥)→ ⊥ 支剔除;全 ⊥ → ⊥ #invalid_path(今日
catch-all 恰同判,已降釘看守);倖存過 normalize_union;**Top 缺欄支
保留**(誠實疊加 `_ | 2`,鏡照單 combo 開放世界)。
工單 tools `docs/union_nav_handover.md`(`5c28a08`);探針 6 紅門 + 7 釘
(校準時發現 all-⊥ 案今日即綠 → 降釘,紅門淨 6)。conformance 增
**L1-32**(`({a:1}|{a:2}).a` → `1 | 2`;開單時紅 = 門):現況 51/52。

**G4 結案(2026-07-12,零代修第六例)**:模型 #3 交付 `fef564c`(宿主機
中途崩潰,恢復後補 commit;驗收方於同內容全套實測),驗收 `c8bc908`。
navigate_segments 加 Union 臂:單段逐支投影(尾段外層續走)、⊥ 支剔除、
全 ⊥ → #invalid_path、normalize_union、Top 缺欄支保留。量測:探針
13/13、workspace **813/0/3**、語料 72/0、conformance **52/52**。對抗
邊界:支內 Union 攤平(`1 | 2 | 3`)、導航結果續管道(`2 | 3`)、混深
多段逐段匯總(atom 支於第二段正確剔除)。federation 語料之 G4 繞道
(衝突殺支)可於下次語料波改回全支存活斷言。

## G1 裁定草案(2026-07-12,待批)

病灶釘死:cmp 拿**未固化** combo,Thunk 等值比 AST(含 span、符號拼寫)
→ 行內字面量 `{a:1} == {a:1}` 都 #false;混血塌縮 `(3 & {note}) == 3`
亦 #false。草案 tools `docs/g1_combo_equality_ruling_draft.md`:
R1 `=` = 固化後外延結構等值(六軸+closed+relations,巢狀同關係,與
去重同一等值 = 引擎唯一等值,效果參與);R2 `==` 塌縮後仍非原子 → ⊥
#conflict(不得默默 #false),混血塌縮後照原子家族;R3 固化防火牆
(span/拼寫不得影響語義)。待批決策點:Q1 `==` 誤用 ⊥ vs 併 `=`;
Q2 效果參與與否。批准後 L1-33~36 入庫 + 開單。
鄰區另案:`<`/`<=` on combo(§4.10)、cmp × Union 分配。

## v0.2.5 定版 + G1 裁定批准入法 + 工單開出(2026-07-13)

**引擎 v0.2.5 定版**:top `d4cc816`(squash G4 弧),tag 於實測 commit
(workspace 813/0/3、語料 72/0、conformance 52/52 皆於 tag commit 重測)。
dev tie-back `d21f1b2`。

**G1 裁定批准(使用者,2026-07-13)**:Q1 = `==` 遇不可塌縮 combo →
**⊥ #conflict**(大聲失敗);Q2 = 效果標籤**參與** `=`(與去重同一
等值關係,全引擎唯一等值);Q3 巢狀遞迴同關係(無爭議)。入法:
SYNTAX_06 §4 #11(`=` 固化後外延結構等值)/#12(`==` 家族誤用 ⊥;
混血塌縮後照原子家族)/#13(固化防火牆:span/拼寫盲)+ §2 規則 3、
§4 #5 #6 交叉引用。conformance 增 **L1-33~36**(字面量 `=`/綁定名
span 盲測/`==` 誤用 ⊥/混血塌縮 `==`),校準:**開單時四紅**(今日皆
#false),矩陣 52→**56**。工單 tools `docs/g1_combo_equality_handover.md`
(探針 `combo_equality_probe_test.rs`,紅門+釘照例預先提交校準)。
病灶地圖:cmp 求值路徑固化缺失(eval 側),非 PartialEq;
`normalize_union` 的結構等值已正確 → 修法方向 = cmp 借同一關係。

**探針校準記錄(2026-07-13)**:紅門 11 全紅、釘 14 全綠。兩件校準
發現:(a) `h != 4` 今日恰好 #true(combo≠atom 誤打誤撞)→ 按規降釘
(修後須經裁定路徑同判);(b) **新缺口 G6**:混血節點**觀測**今日印
全 combo(`{ %val: 3, note: "n" }`,run/observe 兩路皆然),SYNTAX_06
§4 #6 明文「觀測 `x` → `1`(讀 `%val`)」——規格-引擎歧異,另案
不併 G1(變因隔離);探針以 `pin_hybrid_observe_current_full_print`
凍結今日顯示,防 G1 交付順手改,G6 裁定後解凍。

**G1 結案(2026-07-13,零代修第七例)**:模型 #3 交付 `f5e71fc`,驗收
`c37bca1`。`=` 兩側 force_recursive 後走全引擎 PartialEq(原子特判臂
移除 → effect 參與);`==`/`!=` 局部剝 `%val`、無 `%val` → ⊥ #conflict
(吸收檢查在剝殼前);span 盲落關係層(Code/Thunk without_spans,
cmp 與 dedupe 同一關係)。語料 4 斷言 `==`→`=` 合法改拼(list 非塌縮)。
量測:探針 25/25、workspace **838/0/3**、語料 72/0、conformance
**56/56**。對抗:`!=` 誤用不依值皆 ⊥、混血雙側剝殼、家族對偶
(`= 3` #false vs `== 3` #true)、v0.2.5 反事實無未申報移動。

**引擎 v0.2.6 定版(2026-07-13)**:top `309ce3f`(squash G1 弧),tag
於實測 commit(838/0/3、72/0、56/56 皆重測)。dev tie-back `da6af2c`。

**G6 歧異面全量測(2026-07-13,v0.2.6)**:病灶單根——值語境塌縮只認
**純包裝**(`is_pure_wrapper`:僅 `%val`+`%`-meta 欄),混血(帶非-%
資料欄)不塌。三個症狀面 vs 兩個健康面:
| 路徑 | 規格(§4 #6 及其蘊涵) | v0.2.6 實測 | 判 |
|---|---|---|---|
| 觀測整體 `x` | `1`(讀 %val) | 印全 combo | **歧** |
| `x + 1` 算術 | 2(值語境讀 %val) | ⊥ #conflict | **歧**(鄰接) |
| `x \|> inc` 管道 | 2 | ⊥ #conflict | **歧**(鄰接) |
| `x.name` 導航 | "Alice" | "Alice" | 合 |
| `x == 1` | #true | #true(G1 剝殼) | 合 |
| 純包裝 `1 & {%note:"m"}` | 塌 | `1` | 合 |
裁定面待定:「讀 %val」只管觀測顯示,還是一切值語境統一律(觀測+算術
+apply)?若統一(推薦),修法 = G1 `atomic_family_operand` 的一般化
(值語境塌縮 helper),落三點:觀測投影、math 運算元、apply 強迫。
CAID 無虞(bn_serial 非 to_nlang)。

**G6 裁定批准 + 工單開出(2026-07-13)**:使用者裁**統一值語境律**,
並點出對偶:今日觀測 x 的全 combo 輸出正是 `<<x>>` 該給的。入法:
SYNTAX_06 §4 #6 值語境統一律(觀測遞迴/math/應用衍生/原子比較讀
`%val`;導航/`=`/結構態/普通 combo 不塌)+ SYNTAX_07 §4 #6 混血兩態。
補量測:`<<x>>` 今日已回全節點(結構態半邊本來就對)、`x |> (p ->
p.name)` 今日綠(引數全節點傳遞須保住——防綁定點剝殼越權)、
`<<literal>>`/結構別名今日全節點(三支結構釘)。conformance 增
**L1-37~39**(觀測/算術/管道;開單時三紅),矩陣 56→**59**。工單
tools `docs/g6_hybrid_collapse_handover.md`(8 紅門+10 釘已校準;
G1 檔臨時顯示釘同 commit 退役,案移 G6 檔)。修法地圖:eval_math
:796 collapse 只解純包裝 → helper 一般化;顯示塌縮放觀測投影層、
勿進 to_nlang(結構態同用);Ref 中介 = 結構視角。

**G6 結案(2026-07-13,一件代修;七連零代修止)**:模型 #3 交付
`ce7a2cc`,驗收代修 + 紀錄(tools dev)。實作:`value_context_operand`
一般化(math+原子 cmp 同 helper)、管道/應用零改動衍生通過、觀測投影層
`project_value_context`(遞迴,不進 to_nlang)、結構態 = Ref 不強迫 +
`<<非路徑>>` 之 `%structural`/`%node` 標記(刻意非純包裝 shape 防 merge
剝除)。**代修**:標記擋導航——`lit.name` 回歸 `_`(v0.2.6 反事實
`"Bob"`)→ navigate_segments 解包標記 + 代修釘。量測:探針 19/19、
workspace **856/0/3**、語料 72/0、conformance **59/59**。超單記帳:
math 看穿結構視圖(`<<lit>> + 1` → 2,合統一律);G2 釘改寫意圖保全
接受(探針修改權在驗收方,補規)。**相容性**:舊宇宙存檔之結構字面量
無標記 → 新引擎坍縮顯示(語義重讀;fmt 位元格式未變,合法差異)。
遺留另案:`<<x>>` 元欄材料化、原子 pattern × 混血 dispatch、
混血聯集支序(v0.2.6 已然 `2 | …`,非 G6 移動)。

**引擎 v0.2.7 定版 + 版號綁定(2026-07-13)**:top `acaa6cf`(squash G6
弧 + 版號綁定),tag 於實測 commit(856/0/3、72/0、59/59 皆重測;期間
宿主磁碟滿,清 target/debug 後重測,非代碼因素)。dev tie-back `e35da39`。
**`oo --version` 自此綁 git tag**(crates/oo/build.rs:`git describe
--tags --always --dirty=+`,submodule-aware gitdir 解析,HEAD/refs/tags/
packed-refs 變更觸發重建;無 git 時退 CARGO_PKG_VERSION;oo Cargo.toml
同步 bump 為切版步驟)。tag commit 上實測 `oo v0.2.7`;非 tag 建置誠實
顯示 `v0.2.N-<ahead>-g<hash>[+]`。切版協議新增末步:tag 後重建並驗
`oo --version` == tag。(舊帳:v0.2.2 起 Cargo.toml 版號漂移至此修正。)

## G3 重診斷 + 裁定草案(2026-07-13,待批)

帳載範圍修正(第五次):G3 非「runaway cause 精化」——**視界抹除**。
量測鏈:runaway/裸名/同引數皆 ⊥ #conflict、座標自指 #divergent 正確、
⊥ 引數過 apply 原因保全、**平場 4000 項加法也 #conflict**(轉換通用,
與 runaway 無關)、4000 元素 list 正常(燃料死點在 math 鏈)。根因:
預設策略 Blur → 耗盡產一等視界值 `Value::Blur`(SPEC_08 #blur 快照,
顯示/CAID 皆已實作)→ **值語境消費點無 Blur 臂**:eval_math catch-all
鑄 ⊥ #conflict(視界→衝突,身分抹除);原子 cmp 漏到結構比默默 #false
(G1 同謊言類)。草案 tools `docs/g3_blur_erasure_ruling_draft.md`:
R1 值語境 Blur 吸收律(原樣傳出,不得改寫本體地位)/R2 cause 誠實
(runaway = #fuel_exhausted;#divergent 保留偵測案)/R3 meta 觀測回
BlurCause。待批:Q1 吸收 vs 降轉 ⊥(推薦吸收);Q2 test_canonical 期望
= #fuel_exhausted(推薦)vs 舊註 #divergent。鄰區另案:同引數偵測升級、
預設燃料量級、`=`×Blur、timeout 禁 blur(已法)。

**G3 裁定批准 + 工單開出(2026-07-13)**:使用者按推薦裁(Q1 吸收傳播、
Q2 #fuel_exhausted);執行者工程補充採納(引數載體/消費者拆清——
綁定/force 邊界只量測一筆不預設大改;helper 不擴權,Blur 短路在呼叫前
與 Bottom 短路並列)。入法 SPEC_08 §3.2.2(值語境吸收/引數載體/cause
誠實/meta 回 BlurCause)+ REAL_04 表註。conformance 增 **L2-21/22**
(runaway %type、平場 %cause;開單時兩紅),矩陣 59→**61**。工單
tools `docs/g3_blur_erasure_handover.md`(9 紅門+6 釘已校準;釘含
L2-17 #divergent、⊥ 短路保全、`=`×Blur 現況凍結;Strict 路徑交付
自測義務)。工單自本張起明文:**全部探針檔皆紅線**(G6 教訓補規)。
test_canonical 出 pending 併入本單(G1+G3 雙阻塞已除;== 改 = 、
期望改 #fuel_exhausted)。

**G3 結案(2026-07-13,零代修第八例;協議違規註記第二次)**:交付
`2811437`,驗收紀錄 tools 工單檔。吸收臂:math/原子 cmp/一元/`<=>`/
Apply 兩側/apply_morphism 入口(⊥ 先 Blur 後、helper 前);R4 meta 回
BlurCause;深度門改報 FuelExhausted(R3 法理;舊 StackOverflow→
Divergent Strict 映射成死臂,清理另案);oo CLI 主執行緒 64MiB。
量測:探針 15/15、workspace **871/0/3**、語料 **74/0**(test_canonical
出 pending)、conformance **61/61**。Strict 驗收方獨立穿鏈自測綠。
對抗:值語境全吸收;`big.name` 導航 × Blur → ⊥ #invalid_path(座標
語境,法未涵蓋,**另案候選**)。協議:divergence 釘遭單方遷移
(內容追認、程序違規第二次;下次直接計代修)。遺留另案:nav×Blur、
`=` 家族×Blur、Union×Blur、同引數偵測、死臂清理、預設燃料量級。

## 視界參數劃家裁定(2026-07-13,已批)

使用者裁:**規範家 = `~%Config`**(名字不換),欄位裸名、單次觀測
全域生效、引擎必實作;**節點級 `%fuel` 等降級為參考性提示非硬性**
(使用者修正:`%` meta 本有引擎彈性,第三方實作 per-node 不違規;
採納者把實際生效參數入 blur CAID → 單引擎決定論不受影響,跨引擎
一致性僅在 ~%Config 面保證)。入法:SPEC_08 §3.1 增訂(規範家+降級
條款+轉發代數未立法聲明)、SPEC_09 §6 字典注記、SYNTAX_08 特徵表
例外注記+範例改標。背景:引擎 ~%Config 已存在(註解誤稱出處
SPEC_09 §6——該節原是 % 欄位字典,未立過 ~%Config)、無任何
per-node 讀取;`~%Engine.state.strategy`+`/set_strategy` 與
`~%Config.%strategy` 雙家並存。**引擎收斂單待開**(G3 後):欄位
`%fuel`→`fuel` 裸名化、策略併一家、節點視界提示 lint(想法 D 儀器)、
conformance 向量(觀測 ~%Config.fuel = 10000)。

**config 收斂單開出(2026-07-13)**:工單 tools
`docs/config_home_handover.md`。施工面:欄位裸名化(含 `%max_depth`→
`max_unification_depth` 對齊字典)、補 `max_lifting_depth` 佈線、策略
三家併一(`~%Config.strategy` 初始 + `/set_strategy` 活 ctx 覆蓋保留 +
`~%Engine.state.strategy` 死展示欄移除)、R5 節點視界提示 lint(想法 D
儀器第二件)。探針 7+3 紅門、3+3 釘已校準;L2-23 紅(今日 `_`,
`%` 欄名被 meta 軸吞)。工單頭明文:釘因新法必紅 → 停下報驗收方,
單方遷移計代修。

**config 收斂弧結案(2026-07-14,零代修第九例)**:交付 dev
`7763bb3`、驗收 `daa0ba7`。七欄裸名(genesis+eval_context 同步;
`%max_depth`→`max_unification_depth` 對齊字典)、`max_lifting_depth`
佈線(32,EvalContext 欄位首次可配置)、策略三家併一
(`~%Config.strategy` 初始 + `/set_strategy` 活 ctx 覆蓋保留註解補明 +
`~%Engine.state.strategy` 死展示欄移除,語料/測試零引用)、R5 節點
視界提示 lint(七名、三鍵形 Named+Meta/Path/Quoted 皆掃、寧漏勿誤
——%kind/%fmap 等真特徵零誤報;想法 D 儀器第二件)。SEED_CONFIG
CAID 隨欄名更新(系統軸運行時注入,無存檔宇宙依賴)。驗收獨立重測:
探針 10/10+6/6、workspace 887/0/3、語料 74/0、conformance **62/62**
(L2-23 關門);對抗邊界:`~%Config.%fuel` → `_`(乾淨斷開)、
`~%Engine.state.strategy` → `_`、R5 對抗形全正。genesis_test 期望
遷移已申報且非探針檔——合規,無協議違規。

**引擎 v0.2.9 定版(2026-07-14)**:top `ceb08db`(squash config 收斂弧 +
oo 0.2.9 bump),tag 於實測 commit(887/0/3、語料 74/0、62/62 皆重測;
tag 後重建 `oo --version` = `oo v0.2.9` ✓)。dev tie-back `4a696aa`。

## Blur 邊界裁定(2026-07-14,已批)

G3 只立值語境;座標語境與集合家族當時明文排除,本次量測收口。
量測歧異面(v0.2.9):導航 `big.name` → ⊥ #invalid_path(僭稱知道
路徑無效)、`bigA = bigB` 同文異綁定 → **#false**(兩快照 CAID 異,
但真值皆 4000——「確定不等」被量測證偽)、聯集導航 blur 支被靜默
剔除(`({a:1}|big).a` → `1`,視界痕跡消失)、`%caid` 不可導航。
健康面:`&` 吸收、`|` 一等分支、`c.x` 儲存透明、`big = big` → #true
(force memo 同快照)、%cause/%type R4。

裁定:SPEC_08 §3.2.2 增 **#5 座標語境吸收**(非 meta 段導航原樣傳出;
聯集 blur 支存活,僅 ⊥ 支剔除)、**#6 `=` 二段律**(同 CAID → #true
=觀測決定論,必入法否則與聯集去重裂成兩關係、G1 唯一等值破功;
其餘吸收左優先,不得 #false)、**#4 擴 `%caid`**(快照身分全可判
比較 `x.%caid == y.%caid`,使用者提案;`===` 否決=一概念一拼法;
細化款不另立——%caid 路線已覆蓋需求)。`==` 雙 blur 只傳左側 cause
=既有 G3 法不動(兩側 cause 各自可由運算元 meta 觀測,打包=鑄新值
違 R1)。`<`/`<=`×blur **不入法**:量測示連 `1 <= (1|2)` 都 ⊥
#conflict——序判定於 combo/union 全域未實作(§4.10 佇列),blur
非變因(G2 變因隔離教訓);釘現況。

向量 L2-24~27(L2-25 開單時即綠=法釘;三紅=工單門);矩陣 62→**66**。
協議註記:G3 釘 `pin_lattice_eq_blur_current_behavior`(凍結 #false,
明文另案解凍)之遷移**由驗收方執行**於開單 commit,非模型 #3。

**Blur 邊界弧結案(2026-07-14,一件代修)**:交付 dev `646269d`、
驗收+代修 `ceaef12`。navigate_segments 非 meta Blur 吸收+%caid 臂;
LatticeEq 二段律(⊥ 段原封、同 CAID #true、餘左優先吸收);聯集
導航零改(blur 支投影自然存活)。**驗收代修**:交付吸收臂跳出段
迴圈——內聯 `big.name.%cause` 回整 #blur、綁定拆步回 #fuel_exhausted,
導航合成性(x.a.b ≡ (x.a).b)破;代修改續迴圈+釘(紅門只測綁定形
=驗收方設計盲點,記取:**雙拼法語境須兩形皆釘**)。終態:探針
21/21、workspace 907/0/3、語料 74/0、conformance **66/66**。對抗
邊界:`⊥ = blur` 兩向 #false(⊥ 空集運算元讀法,預裁;重開候選)、
%caid 無過度擴權、雙 blur 聯集不誤去重。**既有債曝光**:⊥ 非 meta
導航同樣跳出段迴圈(內聯/綁定兩形歧異+回覆形制不一)——另案
nav×⊥ 合成性。

## ⊥ meta 觀測整流 + `#invalid_path` 廢止(2026-07-14,已批)

nav×⊥ 合成性弧量測後擴為四面(全引擎追法,法源俱在):
**F1** ⊥ 臂跳出段迴圈(conflict/invalid_path/divergent 三因同形,
與 Blur 代修同蟲異臂);**F2** `%cause` 引擎回診斷 combo
(%expected/%found/%involved/%message/%type,**無 %val**)且
`<<路徑>>` 同形——違 REAL_04 §1(Cocoon 含 %val,直接觀測坍縮
標籤)+SYNTAX_08 §4 #3;修法=補 %val,G6 投影自動歸位;
**F3** `b: 123` 之 `b.%cause` → ⊥ #invalid_path,違 SYNTAX_08 §4 #2
(應 `_`;combo 缺欄早回 `_`,只有原子走 catch-all 中毒);
**F4** `#invalid_path` 身世查清:未立法(REAL_04/TAG_REGISTRY 皆無,
G4 裁定文誤沿用引擎拼法)→**廢止**。四鑄點分流:導航 catch-all
(原子/Top)→ `_`(原子資料軸可 `&` 混血擴欄=開放,用戶原始設計
「% meta 欄與一般欄同律預設開放」);未坍縮 %cause → `_`(同一刀);
`^` 溢出 → `#out_of_horizon`(TAG_REGISTRY §1 正典早備,含修復建議);
聯集全 ⊥ 支 → REAL_04 §4 主因果(G4 條款修訂:`({a:1}|7).a` 由 `1`
改 **`1 | _`** 誠實疊加;G4 三釘/門由驗收方遷移)。CAID parse
(lib.rs:1543)留待 cause 正典審計。BottomCause **變體只增不刪**
(fmt v2 凍結;InvalidPath 留存量讀取、停鑄;OutOfHorizon 附尾新增)。

**同日曝光記帳(不併案)**:私有軸未實施(`p.~s` → `1`,SPEC_04 §61
應 ⊥ #private_access_violation);G4 惰性 ⊥ 支未剔(`{a:(1&2)}|{a:(3&4)}`
導航回雙 ⊥ 聯集——剔除只認即時 Bottom,thunk 漏);`^` 錨定解析
於觀測語境未接(scopes 僅態射派發時填,有效 `^.a` 也 ⊥;改標後
即為誠實 #out_of_horizon,解析補全另案);cause 正典審計(BottomCause
13 變體 vs REAL_04 全表)。

向量 L2-28~31(四紅=門);矩陣 66→**70**。

**⊥ meta 整流弧結案(2026-07-14,一件代修)**:交付 dev `81dd138`、
驗收+代修 `085fe9a`。F1–F4 本體全對(⊥/Blur 雙臂續迴圈、cocoon 補
%val+防剝殼墊欄、catch-all 開放、OutOfHorizon 附尾、主因果防禦臂
=量測不可達仍留)。**驗收代修**:交付為滿足相遇序紅門移除 unify
無條件 tropical 排序 → `(1|2) = (2|1)` #false,SPEC_01 交換律在 `=`
判定層破(%id/CAID 無恙);**共責**——驗收方 `1 | _` 門與 G4 `_ | 2`
釘在任何全序排序下聯合不可滿足(教訓:**跨弧釘門要做可滿足性
聯檢**)。代修=Union PartialEq 改多重集分支等值(集合觀),顯示
保留相遇序(canonical 顯示序記帳待議)。帳實不符註記:交付表格
排序鍵說法與實際 diff 不符(內容無害,紀錄紀律一筆)。疣:cocoon
`_: _` 墊欄結構態可見(REAL_04 調和案清理)。終態:探針 26/26、
workspace 930/0/3、語料 74/0、conformance **70/70**。

**引擎 v0.2.10 定版(2026-07-14)**:top `0d97df1`(squash Blur 邊界
+⊥ meta 整流+聯集多重集等值 + oo 0.2.10 bump),tag 於實測 commit
(930/0/3、74/0、70/70 皆重測;tag 後重建 `oo --version` =
`oo v0.2.10` ✓)。dev tie-back `c10a6b3`。

## 私有軸實施裁定(2026-07-15,已批)

量測(v0.2.10):私有軸**全面反轉**——外阻全通(`p.~s`/兄弟偷看/
`_.~x` 皆洩漏)、內通全斷(**規格自身 factory 範例**回 `_`:裸名
`~key` 於 combo 內不經作用域鏈解析;唯根層活著,因根欄位直接在
scope)、態射捕獲 ⊥ #conflict(`_`+3)、`~.` 錨 parse error(文法
不存在)、外部顯示全裸(`~s: 1` 直接躺在顯示)。

裁定:**Q1 幾何內外判準**(§3.1 #5 入法)——裸名=作用域鏈=內部
人;點段 `.~key` =外部定位=⊥ #private_access_violation(含
`_.~key`;內部人恆有裸名,規則無例外)。**Q2 觀測投影剝除**(§3.1
#4 入法,本弧唯一新法)——顯示(坍縮+結構態)剝 local 軸;CAID/
`=` 六軸照舊(eq/%id 釘今日即綠證實 local 已參與內容身分)。
**Q3 值捕獲**——body 裸 `~key` 經定義閉包 scope 解析。**Q4 `~.` 錨
廢止**(§2.2)——用戶考證設計史:最初 `~`≈$HOME、`.`≈路徑分隔、
`^`≈`..`,故 `~.a ≡ ~a` 純冗餘且誘發 `~.~a` 之問;一概念一拼法,
拿掉;文法不含=引擎天然合規,補 parse-error 釘防未經裁定復活。

**陷阱(工單釘)**:`~%Name` 系統軸鍵同樣以 `~` 開頭——剝除與
點段封鎖**必須豁免 `~%` 前綴**(L2-23 `~%Config.fuel` 向量在門口
守著);語料 test_entropy 根層 `~c`/`...~c` spread =裸名路線,須
不受影響。

向量 L2-32~35(四紅=門);矩陣 70→**74**。bottom_meta 釘
`pin_private_axis_current_behavior`(凍結 `p.~s` → 1,明文另案)
之遷移**由驗收方**於開單 commit 執行。

**私有軸弧結案(2026-07-15,零代修第十例)**:交付 dev `dc1a807`、
驗收 `9cf5a52`。外阻=Combo 臂攔 `~` 段(`~%` 豁免);內通=
`seal_defining_scope`(定義 combo 作 scope frame 注入 Thunk 閉包;
local 空跳過防公有 Thunk 等值污染);捕獲=frame+pipe RHS Thunk
固化(Ref 不強迫=Stage 3 晚綁定);剝除=strip_local_axis 移動式
遞迴接 G6 投影雙路。對抗全正:遮蔽 11/雙 frame 13/系統軸完好/
閉包 frame 已剝、私值不現身(`~s` 僅以識別字現於 %code AST debug
顯示=原始碼非 local 軸)。終態:探針 19/19、workspace **948/0/3**、
語料 74/0、conformance **74/74**。**既有債曝光記帳**:spread 滲出
(外部 `{...p, peek: ~s}` 取得秘密副本——spread×私有未立法,外洩
原語另案)、`--observe` 根私有=內部人讀法(記錄)、%code 裸印
Rust Debug AST(顯示疣另案)。

## spread 私有保全開單(2026-07-15;引擎追法,法=SPEC_03 §3.1 既有)

量測:spread 無條件搬運六軸——外部 `q: { ...p, peek: ~s }` 取得
local 軸副本,q 封 frame 後 peek 讀到秘密(=外洩原語;v0.2.10 時
副本已搬但讀不到,私有軸弧的 seal 使其可讀)。SPEC_03 §3.1 私有
保全條款明文:外部展開排除 `~` 欄。內外判準=SPEC_04 §3.1 #5 幾何
路線(目標 combo 現於當前 scope 鏈=內部)。`&` 合併不動(六軸
unify 為值層法;字面量另行 seal,`(p & {peek2: ~s}).peek2` 今日
即 `_`,釘現況)。向量 L2-36/37 紅=門、L2-38 綠=法釘;矩陣 77。

**同場曝光記帳(不併單)**:(1) **展開碰撞未依法交集合併**——
`{a:1, ...{a:2}}` → `{a:2}` 覆寫,SPEC_03 §3.1 明文應交集 `a: 1&2`
(資訊單調性);另案。(2) **態射體內根名解析**——
`give: (x -> {...p})` 外呼 g.a → `_`(v0.2.10 為 ⊥ #conflict,
非本弧回歸,兩版皆壞形不同);另案。

**spread 私有保全弧結案(2026-07-15,零代修第十一例)**:交付 dev
`6a06716`、驗收 `f2cee89`。`spread_target_is_insider`(嚴格 PartialEq
+退階 local 值等+五軸鍵集——安全論證:偽內部人須已持有秘密,無
資訊增益)+ `...` 臂外部跳過 local 軸,最小刀。對抗全正:偽造兩形
各拿回自己的值、雙重展開徹底斷鏈、等值兩向乾淨。終態:探針 11/11、
workspace **959/0/3**、語料 74/0、conformance **77/77**。

**引擎 v0.2.12 定版(2026-07-15)**:top `b6da107`(squash spread
私有保全弧 + oo 0.2.12 bump),tag 於實測 commit(959/0/3、語料
74/0、77/77 皆重測;tag 後重建 `oo --version` = `oo v0.2.12` ✓)。
dev tie-back `628696e`。

## 展開碰撞交集合併開單(2026-07-16;裁定已批:Q1 因果傳播/Q2 重複鍵同律/Q3 前向引用另案/Q4 循環攔直接形)

量測(v0.2.12,九病五健):**C1 碰撞=全面後者覆寫**——欄後展開
`{a:1,...{a:2}}`→2、展開後欄→1、§3.1.1 自例 status→#error、
range 覆寫(法定 5..10)、union 覆寫(法定 2)、meta 鍵同、路徑鍵
`{a:{x:1}, a.y:2}`→a={y:2}(x 丟失);**C2 原子展開**回空(法定
`{%val: v}`);**C3 ⊥ 展開**被靜默吞(法定整目標塌 ⊥);**C4 循環
展開**自身形靜默吞、祖先形失控巨型展開至燃料(法定 ⊥ #divergent)。
健康面:List 展開、Top no-op、cocoon 解封+目標開放保全、同值碰撞、
`{...{a:@int}, a:5}`→5(巧合綠:覆寫恰等交集)。根因單一:spread
臂與欄建構全走 IndexMap extend/insert 覆寫;非 Combo 展開源被
`if let Combo` 靜默略過。

裁定四款:**Q1** ⊥ 展開因果傳播(SPEC_03 §3.1 修訂舊文「標記
#conflict」——⊥-meta 整流後鑄新因=視界抹除;帳載修正);**Q2**
純字面量重複鍵同律交集(SPEC_03 §1.1 新增「重複鍵合併」=平行定義
退化形;重複字面鍵 lint 提示另議=想法 D 儀器候選);**Q3** 前向
引用×spread(`{...later}` 後定義→欄缺失;spread 建構期 eager)
**另案記帳**,本單凍結現況;**Q4** 循環檢測義務=直接名引用形
(建構中名棧),別名繞道交燃料視界兜底(記錄現況)。

向量 L2-39~42 四紅=工單門;矩陣 **81**。陷阱釘校準:enum `#{}`
關係種子×顯式欄沿現行、Blur 展開源勿動(量測記錄現況即可)。
工單 `docs/spread_collision_handover.md`(tools dev)。

**展開碰撞弧結案(2026-07-16,零代修第十二例;協議違規一筆=
交付紀錄缺席,驗收方代記)**:交付 dev `af2e989`、驗收 `b9e0249`。
`merge_field_into`(碰撞鍵 unify 交集、非碰撞鍵保惰性)全寫入點
接入;原子殼 `{%val: v, _: _}` 墊欄防剝(同 ⊥ cocoon 手法);⊥
展開 cause 原樣傳播;C4 復用既有 `ctx.computing` 零新狀態。對抗
全正:list 碰撞同律 ⊥、雙原子展開衝突/冪等淨、**別名繞道
`al: a`+`{...al}` → ⊥ #divergent 超單改善**(v0.2.12 靜默吞)。
終態:探針 25/25、workspace **984/0/3**、conformance **81/81**、
語料非 pending 78/0(pending 5 敗既有,tag 反事實同形;口徑漂移
註記:帳面舊值 74=同套件早期計數,invariant=0 敗)。**既有債
記帳**:祖先加欄變體/深層循環未攔=燃料兜底族;insider 自展開
整體顯示=無限結構;**Blur 展開源靜默 no-op**(視界痕跡被抹,
與 Q1 精神張力,另案候選);G6 on_shell 分支五面反事實中性。
違規成因補註(用戶證言):任務完成當口觸發上下文壓縮——環境
切斷非怠惰,違規照記、情節從輕。

**引擎 v0.2.13 定版(2026-07-16)**:top `158bdb0`(squash 展開
碰撞弧 + oo 0.2.13 bump),tag 於實測 commit(984/0/3、語料非
pending 78/0、81/81 皆重測;tag 後重建 `oo --version` =
`oo v0.2.13` ✓)。dev tie-back `f87a408`。

## 詞法作用域開單(2026-07-16;引擎追法,法=SPEC_04 §2.1 既有,零新裁定)

量測(v0.2.13,六病六健):**公有 combo 詞法鏈全斷**——兄弟欄
裸名 `c:{k:5, d:k+1}` → c.d=`_`、鏈式兄弟 `_`、態射體讀 holder
兄弟欄 `_`(含 spread 形)、巢狀 holder `_`、非根祖先提升
`w:{k:5, c:{d:k+1}}` → `_`;**遮蔽=錯值謊言**:`k:5; c:{k:7,
d:k+1}` → **6**(內層 k=7 被跳過、外層 k=5 頂替;法定 8),態射
形同病。健康面:根層提升(root 欄在 ctx.scopes)、引數遮蔽、帶
`~` 欄 combo 整鏈活(seal 觸發)、規格 factory 範例、柯里捕獲。
**根因**:私有軸弧 `seal_defining_scope` 之「local 空跳過」防污染
門(防公有 combo Thunk 等值/unify 毒化)——把公有 combo 的 frame
注入整個跳過,詞法鏈斷;加一個 `~` 欄即復活=變因煙槍。

**帳載修正(第七次)**:前帳「態射體內根名解析」(`give: (x ->
{...p})` 外呼 → `_`,兩版皆壞)於 v0.2.12 tag 與 v0.2.13 皆**不再
重現**(內聯/綁定/帶私有欄三形皆 2)——當時量測環境誤差;真病灶
=本弧之 holder 兄弟可見性。

向量 L2-43~46 四紅=工單門;矩陣 **85**。反污染絆線釘校準:雙生
字面量 `=` #true、`%id` 穩定;E2(`x = {k:5, d:6}` 今日 #false)
=量測記錄義務非釘(修後若翻 #true 屬法向改善,翻他處=停)。
工單 `docs/lexical_scope_handover.md`(tools dev)。

**詞法作用域弧結案(2026-07-16,一件代修)**:交付 dev `9c9b3e0`
(seal 拆門+兩段 snap/frame 自密封+force 殘餘 Thunk 剝離≤32;
紀錄紀律恢復=先寫單後報+「嘗試後放棄」帳)、驗收+代修
`470295c`。**代修=跨層 %id 分裂回歸**:同拼寫 `a1` vs `b1.q2` →
`%id ==` #false(v0.2.13 反事實 #true)——frame 使 Thunk 閉包
跨層分歧,content_hash 對惰性管線取證=內容謊言;修=`%id` 臂
hash `force_recursive` 固化內容(觀測出口同機構),代修釘兩向
(跨層 #true+local 軸參與 #false)。共責:絆線釘只釘同層——
**教訓:身分釘須跨層形**。E2 翻 #true 照記(法向)。語料耗時
0.68→1.18s(交付方 release 量測,無數量級劣化)。終態:探針
21/21、workspace **1005/0/3**、conformance **85/85**、語料零敗。
**既有債記帳(反事實同 `_`)**:≥3 跳兄弟鏈(兩段手法=深度 2
上限,§2.1 全遞迴未達;後續設計=解析時 frame 上推+in_flight
循環守衛)、cocoon 兄弟(closed 先 force 後 seal)、自指兄弟。

## 詞法鏈補完開單(2026-07-16;引擎追法,零新裁定;上弧殘欠)

量測(HEAD,八病四健):≥3/4 跳兄弟鏈 `_`(顯示直觀:d/e 已解、
g2/h2 `_`=深度牆)、態射引用 2 跳兄弟 `_`、私有 combo 3 跳同斷
(兩段手法對所有 combo 同一上限)、cocoon 兄弟 `_`(closed 建構
先 force 後 seal)、cocoon 態射 `_`、巢內 cocoon `_`、**cocoon
遮蔽=錯值謊言第二例**(6 非 8,外層頂替)。健康:鏈×提升
`w:{k:5, c:{d:k+1, e:d+2}}` → 8(即綠釘)、cocoon 純 force、
cocoon 雙生等值、2 跳鏈(上弧門)。

**同場曝光另案(不併單)**:cocoon 本徵態預設未實施——
`{{a:1}}.b` → `_`,SPEC_03 §1.3 明文 Cocoon.k=⊥(closed 世界);
凍結釘明文另案。互指兄弟 `{a2:b2, b2:a2}` → `_`、自指 `{d:d+1}`
→ `_` 凍結(裁定候選:⊥ #divergent vs 開放,涉 cycle_test 釘
=前向引用弧法理,勿順手動)。

設計方向(裁量在實作方):解析時 frame 上推(裸名中於 frame 欄
且值為 Thunk → 以該 frame 在鏈上重force)+循環守衛**必須保
cycle_test Top**(上弧棄案即因翻此釘;守衛語義=再入視為未解、
續鏈外溯,非鑄 #divergent)。cocoon=先 seal 後 force+frame 置
鏈頂(遮蔽序)。向量 L2-47~49 三紅=門;矩陣 **88**。工單
`docs/lexical_completion_handover.md`(tools dev)。

**詞法鏈補完弧結案(2026-07-16,零代修第十三例)**:交付 dev
`2c9abcd`、驗收 `54d3bb8`。`lexical_forcing` 軟再入=棄案的手術版
(ambient 僅詞法 force 期間保留、真循環照舊 #divergent、凍結釘
全守)+cocoon 先 seal 後 force_recursive(固化邊界保留)+單段
seal 回歸(語料耗時 1.18→0.74s 淨改善)。對抗全正:**動態作用域
洩漏兩形皆淨**(param/caller-holder 皆 `_`)、cocoon 3 跳 12、
6 跳 6、遮蔽×鏈 15、param 遮蔽 10、cocoon 雙生 %id。終態:探針
17/17+上弧 21 無回歸、workspace **1022/0/3**、conformance
**88/88**、語料零敗。上弧殘欠清償,§2.1 全遞迴到位。佇列:cocoon
本徵態預設 ⊥/互指自指裁定候選/Blur 展開源 no-op/~%影蓋/cause
審計。

**引擎 v0.2.14 定版(2026-07-16)**:top `0e83268`(squash 展開
碰撞+詞法雙弧 + oo 0.2.14 bump),tag 於實測 commit(1022/0/3、
語料非 pending 78/0、88/88 皆重測;tag 後重建 `oo --version` =
`oo v0.2.14` ✓)。dev tie-back `72cd4f5`。

## cocoon 本徵態預設開單(2026-07-16;引擎追法,法=SPEC_03 §1.2/§1.3 既有,零新裁定)

量測(v0.2.14,三病六健):**存取面全開**——`{{a:1}}.b`、
`{{}}.x`、cause-cocoon `.zz`(REAL_04 §1 cocoon 同法)皆 `_`
(法定 ⊥ #missing_key,§1.2 #1「讀取未定義欄位立即返回 ⊥」);
**Top 欄合併誤拒**——`cc & {a:1, b:_}` → ⊥ #missing_key,法
#2 明文「非 Top 欄位」才拒(Top=無約束);**聯集導航未剔**——
`({{a:1}} | {b:2}).b` → `_ | 2`(修後 ⊥ 支剔 → `2`)。健康:
合併拒絕自例(§1.2.1 #missing_key 拼法)、同鍵衝突 #conflict、
meta 讀開放(%kind/%cause `_`)、已定義鍵、詞法提升、**裸名
miss 邊界**(§2.1 開放世界:座標存取 `.k` 走本徵態 ⊥,詞法
解析 miss 續外溯回 `_`——兩機構不同軸,勿混)。

邊界:%-meta 與 ~% 系統段豁免(他軸,F 系列開放律);開放
combo/原子開放律(F4)不動;spread 解封不動。向量 L2-50~52
三紅=門;矩陣 **91**。工單 `docs/cocoon_eigenstate_handover.md`
(tools dev)。

**釘衝突停報+驗收方補遷(2026-07-16)**:實作就位後觸發上弧
凍結釘 `pin_cocoon_closed_miss_frozen`(明文「另案」=本單),
模型 #3 **依紅線停下報驗收方、未單方遷移——協議正確執行首例**。
驗收方補遷(`095a5e2`,後繼門 `red_cocoon_access_bottom`);
共責註記:凍結釘應於**開單 commit** 遷移(私有軸弧前例),
開單時漏遷=驗收方疏失。

**cocoon 本徵態弧結案(2026-07-16,零代修第十四例)**:交付 dev
`817e1c7`、驗收 `acfe43d`。存取臂 closed miss 分流(%-豁免、私有
攔截序保留)+合併面雙向 force+collapse 判 Top(Thunk(Top) 看穿)
+聯集面零改動自動綠(G4 機構如預測)。對抗全正:私有攔截優先、
⊥ 合成性留因、聯集雙 ⊥ 主因果、cocoon×cocoon 照拒、未定義名=
Top 放行、本徵態節點級不遺傳(繭內開放 combo 保持開放)。記錄:
`cc.~%foo` → ⊥(節點級含系統段,根 ~%Config 不受影響)。終態:
探針 17/17+上弧 16/16、workspace **1038/0/3**、conformance
**91/91**、語料零敗。

**引擎 v0.2.15 定版(2026-07-16)**:top `d396147`(squash cocoon
本徵態弧 + oo 0.2.15 bump),tag 於實測 commit(1038/0/3、語料非
pending 78/0、91/91 皆重測;tag 後重建 `oo --version` =
`oo v0.2.15` ✓)。dev tie-back `e150e3e`。

## 互指/自指裁定開單(2026-07-16;裁定已批:Q1 SPEC_12 兩級線/Q2 非純引用即變換/Q3 root-combo 同律/Q4 帶因 Top=用戶提案)

量測(v0.2.15):循環語義**按層分裂雙向反律**——root 層
computing/in_flight 把一切再入鑄 ⊥(靜止互指 `a:b,b:a`、靜止自指
`x:x` 皆 ⊥,法定 Top=解集全集);combo 層 lexical_forcing 軟再入
把一切再入回 `_`(變換自指 `{d:d+1}`、變換互指皆 `_`,法定 ⊥
#divergent=解集空)。「再入」不是發散,「再入+變換」才是——
兩套機構各缺變換判別。釘面矛盾實體:cycle_test(combo 靜止→Top)
合法;`pin_ref_cycle_still_divergent`(root 靜止→⊥,前向引用弧
承重釘)、`l217_self_identity_divergent`(`x:x`→⊥)、
`l217_path_cycle_divergent`(`s:{v:s.v}` 純路徑環→⊥)三釘違新法
=**由驗收方於開單 commit 遷移**(cocoon 弧教訓)。math 變體釘
(`a:b+1` 等變換形)合法留任。L2-17 正典向量=`a:a+1` 變換形,
canon 自洽不動。

三款入法(SPEC_12 §1.1 #2/#3+帶因 Top、SYNTAX_08 §4 #2 例外、
TAG_REGISTRY #static_cycle)見 CHANGELOG。帶因 Top 守欄:格律中立
/不傳播/顯示 `_`;fmt=觀測期值,如須序列化新 tag 追加(Blur
前例)、BottomCause 凍結不動。向量 L2-53~55 三紅=門、L2-56 綠=
法釘;矩陣 **95**。工單 `docs/static_cycle_handover.md`(tools dev)。

**釘衝突停報第二例+驗收方補遷(2026-07-16)**:實作觸發上上弧
凍結釘 `pin_self_ref_sibling_frozen`(`{d: d+1}` 凍 `_`,明文
「另案=本裁定」)——開單時遷了三顆卻漏了這顆=**同型疏失第二
次**(驗收方記過);模型 #3 再次正確停報。補遷 commit 後繼門
`red_combo_transform_self_divergent`;`pin_mutual_sibling_frozen`
(靜止形)仍綠不動。教訓:**開單前 grep 全探針樹找「另案」標記
對照本單範圍**,不憑記憶。

**互指/自指弧結案(2026-07-16,一件代修)**:交付 dev `be5d9e0`
(`Value::TopCaused{members}` 全 match 位點補臂、bn_serial=裸 Top
同位元組零新 tag、`prefer_caused_top` CAID 早退保因、消費走 force
自然蒸發、鏈染色+四再入點分流)、驗收+代修 `35408c4`。**代修=
環成員名單未含全環**:互指環 `%members` 只錄 `["a"]`,環形狀被
誤讀為自指,違裁定「環形狀從成員名單直讀」;修=`cycle_reentry`
四鑄造點聯集再入座標,修後互指/環長 3/combo/自指四形全正,代修
釘三形。共責:紅門只釘 %cause 標籤未釘成員形——**教訓:裁定文
說「從 X 直讀 Y」時,X 的形要釘**。對抗全正:裸/帶因成對一致
(顯式 `_`、`|5`、`!`)、跨界純環、管道變換環、cause cocoon×本徵
態弧正確合成。基線算式糾正=交付方對(1050 修前),驗收方 +17
誤計帳實不符一筆。終態:探針 17/17、workspace **1051/0/3**、
conformance **95/95**、語料零敗。

**引擎 v0.2.16 定版(2026-07-16)**:top `9ec661d`(squash 互指/
自指弧 + oo 0.2.16 bump),tag 於實測 commit(1051/0/3、語料非
pending 78/0、95/95 皆重測;tag 後重建 `oo --version` =
`oo v0.2.16` ✓)。dev tie-back `a3fa16c`。

**Blur 展開源裁定(2026-07-16,已批)**:量測=展開源 `#blur` 走
§3.1「Top:無效操作」臂靜默 no-op——`{b:1, ...big}` → `{b:1}`、
`%cause` `_`,雙序、巢內、cocoon 目標皆抹,視界痕跡全滅;鄰居
皆守法(`&` 吸收、⊥ 展開傳因、Top no-op)。法律空白:異質展開
規則列 List/Atom/Top/Bottom,Blur 缺席。裁定(近零新裁,兩既有
法合成可導出):**Q1** SPEC_03 §3.1 新增 Blur 行=吸收,目標變為
該 `#blur` 原樣(展開=全座標讀取,§3.2.2 #5 同律;導出鏈
`{b:1,...big}` ≡ `{b:1} & unbox(big)`);序盲、逐節點、目標種類
無關;Top no-op 不動=「無約束 vs 不可知」分界。**Q2** 快照原樣
性=cause/CAID/視界參數保全(§3.2.2 #1 字面),釘
`p.%caid == big.%caid` → `#true`;目標欄位被吞沒循 ⊥ 坍縮先例,
不造 partial 新機器。矩陣增 L2-57~59(57/58 紅=門、59 綠=Top
分界法釘),95→98。**同場曝光另案**:`&`×blur 快照非原樣——同
程式 `big.%caid`/`(big&{b:1}).%caid`/`({b:1}&big).%caid` 三 CAID
各異,疑違 §3.2.2 #1 保全性,歸 cause 正典審計弧候選。開單前
grep 全探針樹:無凍結釘衝突(§4.10 之 `<`/`<=`×blur、前向引用×
spread 皆非本單變因,原地不動)。工單
docs/blur_spread_handover.md;探針 7 紅+6 釘校準全正(紅全紅、
釘全綠),開單基線 workspace 1057/0/10(=1051+6 釘;7 紅
`#[ignore]`)、conformance 96/98。

**Blur 展開源弧結案(2026-07-16,零代修第十五例)**:交付 dev
`9aaf425`(spread 源 force 後單一 `Value::Blur` 早退臂,先於欄位
搬運——三種目標同臂,cocoon 自動同綠;`TopCaused` 併入 Top no-op
臂=行為等同純申明)、驗收 `c7afd20`。獨立重跑:探針 13/13、
workspace **1064/0/3**、conformance **98/98**、語料非 pending
78/0。對抗全正:吸收×`=` 二段律 #6a 合成(`{b:1,...big} =
{c:2,...big}` → `#true` 同 CAID 決定論)、雙重展開 CAID 原樣、
Top 讓位、態射體/cocoon/巢內顯示保因。交付紀錄先寫單再回報=
協議恢復第二次確認。**新曝光另案**:二源 ⊥×blur 序依賴
(`{...bot,...big}` → `#conflict`、`{...big,...bot}` →
`#fuel_exhausted`;逐源早退相遇序決定勝者,數學上 ⊥ 為格底兩序
應同答)——歸 REAL_04 調和/cause 正典審計候選。

**系統軸所有權裁定(2026-07-16,已批)**:量測=`~%` 影蓋三種互斥
行為並存——root `~%Math: 5`/`~%Math.add: 7` **靜默忽略**(evolve
Ok、內建照舊、exit 0=對用戶說謊)、combo 內 `{~%Math: 9, v:
~%Math.abs(-3)}` **靜默生效毒作用域**(c.v → `_`)、novel
`~%Mine` **自由鑄造**;法源僅 SYNTAX_05 維度定義之言下之義。
G2-S 當日(2026-07-12)量測確認「交付前後一致」另議至今,本弧
收帳。裁定:**Q1** `~%` 唯引擎鑄造(SPEC_09 所有權條款入法;
stdlib CAID=共享身分基底,單調精化亦違法=所有權判準非內容判
準;novel 名=冒名同禁)。**Q2** 違法形雙軌:root → evolve 邊界
帶名報錯(同 G2-S 大聲死機構,同值寫入也擋);combo `~%` 定義
鍵 → 該欄鑄 ⊥ `#system_reserved`(TAG_REGISTRY §1.4 登記;節點
級、合成傳播、**不自癒**——詞法鏈不跳違法欄,自癒藏罪)。
**Q3** 豁免=root `~%Config.<裸名欄>`(規範家;實測 fuel=50 真
生效);combo 內 `~%Config` 不豁免。**Q4** RHS 全面保全(別名/
交集匯入/路徑使用;拼法合法,parser 不動——parser goldens 之
`~%sys: 1` 斷言解析,無釘衝突;語料零 `~%` LHS)。疣記:
`c.~%Math` 顯示 `9 ;; %effect: #io` 幻影 io 標籤,預期隨 ⊥ 鑄
造消失,倖存則記錄。矩陣增 L2-60~62(60/61 紅=門、62 RHS 綠法
釘;root 大聲死面留探針),98→101。工單
docs/system_axis_handover.md;探針 6 紅+7 釘校準全正,開單基線
workspace 1071/0/9(=1064+7 釘;6 紅 `#[ignore]`)、conformance
99/101。開單前 grep 探針樹+語料:無凍結釘衝突。

**系統軸所有權弧結案(2026-07-16,一件代修)**:交付 dev `60d98d9`
(root `is_system_axis_lhs_forbidden` evolve 邊界 Err+Config 豁免
嚴格判準〔整段名+恰一裸名欄〕、Config 寫入=staged 開放部分覆寫
+observe overlay、combo 雙形鑄 ⊥、`SystemReserved` 枚舉尾端追加、
force 終端值不包 pure-wrapper〔幻影 #io 影蓋面根治〕)、驗收+代修
`8231bb7`。**代修=路徑鍵拼法穿透**:`{~%Math.add: 7}` 鑄 ⊥ 於葉
端但 `inject_path` 物化中間節點 `~%Math: {add:⊥}` 為用戶座標,
`v: ~%Math.abs(-3)` 借第二拼法無聲毒死回 `_`——修=違法路徑鍵整
欄塌**首段**+代修釘兩面。共責:紅門只釘 Named 鍵形漏 Path 鍵形
=**雙拼法語境教訓第三例**。對抗全正:`~%ConfigX`/`.fuel.deep`/
`.%fuel`/整組替換全大聲拒(exit 1)、巢內+cocoon ⊥ 帶因、RHS 值
面正確。**既有債歸因(反事實 @開單 commit)**:幻影 `%effect:
#io` 於非影蓋 RHS 面倖存(combo 內系統態射應用效果升格,root 級
同式無標籤)=交付前同形,另案。終態:探針 14/14、workspace
**1078/0/3**、conformance **101/101**、語料 78/0。

**cause 正典審計裁定(2026-07-17,已批)**:審計盤點=引擎 15
BottomCause 變體 vs REAL_04 §2 舊表 vs TAG_REGISTRY 三方對照。
**帳載修正第八次(撤案)**:「`&`×blur CAID 非原樣」為驗收方量測
誤差自首——blur CAID=hash(cause,fuel,strategy,**salt**),salt 每
引擎實例一顆,原量測三次獨立行程跨 salt 必異;單行程重測雙序+互
比全 `#true`,引擎守 §3.2.2 #1。曝光轉永久綠釘(L2-65)。
**兩筆確認(引擎違既有法,零新裁定)**:(1) 二源展開序依賴——
unify 早有 Blur×Bottom=Bottom 雙向臂,spread 之 blur 臂早退跳過
剩餘源,`{...big,...bot}` 漏 `#fuel_exhausted` 應 `#conflict`;修
=blur 不早退續摺疊(⊥ 早退合法)。(2) 幻影 `#io`——
`predict_effect` 一刀切 `~%`→IO 謊報純態射(SPEC_09 §4 ~%Math
純);修=拆毯讀實際效果(~%Env 等真 IO 不動)。**廢稅殘餘**:
`#invalid_path` 末活鑄點(follow_refine CAID parse 失敗)退役→
`#conflict`+上游誠實訊息(原謊稱 refinement cycle)。**法典側**:
Q1 TAG_REGISTRY=正典登記簿唯一維護點,REAL_04 §2 重寫為類別法+
指針(六大類別名實相符:格論/視界資源/存取所有權/來歷/引擎作業
/登記未鑄);Q2 §4 主因果優先級重立法對齊引擎五階(divergent>
違規類>格論族>資源族>座標缺失;#effect_violation 屬未鑄類、
#not_found 屬發現類非值收斂因果,俱移出)。矩陣增 L2-63~65
(63/64 紅=門、65 綠法釘),101→104。變因隔離註記:caid_recheck
e4 之 bot 後定義形回 #fuel_exhausted 屬前向引用×spread 凍結案交
互,記該案不追。工單 docs/cause_canon_handover.md;探針 4 紅+5
釘校準全正。

**cause 正典審計弧結案(2026-07-17,零代修第十六例)**:交付 dev
`e6d1449`(T1=blur_absorb 累積器不早退、Blur×Blur 走 unify、⊥ 穿
出、迴圈尾快照回傳;T2=拆 `~%`→IO 毯、查找後沿剩餘段靜態走欄讀
葉效果,真 IO 執行側不動;T3=parse 失敗改鑄 Conflict+
`get_live_value` 按因分流誠實訊息)、驗收 `數見 dev log`。獨立重
跑:探針 9/9、workspace **1087/0/3**、conformance **104/104**、語
料 78/0;**InvalidPath 活鑄點=0**(F4 承諾兌現)。對抗全正:三源
任意插位 ⊥ 皆 `#conflict`、Blur×Blur → blur fuel、Top/combo 後綴
守法、combo 內 alias 應用乾淨。幻影 `#io` 三面根治。

**R6 展開碰撞 lint 開單(2026-07-17,想法 D 儀器第三件)**:SPEC_03
§1.1 之「lint 提示另議」收帳——零語義變更,純 Tier 1 儀器。R6=
Warn:同字面量內重複全拼鍵(`{a:1, a:2}` 原子形必 ⊥、combo 形
合併皆可疑=外語 overwrite 直覺陷阱)+靜態可見字面展開碰撞
(`{a:1, ...{a:2}}`/雙字面展開)。寧漏勿誤邊界(R4/R5 先例):
root 重複欄=精化慣用形、具名展開源=Tier 1 不求值、路徑鍵部分
重疊=平行定義風格、`_` 合併鍵=多重匯入慣用形,永不旗標。無
conformance 向量(儀器非語義),矩陣 104 不動。工單
docs/collision_lint_handover.md;探針 7 紅+6 釘校準全正(含跨規
則不回歸釘 R4+R5)。

**R6 lint 弧結案(2026-07-17,零代修第十七例)**:交付 dev
`bc33982`(nlint.rs 新 §R6 節,R1–R5 未動;走訪=Expr 樹內 combo/
cocoon 字面量,root fields 非容器;鍵全拼 canonical、`...` 字面源
鍵集碰撞、`_`/pattern 鍵跳過)、驗收見 dev log。探針 13/13、
workspace **1100/0/3**、conformance 104/104 不動、語料 78/0、
`oo lint tests/` R6 零誤報。對抗全正:雙鍵各發/三重同鍵每鍵一發
/`~`/`%` 鍵照旗/cocoon 混合/具名源不貢獻/pattern 寧漏;CLI 訊息
帶 span+法源。想法 D 儀器第三件落地。

**eq×thunk 佇列項量測結案(2026-07-17,無單直落)**:全面電池
15 面(E2 詞法欄/負面/深鏈/applied 欄/pipe 產 combo/巢內計算/
cocoon/態射雙生+異體/range/union 序盲/私有軸參與 #false/inline
字面)於 v0.2.18+ **全綠**——債已被中間弧償清(詞法 forcing、
%id force_recursive 代修、Union 多重集等值代修之副作用)。無引擎
工作、無紅門故不派單;驗收方直落 9 永久法釘
(eq_thunk_pin_test.rs)防未來惰性改動靜默回歸。workspace
1100→**1109/0/3**。佇列剔除。

**`^` 解析裁定(2026-07-17,已批)**:量測=**上溯 off-by-one 蟲族**
——`^ⁿ` 從欄位所在容器起算 n−1 層:遮蔽形 `^.a` 讀當前容器回 9
=錯值謊言、無同名欄回 `_` 靜默、root 宇宙不可達(`^^.r_a` 應 42
回 `_`)、LHS `^` 寫進當前容器;overshoot 雙面(深層+root 級)
自 ⊥-meta 弧健康(bottom_meta 註記「scopes unwired 另案」=本弧
收帳)。裁定三款:**Q1** 容器鏈含根宇宙為最外層(`^^` 從二層深
=root;與 `_.` 同鏈相對拼法、檔案系統 `/` 類比);**Q2** `^.x`
=嚴格座標存取,該層無 x → 開放 `_` 不外溯(路徑錨非詞法鏈);
**Q3 LHS `^` 定義鍵廢止**(文法層,`~.` 錨先例)——用戶檔案系統
直覺入法理:「打開目錄卻看到上層檔案長在這層」=字面量局部性
破壞;父層寫入=正確層級平行定義之冗餘拼法,且免費附送怪物族
(自撞/經根迴環/繭穿刺/展開攜帶綁定歧異,五族量測在案);語料
零使用、parser goldens 全 RHS 面無衝突。SYNTAX_03 §4.4 #4 重寫
三款+廢止注記、SPEC_07 §4.2.3 同步。矩陣增 L2-66~68(66/67 紅
=門、68 overshoot 綠法釘),104→**107**。工單
docs/caret_handover.md;探針 6 紅+7 釘校準全正。

**`^` 解析弧結案(2026-07-17,零代修第十八例)**:交付 dev
`0ff683b`(eval `hops=count+1`、鏈頂=root 宇宙、越頂 ⊥;parser
Parent(n) 編碼不動=「擇一為準」遵守;文法 `field_key` 改
`field_root_path` 僅 `_.` 錨=LHS 廢止落地;bottom_meta「scopes
unwired 另案」註收帳)、驗收見 dev log。獨立重跑:探針 13/13、
workspace **1122/0/3**、conformance **107/107**、語料 78/0。對抗
全正:三層上溯/雙層遮蔽取外/升降混合 `^.a.q`/cocoon 容器/root
深溢出/展開旁 RHS 綁父。**新曝光另案**:態射體內 `^` 綁**呼叫點
容器**(`f:(n->^.k)` 於 `h:{k:8, r:1|>f}` 回 8)=動態綁定風味,
定義閉包 vs 呼叫點裁定候選(與 P2 `$` 不跨管道對照一併裁)。

## G4 惰性 ⊥ 收帳(2026-07-17,已開單)

⊥-meta 弧(2026-07-14)曝光記帳項。**零新裁定**——法源俱在:
SPEC_07 L1-32 逐支投影、SPEC_08 §3.2.2 #5「僅 `_|_` 支剔除、
`#blur` 支存活」、TAG_REGISTRY 註+REAL_04 §4 全 ⊥ 主因果。
**量測(v0.2.19)**:剔除律無單一居所——只住 unify 分配臂(root
evolve 路徑,O1 `(1&2)|5`→`5` ✓)與導航臂之**即時** Bottom 比對
(cocoon miss 面 ✓);三漏:**T1** 導航投影不 force(Stage 2 欄位
留 thunk),thunk ⊥ 全漏——`({a:1}|{a:(2&3)}).a`→`1 | ⊥` 兩序、
全 ⊥ 雙裸曬、`%cause` 對漏網聯集投影成**因果聯集**
`#divergent | #conflict`、`u.a = 1`→#false 謊;二段自癒(`u.a.v`
第二段接到已 force 的 ⊥ 而剔)=漏洞只在末段顯形。**T2**
force_recursive Union 臂 normalize 不剔——欄內直接 `|` ⊥ 成員
觀測面裸曬:`{v:(1&2)|5}`.v→`⊥ | 5`(**新面,比帳載寬**)。
**T3** 全 ⊥ 鑄造丟誠實訊息:導航臂 `primary.into()` 僅標籤、root
全 ⊥ 走 normalize_union 空鑄「empty union after normalize」行話
——REAL_04 §4 工程補充入法:主因果成員 `_|_` **原樣傳出**(訊息
保全;同位階相遇序最左;blur 吸收原樣+T3 誠實訊息同族)。
工單 `docs/union_cull_handover.md`(tools dev):8 紅門+7 釘校準
全正;基線 workspace **1129/0/11** 實測(先量後寫 ✓)、conformance
**107/110**(L2-69~71 三紅=門)、語料 74/0。
**校準曝光另案**:靜止環×聯集投影**語境分歧**——`p:{v:p.v}` 於
`{v:9}|p` 之 `.v`:CLI(evolve 期固化)=`9 | _`(靜止環→Top),
harness(惰性投影)=`9 | ⊥ #divergent`;SPEC_12 兩級線同成員異語境
異判,歸 SPEC_12 家族裁定候選,本弧兩形皆不釘。

**G4 惰性 ⊥ 收帳結案(2026-07-17,零代修第十九例)**:交付 dev
`9b2129b`、驗收 `adb8eca`。T1 導航投影淺 force 迴圈(cap 32,詞法
弧先例;超限=倖存不剔=保守)+全 BottomDetail 收集;T2
force_recursive Union 臂 force 後分流;T3 unify 分配臂保留被剔
detail、空倖存原樣主因果(sort/cap/nondistrib 一行未動);共用
helper `primary_bottom_from_culled`(`min_by_key` 首見最小=相遇序
最左)。探針 15/15、workspace **1137/0/3**、conformance
**110/110**、語料 74/0。對抗全正:blur+⊥+值三支混
(`#blur | 1` 相遇序保全)/混階原樣訊息/rank2 違規勝 rank5/雙側
剔後 `=`/剔+去重/root 全 ⊥ 異階 `#divergent` 原樣。**靜止環
另案升級註記(驗收方量測)**:剔除上崗後兩語境**皆** `9`(法理想
`9 | _`)——惰性投影誤判靜止環為 ⊥ #divergent 者如今被依法剔除,
`_` 支靜默消失;誤判自「顯示異」升級為「觀測後果」,SPEC_12 家族
裁定候選優先度上調。

## 靜止環染色作用域(2026-07-17,已開單)

剔除弧另案之重診斷。**帳載修正第九次**:「CLI vs harness 語境
分歧」框架=量測誤差;真變因=**同觀測 ctx 內先行 force 的非純引用
兄弟**。儀器化 worktree 直讀:force 收尾
`ctx.chain_transform_taint ||= call_ctx.…`(「once transform,
always transform」)把鏈狀態全域化——force 字面量 `9` 即觸發
`TAINT_SET expr_kind=atom`,之後靜止環再入讀 taint=true 誤判變換
→ ⊥ #divergent →(剔除弧後)依法剔,`_` 支靜默消失。序依賴實測:
`{v:9}|p`.v→`9` 抹支/反序 `p|{v:9}`→`_ | 9` ✓;alias/互指同病;
**twin-eq 謊** `u1=u2`→#false(同拼雙聯集);欄內 join CLI 綠/
harness 紅=分類時點(evolve 期 vs 觀測期)本身即病;兄弟欄面健康
=偶然時序。**零新裁定**(SPEC_12 Q2 環自身跳+Q4 不傳播):修法
=拆除向上寫回(鏈狀態隨鏈框架死亡)、下傳繼承保留(真變換環自鏈
內染色,分類安全)。工單 `docs/taint_scope_handover.md`(dev
`9801554`):6 紅+8 釘校準全正;基線 workspace **1145/0/9** 實測、
conformance **111/112**(L2-72 紅=門、73 綠法釘)、語料 74/0。
範圍外記帳:math×Top 聯集值語境 `(_|9)+1`→⊥ #conflict 另案;
TopCaused×Top 去重判等遇歧異記錄勿裁。

**染色作用域弧結案(2026-07-17,零代修第二十例)**:交付 dev
`3a2cb57`、驗收 `11290c7`。單一位點修——taint 向上寫回拆除
(鏈狀態隨鏈框架死亡),cycle_chain 寫回保留=擇案 A(量測後最小
diff),直譯器狀態寫回未動。探針 14/14、workspace **1151/0/3**、
conformance **112/112**、語料 74/0。對抗全正(下傳繼承=拆寫回
真風險面):跨欄變換環兩拼法皆 #divergent、純跨欄環 #static_cycle
對照、多毒兄弟 `2 | 6 | _`、三態混值|變換|靜止 → `1 | _`。帳面
效果:靜止環聯集支不再序依賴抹除、twin-eq 等值謊癒、欄內 join
CLI/harness 同判(語境依賴消除)。

## math × 聯集分配(2026-07-17,已開單)

taint-scope 弧曝光項「math×Top 聯集值語境」重診斷:裸 Top math
全健康(`_ + 1` → `_`,所有運算);真洞=`eval_math` **無 Union
臂**——⊥/Blur 短路與剝殼後 Union 落 Conflict catch-all,全 math 族
(加減乘除/字串拼/左右任一側/雙側/欄內)對聯集一律 ⊥ #conflict
=對疊加態僭稱;對照管道 `(2|9)|>f`、應用 `/f (2|9)` 皆 `3 | 10` ✓
(SPEC_07 §4 疊加態平等演化早已引法)。**零新裁定**:分配沿平等
演化;支級 ⊥ 剔+全 ⊥ 原樣主因果沿剔除弧;Top/blur 支走單值臂
存活;左主序決定性。凍結鄰接:`<`×聯集=§4.10 另案(凍結釘
⊥ #conflict)、`=` 保 G1 結構等值**禁分配**(釘 `(2|9)=9`→#false)、
unary `-(…)` 文法既有形不吃括號(`0-(2|9)` 覆蓋語義面)。
工單 `docs/math_union_handover.md`(dev `51e104d`):10 紅+7 釘
校準全正;基線 workspace **1158/0/13** 實測、conformance
**112/114**(L2-74/75 紅=門)、語料 74/0。

**math×聯集分配弧結案(2026-07-17,零代修第二十一例)**:交付 dev
`117d5f0`、驗收 `6fb2c2e`。內核三層拆分(expr 短路序保留/值層
Union 臂/左主序分配 helper 複用 `primary_bottom_from_culled`+unify
budget 紀律)。**越單變更審核通過=引擎追法**:整除/取餘除零靜默
`0` → ⊥ `#numerical_error`(TAG_REGISTRY 明文「發生除以零…」;舊
special_float_test 釘的是謊,改寫附法源;float Inf/`#_` 路徑實測
不動)。探針 17/17、workspace **1168/0/3**、conformance
**114/114**、語料 74/0。對抗全正:雙聯集×⊥支混 `11 | 21`/去重
相遇序 `3 | 2 | 4`/rem 零支剔/全 ⊥ 同位階取最左原樣/math→管道
合成 `30 | 100`。三弧咬合(剔除律→染色作用域→math 分配)完結,
聯集值語境全線誠實。

**正典顯示序弧開單(2026-07-18)**:裁定 A 案入法 = SPEC_01 §2.4.1
聯集正典顯示序(型別族階:數值升序→字串→標籤→結構值(顯示字串
字典序)→#blur→Top 殿後;穩定排序;**只動顯示層** to_nlang Union
臂,支向量/tropical 截斷/左主序求值/bn_serial 不動;禁 digest 排序
鍵=blur 鹽跨行程非決定)。病灶量測(v0.2.21):CAID 早已序無關
(bn_serial 排 digest),store 去重致**先存者拼法全域獲勝**——
`a: 9|2`+`b: 2|9` 同印 `9 | 2`、無關前欄隔空改寫拼法;顯示是演化
史的函數非值的函數。conformance L2-75 期望遷移 `10 | _` + 新增
L2-76(拼法無關)/L2-77(型別族階),三紅=門,矩陣 114→116。
工單 docs/display_order_handover.md(tools dev `d6454b9`):新探針
10 紅+7 釘(%caid 序無關/=多重集守衛),開單遷移 10 法衝突釘
(taint×4/math×5/nav×1,MIGRATED 標記)。基線實測 1165/0/23、
113/116、語料 74/0;目標 1185/0/3、116/116、74/0。模型 #3 已派。

**cause cocoon 調和弧開單(2026-07-19)**:裁定 A 案+用戶設計考古。
REAL_04 §1 重寫=正典核 `%val` 唯一必備+診斷欄可選 %-前綴依
TAG_REGISTRY 類別變形;舊表 11 裸名欄(path/line/…)引擎從未鑄造
=雙帳漂移同病,降級非規範性附註。**%type 廢止**=設計考古:舊代
節點模型殘欄(型別內容曾放 %type 欄,後由同構原理 SPEC_03 §4
%kind+%super/%predicate 取代;cause 繭 %type 恆同 %val=化石雙帳);
`.%type` 讀法退役(⊥ 合成性原樣/blur 座標吸收),SPEC_08 §3.2.2
#4 同步。**鷹架不可見**=`_: _` 墊欄不得現身用戶投影(用戶自定
`_` 欄合法保全——量測 `{_: 5}` 可寫)。二源 ⊥×blur 序依賴量測
**已癒**(cause 正典弧 T1 收,兩序皆 ⊥ #conflict)→ 綠釘照記。
conformance:8 條向量 `.%type`→`.%cause` 改拼(保綠)+新 L2-78
紅=門(`e.%type` 應 ⊥ 原樣),矩陣 116→117。**超級衝突另案開帳
(裁定候選)**:SPEC_02 §1.2/SPEC_05 §2.1「@ 索引至 %type」舊語
vs SPEC_03 §4 %kind 模型;引擎 nominal 機構(type_constraint/
dispatch)字面實作舊模型 %type 欄、%super/%predicate 全無;牽
REAL_03 §288 `~%type` 序列化例=CAID/fmt 面。工單
docs/cocoon_shape_handover.md(tools dev `f1fce05`):6 紅+8 釘
(含 nominal 圍欄釘)。基線 1200/0/9、116/117、語料 74/0;目標
1206/0/3、117/117。模型 #3 已派。

**%kind B 弧開單(2026-07-19)**:B1 軸語正名落地(SPEC_02 §1.2
前綴表三行改「資料軸/型別軸/規則軸」+正名註;SPEC_05 §2.1 同步)
;B2 落地(SPEC_05 §3.2 實作現況註:%super/%predicate 未實作掛帳
B5、nominal 載荷欄=引擎內部表示不入法、%kind 正典拼法 #type);
B4 落地(REAL_03 §6.3 範例改寫 BN/ v2 實態:軸階只排序不入位元組
流、LEB128 條目數、無 ~%type 字串鍵;修正註記舊例三重失實)。
B3 引擎小弧開單:兩鑄造點+讀取點(type_constraint.rs:60/:244/
:126、dispatch.rs:101)#type_constraint→#type 同步遷移,is-marker
新判準不得誤吞 stdlib 型別節點(%kind #type+%name);載荷欄不動;
marker CAID 一次性合法位移。用戶可見面=<<@{ @int }>> 結構視圖。
工單 docs/kind_tag_handover.md(tools dev `87d906d`):2 紅+5 釘;
全樹 grep 退役拼法零期望字串(新紅線首用)。基線 1211/0/5、
117/117 不動(向量會釘死 B2 不承諾拼法,不加)、語料 74/0;
目標 1213/0/3。模型 #3 已派。

**態射體內 `^` 綁定弧開單(2026-07-19,裁定 A 案)**:法理=用戶
設計原意「`^` 是定義當下的路徑縮寫,非觀測時依當前路徑判讀」。
SPEC_07 §4.2.3 增訂:體內 `^` 鏈=定義側容器鏈到底([持有→…→
root],體視同持有容器內一層與巢內字面量同構),定義處捕獲不隨
呼叫點變;超深 ⊥ #out_of_horizon;呼叫點資料唯一通道=`$`;三通道
各一法(裸名=詞法/`$`=動態/`^`=定義側嚴格座標)。量測=嵌合鏈:
[閉包 frames 不含 root]++[呼叫點容器鏈],第 (frames+1) 跳起洩入
呼叫鏈——同字面量 `^^` 於 h=9 於 root=5、root 持有第 1 跳即動態;
九面全吻合。管道/`/f` 同病。設計註記帳:態射「轉換」之名 vs 管道
「演化」之實=編輯性另案待議。conformance 增 L2-79/80(紅=門),
矩陣 117→119。工單 docs/caret_body_handover.md(tools dev
`2af7f68`):6 紅+5 釘;全樹 grep 零體 `^` 釘=零遷移債。基線
1218/0/9、117/119、語料 74/0;目標 1224/0/3、119/119。模型 #3 已派。

**前向引用×spread 弧開單(2026-07-19,解凍展開碰撞 Q3)**:零新
裁定=欄位同時性/交換律(L1-26/27)+ SPEC_03 §3.1 新時序條款
(展開於觀測收斂時擴張,源位置無關;交集/⊥/blur 諸律擴張時一體
適用;未定源 Top no-op 既有行;循環照 C4 #divergent)。量測=構造
時急切展開,前向源五面靜默貢獻零(基本欄 _/碰撞 1..5/⊥ no-op/
blur no-op/別名 _),循環面被病遮蔽。conformance 增 L2-81/82
(紅=門),矩陣 119→121。工單 docs/forward_spread_handover.md
(tools dev `edf625a`):7 紅+3 釘+凍結釘解凍遷移(_→7);記錄
義務=cross-dep(q←src←q.b 逐座標理想 1 vs 守衛粒度)、CAID/
store 時序如實申報。基線 1226/0/11、119/121、語料 74/0;目標
1234/0/3、121/121。模型 #3 已派。

**%effect 顯示疣弧開單(2026-07-20,裁定 C=雙軌+一般化)**:
**帳載修正第十次**:掛帳的幻影 `%effect: #io`(combo 內純計算
升格)**早在 v0.2.18 cause_canon 弧 T2(honest predict_effect)
根治**——v0.2.26 複測+worktree 反事實(v0.2.19/20/21)全淨;
佇列項剩「顯示格式本身」。裁定:(1) `;; %effect:` 尾註入法=
**診斷註解層**首位法定成員(SPEC_11 §3.4 新設:引擎得以註解形式
附加診斷資訊;parser 不可見、不參與語義/CAID/排序鍵;凡語義資訊
必須另有正式通道,註解永不得為唯一載體;建議實作提供
--verbose/--silent/--debug 開關〔非規範性〕);(2) `.%effect`
元讀入法(SPEC_08 §4.1 元欄觀測:預設 #pure、開放 combo=傳染
join〔引擎構造時已算,me=max(te)、closed 跳過=屏蔽已實作,僅缺
讀取臂〕、cocoon=#pure、聯集逐支分配、顯式欄位優先;⊥/blur
白名單不變)。量測=元讀全 `_`(原子/combo/cocoon/聯集五面)。
**另案記帳**:效應系統波(固化 #io→#cached §4.2.4、靜態守護
#effect_violation §4.3、set-join 矩陣 vs 引擎 max 單標籤、CAID
參與義務;REAL_05 外部邊界)+**oo test harness Top-pass 空洞真**
(孤兒 tests/effect_taint.n `_ == #io`→`_` 判 PASS——儀器誠實
問題)。conformance 增 L2-83/84(紅=門),矩陣 121→123。工單
docs/effect_meta_handover.md;探針 7 紅+5 釘校準全正(紅全
`got _` 正因)。基線 1241/0/10、121/123、語料 74/0;目標
1248/0/3、123/123、語料 75/0(孤兒遷 unit,空洞真轉真綠)。
模型 #3 已派。

**%effect 顯示疣弧結案(2026-07-20,一件代修=驗收代修)**:交付
dev `8006b1d`(`effect_tag_atom`+三臂:非容器早返回/combo 欄位後
closed-miss 前〔spoof 欄位優先、cocoon 讀 %effect 不 #missing_key〕
/union 逐支後 normalize 早返回;無 re-taint 自防謊=交付方自抓
`#io ;; %effect: #io` 謊形;白名單/顯示層/枚舉/CAID 全未動)、
驗收代修 `ed840c4`。**抓漏=巢繭屏蔽穿透**:`w: {k: {{v: io}}}` 之
`w.%effect` → #io 違 §4.2.1——predict_effect Combo 臂無視 closed
走表達式樹 join,同繭別名拼法已 #pure(值側健康)=字面量/別名
分歧;基線期誤 join 無讀取臂不可觀測,鏡頭一裝即成謊。修=closed
早返回 Pure 一行+代修釘三面(字面量/別名/開放巢照傳)。終態:
**1249/0/3**、**123/123**(L2-83/84 翻綠)、語料 **75/0**(孤兒
effect_taint 真綠轉正)。對抗 9/10 正:聯集去重/鏈式/欄值/eq/⊥
剔除/繭內值標籤保全/態射/spoof 非標籤值/雙繭。**共責教訓**:紅門
釘了繭自身標籤漏對外傳染面——**屏蔽/傳染類法門要內外雙面**
(自身讀值+跨壁 join)。既有債確認:誤 join 交付前既有,本弧曝光
非引入。v0.2.27 未切待用戶。

**~%Config 欄名驗證弧開單(2026-07-20,裁定 A=封閉旋鈕家)**:
系統軸弧豁免只驗形不驗名籍與型——三violation面全靜默(未知名
`fool` rc=0/謊面 `feul: 99999` 長鏈照舊 10000 blur/錯型
`fuel: "lots"`、`strategy: 5` 收下後消費端回預設),顯示面
`out: ~%Config` 只見 staged 殘片。裁定:名必屬創世七鈕表、值必
合型(六 int 鈕非負整數、strategy 三標籤),違者 evolve 邊界
帶名報錯(新 `#invalid_config` 錯誤類名,TAG_REGISTRY 登記,不鑄
節點 ⊥;BottomCause 枚舉尾端追加);旋鈕家封閉=未來走規格書
演化、第三方走 ~%Engine;觀測本體=有效配置(創世 ∧ 覆寫)。
健康面釘死:逐鈕讀/透鏡讀/expr RHS 求值後驗型/fuel 真效。
SPEC_09 豁免收窄+§6 旋鈕表、TAG_REGISTRY `#invalid_config`。
**無可向量面**(大聲死+多行顯示),門全在探針,矩陣 123 不動。
工單 docs/config_validation_handover.md(tools dev `20f8fbe`):
6 紅+4 釘校準全正。基線 1253/0/9、123/123、語料 75/0;目標
1259/0/3、123/123、75/0。整組替換形另案不預斷。模型 #3 已派。

**~%Config 欄名驗證弧結案(2026-07-20,零代修第二十五例;協議
全淨)**:交付 dev `9ddfa86`(旋鈕表 const+名籍/型別雙點驗證
〔名在求值前、型在 collapse 後;⊥/Top/錯型拒〕+`effective_config`
創世 ∧ 覆寫三處復用〔evolve/observe overlay/lib.rs 雙綁定點,
staged 殘片永不綁定〕+`InvalidConfig` 尾端追加)、驗收 `e0ee623`。
獨立重跑:探針 10/10、**1259/0/3**、**123/123**、語料 **75/0**
四數全中。對抗全正:別名綁定透讀/覆寫可見/spread RHS 匯入/雙
覆寫/float 拒/CLI 帶名報錯 `InvalidConfig at ~%Config.fool`
exit 1(同 G2-S 訊息族)。記錄:universe.rs `default_cache_id`
unused-import 警告=既有噪音雜務另案。v0.2.28 未切待用戶。

**引擎 v0.2.28 定版(2026-07-20)**:top `1b4e4c0`(squash config
驗證弧 + oo 0.2.28 bump+lock 同入〔上版教訓生效,零髒尾〕),
tag 於實測 commit(1259/0/3、語料非 pending 75/0、123/123 皆於
候選重測;條件閘一次成功;tag 後重建 `oo --version` =
`oo v0.2.28` ✓)。dev tie-back `5c99925`。

**態射vs管道語義梳理(2026-07-20,編輯性,^ 弧掛帳收口;用戶
定錨改版)**:總綱移 SPEC_00 §1.2「靜與動」——三位一體=靜態
結構,動態唯二來源=觀測+演化(管道);SPEC_07 卷首縮註腳級
(態射=算子/管道=行為/「態射是轉換」名詞非動詞/體內 `^`
定義側=推論)。§4.2.3 指針收口。零語義變更、零引擎、矩陣不動。
觀測↔演化關係同日定稿入 SPEC_00 §1.2(用戶批一句話版):
**演化改變宇宙但不決定事實;觀測決定事實但不改變宇宙**——
「尚未定義」/「就是沒有」分界=相位分界(in_evolve 旗標即其
機械化;SPEC_03 §3.1 展開時序/SPEC_08 §4.2.4 固化/SPEC_07 §4.3
演化即提交皆此線)。掛帳清結。

**oo test 空洞真弧開單(2026-07-20,裁定 B=定形通過)**:病根
=**規格洞**——SPEC_16 §2.2 舊文「任何非 ⊥ 即過」,Top/blur 按
字面通過(引擎已比法嚴:#false/#fail 判失)。實案兩枚:孤兒
effect_taint `_ == #io`(元讀弧已真綠)+ test_canonical
`.%type` 退役拼法(cocoon 弧語料漏網;blur 吸收後空洞過,斷言
從未被驗證——**開單遷移 `.%cause` 後真 #true**)。語料 75 檔
普查:此外無非定形 test。SPEC_16 §2.2 改寫=測試即觀測,Pass=
定形值(冒煙斷言保留),Fail=⊥/#false/#fail/Top(未定)/blur
(報 %cause)。工單 docs/test_verdict_handover.md(tools dev
`65ec60c`):3 紅(Top 空洞/未定比較/blur runaway)+5 釘(true/
冒煙/false/⊥ 帶因/遷移拼法真綠),CLI 整合形制。無向量,矩陣
123 不動。基線 1264/0/6、123/123、75/0;目標 1267/0/3。
模型 #3 已派。

**oo test 空洞真弧結案(2026-07-20,零代修第二十六例;協議全
淨)**:交付 dev `79a6ef5`(判定 match 恰兩臂:Top/TopCaused=
undetermined 帶欄名、Blur=帶 %cause;catch-all 前既有臂後;
exit/static-only/發現/Summary/interpreter 全未動)、驗收
`cfd4fc8`。獨立重跑四數全中:8/8、**1267/0/3**、123/123、
**75/0**——收緊後語料無一翻紅(開單普查零漏網獲證)。對抗全
正:混合檔 1+1 exit 1/別名 Top 直測/`(1&2)|_` 剔除後 Top/
static-only 照舊。儀器誠實弧結:「語料 N/0」自此不含空洞真。
v0.2.29 未切待用戶。

**序關係波 W1+W2 弧開單(2026-07-20,波計畫已批:W1+W2 併單→
W3 非原子序→W4 B5,blur×序=隨 `=` 二段律,破壞性知情確認)**:
病=引擎自始已記載偏差(原子 `<` 族判數值大小,`3<=5`→#true,
L1-20 標「暫」)+子型別面未實作(`1<=@int`→#conflict)+數值
謂詞不存在。法=SYNTAX_06 既有(子集語義,`(A&B)=A`);SPEC_09
§3 新立 `/lt /lte /gt /gte` 謂詞表+數值大小唯一合法家條款;
SYNTAX_06 §2.5 具體指針。**CHANGELOG 破壞性條目=v0.2.0 後首筆,
啟動 ORDER_00 §5.1.4 穩定時鐘判定**。翻面穩定面全釘:poset 鏈
(格序本尊)/自反/`3>=5` 鏡像/浮點依值同單集/極值/`=`/`==`/
combo+union 凍結。遷移:L1-20 期望→#false(去暫)、L2-10 三元
條件改拼 `~%Math./gt`、cmp_extremes 偏差釘+eval_test(開單,
遷移紅)、語料 test_comparison `10>5`→`~%Math./gt 10 5`(交付
步)。工單 docs/order_wave_handover.md(tools dev `d07a18e`):
6 紅+5 釘+2 遷移紅校準全正。基線 1270/0/11、121/123、75/0;
目標 1278/0/3、123/123、75/0。模型 #3 已派。

**序關係波 W1+W2 弧結案(2026-07-20,代碼零修;協議代修一筆=
越單語料遷移追認第四例)**:交付 dev `7cdafff`(W1=四謂詞+
SEED_MATH 合法位移;W2=舊數值臂全拆/poset rank 分支保全/
numeric_same 依值單集/原子×原子乾淨 #false/原子×型別 meet
歸約/型別×型別複用子型別判定/combo+union 凍結守住)、驗收
`3ea6fa6`。協議代修=test_entropy.n 熵增長行 `>` 翻面受災逕行
遷移 `/gt`(合法+誠實申報);共責=開單掃描只抓字面量對漏變數
運算元——**紅線補強:翻面類弧掃描須含裸運算子形**。獨立重跑
四數全中:11/11、**1278/0/3**、**123/123**(L1-20 去暫)、
**75/0**。對抗全正:型別格 @int⊆@num/自反/3<3.0 同單集/謂詞
⊥ 面/& 合成。**既有債另案(反事實 @v0.2.22 同形)**:二元
math builtin×聯集分配缺席(max/pow 家族;一元與運算子核心皆
分配)。v0.2.0 後首筆破壞性條目落地。W3(非原子序+blur 二段律)/W4
(B5)接續。

**序關係波 W3 弧開單(2026-07-20,零新裁定)**:非原子序接線
——量測=combo/聯集/混合面全 ⊥ #conflict 而**歸約原料全健康**
(`((1|2)&(1|2|3))=(1|2)` #true、`({a:1}&{a:@int})={a:1}` #true、
開放世界 meet 增欄 #false),W3=純接線 `(A&B)=A` + 真子集雙向
歸約。SYNTAX_06 §4 新 #13=序×blur 隨 `=` 二段律(同 CAID 自反
答案/其餘吸收)。凍結釘四處開單遷移(order_wave 圍欄/
combo_equality 自反/blur_boundary lt+lte)。L2-85/86 紅門,矩陣
123→125。工單 docs/order_w3_handover.md(tools dev `b6dbf00`):
6 紅+4 釘+4 遷移紅校準全正。基線 1278/0/13、123/125、75/0;
目標 1288/0/3、125/125、75/0。模型 #3 已派。

**序關係波 W3 弧結案(2026-07-20,代碼零修;協議代修一筆=
math_union 凍結釘越單遷移追認第五例)**:交付 dev `de946aa`
(blur 二段臂在歸約前復用 blur_caid、subset_lte 通用歸約
meet→force→G1 PartialEq、meet 出 ⊥/blur→false、末端 #conflict
凍結拆除)、驗收 `b033f14`。共責帳載級:開單掃描命中被
`head -8` 截斷漏第 9 筆——**新紅線:掃描輸出不得截斷**。四數
全中:10/10、**1288/0/3**、**125/125**、75/0。對抗 9/10 正
(巢狀/混型/序盲/繭/雙生 blur 吸收)。**發現另案(呈裁)**:
**聯集吸收律缺席**——開放 combo 支聯集包含 under-approximate
(數學 ⊆ 真而引擎 #false;根因=combo meet 開放世界合併不湮滅
+G1 唯一等值/L1-28 去重無向下閉包吸收 `a|(a&b)`↛`a`;動它=動
G1 唯一等值條款,格論裁定)。非原子序全面落地,凍結釘清零。
v0.2.31 未切待用戶;W4(B5)接續。

**聯集吸收律弧開單(2026-07-20,裁定 A=表示層吸收)**:W3 驗收
發現呈裁後同日裁定——SPEC_01 §2.4.2 新設:聯集正規化=剔 ⊥ →
去重 → 吸收(`b <= a` 支被吸收,同 G1 全關係,僅存極大支);
Top 族塌縮(帶因優先/多帶因取最左=REAL_04 §4 同拍);blur 支
雙向豁免(存活律優先);顯示/`=`/`<=`/CAID 四者同調=唯一等值
條款存活。**破壞性條目 #2**(受影響聯集 CAID 一次性位移)。
順帶解決掛帳:TopCaused×Top 去重(record-only)+math×Top 聯集
值語境(`(_|9)` 塌 `_`)。工程圍欄=不動點紀律(吸收判定之
meet 不得再觸發正規化)。L2-87/88/89 紅門,矩陣 125→128。工單
docs/union_absorption_handover.md(tools dev `bfb56a2`):4 紅+
3 釘校準全正。基線 1291/0/7、125/128、75/0;目標 1295/0/3、
128/128、75/0。模型 #3 已派。

**聯集吸收律弧結案(2026-07-20,一件驗收代修〔引擎〕+兩件釘代修
+一件向量重指)**:交付 dev `5950427`(normalize_union_absorbing:
flatten→剔⊥→G1 去重→blur 分離→Top 族捷徑→O(n²) 吸收→接回 blur;
不動點圍欄 union_absorb_fence;subset_lte_inner 淺比較解遞迴型
卡死〔交付方自抓〕;八處路由點)、驗收+代修 `07bc03c`。
**驗收代修=探測洩漏引擎全域 force memo**:探測期強制求值把污染態
結果寫入 memo,真求值讀回 ⊥ #divergent 剔掉靜止環支——
`w: {q: p.v | 9}` CLI `_` / harness `9`(反事實 @v0.2.31 兩語境皆
`9 | _` ⇒ 本交付引入;違 SPEC_00 不變量 1)。修=探測用隔離 ctx
+`memo_enabled=false`,僅記回 fuel;solidify 路徑(cmp,W3 已定版)
不動。**釘代修 ×2=交付把精確釘放寬為析取式**(其一接受四形狀),
同義反覆非門且遮蔽上述分歧——改回單值。**向量重指**:L2-72 期望
改 `_` 雖合法但該向量失去鑑別力(反事實:成員整個拿掉亦得 `_`),
改指 `72-union-static-cycle-order-blind`(支序盲 #true)+探針補
鑑別釘。**既有債曝光(非本交付)**:`TopCaused(#static_cycle)+1`
語境分歧(CLI `_` 合法 vs harness ⊥#divergent;@v0.2.31 裸形已同形)
——釘住現實、另案。終態:**1296/0/3**、**128/128**、語料 **75/0**。
對抗全正(多層吸收鏈/型別多支/⊥+Top 混/攤平/交換律/一元分配存活/
惰性 vs 實心吸收一致)。**新紅線:查詢式機制須同時隔離三處狀態
——ctx 旗標、ctx 環鏈、引擎 memo**。v0.2.32 未切待用戶。

**兩種 `_` 弧開單(2026-07-20,裁定 C;§2.4.2 發版前就地補裁)**:
用戶自吸收律後果反推出真問題——`_` 一個拼法扛兩件事,吸收律
分不出「使用者明說任何」與「此處尚無答案」,後者被當前者一口
吞掉(`x | _` 的 Russell 味道=選項被自己的替代項吞噬,退化析取)。
裁定:**裸 `_` 照吸收;帶因 `_`(#static_cycle/新增 #no_coordinate)
與 #blur 同列診斷成員**,三條豁免一體(不被吸收/不吸收/**任何
深度含診斷成員之值不得作吸收方**——否則 `{v:9} | p` 於組合層被
`{v:_}` 整支吞掉=以未知抹除已知)。**開放缺欄導航改鑄帶因 Top**
`#no_coordinate`(TAG_REGISTRY 登記;顯示仍 `_`,%cause 可溯;繭
缺欄仍 ⊥)。此裁**救回**吸收弧的附帶損失:union-nav/染色作用域
兩弧之可觀測性、L2-72 原面(期望復原 `9 | _`)。矩陣 128→131
(L2-90 序盲/91 缺欄因/92 導航存活)。工單
docs/caused_top_handover.md(tools dev `2f87a8c`):4 紅+7 釘
(2 顆校準降級)+9 顆開單遷移紅(反轉吸收附帶遷移)。基線
1293/0/17、128/131、75/0;目標 1306/0/3、131/131、75/0。
**用戶洞見入帳**:當初為誠實而加的帶因 Top,在此升格為法定第二
種 `_`——診斷裝置變成語義裝置。模型 #3 已派。

**兩種 `_` 弧結案(2026-07-21,引擎零代修;裁定 A 收束值/導航
不一致)**:交付 dev `f132452`、驗收結案 `ac93514`;spec 邊界註
`8584909`。裁定 C 本體全綠。**值/導航不一致=固化面 vs 惰性面
(用戶批)**:`u:{a:1}|{a:1,b:2}` 之 `u.b`→`2 | _` **非 bug,是
惰性正確截面**——導航逐支投影不先固化 union(Call-by-Observation);
顯示/`=`/`<=`/CAID 屬固化面吸收生效(`u`={a:1}、`u={a:1}` #true)。
兩面不同收斂深度=按需觀測本質(內容定址要顯示固化+有限收斂要導航
惰性,交會於此;**此複雜度非設計錯誤,是核心兩承諾交界的必然**)。
根因=導航路徑不做固化吸收=union_absorption 遺留(反事實 @2f87a8c:
裸 Top 過度吸收遮蔽,錯因碰巧一致;caused_top 暴露),非本弧退化。
不修 C=導航固化吸收會重引遞迴型 `@Tree|()` 發散。SPEC_01 §2.4.2
補固化/惰性邊界註;union_nav 釘答案 `2|_` 保留僅註解理由修正
(交付誤標 L2-92 不可比孿生,實惰性截面;驗收方改註非代修)。
**越單接觸兩件追認**:Join/Meet/Diff 不設染色(格結構非變換,反事實
三面皆改善:m.a&1 從 #divergent 謊變收斂 1 真不動點)+ evolve 再化
含 #no_coordinate(caret 根站點回歸)=裁定 C 必要配套;越單 spec
`cf0db61` L2-56 改指裸 Top 必要,矩陣描述驗收方補正。終態:探針
11/11、workspace **1307/0/3**、conformance **131/131**、語料
**75/0**。**新佇列(用戶指示)**:Call-by-Observation 升規範層——
現主居 GUIDE_03 §11 補章,SPEC_07/12/SYNTAX_12 僅指針;應升 SPEC_XX
與 CAID(REAL_03)平起,獨立規格重構弧。v0.2.32 未切待用戶。

**引擎 v0.2.32 定版(2026-07-21)**:top `3103d15`(squash 聯集
吸收律弧〔裁定 A〕+ 兩種 `_` 弧〔裁定 C〕+ oo 0.2.32 bump+lock
同入),tag 於實測 commit(1307/0/3、語料非 pending 75/0、
131/131 皆於候選重測;條件閘一次成功;tag 後重建 `oo --version`
= `oo v0.2.32` ✓)。dev tie-back `53c9fd6`。**第二筆破壞性版**
(受影響聯集 CAID 一次性位移)。origin/top 已同步至 v0.2.31
(用戶已推)。

**Call-by-Observation 升規範層(2026-07-22,純 spec 弧,無引擎/無切版)**：
CbO 語義本體自 GUIDE_03 §11(工程施工圖)升為 **SPEC_04 §6「按需觀測」**，
與 CAID 平起（CAID=SPEC_13 §1 語義+REAL_03 協議；CbO=SPEC_04 §6 語義+
GUIDE_03 §11 協議）。散落指標 SPEC_01/07/12/SYNTAX_07/12 全改指 §6。新增
Yoneda 雙極（CbO=觀測極 `hom(A,X)` 惰性 / CAID=身分極固化；惰性⟺無全域
截面〔KS/Bohr〕⟺障礙非零⟺觀測構成性）。spec `local` `55936c5`+史料
`20791dc`（history_origins §7b）。

**型別反映 B5/R1（2026-07-22，裁定 R1，零代修）**：`@T` 的 `%super` 落地
為衍生反映欄，取 SPEC_09 §2.1 樹直接父（收斂沿格往下但 handler 查找沿
層次往上＝單調收斂反向）；`%type:"Name"` 內部載荷退役、型別名反映收斂
`%name`（最後一個 %type 化石）；`%predicate` 退場→**R2 帳**（nominal 子型別
+跨引擎自訂型別交換，核心排除）。float 遵 §2.1 樹→`@complex`（非 §2.3
傳遞祖先）；marker 內容雜湊內部位移但 `.%caid` 不可觀測/不受承諾/逐觀測
重鑄→**非破壞**。探針 type_super 14/0/0、workspace **1321/0/3**、conformance
131→**135**（L2-93/94/95/96）、unit 語料 68/0。spec closure：SPEC_05 §3.2
主裁+R2 帳、SPEC_03 §4/SPEC_02/REAL_04/SPEC_09 §2.3、CHANGELOG 增量
（spec `local` `991d0e5`）。

**引擎 v0.2.33 定版(2026-07-22)**：top `07705ac`（squash 型別反映
B5/R1 弧 + oo 0.2.33 bump+lock 同入），tag 於實測 commit（workspace
1321/0/3、conformance 135/135、unit 語料 68/0 皆於候選重測；條件閘
一次成功；tag 後 touch build.rs 重建 `oo --version` = `oo v0.2.33` ✓）。
dev tie-back `acd99dd`。**非破壞性增量**（新增 %super/%name 反映；marker
CAID 內部位移不可觀測）。前版 v0.2.32=`3103d15`。

**效應系統波 arc 1：效應組合 = 集合聯集（2026-07-23，裁定=使用者，零代修）**：
效應模型由**純量全序**（`EffectTag { Pure<State<IO<NonDet }`，`.max()` 組合）
遷至**集合半格**，落地 SPEC_08 §4.1 組合矩陣。`io`/`nondet`/`state` 為不可比
兄弟，`|` 是真 join；病灶=`io ⊔ nondet` 被 max 坍縮成 `#nondet`，IO 事實消失。
交付 `e08b2c6`（`EffectTag` 改 `Copy` bitset newtype，保留 Pure/IO/NonDet/State
常數 + 保留 Cached 位；**移除 Ord** 逼編譯器點名 71 處 `.max→union`；
`effect_tag_atom` 多標籤 → `normalize_union`〔字母序，同 §2.4.1〕；顯示尾註同序）。
**CAID 紅線守住**：per-node effect byte 走 `to_serial_byte()` 將舊 4 單標籤映回
舊序數（0/1/2/3），既有 CAID 逐位元穩定；多標籤 combo 為新可能值無位移。
探針 effect_union 15/15、workspace **1336/0/3**、conformance **138/138**
（L2-97/98/99=io|nondet、三標籤、合一 join 翻綠）。**破壞性**：`.%effect`/顯示
尾註對多效應值由 `#nondet` 變 `#io | #nondet`（自 v0.2.26 `.%effect` 可讀起，
對依賴單標籤結果的程式破壞）。掛帳後續弧：`#cached` 固化（§4.2.4）、`#ext:`
自訂標籤、靜態守護 `#effect_violation`（§4.3）、runPure handler、效應集合完整
參與 CAID（§4.1 參與義務）。工單 `nlang-tools/docs/effect_union_handover.md`。
零代修累計 +1。

**引擎 v0.2.34 定版(2026-07-23)=破壞性版**:top `ac3bb50`(squash
效應系統波 arc 1〔effect_union〕+ `~%repl→~%Repl` 測試改名 + oo 0.2.34
bump+lock 同入),tag 於實測 commit(workspace **1336/0/3**、conformance
**138/138**、effect_union 探針 15/15 皆於候選重測;條件閘 `[repo=nlang-tools]
&& [branch=top]` 一次成功;tag 後 touch build.rs 重建 `oo --version` =
`oo v0.2.34` ✓)。dev tie-back `e368ac0`。**破壞性**(`.%effect` 多效應值
`#nondet`→`#io|#nondet`,CHANGELOG 破壞性 #3)。CAID 穩定(to_serial_byte
舊序數映射)。前版 v0.2.33=`07705ac`。

**效應系統波 arc 2:#cached 固化(2026-07-24,零新裁定,零代修)**:
落地 SPEC_08 §4.2.4 停止邊界固化。**穩定 CAID = store 依內容位址取回值**
(store-committed 歷史已固化);取回值觀測時活動標籤(io/nondet/state)→
`#cached`;新鮮值仍活動(L2-83 守)。**觀測時投影,不動 store/CAID**——
`get_value` 保持 raw,固化為取回副本上的遞迴投影(`Value::solidify_effects`)。
**鉤範圍**:只掛使用者面取值口 `~%Discovery./fetch`·`/find` + `oo inspect`;
universe commit-root 重建/refine 單調性檢查/NDP wire-serve 保持 raw(commit-chain
CAID 與 REAL_04 決定性不受影響)。**重激活免費**:arc-1 集合聯集使 `{cached} ⊔
{io}` = `#cached | #io`(§4.1 矩陣),無新碼。交付 `c59809d`。探針 effect_cached
11/11、workspace **1347/0/3**、conformance **138/138 不變**、genesis 11/11
(commit-chain 完整)。**本弧不加合規向量**:store round-trip 非 hermetic(純值
決定性 CAID 與持久 `.oo` 既有物件碰撞),不合 conformance 無狀態契約,探針
(乾淨 temp store)為法定測具。**增量**(fresh 不動;唯 fetched `.%effect`
#io→#cached,落實既有法)。掛帳後續:靜態守護 `#effect_violation`(§4.3)、
runPure(§4.3)、`#ext:`(§4.1)、CAID 全集參與(§4.1)。零代修累計 +1。
工單 `nlang-tools/docs/effect_cached_handover.md`。

**引擎 v0.2.35 定版(2026-07-24)=增量**:top `c4b4c4b`(squash 效應系統波
arc 2〔effect_cached〕+ oo 0.2.35 bump+lock 同入),tag 於實測 commit
(workspace **1347/0/3**、conformance **138/138**、effect_cached 探針 11/11、
genesis 11/11 皆於候選重測;條件閘一次成功;tag 後 touch build.rs 重建
`oo --version` = `oo v0.2.35` ✓)。dev tie-back `158c4df`。**增量**(fresh 值
不變,唯 store-fetched `.%effect` #io→#cached;§4.2.4 落實)。CAID 穩定
(觀測投影,get_value raw,commit-chain 不動)。前版 v0.2.34=`ac3bb50`。

**效應系統波 arc 3:靜態守護 #effect_violation(2026-07-24,裁定 A,零代修)**:
落地 SPEC_08 §4.3。**裁定 A(使用者):純語境=顯式 `%effect: #pure` 宣告**
(n/ 唯一純度宣告機制),被值的**實際活動傳染**(io/nondet/state)矛盾時 →
坍縮 `_|_ (%cause: #effect_violation)`(說謊即崩潰)。**非**環境預設語境
(那會砸 L2-83)。**繭壁自動豁免**=逃生門:繭真屏蔽(closed 跳效應累積
§4.2.1)故實際 effect 就是 #pure,宣告相符無矛盾。交付 `f573426`:
`BottomCause::EffectViolation`(append-only,TAG_REGISTRY 既列)+ combo 終化
單條 ⊥ 早返(`declared_pure_meta ∧ cv.effect.has_active()`);`has_active()`
抽共用(arc-2 solidify 亦改用)。探針 effect_violation 11/11、workspace
**1358/0/3**、conformance **141/141**(L2-100 宣告純疊 io→⊥、101 真純宣告
→#pure、102 繭逃生→#pure)。對抗:內繭滿足外純(io 封→外純真)、`.%cause`
讀 ⊥ 白名單守。**增量**(僅顯式假純宣告變 ⊥;回歸掃描全樹無既有此形;
opt-in 實務非破壞)。掛帳:runPure+特權(§4.3)、`#ext:`(§4.1)、CAID 全集
參與(§4.1)、下宣告。零代修累計 +1。工單
`nlang-tools/docs/effect_violation_handover.md`。

**引擎 v0.2.36 定版(2026-07-24)=增量**:top `fac9376`(squash 效應系統波
arc 3〔effect_violation〕+ oo 0.2.36 bump+lock 同入),tag 於實測 commit
(workspace **1358/0/3**、conformance **141/141**、effect_violation 探針 11/11
皆於候選重測;條件閘一次成功;tag 後 touch build.rs 重建 `oo --version` =
`oo v0.2.36` ✓)。dev tie-back `a4e9319`。**增量**(僅顯式假純宣告 → ⊥,
opt-in 無既有用例;§4.3 落實)。前版 v0.2.35=`c4b4c4b`。

**效應系統波 arc 4:~%Effect./runPure + 特權(2026-07-24,裁定 P1,一件驗收
代修)**:落地 SPEC_08 §4.3 masking/handlers 兩半之 runPure(§6.2 #effect_override)。
**裁定 P1(使用者):特權 = horizon 能力位**(`EvalContext.privileged`),**只經
可信程式外通道建立**(CLI `oo run/eval --privileged`)——程式內無法自授權
(§6.1.2 無後門);token 字串屬 REAL_02,語言只見布林能力。runPure:特權 →
force + `purify_effects`(遞迴活動→Pure);非特權 → `_|_ %cause #privileged_required`。
逃生門仍=繭壁(非特權)。交付 `5b35303`:Ouroboros/EvalContext.privileged +
`~%Effect./runPure` + `BottomCause::PrivilegedRequired` + CLI 旗標;能力位僅
main.rs CLI 設(安全核心守)。CAID 不動(觀測投影)。**驗收代修 `b43eb52`**=
arc-3×arc-4 縫:`predict_effect` 對 `~%Effect./runPure X` 過度近似 arg 之 io,
致 `{ %effect:#pure, v: runPure(io) }` 誤觸 arc-3 守護 ⊥;修=callee 為 runPure
時 predict 回 Pure(雙面皆真;正典 callee 語法偵測,別名掛帳)+ 縫釘。探針
A 6/6 + B 6/6(含代修釘)、workspace **1370/0/3**、conformance **142/142**
(L2-103=非特權 runPure→⊥)。**特權路徑無合規向量**(runner 無 --privileged),
CLI 探針為法定測具。**增量**(純增能力,未宣告 io/一般值不動)。掛帳:別名
callee predict 保守、#pin+其餘 §6 特權操作(#commit/#rollback/#squash,同能力位
基建)、commit 層審計(§6.1.3)、token 驗證+線程隔離(REAL_02)、`#ext:`(§4.1)、
CAID 全集參與(§4.1)。零代修累計不變(本弧一代修)。工單
`nlang-tools/docs/effect_runpure_handover.md`。

**引擎 v0.2.37 定版(2026-07-24)=增量**:top `aa1eb8e`(squash 效應系統波
arc 4〔effect_runpure + 驗收代修〕+ oo 0.2.37 bump+lock 同入),tag 於實測
commit(workspace **1370/0/3**、conformance **142/142**、runpure 探針
6/6+6/6 皆於候選重測;條件閘一次成功;tag 後 touch build.rs 重建
`oo --version` = `oo v0.2.37` ✓)。dev tie-back `bda4d01`。**增量**(純增
`~%Effect./runPure` + `--privileged` 能力;未宣告 io/一般值不動)。CAID 不動
(觀測投影)。前版 v0.2.36=`fac9376`。

**效應系統波後續弧:`#ext:` 降級(2026-07-25,裁定 A,spec-only,引擎零變更)**:
掛帳自 arc 1 起四弧的 `#ext:`(§4.1)結案——**不建,降級**。量測四項:
(1)**無分辨性消費者**——§4.1 原文對 `#ext:` 唯一規定語義是「視為非純粹」,
與任何活動標籤同義;無物在識別碼**身分**上分派,因 n/ 無使用者自訂 handler;
(2)**非新障礙種類**——四基礎標籤分類的是全域截面**如何**失敗(外部座標/
給定 frame 仍不定/commit 流位置/已截斷),而 `#ext:file_write` 與
`#ext:db_query` 同屬 `#io`,差別僅**出處**,出處屬審計關切(REAL_02)非格元素;
(3)**CAID 跨引擎矛盾**——SPEC_08 §4.1 要求 `%effect` 入 CAID,REAL_03 §7 嚴禁
非標準 `#ext:` 納入,推到底為真衝突(有該邊界 builtin 的引擎 A 與無的引擎 B
對同節點算出不同 CAID);結構同 B5/R1 弧將 `%predicate` 判出核心 → R2 帳
(跨引擎自訂詞彙);(4)**成本高**——`#ext:foo` 今日不 parse(tag 文法不含 `:`,
實測三式皆 Parse Error),且 `EffectTag` 為 `Copy` 的 u8 bitset,無界字串標籤
逼其改 heap set → 失 `Copy`(~480 呼叫點)並打破 arc 1 死守的 `to_serial_byte()`
CAID 穩定映射(arc 1 紅線)。**裁定 A(使用者)**:降級為**引擎本地 provenance
標籤**,非核心格元素;引擎**得**(非必須)附加,不行使者完全合規。三條:
語義貢獻僅「活動」一位(等同依附的活動標籤,預設 `#io`;不得在識別碼上分派
語義);識別碼**不入 CAID**(正式消解 §4.1×REAL_03 §7 矛盾——入者為核心標籤
集合與活動語義位,§4.1 目的〔不純不得偽裝 `#pure`〕完整保存,僅出處相異者
不產生 CAID 位移);顯示歸 **SPEC_11 §3.4 診斷註解層**(`.%effect` 回報依附
標籤,識別碼不得為語義資訊唯一載體)。spec closure:SPEC_08 §4.1(主裁 + CAID
參與範圍釐清)、REAL_03 §7(排除理由 + 交叉指標)、SPEC_11 §3.4(法定成員增
`#ext:` 識別碼)、CHANGELOG 編輯性。**引擎零變更**(現不行使此許可),故無探針、
無合規向量、無四數重測義務、不切版。掛帳去除一項。**下一個有內容的效應弧
= 選擇性 discharge(特權由 bool 升為效應格:此 horizon 獲授權固定哪些觀測
座標)**——它以四基礎標籤即成立,不需 `#ext:`;`#ext:` 僅為其更細粒度細化,
依賴單向。相關:討論 023(docs/discussion/023,超專案 top `5cdd2c4`)。

**選擇性 discharge:特權能力格(2026-07-25,裁定 Q1+Q2,零代修第 26 例)**:
落地 SPEC_08 §6.1.4(新設)+ §4.3(增訂)。**裁定 Q1(兩軸複合)**=特權不是
布林而是**格值**:軸一 = §6.2 五操作各自授予(授一不蘊含其他),軸二 =
`#effect_override` 之能力再攜**效應標籤集**;`pin`/`commit`/`rollback`/`squash`
為**已宣告但惰性的槽**(接受儲存,尚無消費者;日後各弧填槽,不必再動能力位
形狀)。**裁定 Q2(全有全無)**=能力集 C、force 後活動效應 E:`C ⊇ E` → 固化
`#pure`;`E ⊄ C` → ⊥ `#privileged_required`,**不做部分 discharge**(名為
runPure 者絕不得回傳非純值)。交付 `cea0eda` 零代修:`Privilege{effect_override:
Option<EffectTag>, pin, commit, rollback, squash}`(Copy)+ `union`/`may_discharge`
+ `EffectTag::active_part()`;`run_pure` **兩軸閘**——軸一在 **force 之前**
(`effect_override.is_none()` → ⊥ 不 force,精確保住 arc-4「無授權時純參亦拒
且不觸發副作用」),軸二用 **force 後的實際效應**(不用 predict,因過度近似會
偽拒;且 force 後才拒不外洩能力——未授權程式本來就能直接跑 io);CLI `--grant
<SPEC>` 可重複、union 累加,`--privileged` 保留為全授墊片(語義不變)。
**驗收(零代修)**:diff 純度 ✓(探針僅移 9 個 `#[ignore]`);**安全核心 P1** ✓
(能力寫入僅 `apply_cli_privilege`,由 run/eval 兩處呼叫;builtin 只讀作閘;
無 n/ 欄位/`~%Config`/態射自授權路徑);四數 ✓ 探針 **15/15**、workspace
**1385/0/3**、conformance **142/142**(不變)、genesis **11/11**,前四弧效應探針
全守(union 15/cached 11/violation 11/runpure 6+6)。**對抗 16 例全過**:arc-3×
本弧縫(宣告純 combo 內 runPure 於不足能力下——惰性面讀 `.%effect` 得 `#pure`
〔predict 回 Pure,v 未 force〕、**固化面**強制 `.v` 正確得 ⊥ 並列出「may
discharge #io but the value observes #io | #nondet」,兩面皆真,守護未誤觸)、
空活動集覆蓋(純參在窄 `{state}` 授權下正常 discharge=`#cached` 同路徑,
`active_part` 生效未誤拒)、軸一保序(僅授 `pin` 時純參仍 ⊥)、CLI 邊界
(空標籤列/未知標籤/未知 SPEC 皆大聲死且訊息含原字串;重複標籤冪等;
`--grant`+`--privileged` union)、eval 子命令同通;**CAID 不受能力影響**
(同程式跨不同授權 `--format` 輸出逐位元相同)。**增量**(`--privileged`
語義不變,既有程式零影響;新增的是更**窄**的授予)。spec closure:SPEC_08
§4.3+§6.1.4、TAG_REGISTRY(`#privileged_required` 兩種拒絕模式)、CHANGELOG 增量。
**本弧無新增合規向量**(runner 不傳能力旗標,CLI 探針為法定測具,同 arc-4)。
工單 `nlang-tools/docs/selective_discharge_handover.md`。掛帳:`#pin`+其餘 §6
操作**本體**(能力槽已備)、commit 層審計(§6.1.3)、token 驗證+線程隔離
(REAL_02)、能力對程式可觀測性(維持不可觀測)。

**引擎 v0.2.44 定版(2026-07-27)=增量**:top `e3376fc`(squash 對等取用位址驗證弧
〔含兩件驗收代修〕+ oo 0.2.44 bump+lock 同入),tag 於實測 commit(workspace
**1475/0/3**、peer_fetch 探針 **12/12**、cas **13/13**、store_boundary **20/20**、
conformance **143/143**、genesis **11/11** 皆於候選重測;條件閘一次成功
`GATE OK: repo=nlang-tools branch=top head=e3376fc`;tag 後 touch build.rs 重建
`oo --version` = `oo v0.2.44` ✓ 無髒尾,`git describe --exact-match` = v0.2.44)。
dev tie-back `1f06d55`(dev/top 內容一致驗畢)。**增量**:**位址零位移**——對 v0.2.43
二進位對跑 **25 種值形狀 0 位移**(含 7 種攜 ⊥ 之值),genesis 種子穩定
〔**更正 2026-07-27**:原記「全語料 143/143 逐字相同」係空洞量測,見弧紀錄末〕;觀測面
變動僅及**持有不可認證位元組之來源**(原壓平為 `#conflict` 或靜默略過 → 具名
`#caid_mismatch` 且裁決浮現),純粹缺席語義不變。前版 v0.2.43=`e217d3a`。

**引擎 v0.2.45 定版(2026-07-27)=破壞性(Layer 1),破壞性條目 #4**:top `fe5d4d1`
(squash 引擎不再鑄造治理根弧〔含一件驗收代修〕+ oo 0.2.45 bump+lock 同入),tag 於實測
commit(workspace **1487/0/3**、universe_determinism **12/12**、peer_fetch **12/12**、
cas **13/13**、store_boundary **20/20**、conformance **143/143**、genesis **11/11** 皆於
候選重測;條件閘一次成功 `GATE OK: repo=nlang-tools branch=top head=fe5d4d1`;tag 後
touch build.rs 重建 `oo --version` = `oo v0.2.45` ✓ 無髒尾,`git describe --exact-match`
= v0.2.45)。dev tie-back `2981d65`(dev/top 內容一致驗畢)。
**破壞面**(三項,已於 CHANGELOG 逐條列):`~%Official.architects` 自語言表面移除
(→ `⊥ #missing_key`);新建宇宙根 CAID 與舊引擎所產者不同(惟舊引擎每次所產本就互不
相同,無人能依賴);空白名單之新倉庫 `#refine` 不再要求 `--sign`。**不受影響**:一般值
CAID(**25 種形狀 0 位移**含 7 種攜 ⊥ 之值)、genesis 種子、既有倉庫(v0.2.40/v0.2.43
所建者實測讀取/驗證/續提交皆正常)。**核心結果**:8 行程 8 新倉庫同源 ⟹ **1 個根 digest**
`6ef56ffc…`。**本條啟動 ORDER_00 §5.1.4 之 90 天穩定時鐘判定。** 前版 v0.2.44=`e3376fc`。

**引擎不再鑄造治理根弧(2026-07-27,裁定 A/B/C,**一件驗收代修**,SPEC_13 §4.1.2 義務 #3 新設 + SPEC_10 §93 補兩條;**破壞性條目 #4**)**:
**承重量測**:同一份原始碼、6 個新倉庫、6 個行程 ⟹ **6 個不同的根 CAID**;對照(一般值)⟹ **1 個**。
窮舉兩根全部葉節點:**2,588 條路徑,恰好 1 條不同** = `~%Official.architects`
= `hex(Identity::new_random().public_key)`,每次 `Ouroboros::init` 現鑄、由 `root_with_system()` 寫進宇宙。
**雜湊沒錯,內容真的不同——錯的是一個隨機數是宇宙的一部分。**
**比隨機數更嚴重**:ORDER_01 §117 定其為信任根、Voter **集合**,§88 定只經 RFC 變更,SPEC_10 §93 定
refine signer 必在其中;引擎鑄的是**字串**、**本地隨機自任**、**行程啟動**時。`~%Official` 不在 SPEC_13
§3.1 種子清單內,亦無 ORDER_01 §46/§91 之 `blacklist`。同鑰又入 `architect_registry` ⟹ refine 要 `--sign`
而 `--sign` 永遠成功 ⟹ **權威檢查被自任滿足 = 會說謊的審計面**。**引擎在本地鑄造全域治理物件的贗品
並自任為唯一成員;CAID 不決定只是症狀。**
**裁定 A**=`architects` 退出根(斷言層)。**裁定 B**=不再自任 ⟹ 空 registry ⟹ 創世豁免 ⟹ refine 免簽
(**實質放寬且是誠實的那個**:原拒絕所要求者僅為同一行程永遠開得出的簽章)。**裁定 C(我方推論)**=
未驗證必須留痕,且**空白名單下即使附有效簽章亦記為未驗證**(無可比對之集合時,簽章證明「某人簽了」
非「有權者簽了」)。**落點由量測決定**:`Commit::content_hash` 僅雜湊 `RefineInfo` 之 source/target digest
⟹ 落 `RefineInfo` **既有 commit CAID 零位移**;**不得**落 `CommitMeta`(其 `Debug` 入雜湊,而其位元穩定
至今僅賴一個**手寫 `Debug`** 在 `abandoned` 為 `None` 時省略該欄——**此前無測試釘住**,本弧 R7 補釘)。
**交付**:`db01d24`(+`4456e17` 交付紀錄);diff 純度合格(探針僅少 7 個 `#[ignore]`;工單與探針檔頭另有
**驗收方自己的修訂**夾帶其中,責任在驗收方——見下)。
**四數**:workspace **1487/0/3**、universe_determinism 探針 **12/12**、conformance **143/143**、genesis **11/11**。
**位址**:新建宇宙根 **8 行程 8 倉庫 ⟹ 1 個 digest**(`6ef56ffc…`);一般值對 v0.2.43 二進位 **25 種形狀
0 位移**(含 7 種攜 ⊥ 之值);genesis 種子穩定;**跨版實測** v0.2.40 與 v0.2.43 所建倉庫皆讀取/驗證/續提交
正常。**A/B**:探針搬回 v0.2.44,7 紅仍全紅、5 pin 仍全綠。
**對抗實測**:未簽 refine → `unverified`;**已簽** refine 於空白名單 → 仍 `unverified`(誠實);`oo log` 顯示;
白名單**不含你** + `--sign` → **拒絕並指名簽署者**(權威檢查第一次真的會失敗);白名單不含你且未簽 → 拒絕。
**驗收代修一件**:`oo log` 新增之權威行用 `if let Ok(commit) = get_commit(…)`,即 §6.6 條款四所禁之丟棄裁決
形狀,亦即 v0.2.44 整弧清掉的那個;**經判定為潛伏非活躍**(`engine.log()` 已於數行前以 `?` 讀過同一 hash,
第二次不可能失敗),仍修——形狀會被下一次重構繼承,而 `log()` 一旦變惰性即刻轉為活躍。
**ORDER_01 §66 不適用之理由**已寫入 SPEC_13 §4.1.2 義務 #3:被移除者是本地**合成**的同名偽造品,規格所定
之 `~%Official` 為**經發現取得**的全域治理物件,本地引擎從未持有。
**過程事故(驗收方)**:交付飛行途中我以 `git add -A` 提交工單修訂,把 #3 進行中的成果掃進一個訊息只描述
文件變更的提交;以 `reset --soft` + `reset` 撤銷,工作樹一字未動,#3 隨後自行乾淨提交。**常設紅線新增:
交付進行中絕不 `git add -A`,只提交逐一指名的檔案。**
**掛帳(已排序)**:A 是**身分持久化的前置而非對手**(A 後身分不在根裡,持久化不再影響定址)→ 操作者帶外
宣告(**REAL_01 §7.2 `~/.oo/authorized_keys`,引擎完全未讀**,亦無令牌生命週期/CRL)→ 第一個可能失敗的
權威檢查。**冷啟動規格已有兩解而引擎二者皆未用**:憲政(ORDER_00 創世精煉清單 + §93 `Epoch < 0`)、本機
(REAL_01 §7.2);引擎自創第三種,而該種正是 SPEC_08 §6.1.2 裁定 P1 所禁之自授,低一層。
**其餘掛帳**:既有宇宙遷移;紀元模型;`~%Official.blacklist`;architects 成為真正的 Voter 集合;
儲存量三件(縮排 3.3×、創世重複 77KB、遞迴型別 2KB 常數)。

**符合性觀測:節點金鑰路徑之正規化(2026-07-28)**:工作區自 `/mnt/d/Workspace/ai_ai/nlang`
搬至 `/home/gali/nlang`,原處留下指向新址之符號連結。實測兩條路徑得到**同一個** `node_id`
(`…:2a5995079361e9bb…`),且金鑰檔名 `1b0fb28744abfc8c…` 等於 `sha256("/home/gali/nlang")`
——即 `sha256` 之**解析後**絕對路徑。**現行引擎已滿足** REAL_02 §4.1.1 新補之正規化要求。

> 該要求本身(符號連結、`.`/`..`、重複分隔符須於導出身分前解析)寫在 REAL_02 §4.1.1,
> 連同其理由(兩個名字不是一份複本)。**此處只記「這一版的引擎做到了沒有」**——
> 符合性屬本檔,義務屬規格。混寫的實害是:另一個引擎的實作者會在規範條文的位置上
> 讀到一句關於**別人家引擎**的陳述,而那句話還會過期。
> (可對照:規格中留下的量測皆為**論證性**——§4.2.3 的「求值早於檢查」與 §4.3.5 的
> 67.1 MB/143 MB,拿掉之後那兩條 MUST 就只剩斷言。)

**引擎 v0.17.1 定版(2026-08-10)= D1 弧,引擎 patch,規格不動**:top `82fd10d`
(squash nesting_doubles 弧 + oo 0.17.1 bump;故事提交
**"Every level of nesting doubles the universe"**)。
squash 後先驗樹逐位元等同 dev(`fce973a8`)才提交;tag 於實測 commit
(workspace **1849/0/3**、conformance 143/143、genesis 11/11 皆於候選上重測)。
dev tie-back `fc6d333`。

**版號位階的判定**:VERSIONING §2 明文「**引擎 patch ＝ 引擎自己的 bugfix／效能,
與規格 patch 無對應義務**」。本弧零規格變更、零語義變更、非破壞性
(v0.17.0 的倉 root 逐位元不變,已實測 `7cbf0865…`)⟹ **走 patch,規格側不切版**。

**這一版的引擎做到了沒有**(符合性,非義務):

* 巢狀 combo 的求值代價由 **2^depth** 降為約 **n²**。
  實測:nest=16 由「不會結束」→ 0.072 s;nest=100 → 0.688 s;
  nest=14 峰值 RSS 由 **503,684 KB** → **22,384 KB**(22×)。
  成因:`seal_defining_scope` 把整個 combo 深複製為 frame 並塞進每個 thunk 的閉包,
  而第 n 層的 frame 已含第 n−1 層塞入者 ⟹ 每層加倍。frame 現以參考計數共享。
* **止於 n² 不是線性**——frame 複製仍會複製該層自身的結構。已寫入交付文件,
  避免日後被誤讀為線性。
* `~%Config.timeout` 於任意深度皆可終止觀測(探針 R4)。

**代修一件,記其類別**:首次交付為了讓循環偵測維持便宜,把鍵改成
**frame 的配置位址**(`Arc::as_ptr`)。結構相同而各自配置的兩個 thunk 因此不再認出再入,
87 層以上引擎不再回應操作者設定的 `timeout`——**牆搬走了,新牆沒有門**。
量測:n=88 配 `timeout: 3000`,代修前退出 0(5.0 s),交付後 150 秒未結束。
**位址是情境不是內容**,正是本倉四天前對 span 與鹽所裁定的同一件事
(SPEC_01 §2.4.1 禁止條明列記憶體位址)。循環鍵已改為內容導出,53 支既有循環守衛全綠。

**仍在前方的一道更老的牆**:約 **140 層**原生堆疊溢位,行程 abort 而非回報
(130 ok / 140 abort;`~%Config.timeout` 無效)。**既有缺陷**——同一 fixture 於
v0.16.0 與 O42 兩支二進位皆 exit 134,只是先前被指數與掛死擋著走不到。
**違反 TAG_REGISTRY §2.7.3 第一條 MUST**(實作上限須嚴格小於原生天花板,方能回報)。
列為下一弧的正面。

**引擎 v0.17.0 定版(2026-08-10)= O42 弧,破壞性**:top `71cc709`
(squash snapshot_not_a_reading 弧 + oo 0.17.0 bump;故事提交
**"A snapshot is not a reading of the ruler"**)。squash 後先驗樹逐位元
等同 dev(`8ddd1d7a`)才提交;tag 於實測 commit(workspace **1841/0/3**、
conformance 143/143、genesis 11/11 皆於候選上重測)。
dev tie-back `2ffdb78`,merge-base 已前進且兩支樹相同。
規格同步切 `v0.17.0-draft.1`。**破壞性條目 #11**,90 天時鐘自本日重啟。

> **壞檔檢查的方法更正(2026-08-10)**:v0.14.0 之後把「檢查 `target/debug/deps`
> 有無壞檔」列為切版步驟,本次首度以 ELF magic 實作,**結果幾乎每個檔都被誤報**
> ——`.rlib` 是 `ar` 封存(`!<arch>`)、`.rmeta` 是 rustc 中繼資料(`rust\0\0\0\n`),
> 本來就不是 ELF。當初的壞檔特徵是**整檔全零**,判準應為「大檔而檔頭全零」,
> 不是「不是 ELF」。已改正並實測:零命中。

**O42「一個快照不是那把尺的讀數」弧驗收(2026-08-10)**:
交付 `990cf9f`,代修 `eb722f4`,開弧 `6f2f73b`,基線 `ba10853`(v0.16.0)。
**破壞性條目 #11。**

**量測**:探針 15/15、重複 ×5 全同、workspace **1837/0/3**、conformance 143/143、
genesis 11/11。

**這一版的引擎做到了沒有**(符合性,非義務):

* REAL_03 §7.3 六項強制參數:**做到**。此前六項到齊零項——`node_content` 缺、
  `%fuel` 放的是剩餘量、`max_branches`/`max_unification_depth`/`max_pattern_nodes`
  三項缺、且放了一個 §7.3 明文禁止類別的輸入(時鐘鹽)。
* §7.3.2(局部結果以 CAID 入 CHS):**做到**,且本節條文是由這次代修導出的
  ——見下方「第一次交付」。
* SPEC_08 §3.2.2 #6(a) 可達性:**做到**。實測 `p == q` 於兩個逐字相同的 `#blur`
  上回 `#true`;此前該款自 2026-07-14 訂立以來從未可達。
* SPEC_01 §2.4.1 第 5 項新鍵:**做到**(cause, 策略, CHS 摘要)。
* SPEC_03 §90「原樣」含 `partial` 不被改寫:**做到**。
* **REAL_03 §7.3 記錄集合的正準序(R-6 / O46):代修 M4 後做到**。
  實測(控制已武裝:A 單獨 `d0967392…`、B 單獨 `e3d8e76a…`,兩側非空且相異;
  合併結果與兩者皆不同 ⟹ 合併確實發生):`A & B` ＝ `B & A` ＝ `72c635e0…`。
  M4 之前為 `7967db7f…` / `c64f900f…`,不交換。
* **REAL_03 §7.4(原始碼位置不入身分):做到**,且本節條文由 M4 導出。
* REAL_04 §4 `#blur` 之 `%cause` 投影:**做到**(單一標籤;兩序皆
  `#max_depth_exceeded`)。

> **⚠ 驗收方診斷更正(2026-08-10)**:上一版本檔案曾記「未達成,成因是 CHS 把主記錄
> 與 `co_horizons` 分開餵」。**那個成因是錯的**——記錄集合本來就已正準排序;
> 真正的成因是 **`Value::Code` 的雜湊含 span**:`format!("{:?}", expr)` 把原始碼
> 位置烘進了局部結果的摘要,而 `A & B` 與 `B & A` 之中 A、B 落在不同的位元組偏移上。
> 我讀了結構就下診斷而沒有量到 span 這一層。**留下這筆,因為一個被更正的診斷
> 比一個被悄悄換掉的診斷有用。**

**破壞面在 M4 之後比原先宣告的更廣**:§7.4 使**任何持有程式碼值的宇宙**根 CAID 移動,
不限於含 `#blur` 者。跨 M4 實測:純值宇宙 `4c45e486…` **不動**;
含態射者 `ba89a8a9…` → `5529bc46…` **動**。驗收方的 P3 釘看不到這件事
(其 fixture 不含程式碼值),已新增 P5 釘住正確的邊界。

**破壞面(條目 #11)**:每個 `#blur` 的 CAID 與每個含 `#blur` 的 root CAID 皆移動。
雙向實測(控制已武裝:舊引擎讀舊倉正常):新引擎讀 v0.16.0 舊倉 **正常**;
舊引擎讀新倉 **`#object_undecodable`,訊息為 "present but cannot be decoded
(integrity unknown): missing field `salt`"** ——具名、說得出為什麼、不當機、
且未謊稱完整性受損。

**須記的兩件事**:

1. **合一側的那些 CAID 在此之前本來就是隨機數。** 鹽只有一個呼叫點(evolve 路徑),
   所以 `#fuel_exhausted`(observe 期鑄造)可重現而 `#max_depth_exceeded` 不可
   ——**一個 blur 有沒有身分,此前取決於它是被哪一種資源攔下的**。本弧不是
   「弄壞了可重現性」,是把隨機數換成穩定值。
2. **第一次交付曾重新打開 v0.16.0 剛關上的當機路徑。** 為了讓內嵌的局部結果讀得回來,
   它關掉了 serde 的遞迴守衛;A/B 實測(同機同時同 fixture)交付前 12000 項退出碼 0、
   交付後 8000 項起 SIGABRT。成因量測:`.oo/staged` 的 JSON 深度由**與程式大小無關的 10**
   變成**線性成長**(5000 項時 14,917 層 / 591,432 B,約 900 倍)。
   代修改為「局部結果以 CAID 入身分、本體於 evolve 落 CAS」後,深度回到固定 10、
   大小為 +177 B 常數,守衛得以留著。**§7.3.2 即由此導出。**

**引擎 v0.16.0 定版(2026-08-09)= W4‴ 弧,破壞性**:top `3783fd5`
(squash a_limit_you_cannot_choose 弧 + oo 0.16.0 bump;故事提交
**"A knob is an interface, not a hand grenade"**)。squash 後先驗樹逐位元
等同 dev(`a544e6d4`)才提交;tag 於實測 commit(workspace 1822/0/3、
conformance 143/143、genesis 11/11 皆於候選上重測,且先驗過 deps 無壞檔)。
規格同步切 `v0.16.0-draft.1`。**破壞性條目 #10**,90 天時鐘自本日重啟
(距 #9 同日——W4′ 與 W4‴ 在同一天,深水期的正常代價)。

**W4‴「一個你選不了的上限」弧驗收(2026-08-09,尚未切版)**:交付 `89c7f49`,
開弧 `47d7b50`,基線 `d61d010`(v0.15.0)。**破壞性條目 #10。**

**量測**:探針 10/10、重複 ×5 全同、workspace **1822/0/3**、conformance 143/143、
genesis 11/11。**對抗**:`max_unification_depth` = 401／10000／**4294967295**
配 8000 項鏈,**退出碼全為 0**;硬界回報 `_|_ (%cause: #stack_overflow)`
——自己的名字、⊥ 而非 blur。`HARD_RECURSION_LIMIT = 400`(實測 488 安全／499 dump core)。
**跨版本**:新引擎讀 v0.7.0 的倉,commit CAID 相同、根解得開、值印得出。

**⚠ 探針完整性違規(交付方)**:交付**自行改了三個釘的期望值**
(`aa1b70f7…`→`8698d297…` ×2、**`6e8eae8b…`→`16ba5683…`**),
並改寫三支既有測試(其中一支斷言被反轉)。**內容全部正確,但探針修改權在驗收方**,
而工單 §7 明文寫著「回報,不要自行改」。

**根因在工單(驗收方)**:我寫了「破壞性:否」,並把 P1 釘在一個 **O41 使其不可能滿足**
的值上——留著那個釘,交付**必然**失敗。與 W4′ §7 同型,差別是那次我事先給了逐項授權。
**處置**:值保留(已獨立驗證:同一份 `x: 1` 連建三倉,根皆 `8698d297…`),
三個釘的**註解由驗收方改寫**,把機制寫進去
(系統軸 → CAID → 改一個創世預設就移動每一個根),
而不是只寫「recalibrated after O41」——**一個沒有說出為什麼會動的釘,下次還是會被人靜靜地改。**

**驗收方最該記住的一條**:W8′ M2 的原文就是「引擎多一個內建 ⟹ 過去每一次提交的根 CAID
都會移動」,我還補了「這是下一次新增內建的風險」。**改一個創世旋鈕的值是同一個機制。**
我在同一天量過、寫過,然後在下一張工單裡宣告「不動任何 CAID」。
**帳本裡有的東西沒有被讀回來——不是量測不足,是量測沒有被使用。**

**規格收尾(驗收方)**:TAG_REGISTRY **§2.7.3 新設**並**更正 §2.7.2**;
`#stack_overflow` 已登記(§1.2,載體 ⊥,48 個);SPEC_09 §6 旋鈕表新增
「可設 `#_`？」欄、`timeout` 預設改 `#_`;§6.0.2 增兩條 MUST NOT。
反向盤點由 3 降為 **2**(只剩兩個刻意廢止的)。

**⚠ v0.15.0 已出貨一個當機路徑(2026-08-09 W4‴ 偵察發現,由 W4″ 引入)**

`~%Config.max_unification_depth` 在 W4″ 之後**在演化期真的生效**了。
副作用:**操作者把它調大就能讓引擎當掉**。

| 量測(5000 項加法鏈,`oo evolve`) | 結果 |
| :-- | :-- |
| 預設 `256`(**控制**) | 退出碼 **0**,`#blur { %cause: #max_depth_exceeded }` |
| `488` | 退出碼 0 |
| **`499`／1000／2000／4000／100000** | **退出碼 134(SIGABRT)** |
| 1000 項鏈 + `depth: 900` | **退出碼 134** |
| **v0.7.0**,`depth: 4000`(**歸因控制**) | 退出碼 0 ⟹ **W4″ 之前不會當** |

⟹ 原生堆疊約撐 **~490** 層本求值器的遞迴,而**預設 256 剛好坐在它的一半**。
**旋鈕失效時這件事不可能發生;旋鈕一生效,它就是操作者按得到的當機鈕。**
當掉時**沒有 `⊥`、沒有 `#blur`、沒有訊息**——比視界嚴格地差。

**驗收方的責任**:W4″ 的對抗量測只**調小**旋鈕、或在安全區間內做兩點判別
(16 vs 300,兩者都在 490 以下),**從未把它調大**。
「讓一個上限旋鈕生效」的對抗面,第一項就該是**把上限拿掉會怎樣**。

**引擎 v0.15.0 定版(2026-08-09)= W4″ 弧,增量**:top `4586223`
(squash a_knob_that_does_nothing 弧 + oo 0.15.0 bump;故事提交
**"A knob that changes nothing is worse than no knob at all"**)。
squash 後先驗樹逐位元等同 dev(`e3fd4b6b`)才提交;tag 於實測 commit
(workspace 1812/0/3、conformance 143/143、genesis 11/11 皆於候選上重測,
且**先驗過 `target/debug/deps` 無非 ELF 壞檔**——見 v0.14.0 切版的教訓)。
規格同步切 `v0.15.0-draft.1`。**非破壞性**。

**W4″「一個不做事的旋鈕」弧驗收(2026-08-09,尚未切版)**:交付 `86efa7d`,
開弧 `4211a47`,基線 `9cff223`(v0.14.0)。**零代修。** 非破壞性(P1 根 CAID 不動)。

**量測**:探針 10/10、重複 ×5 全同、workspace **1812/0/3**、conformance 143/143、
genesis 11/11。commit 實測輸出:
`note: ~%Config was not committed (horizon parameters stay staged as session state)`。
**P2 從空過變成真的在比對**:有 `~%Config` 那側的根 = `aa1b70f7…`,與無者相同。

**§6.3 那個數字是零,而工單說零本身要解釋(交付未回報,驗收方補)**:
1807 → 1812 恰好 +5,**沒有任何既有測試改變行為**。原因:全 workspace 會**設定**
旋鈕的只有 `config_validation_probe_test`(23 處全在驗證壞值被拒)與
`system_axis_probe_test`(2 處)。**沒有人依賴「上限不生效」——也沒有人在測它們**,
這正是五個旋鈕能長期失效而無人發現的原因。

**驗收方偵察有一處太寬,已更正**:我把 `max_unification_depth` 記為平坦的
「不生效」。實測(交付前後皆然)**combo 合併路徑一直 respect 旋鈕**——
`depth: 2` → `#max_depth_exceeded`、`depth: 64` → 收斂,而那正是 **W4′ 探針
R1/R2/C2 的形狀,它們在 v0.14.0 就是綠的**。**反證躺在上一弧自己的探針檔裡。**
真正的缺陷是「求值路徑不 respect、unify 路徑 respect」。
**方法論**:兩點法控制的是「這個輸入有沒有碰到那道閘」,**控制不了「有沒有
另一條路徑會碰到」**;一個旋鈕一個 fixture 得出的「不生效」是**關於那條路徑的**。

**符合性殘留(→ W4‴)**:
(a) **暫存只剩 `~%Config` 時 `oo commit` 會鑄空提交**——兩次提交的根皆
`aa1b70f7…`,各鑄一個 commit 物件。**本交付引入**,而**工單 R4 未涵蓋
「只有 Config」的情形,缺口在驗收方**。
(b) ~~磁碟上的 `~%Config` 在新行程不生效~~ **⚠ 本條錯誤,同日撤回(2026-08-09)**。
重測:暫存 `max_unification_depth: 8` 後,**新行程** `oo evolve` 一條 200 項加法鏈
得 `#blur { %cause: #max_depth_exceeded }` ⟹ **旋鈕跨行程是生效的**。
原依據不成立,因為 **`oo run` 根本不載入這個倉**——提交 `y: 5` 之後
`oo eval 'y'`／`oo eval '_.y'`／`oo run` 觀測 `_.y` **三者皆回 `_`**。
**我用一個看不見倉的指令去證明「倉裡的東西不生效」,而那個指令對任何倉裡的
東西都會給出同樣的答案。** 真正的待裁問題是「一次性求值器該不該看見倉」
(→ W4‴ (b′));附帶:`oo run` 沒有 `--load`,而 **REAL_01 §1.1 的用法行寫著它**。
(c) **`timeout` 只在明設時生效**——未設時創世的 `timeout: 1000` 未武裝,
實測 2144 ms 的運算跑完。交付明文說明理由(武裝它＝給每次 stdlib 觀測套上一秒的牆),
判為**合理的射程收窄**,但**記為「未完成」而非「已完成」**。

**一項刻意的不對稱**:evolve 套用 `max_branches`／`max_unification_depth`／
`max_lifting_depth`／`max_pattern_nodes`,**不套用 `fuel`／`strategy`**
(理由:於 evolve 套 fuel 會以 evolve 的 salt 鑄 `#blur`,移動燃料側 CAID)。
實測 `fuel: 5` 下淺算術照常算出 5。⟹ 已入 **SPEC_09 §6.0.2 的自陳缺口**。

**引擎已知未實作項(2026-08-09 掛帳,用戶裁定 O39)**:
`~%Config.max_lifting_depth` 與 `~%Config.max_pattern_nodes` **全樹從未被讀**
——宣告、預設、驗證、兩處賦值、旋鈕表俱全,消費點為零;
對應的 `#max_lifting_exceeded`／`#max_nodes_exceeded` 亦從未被鑄。

**裁定:不廢止,之後實作。** 用戶理由:廢止之前要先論證「當初的設計沒有必要」,
而那個論證沒有做;引擎本來就還有許多未實作項,這只是其中一個。
⟹ **規格側維持現狀**(旋鈕與錯誤碼都留在登記簿),**本檔記其為已知未實作**。
**不在 W4″ 射程。**

**W4″ 偵察:`~%Config` 七個旋鈕逐一量測(2026-08-09,引擎 v0.14.0)**

每個旋鈕都用**兩點法**——同一份輸入、兩個旗鼓相當的旋鈕值,看門檻是否移動。
只設一個值而「沒事發生」不算量測(那分不出「旋鈕無效」與「輸入沒碰到那道閘」)。

| 旋鈕 | 暫存後讀得回? | 生效? | 證據 |
| :-- | :-- | :-- | :-- |
| `fuel` | ✓ | **✓** | `5` → `#fuel_exhausted`;`100000` → `_` |
| `strategy` | ✓ | **✓** | 同輸入:`#strict` → `_\|_`;`#blur` → `#blur` |
| `timeout` | ✓ | **✗** | `timeout: 1`(毫秒)下,一個 **2286 ms** 的運算**正常跑完** |
| `max_branches` | ✓ | **✗** | 上限 `2`,分支算術 11 支**全部存活**(此即 `eval.rs:2043` 那道閘) |
| `max_unification_depth` | ✓ | **✗** | 二分臨界恆為 **256**(＝預設值),旋鈕設 8／64／256／4000 **皆不動** |
| `max_lifting_depth` | ✓ | **✗** | **全樹從未被讀**——只有宣告、預設、驗證、兩處賦值、旋鈕表 |
| `max_pattern_nodes` | ✓ | **✗** | 同上 |

**⟹ 七個旋鈕有五個不做事。** 其中兩個(`max_lifting_depth`／`max_pattern_nodes`)
連消費點都沒有——**寫入端俱全、讀取端為零**,與 W8′ M7 的 `legacy_fields` 同類。
對應的 `#max_lifting_exceeded`／`#max_nodes_exceeded`／`#max_branches_exceeded`
在 W4 盤點中亦為 `absent`:**旋鈕、閘、錯誤碼,三者一起不存在。**

**且七個旋鈕一個都提交不了。** `~%Config.<任何旋鈕>` evolve 成功、`oo commit`
**一律失敗**,訊息是裸的 `Error: Commit failed`(控制:同一個倉 `x: 1` 提交成功)。
⟹ **視界參數只能活在暫存區,活不過一次提交。**

**提交失敗的訊息是 W3′-a 那個缺陷的同一個實例,在提交邊界上**:
`universe.rs` 的 `commit` 對 `engine.unify(root, staged)` 只 match `Value::Combo`,
其餘一律 `Err(anyhow!("Commit failed"))`——**`BottomDetail` 整個被丟棄**,
沒有 cause、沒有座標、沒有錯誤碼。**這推翻了先前「W3′-b 阻塞於 W12」的判定**:
當時的理由是「合併型 ⊥ 在 evolve 邊界就被攔,不會到 commit」,
而這裡就是一個**到得了 commit 的 ⊥**,而且是使用者一寫 `~%Config` 就會撞到的。

**引擎 v0.14.0 定版(2026-08-09)= W4 ＋ W4′ 兩弧,破壞性**:top `1d9681d`
(squash the_name_points_at_the_remedy 弧 + oo 0.14.0 bump;故事提交
**"A resource boundary is not an attack"**)。squash 後先驗樹逐位元等同 dev
(`63351de5`)才提交;tag 於實測 commit。規格同步切 `v0.14.0-draft.1`。
**破壞性條目 #9**,90 天時鐘自本日重啟(距 #8 十日)。
W4 為純規格弧、無引擎交付,故與 W4′ 併入同一版。

**W4′「名字要指向補救」弧驗收(2026-08-09,尚未切版)**:交付 `feee5ee`,
開弧 `1d23f31`,基線 `72c5fa8`(v0.13.0)。**引擎側零代修。**
**破壞性條目 #9**(只動因深度耗盡而生的 `#blur` 之 CAID)。

**量測**:探針 9/9、重複 ×5 全同、workspace **1802/0/3**、genesis 11/11、
conformance **143/143**(語料六向量已由驗收方更新,見下)。
深度 blur 的 CAID 如預期移動 `6ebb46d7…` → `6b537130…`;
**燃料 blur 的 `e4dc016e…` 逐位元組不變**(釘 P2)——破壞面就是工單畫的那條線。

**交付比工單多做對一處**:`BottomCause::obstruction_degree` 的 `=> 3` 分支
也必須收新變體,工單未列,交付自己補上。連同 `as_tag`／`as_cause_combo`／
`oo/src/main.rs`,**一個新 cause 要改四處,而漏掉任何一處都不會有測試變紅**。

**驗收方的工單有兩處錯,根因記在工單側**:
(1) §7 的例外授權只列了 `semantic_eclipse_test.rs`,漏了 `disc_multihop_test.rs`
——**掃了鑄造點,沒掃測試裡的期望點**(與 v0.6.0「工單列舉漏兩個套件」同型)。
(2) 成功標準寫「反向盤點 3 降為 2」,但 §2.7.1 **明文允許保留讀取能力**,
列舉分支必須留著 ⟹ 盤點必然仍看得到它。**標準與自己的裁定衝突**;
正確的檢查是探針 R4(鑄造點 = 0),而它是綠的。

**規格側收尾(驗收方)**:合規語料六個向量的期望由 `#fuel_exhausted` 改為
`#max_depth_exceeded`——**它們原本編碼的就是這個缺陷**。其中 `L2-21`
需要用戶裁定才改,見 CHANGELOG「SPEC_08 §3.2.2 第 3 款改寫」。

---

**W4″(新開,尚未動工):`max_unification_depth` 這個旋鈕是壞的**

W4′ 的對抗量測抓到,**與本交付無關且早於它至少六個 minor**:

| 量測 | 結果 |
| :-- | :-- |
| 臨界值二分(`1 + 1 + …` 之項數) | **n=256 通過 / n=257 失敗**——正是預設值 |
| 設 `~%Config.max_unification_depth: 4000` | 臨界值**仍是 256/257** |
| 同一次執行讀回該旋鈕 | **4000**(寫進去了、讀得到、**沒有被用**) |
| 提交後再讀 | **256**(連值都沒存活) |
| v0.7.0 同一組量測 | **同樣忽略該旋鈕** ⟹ 先於 W4′ |

⟹ W4′ 使名字指向了**正確的**旋鈕,而**那個旋鈕不動**。
本弧的論旨(名字要指向補救)因此只兌現了一半。
`~%Config` 的其他旋鈕是否同樣不生效**尚未逐一量測**——W4″ 應先做這件事。

**W4 完成後的殘留(2026-08-09,引擎 v0.13.0)**:規格側已落 TAG_REGISTRY §0／
「軸·載體」欄／§2 逐載體索引／§2.7 兩則命名裁定,**引擎尚未跟上**。反向盤點
自 5 降為 **3**,且三者皆為刻意:

| 標籤 | 現況 |
| :-- | :-- |
| `#invalid_path` | 已廢止(2026-07-14),登記簿有注記無列;引擎保留讀取能力 |
| `#semantic_eclipse` | **§2.7.1 廢止**,引擎仍在鑄——**W4′** |
| `#stack_overflow` | **§2.7.2 決定不入登記簿**,引擎列舉仍有(不可達) |

**引擎待辦(W4′)**:(a) 路由跳數用盡改鑄 `#routing_budget_exceeded`;
(b) 深度耗盡改鑄 `#max_depth_exceeded` 而非 `#fuel_exhausted`;
(c) `#stack_overflow` 不再對外(其 variant 在 `BlurCause::as_bytes` 內進 `#blur` 的
CAID,**刪 variant 屬 fmt 紀律,不在 W4′ 射程**)。三者皆改變操作者看到的字串。

**`#incomplete` 的符合性事實**:規格保留該狀態(§3.2.1 給了它「不可內容定址」
這個硬理由),而**參考實作 v0.13.0 未實作**——`ObservationState` 有匯出、
`to_tag()` 有 `"incomplete"` 字串,但**全樹沒有任何一處建構它**。
`handle_resource_exhausted` 只有三支:Strict→`⊥`、Blur→`#blur`、Approximate→`#approximate`。
⟹ **規格描述的暫態在跑著的引擎裡不存在**;此為符合性缺口,不改規格。

**TAG_REGISTRY ↔ 引擎 標籤盤點(2026-08-09,引擎 v0.13.0;W4 偵察)**:
新增 `scripts/error-code-inventory.py`(唯讀,不改語料;自帶雙控制——
`#conflict` 必須判為 `enum`、一個假標籤必須判為 `absent`,控制失敗即中止)。

    python3 scripts/error-code-inventory.py --engine-src ../nlang-tools/crates

**它回答的是「引擎裡有沒有這個名字」,不是「引擎做得對不對」**,也不是
「引擎鑄不鑄得出來」——用戶 2026-08-09 明確如此界定射程。

| 判別 | 數 | 意思 |
| :-- | --: | :-- |
| `enum` | **22** | 出現在 cause 列舉的標籤對映(`BottomCause`／`BlurCause`／`TopCaused`) |
| `literal` | 5 | 以字串字面值出現在非註解程式行 |
| `comment` | 1 | 只在註解裡(`#recursive_lazy`) |
| `absent` | **33** | 四種形狀都找不到 |
| **合計** | **61** | TAG_REGISTRY §1 的表格列數 |

逐節 `absent`:§1.1 六、§1.2 五、§1.3 十一、§1.4 五、§1.5 六。

**反向(引擎列舉中而 TAG_REGISTRY 未收錄)= 5**:
`#h1_split`／`#h2_split`／`#invalid_path`(已廢止,有注記無列)／
**`#semantic_eclipse`**／**`#stack_overflow`**。

**判別強度的界線要說清楚**:`#incomplete` 被判為 `literal`,因為
`observation.rs:48` 有 `"incomplete"` 這個字串;但 `ObservationState`
**全樹沒有任何一處建構它**(`ObservationState::` 於該檔之外零命中)⟹
**「有這個名字」不等於「鑄得出來」**,而本盤點只答前者。

**三套 cause 詞彙表互不相同(這是 W4 的承重量測)**:
`BottomCause` 24 個(enum,封閉,fmt v2 append-only)／`BlurCause` 4 個
(3 固定 + 1 開放 `String`)／帶因 `Top` 為裸 `String`(實得 2 個)。
**三者交集只有 `fuel_exhausted` 與 `timeout` 兩個。**
`#stack_overflow` 只活在 `BlurCause`,`#semantic_eclipse` 只活在 `BottomCause`。
⟹ TAG_REGISTRY 把它們攤成一張 61 列平表,**表格的形狀宣稱了一種實作沒有、
規格也從未陳述的統一性**。

**引擎 v0.13.0 定版(2026-08-09)= W8′-a「印出來的東西要能被讀回去」弧,增量**:
top `e36706d`(squash print_what_can_be_read 弧 + oo 0.13.0 bump;故事提交
**"What the engine prints, it must be able to read"**)。squash 後先驗樹逐位元
等同 dev(`4f9ffa1e`)才提交;tag 於實測 commit(workspace 1793/0/3、
conformance 143/143、genesis 11/11 皆於候選上重測)。規格同步切
`v0.13.0-draft.1`。以下為該弧驗收全文。

**驗收(2026-08-09)**:
交付 `3dfdd1f`,開弧 `e6ba836`,基線 `6e8beee`(v0.12.0)。**零代修**。
規格側新增 **REAL_01 §1.3**(四條 MUST／MUST NOT ＋ 論證性量測 ＋ 自陳缺口),
並在 **SPEC_10 §2.2.1** 留下升格註記。**新增規範條文 ⟹ 語義變更 ⟹ 走 minor**。

**符合性紀錄(此弧引擎做到了什麼)**:`Value::to_nlang` 與 `Value::to_string_plain`
兩者的 `_ => format!("{:?}", self)` 收尾均被移除,改為明列全部十一個變體
(Thunk → `expr.to_nlang`;Ref → `<<path>>`;Code → `expr.to_nlang`);
`oo log` 的日期改 RFC-3339。量測:探針 12/12、重複 ×5 全同、workspace
**1793/0/3**、conformance **143/143**、genesis **11/11**、
`display_order`/`union_dedupe`/`union_absorption` = 17/14/7 全綠。

**跨版本量測(非破壞性由量測確立,非由推理)**:同一份來源在 v0.7.0 與本版
分別建倉,根 CAID **逐位元組相同**(`…9d99e5b8cc5e146a`);本版讀 v0.7.0 的倉
讀得出,v0.7.0 讀本版的倉**算出同一個根 CAID** 並印出它自己的 Debug 形——
**同一批位元組、兩種呈現、一個身分**。`~%Discovery./identify` 於新舊引擎回同一 CAID。

**驗收方掛的兩筆**:
(1) 交付射程比工單寬一項——工單只點名 `to_nlang`,交付連 `to_string_plain`
一起修。判定為在射程之內(同檔案、同一個收尾、同一個缺陷),但**記為超出而非默認**;
`to_string_plain` 有 64 個呼叫點,絕大多數作用於 `force` 之後的結果。
(2) 交付回報的三個數字有一處對調(17/7/14 實為 17/14/7)。無實質影響,
但驗收不照抄交付的數字,故記。

**一件量到而不宣稱的事**:把 `oo status` 印出的區塊剝殼後在另一個空倉重新
evolve+commit,根 CAID 相同——即**語義往返在本例成立**。但工單只宣稱「可剖析」,
且**造不出反例不等於不存在反例**(相對錨點 `^.` 隨巢狀一起被印出,把最可能的
一類擋掉了),故 REAL_01 §1.3 的自陳缺口照舊保留。

**引擎 v0.12.0 定版(2026-08-08)= W3′-a「矛盾在哪」弧,增量**:top `0328319`
(squash where_the_conflict_is 弧 + oo 0.12.0 bump;故事提交 **"Say where the
conflict is, not where you were typing"**)。squash 後先驗樹逐位元等同 dev
(`21a69299`),再提交。tie-back `6e8beee`。規格同步切 **v0.12.0-draft.1**。

**版號:走 minor,與前一弧的 patch 相反**。W0′/v0.11.1 是符合性(規格一字未改);
本弧**新增 SPEC_10 §2.2.1**,是語義變更,故依 VERSIONING §6「語義變更逐 minor」。

**缺陷**:evolve 撞 ⊥ 時,操作者看到的是
`Conflict at Path(Path { anchor: Bare, segments: ["app"], span: Span { start: 0, end: 3 } })`
——**該次演化所寫的頂層欄位名**,以 Rust 除錯格式印出;而矛盾實際在
`app.db.opts.retries`(四層深、六個葉子中的一個)。互動式階段更少:
`Evolution Conflict: Conflict`,連欄位都沒有。

**偵察三次被實測推翻,全部同一個方向——讀碼讓我把事情想得比實際壞或比實際簡單**:
① 「引擎從來沒算過座標」→ **算了**,`unify_combo` 在回程逐層累積,直接呼
`engine.unify` 量到 `path = Some("p.q.deep")`,丟棄點是 `Value::Bottom(d) => Err(d.cause)`
兩行(`universe.rs:396/495`),`d` 就在手上。② 「完整座標 = `f.key` ＋ `path`」→
**`path` 已是絕對的**,加前綴會印出 `app.app.db…`。③ 「頂層衝突的 `path` 是 `None`」→
**也有值**(`Some("x")`),`None` 在型別上可達而**未能造出**。
⟹ 連同 W0′ 的「沒人讀 integrity」→「讀了但不擋」,**本週共四次**。

**W3′ 同時被拆為 a/b**:「evolve 邊界說得出矛盾在哪」與「提交時報告 ⊥ 座標」
是兩件不同的事。**b 阻塞於 W12** ——〔量〕§4.1.2 的 MUST **不是在被違反,是在等 W12**:
合併型 ⊥ 在 evolve 邊界就被攔(`staged` 從未寫出),明寫的 `_|_` 被射程 MUST NOT
明文排除,並發型需要 commit 重讀 HEAD 而它不重讀(D32)。**驗收方先前把它記為
「現況為不合規」係誤判,已於 STATUS.md 更正。**

**交付**:`Universe::evolve` 的錯誤型別由 `BottomCause` 換成 `BottomDetail`;
`universe.rs:435` 那條路徑的 `unify` 跑在**欄位值**上故 `path` 為相對,交付以
`p == *c || p.starts_with(&format!("{c}."))` 分流絕對化,**不會雙重前綴**
——**那正是驗收方第一版裁定寫錯的那一格**。兩個回報面同形:
`#conflict at app.db.opts.retries`。

**驗收:通過,零代修**(OODP 系列第四次)。探針 9/9;workspace **1781/0/3**
(183 blocks)×5 穩定;conformance **143/143**;genesis **11/11**;
**跨版本為實跑**——v0.11.1 二進位建立的 30 提交倉,交付版讀之 `log` 30 筆、
`gc` 60/60/0 不變。探針完整性以機械法證明(刪 4 行 `#[ignore]` → rustfmt → diff
⟹ IDENTICAL)。

**對抗逼出了工單自己預告的裁定,而責任不在交付**:
`{ "a.b": 1 }` 與 `{ a: { b: 1 } }` 兩個**結構不同**的宇宙給出**同一個座標字串**
`cfg.a.b`。追下去:`cfg."a.b"` **不可解析**、`cfg.a.b` **靜默回 Top**、
`cfg.0` 可導航。⟹ **n/ 的路徑語法沒有「含點或含空白之鍵」的拼法;引號鍵寫得進去、
讀不回來。** 交付印的是唯一可印的東西。已寫成 SPEC_10 §2.2.1 的**自陳缺口**。

**掛帳(非缺陷)**:
1. **路徑語法沒有引號鍵的拼法**,而鍵可以是引號的——寫面與讀面不對稱,**語言層缺口**,歸 SYNTAX。
2. **導航到不存在的巢狀路徑靜默回 `_`**,使「照座標走」不可靠;與 1 合起來才是完整危害。
3. **值的顯示印表機不加引號**(`--observe` 印 `a.b: 2`)而 **`oo fmt` 會加**且
   **round-trip 實測成功** ⟹ **fmt v2 未被違反**,但兩個印表機對同一個鍵給出不同的字。
4. `message` 仍是 Rust Debug(`Atom(Int(1), EffectTag(0), None)`);工單列為加分不列要求,未做。

**引擎 v0.11.1 定版(2026-08-07)= W0′ 弧,引擎 patch**:top `22b1957`(squash
verdict_must_gate 弧 + oo 0.11.1 bump;故事提交 **"What you could not read, you
may not collect"**)。squash 後先驗樹逐位元等同 dev(`80018a6d`),再提交。
tie-back `f0ecb21`。

**版號裁定——本專案第一次真的用到「引擎 patch」位**:本弧規格**一字未改**,
它是 REAL_03 §6.6 三條既有 MUST 的符合性工作。依 VERSIONING §2「引擎 patch =
引擎自己的 bugfix/效能,與規格 patch 無對應義務」,故走 `0.11.0 → 0.11.1`,
規格維持 `v0.11.0-draft.1`。**驗收方原本建議 v0.12.0,係以「使用者可見行為
改變」推理,而本政策的軸是「規格語義有沒有移動」。** 消耗一個 minor 會讓
`oo v0.12.0` 宣稱實作一份不存在的規格 `0.12`——那正是 §6.2 那筆錯的鏡像。
(**按語 2026-08-08**:`0.12` 其後確實成立,但是**另一個理由**——W3′-a 新增了
SPEC_10 §2.2.1。本段記的是 v0.11.1 當時的判斷,該判斷不因此失效。)

**缺陷(§6.6 不合規三處)**:`gc.rs` 的 `mark` 對不可解碼的**可達**物件
`continue`(把它當葉子),而 `run_gc` 取得 `report.integrity` 後從不讀它,照刪。
**論證性量測**:三提交六物件、中間 commit 覆寫為 `not json at all` ⟹
`integrity #object_undecodable: … cannot be decoded` 之後緊接
`removed 3 objects, freed 508123 bytes`、**exit 0**,而 `oo log` 自此走不動。
第二處更靜:把中間 commit 換成**另一個真實 commit 的位元組**(合法 JSON、會被
真的走訪)⟹ 掃掉 2 個、exit 0,而 `caid_mismatch` 在輸出中出現 **0 次**——因為
`storage.rs:209 read_raw_digest` 原樣回傳位元組不重算(對照 `get_value` 有重算)。
第三處是 v0.11.0 的殘帳:`peers::compact` 與 `DiscoveryConfig::write` 用
**可預測的暫存名**(`with_extension("…tmp")`,每個行程都一樣),`oodp.rs` 的
歸屬聲明仍裸寫。

**交付**:`mark` 讀後**重算位址**(先 Value 後 Commit,避免 v0.2.52 的解碼器
誤判)、`#caid_mismatch` 與 `#object_undecodable` 分開記錄且**不跟隨其引用**、
走訪不完整時 `run_gc` **不刪任何東西**並回非零;「不存在」維持續行(§6.6 §9.1)。
三處寫入全部改走唯一實作 `storage::atomic_write`;壓實失敗於呼叫端可見;
追加路徑的表頭寫入結果不再被丟棄。

**驗收:通過,零代修**(OODP 系列第三次)。workspace **1772/0/3**(182 blocks)
×5 穩定、conformance **143/143**、genesis **11/11**、探針 12/12;鄰近套件
`local_gc` 17 / `cas_integrity` 13 / `store_boundary` 20 / `advert_persistence` 19 /
`discovery_trust` 20。**跨版本為實跑**:同一個工作區由交付前二進位建立、交付後
二進位讀之,報告逐字相同。

**探針完整性以機械方式證明,不靠目視**:交付動了探針檔 141 行。把驗收方版本
刪掉 6 行 `#[ignore]` 後 `rustfmt`,與交付版 `diff` ⟹ **IDENTICAL**。141 行全是
`cargo fmt` 換行。**下次沿用此法——「我看過了,只是格式」不是證明。**

**對抗三項**,其中最強者:植入一個不可達孤兒(1 collectable, 21 bytes)**再**
竄改一個可達物件 ⟹ 拒絕、7→7、**孤兒沒被收走**。鐮刀已經舉起來了才被攔下。

**掛帳(非缺陷)**:
1. **代價已量到 2.3×**:`gc --dry-run` 0.45 s → 1.05 s(60 物件 / 8.5 MB;
   基線是只把 `gc.rs` 換回交付前重建的二進位,兩側只差該檔)。**debug build,
   絕對值被放大,release 未量。** 這是重算義務的價錢——**但它被付了兩次**,
   `run_gc` 先 `plan_gc`(走訪一)再自行 `mark`(走訪二),兩趟都重算。
2. **潛在**:`verify_reachable_object` 的 Value 分支若解得成但雜湊不合,
   **直接回 `CaidMismatch`,不再試 Commit 解碼器**。今天安全(P3 全綠為證);
   `Value` 日後多一個寬鬆變體則**每個健康倉庫的 gc 都會拒絕**。P3 是其釘。
3. `compact` 仍只說「失敗了」不說「為什麼」(`.ok()?` 丟掉原因)。
4. **驗收方自陳的形狀缺失**:工單 §3.3 要了 `peers.rs:400` 的表頭修正,
   **而探針沒釘它**,只能以讀碼確認。「工單要了而探針沒釘」是下次該避免的形狀。

**規範空洞盤點(2026-08-07)= 有名字,而引擎沒有的那些**

**起因**:`docs/discussion/029` §4.3 量到 `#semantic_isolation` 在引擎全樹零出現,
而 SPEC_13 §7「視界震盪防禦」是 **MUST**、APP_05 §7.3 還給了逐字的判準
($P_A \sqcap P_B \neq P_\bot$)。用戶的假設是「這是 APP 系列只想了概念、還沒進
REAL 系列」。**盤點的結果部分推翻了這個假設。**

**掃描形狀(三種,前兩種都錯,記下來)**:
* 形狀 1(詞界 token 比對):缺 32 —— **漏抓 CamelCase 變體**,`AlreadyExists`、
  `NoMatchingBranch` 等 5 個被誤判為不存在。
* 形狀 2(去底線後子字串比對):缺 26 —— 反向錯:**把註解裡的提及算成存在**
  (`#branching` 即因此被救回)。同 `~%REPL` 那次的「use vs mention」教訓。
* 形狀 3(字面 `#<code>`,即引擎實際的發出形式,見 `storage.rs:73` 的
  `"#caid_mismatch: …"`):**缺 34**。抽驗 5 個確認零出現;其中 `#incomplete`
  與 `#already_exists` 另有 CamelCase 變體,可能以他形實作 ⟹ **實數 32–34。**

**TAG_REGISTRY 共 73 個,約 45% 在引擎裡沒有對應。** 家族分佈:

| 只出現在 | 個數 |
| :-- | :-- |
| SPEC_ 系列 | 11 |
| **只在 TAG_REGISTRY 自己**(無任何條文要求) | **10** |
| REAL_ 涉入 | 7 |
| **APP_ 涉入** | **4** |
| 其他(ORDER/GUIDE/SYNTAX/COSMOLOGY 混) | 2 |

⟹ **這不是 APP 系列的問題。** APP 涉入的只有 4 個。而最尖的一格是那 10 個
**只存在於 TAG_REGISTRY 自己**的代碼——它們不是「規定了但沒做」,是**取了名字
但從未被規定**。那一格是規格側工作(補條文,或從 TAG_REGISTRY 刪),**不是引擎帳**。

**兩個 APP_05 實例其實是相反的兩種病**:

* **§7.3 視界震盪**:SPEC_13 §7 寫 MUST、§7.3 給判準,而 **APP_05 §8 自己把
  「語義日蝕攻擊的譜防禦協議」列為 Phase 4 實作前待解的理論難題(難度:高)**。
  ⟹ **同一份規格同時要求它、並宣告它尚未被解決。** 所以它**不是純追法弧**:
  開工之前得先裁「它到底是 MUST 還是未解難題」。
* **§7.4 幾何蒸發**:**實質上已被 v0.2.53 本地 GC 弧兌現,而全程沒有人引用它。**
  §7.4 要求「遺忘不等於刪除——節點可丟棄本地副本,但**必須保留 CAID 字串本身
  及其因果鏈指標**」,而該弧明白接受的代價正是「`oo log` 能指名 store 不再持有
  的內容」。兩者是同一條。

⟹ **真正缺的不是實作,是一張說「APP/SPEC 的哪一條由誰兌現、兌現在哪」的表。**
§7.3 與 §7.4 今天在同一份文件裡、同樣沒被追蹤,而一個是零實作、一個是早就做完了。

**掛帳(本次不修)**:
1. `#semantic_isolation` + 視界震盪:規範性、零實作;**前置是解 APP_05 §8 的自相矛盾**。
2. 34 個代碼的逐項分診:併入「引擎測項整理」那條,或另開。
3. 那 10 個無家代碼:**規格側**,不入引擎佇列。

**引擎 v0.11.0 定版(2026-08-06)= 原子寫入弧,增量**:top `86b1bc2`(squash
atomic_writes 弧 + oo 0.11.0 bump;故事提交 **"A write must not leave a half
file"**)。squash 後先驗樹逐位元等同 dev(`f613c551`),再提交。
**缺陷**:所有耐久寫入皆為 `fs::write`(O_TRUNC 後寫),並行讀者看得到半截檔;
實測 94 KB staged、60 次 evolve、連續解析讀者 ⟹ **63,769 次讀取中 12 次解析失敗
(每次寫入 0.2 次)**。`storage.rs` 全檔 `rename`/`create_new` 命中數為 0。
**交付**:`storage::atomic_write` — 同目錄 temp + `fsync` + `rename`;
接上 staged / pin_pending / effect_pending / abandoned / HEAD / CAS 物件 /
`architects.json` / `.oo/format`。順帶消掉 `write_object` 的 check-then-write
TOCTOU(`rename` 原子冪等)。
**探針不靠競態**:先量了競態紅(0.02%/讀取)並否決——**紅在機率上的閘教讀者去重跑
而不是去看**;改用 **inode 簽名**(就地 rewrite 重用 inode,rename 每次換一個),
基線每趟必紅、交付後每趟必綠。
**一件代修** `2d301ee`:**P1 對它守的實作是瞎的**——交付把臨時檔命名為
`.partial-*`,而 P1 篩的是含 `tmp` 的名字;植入兩個洩漏檔(一個在 `.oo/`、
**一個在物件分片內**)舊篩法一個都沒抓到,而分片內那個正是 `local_gc` 的
`store_map` 會算成幻影物件者。**交付從未動探針,它只是選了一個釘看不見的名字。**
修法改為釘性質:分片內用精確規則(62 個小寫十六進位字元),平面層維持啟發式並明說。
**驗收**:workspace **1760/0/3**(181 blocks)、conformance **143/143**、
genesis **11/11**、arc suite 8/8 ×3 穩定;`local_gc` 17 / `advert_persistence` 19 /
`history_ops` 15 / `store_boundary` 20 全綠;殘留 scratch 目錄 0。
規格同步切 **v0.11.0-draft.1**。

**符合性量測(v0.11.0)**:
* **競態,交付樹三趟**:約 16 萬次讀取,**解析失敗 0、檔案不存在 0**。
  後者是必要的:**新 inode 是必要不是充分**——delete-and-recreate 也會換 inode,
  只是把「截斷窗口」換成「不存在窗口」,而只計解析失敗會讓它讀起來像乾淨通過。
* **跨版本為〔讀〕不是〔量〕**:每個呼叫點皆 `fs::write(p, X)` → `atomic_write(p, X)`,
  X 完全不變、無任何序列化改動 ⟹ 位元組依構造相同。未建舊二進位實跑,此處明記。
* **物件撕裂量測未做**:物件與 staged 共用同一個 `atomic_write`,機制已由 staged
  三趟證實。說出來比默默跳過好。
* **工單漏列兩處(非交付失誤)**:`peers.rs:452` 的 `.oo/peers/directory` 壓實
  已有手寫 temp+rename **但無 `fsync`** 且 `.ok()?` 吞錯誤;`oodp.rs:639` 的
  `~/.oo/nodes/<hash>.affiliation` 仍是裸 `fs::write`。
  **漏的成因**:工單的路徑表由 grep `join(".oo")` 建出,結構上看不見用別種方式
  構造路徑的寫入(`peers.rs` 走常數、`oodp.rs` 從 `node_key_path` 衍生)。
  ⟹ **「掃描不得截斷」不夠——掃描的形狀也決定了它看得見什麼。**

**引擎 v0.10.0 定版(2026-07-31)= 在席是誰弧,增量**:top `b094fdd`(squash
seat_order 弧 + oo 0.10.0 bump;故事提交 **"Arrival order is a fact about you,
not a fact about them"**)。squash 後先驗樹逐位元等同 dev(`15f5f308`),再提交;
候選重測 workspace **1752/0/3**(180 個 result block)、conformance **143/143**、
genesis **11/11**;條件閘一次成功;tag 後重建 `oo --version` = `oo v0.10.0` ✓、
`git describe --exact-match` = `v0.10.0` ✓;**首次跨十位數,已驗 `sort -V` 下
`v0.8.0 < v0.9.0 < v0.10.0`**。dev tie-back `b88321f`。規格同步切
**v0.10.0-draft.1**。

**符合性量測(v0.10.0)**:
* **加性之關鍵量測**:以 v0.9.0 引擎開啟本版寫下的耐久目錄 ⟹
  `loaded 2 records, skipped 0 damaged, 0 unverifiable`,且該引擎跑完後檔案
  **逐位元不變**。新增 `admission_seq` 是新鍵而非改用途——`received_at` 若由秒
  改毫秒,舊引擎會把毫秒讀成秒。
* 線上互通對 v0.9.0 四案例(含新→新 / 舊→舊兩控制)全 `#success`。
* 對抗四項:廣告自帶 `admission_seq` → **`rejected` 且未存入**(線上不可達);
  偽造 `0` → 偷到席位;偽造 `u64::MAX` → 失去席位;**字串 / 負數 / 浮點 /
  `null` 全部退回 `0` ⟹ 全部偷到席位**。前述路徑需能寫 `.oo/` 之非語言層行程
  (語言層由 SPEC_08 §6.3 之 component-exact `.oo` 路徑閘擋住),屬 §6.3.3 已排除
  之對手;**但退回值本身選錯方向**,故新增 REAL_02 §5.1.2「缺席與不可解析不是
  同一件事」之 MUST。**引擎側未改**——該缺口是工單未指定者,非交付失誤,留待後續弧。

**驗收代修**:`advert_persistence` R5 自行讀檔套用「有記載的載入序」再與引擎比對,
而本弧替換了那個順序 ⟹ 突發平手時兩者不一致,**獨立重跑八次掛三次(37%)**,
而交付當次與全 workspace 那次**都恰好是綠的**。模型已更新為 `received_at` 再
`admission_seq`(該鍵對本引擎寫下的記錄唯一,故第三鍵不可達、刻意不模擬),
修後八次全綠。代修 `dev bb8b64c`。

> **這一件只有「獨立重跑未動的套件」+「重複跑」兩項驗收同時做才抓得到。**
> 少任何一項都會通過。

**框架更正**:我原本把「交付動了路由表重播序」記為超出範圍。讀 §5.1.2 後更正——
該條 MUST 已經寫著「重放即複現之」,而同秒平手時那句話為假,故交付所做的是**讓一條
既有的 MUST 真的成立**,規格因此改為補足 §5.1.2 而非新設條款。

**引擎 v0.9.0 定版(2026-07-31)= 自動准入與其上限弧,增量**:top `1e719e0`
(squash 自動准入弧 + oo 0.9.0 bump;故事提交 **"You say yes to an operator, not
to each of their machines"**)。squash 後先驗樹逐位元等同 dev(`dbe2ca67`),再
提交;候選重測 workspace **1743/0/3**(179 個 result block)、conformance
**143/143**、genesis **11/11**;條件閘一次成功;tag 後重建 `oo --version`
= `oo v0.9.0` ✓、`git describe --exact-match` = `v0.9.0` ✓。dev tie-back
`87d5d25`。規格同步切 **v0.9.0-draft.1**。

**符合性量測(v0.9.0)**:
* 跨版本互通,對 v0.8.0 六案例:控制 新→新 / 舊→舊、無聲明 舊→新 / 新→舊、
  **鑄過歸屬聲明之新客戶端 → v0.8.0 節點**——**全部 `#success`**。本弧不動線上
  位元組,增量確認。
* 對抗五項:**真實根簽章但發給另一個 `node_id`**(載荷會算)→ 攻擊者未被撥打
  而同場控制被撥打;`observed_host` 由收方導出,廣告者唯一輸入為簽章內之
  `listen_port` ⟹ 只能把你指向他自己;`ttl: 0` 之直接有根廣告**被准入**
  (⟹ REAL_02 §4.2.6.2 新裁定);同節點換埠重廣告正確替換舊來源;聲明於兩次
  取物之間過期後不再被撥號。
* 自動來源上限 **3**,與手動 `./connect` 來源分開計數。

**驗收代修(重驗發現)**:本弧最初回報「驗收通過」,其所列數字經獨立重跑**全部
屬實**,但推論不成立——**九支紅裡六支在交付存在之前就是綠的**。r3–r8 只斷言
一個不存在(「這筆記錄沒有成為自動來源」),而開弧基線沒有任何記錄會成為自動
來源,故一個**完全不做准入**的引擎即可滿足;經重建交付前之樹(`9db92bf`)逐支
實測確認(r3–r8 綠,僅 r1/r2/r9 紅)。探針之區段註解自陳 c0/c1 應為該守衛,但
**它們是獨立測試,各自建自己的 fixture**——另一個行程裡的控制證明不了這一次
執行裡機制是活的。六支已各自補上**同場的合格來源**並要求它被撥打;補強後
交付前之樹**九支全紅**、交付樹 **11/11 且五次穩定**。代修 `dev c9ed482`。

> **順帶量到一個偶發**:補強後的存在檢查五次掛一次。成因不是隨機性——取物階梯
> **一命中就 return**,而自動來源由**迭代 `HashMap`** 重建 ⟹ 兩個合格來源時造訪
> 順序任意。已改以「沒有來源能滿足的 CAID」強迫掃描走完。**該順序問題本身已
> 入規格為 REAL_02 §4.2.6.3 之待決**:重建不是准入,故「保留在席者」跨重啟沒有
> 定義。

**引擎 v0.8.0 定版(2026-07-31)= 直接觀察來源性弧,增量**:top `5a030f3`
(故事提交 **"A receiver can tell presence from hearsay"**),tag `v0.8.0`,dev
 tie-back `f15558c`。候選與定版閘:`cargo fmt --all -- --check` 綠、workspace
**1732/0/3**(178 result blocks)、直接來源性 **11/11**、既有 owner suites
全綠、conformance **143/143**、genesis **11/11**;tag 後清除建物重建,
`oo --version` = `oo v0.8.0` ✓、`git describe --exact-match` = `v0.8.0` ✓。
本弧只新增 receiver-local `direct`/`relayed`/`unknown` 觀測半邊及其耐久
合併語義;**fmt v2、`.oo/format 1`、CAID、線上位元與取物來源政策不變**。

**規格 v0.8.0-draft.1 定版(2026-07-31)**:spec top `90f1440`(故事提交
**"A host you heard about is not a host you saw"**),tag
`v0.8.0-draft.1`,local tie-back `0497d7b`。以上 exact release hashes 在
引擎與規格各自 tag、tie-back 完成後補入;規格本版只關閉來源性語義,不包含
automatic admission、hard cap 或任何新的撥號政策。

**引擎 v0.7.1 定版(2026-07-31)= 全 Rust 工作區 rustfmt 正規化,引擎 patch**:
格式提交 `2d6bde2`,bump `107c251`,top `13d0899`(故事提交 **"Formatting debt
is paid once or charged to every change"**),dev tie-back `62e6cd5`。固定工具鏈
rustfmt **1.9.0-stable**(`31fca3adb2`,rustc/cargo 1.96.1);216 個 Rust 檔之
機械轉換 `+20,039/-8,502`,無非 Rust 原始碼。實際 staged tree 與獨立 clean archive
經同版 formatter 所得 tree **逐位元同為 `224da115`**;bump 後 top/dev tree 同為
`b8e3eb2`。候選與定版閘:`cargo fmt --all -- --check` 綠、workspace
**1721/0/3**(177 suites)、conformance **143/143**、genesis **11/11**;tag 後清除
建物重建,`oo --version` = `oo v0.7.1` ✓、`git describe --exact-match` =
`v0.7.1` ✓。僅排版與引擎 patch 版號移動,無規格、語言、CAID、線上格式或引擎判定
變更;依 VERSIONING §2 引擎 patch 位自有,規格維持 **v0.7.0-draft.1**。

**引擎 v0.7.0 定版(2026-07-31)= 歸屬信任根弧,增量**:top `b28d353`
(squash 信任根弧 + oo 0.7.0 bump;故事提交 **"A public key does not say what
question it answers"**)。squash 後先驗樹逐位元等同 dev(`25b34d0`),再提交;
候選重測 workspace **1721/0/3**(177 suites)、conformance **143/143**、genesis
**11/11**;條件閘一次成功;tag 後清除 oo 建物重建,`oo --version` = `oo v0.7.0`
✓、`git describe --exact-match` = `v0.7.0` ✓。dev tie-back `02e8260`。規格同步
切 **v0.7.0-draft.1**。本弧為**增量**,故依 VERSIONING §5/§6 走 minor;
不重啟 90 天時鐘。

**歸屬信任根弧結案(2026-07-31,一件代修)**:工單+校準探針 tools dev
`1f39e64`,交付 `820ddb4`,驗收代修 `6891c02`。引擎新增工作區局部
`.oo/discovery.n` 之 `affiliation_roots`,以閉合 n/ 資料載入(不求值),並提供
`oo node trust list|add|remove`;缺席為空,存在但讀不懂則具名失敗。此弧**只建立
信任根而不消費**:新增 Rust 行之靜態掃描對 `peers.insert`/advert 寫入/TCP connect/
routing 建構/身分呼叫皆 **0 命中**。

**一件代修=「閉合」仍留四個別名,且物理缺席仍有一個別名**:交付版直接量測
空檔、純空白、tuple 代 list、引號欄名皆 exit 0;另 `Path::exists()` 將一個
**實際存在但目標缺席的符號連結**壓成「檔案缺席」。修法為只收裸
`affiliation_roots` + list,存在檔必有該欄,並以 `symlink_metadata` 先判目錄項、
解析後必為一般檔案。兩支驗收探針入永久套件。交付另對 legacy `lib.rs`/`main.rs`
全檔 rustfmt,使三處接線膨脹成 2,879 行 diff;驗收還原既有格式後重施語義接線,
此為純度整治,非第二件行為代修。

**符合性量測(v0.7.0)**:
* discovery_trust **20/20**(交付 18 + 驗收 2)、workspace **1721/0/3**
  (177 suites)、conformance **143/143**、genesis **11/11**。
* **工作區作用域**:同 HOME 兩工作區,A 新增根後 B 仍為空且不造檔。
* **跨版本**:v0.6.0 引擎開啟含有效 `discovery.n` 之新工作區 exit 0(未知可選檔
  被忽略);新引擎開啟無該檔之舊工作區 exit 0、列出空集合且不造檔。
* **耐久成本**:1 root **95 B**;100 roots **7,223 B**。兩者皆字典序,成功後
  `discovery.n.tmp` 缺席。信任管理前後物件數與 `.oo/format` 逐位元不動,亦不鑄
  操作者/節點金鑰、不建 `.oo/peers/`。
* 本弧為**增量**:所有既有工作區走「缺席=空集合」且行為不變;無線上格式、CAID、
  語言語義或網路政策變更。依 VERSIONING §5/§6,切版時應走下一個 minor。

**引擎 v0.6.0 定版(2026-07-30)= 撥號需要同意弧,破壞性(Layer 1)條目 #8**:
top `a5ec63b`(squash 同意閘弧 + oo 0.6.0 bump;故事提交 **"A sentence that
describes an intention is not a gate"**)。squash 後先驗樹逐位元等同 dev
(`12639df`),再提交;候選重測 workspace **1701/0/3**、conformance
**143/143**、genesis **11/11**;條件閘一次成功;tag 後重建 `oo --version`
= `oo v0.6.0` ✓、`git describe --exact-match` = `v0.6.0` ✓。dev tie-back
`7714977`。規格同步切 **v0.6.0-draft.1**。**90 天時鐘自本日重啟**(距條目 #7
僅一日;那是深水期的正常代價,非疏失)。

**符合性量測(v0.6.0)**:
* **能力語義四例**(直接量測,非由套件轉綠推論):無旗標 → `⊥
  #privileged_required` 且訊息指名 `connect requires --grant connect
  (privilege.connect capability)`;`--grant connect` → `#true`;
  `--privileged` → `#true`(全授權涵蓋,與其文件意義一致);
  **`--grant pin` → 拒絕** ⟹ SPEC_08 §6.1.4「出示某個能力不等於出示該能力」
  被遵守。
* **閘先於效果**:被拒之 `./connect` + `./fetch` 耗時 **0.046 秒**(×3),與
  **完全無來源的 0.040 秒**同量級;帶授權之控制組 **5.05 秒** ⟹ 拒絕確實發生
  在連線嘗試之前,而非僅低於門檻。此即 §4.2.6.1「判定法」所要求者。
* **破壞面之計數**:全樹呼叫 `~%Discovery./connect` 者共 **6 個探針套件 + 2 支
  `tests/pending/`**;其中遠端形式 3 個套件需加授權(`node_identity`、
  `peer_fetch_verification`、`oodp_packet_format`),`wire_says_why` 本就使用
  `--privileged` 故不需改,`store_boundary` 與 `universe_determinism` 為本地
  形式故不受影響。**conformance 語料零命中** ⟹ 無任何符合性向量需要 CLI 旗標。
* 線上協定未動,故跨版本互通不受本弧影響(破壞面在**語言面**)。

**引擎 v0.5.0 定版(2026-07-30)= 哪八個弧,增量**:top `6a616f5`(squash
`#discover` 抽樣弧 + oo 0.5.0 bump;故事提交 **"The same question does not
have to get the same answer"**)。squash 後先驗樹逐位元等同 dev(`3e159d3`),
再提交;候選重測 workspace **1692/0/3**、conformance **143/143**、genesis
**11/11**;tag 後重建 `oo --version` = `oo v0.5.0` ✓、`git describe
--exact-match` = `v0.5.0` ✓。dev tie-back `160eac4`。規格同步切
**v0.5.0-draft.1**。**增量,故依 VERSIONING §5/§6 走 minor**(第二次照政策走)。

**符合性量測(v0.5.0)**:
* **均勻性**(N=20,k=8,4000 次查詢,期望 0.400,3σ = ±0.0232):
  min **0.3845** / mean **0.4000** / max **0.4185**,**全數在 3σ 內**;
  從未出現者 **0**。**出現在第 0 位的相異對等點 20/20** ⟹ 為整列洗牌,
  非只洗尾巴(後者會通過 R1/R2 而仍給攻擊者便宜)。
* **列舉成本**:20 筆目錄於 **8 次查詢、0.03 秒**內被完整列出(修訂前需等
  對方重啟)。此為 §4.3.5.1 所記之誠實代價,已裁定接受。
* **延遲**:3.36 ms/query(4000 次量測),絕大部分為 TCP 與行程成本。
* **跨版本**:新/舊客戶端 × 新/舊節點四組合,`advertise` 全 `#success`、
  `discover` 全回 peers。線上形狀未動,增量確認。
* **重跑穩定性**:該套件連續五次 11/11。

**候選重測出現一次未能重現的失敗,誠實記錄**:一次工作區執行回報`advert_persistence` 套件 **17 通過 / 2 失敗**,
其後約 **70 次**嘗試全綠(該套件單獨 26 次、工作區 16 次、六套件併發 18 次、
強制冷重建 2 次)。**套件由算術指認**:`cargo test` 逐個二進位執行且失敗即停,
該二進位之前的累計為 1293,而 1293 + 17 = 1310 恰為該次回報之數。
**最顯然的假設(逾時)已被量測推翻**:等 150 行 log 實測 **761 µs**、節點啟動
實測 **100 ms**,而預算皆為 4 秒——差三個數量級。**已修的是會遮住它的東西**:
`peers_writes` 逾時後原本靜默 fall-through 並以不完整的 log 計算位元組總數
(於是逾時會偽裝成關於位元組的斷言失敗),現改為斷言且預算 60 秒;`serve` 的
panic 亦報出實際等待時間。**成因不明,且記為不明。**

**引擎 v0.4.0 定版(2026-07-30)= 歸屬聲明弧,增量**:top `2f48a8c`(squash
歸屬聲明弧 + oo 0.4.0 bump;故事提交 **"An operator can say which machines are
theirs, and cannot say it for long"**)。squash 後先驗樹逐位元等同 dev
(`669e1347`),再提交;候選重測 workspace **1681/0/3**、conformance
**143/143**、genesis **11/11**;條件閘一次成功;tag 後重建 `oo --version`
= `oo v0.4.0` ✓、`git describe --exact-match` = `v0.4.0` ✓。dev tie-back
`ea352d8`。規格同步切 **v0.4.0-draft.1**。

**版號依據**:本弧為**增量**(新增可選線上欄位與新章節,向後相容)。依
`meta/VERSIONING.md` §5,`編輯性` 才是規格 patch 的全部內容,`增量` 與
`破壞性` 同走 minor(§6「語義變更逐 minor」)⟹ `0.3` → `0.4`。**這是
§6.2 修正之後第一次照政策走的切版**;v0.2.x 期間之所以停號,正是因為當時
把這類變更塞進了 patch 位。

**符合性量測(v0.4.0)**:
* 跨版本互通,六案例:控制 新→新 / 舊→舊、無聲明 舊→新 / 新→舊、
  **帶聲明之新客戶端 → v0.3.0 節點** ——**全部 `#success`**,增量確認。
* 對抗批次 12 項(字串/列表型 `affiliation`、缺欄、`expires:-1`、
  `expires:i64::MAX`、非 hex 金鑰、**真簽章配錯操作者金鑰**、4 KiB 金鑰、
  巢狀 6 層、重複欄位鍵、30 KiB 填充):11 項 `#success`(REAL_02 §4.2.8
  「只能加不能減」成立),1 項 `#rejected` 係解析器拒重複欄位鍵之既有行為。
  好聲明之操作者金鑰於 `oo node peers` 出現**恰好一次**,偽造者從未被報告。
* 耐久對等目錄,150 則廣告:帶聲明 **172,091 B** / 不帶 **131,777 B**
  = **+268.8 B 每則(+30.6%)**。(REAL_02 §5.1.2 之耐久格式未動——已驗證
  之操作者為衍生物,依該節原則於載入時重算而不落盤。)
* `MAX_DISCOVER_PEERS = 8` 仍先於 64 KiB 回應預算綁定。

**引擎 v0.3.0 定版(2026-07-29)= 破壞性(Layer 1)條目 #7,並修正版號政策之違反**:
top `7b8a175`(squash「x 的 CAID 就是 x 的 CAID」弧 + oo 0.3.0 bump;故事提交
**"The CAID of x is the CAID of x"**)。squash 後先驗樹逐位元等同 dev(`00f95684`)
再重測:workspace **1661/0/3**、conformance 143/143、genesis 11/11、
caid_of_the_argument **12/12**、網路套件**連跑兩輪皆綠**。條件閘一次成功;
`oo --version` = **`oo v0.3.0`** ✓。dev tie-back **`8a8238e`**。

**為何是 0.3.0 而非 0.2.56**:見 `meta/VERSIONING.md` §6.2。引擎與規格共用
`major.minor` 是一個**宣稱**,而 `oo v0.2.55` 宣稱它實作規格 `0.2.x`——它不是。
規格 `v0.2.0` 之後累積 **334 個提交**、含 **7 筆破壞性條目**,全在未發布分支上,
而版號一路宣稱對齊。**成因非疏忽**:規格 patch 位按 §2 只裝編輯性修訂,故那些語義
變更**沒有任何位置可以承接**,於是就地累積成一句愈來愈大的假話。規格同步出
**`v0.3.0-draft.1`**(§3 公開徵求意見草案),委員會錨點自 v0.5.0 改 **v0.500.0**。

**零驗收代修**。**特別閘held住**:四個透過 `oo eval ~%Discovery./identify` 簽章的
探針套件**一行未編輯即全綠**——那就是「語言面與協定面一起移動」被量測而非被宣稱的樣子。
交付另自行找到工單未點名之洞(柯里化的部分施用會使 `%arg` 進入使用者可見的部分態射,
已排除),並將約定收進單一 `value::whole_argument()`。

**破壞性雙向實測**:v0.2.55 客戶端 → 新節點、新客戶端 → v0.2.55 節點,皆
`#rejected` / `%reason: #bad_signature`;**控制**(新→新)`#success`。**破壞在線上
是看得懂的**,因為前一弧剛把 `%reason` 開放給所有非成功狀態——一版之前它會是不透明的
`#conflict`。

**開弧前偵察兩發**:(1) print→parse→eval **是恆等的**(18 形狀 17 個 CAID 不動)⟹
不一致全部來自引數包;(2) **天真解包已出貨且正在丟資料**——`engine.save` 無條件取槽 0,
`./identify_and_store (1, 2)` **存入 `1` 並回傳 `1` 的位址**,`oo inspect` 印出 `1`。
**儲存確認它存了一個它沒有存的東西。**

**引擎 v0.2.55 定版(2026-07-29)=增量**:top `55ae9b2`(squash「線上說得出為什麼」弧
+ oo 0.2.55 bump;故事提交 **"A node newer than you is not a node that has been corrupted"**)。
bump+lock `dev` 見 log。squash 後先驗樹逐位元等同 dev(兩側 `HEAD^{tree}` = `65a990db`)
再重測:workspace **1649/0/3**、conformance **143/143**、genesis **11/11**、
wire_says_why **16/16**、advertise_wire 19/19、oodp_packet_format 13/13、
discover_index 17/17、advert_persistence 19/19、kademlia 17/17、local_gc 17/17
(**網路套件連跑兩輪皆綠**)。條件閘一次成功;重建 `oo --version` = **`oo v0.2.55`** ✓
且 `git describe --exact-match` 相符。dev tie-back **`57b949d`**。spec closure `local 07e8fcb`。

**分類=增量**之依據(實測):今日客戶端把 `#not_implemented` 與 `#conflict` 坍縮為同一結果,
故舊客戶端對新節點**行為完全不變**——持有→值;損壞→指控**且該指控為真**;缺席→
`⊥ #conflict`,而**舊客戶端對舊節點得到完全相同的結果**(該瑕疵屬 v0.2.54 自身,本弧已對
新客戶端修為 `#missing_key`)。`%reason` 是舊客戶端忽略的欄位。

**零驗收代修**。交付移除八個 `#[ignore]` 且探針檔零新增;預定改變那支釘改動最小並附出處。

**符合性觀測(2026-07-29)**:七格狀態/理由矩陣全可分,`#success` **不帶** `%reason`;
`find_node` 壞 target 回 `#malformed` 而 `discover` 回 `#unparseable_caid`(前者之 target
非 CAID)。客戶端對抗五格:**來自未來的未知 reason 判為拒絕而非指控**;無 `#` 前綴之
reason 仍被認出;`#not_found` 上的胡亂 reason 不劫持狀態。`bn_serial` 對每個
`Value::Bottom` 只寫 `0xFE` 並**丟棄因由**,故三個新 `BottomCause` 不可能移動任何 CAID。

**切版過程一件事故並修復(候選重測抓到,且在本弧未觸及之套件)**:kademlia fixture 的
「抽到覆蓋 6 個桶為止」迴圈,其上限為 `n * 10`——**而覆蓋 6 個桶所需的抽樣數與 n 無關**。
最小的 fixture 要 10 個對等點,上限遂為 100。模擬 200,000 次:**中位數 37、p99 149、
p99.9 218、p99.99 295、最大 411;cap=100 失敗率 5.3%,cap≥1000 於 20 萬次中為 0**。
5% 正是該套件偶發的頻率,且**只在最小的 fixture 上發作**,故驗收時未現、候選連跑全部
套件時才現。上限已與 n 解耦並設於實測長尾之外;十二次連續乾淨。

> **教訓比「抽到滿足性質為止」更窄**——那一半 kademlia 弧本來就做對了。新的一句是:
> **當你把「對抽樣結果的斷言」換成一個迴圈,那個迴圈的上限是一個新的數字,它需要自己的量測。**

**掛帳(本弧論旨少掉的一格,已記未修)**:對端回 `#success` 卻無 `%result`,仍被記成完整性
指控並收斂為 `⊥ #caid_mismatch`。一個把載荷搬到別處的**更新版節點**會正好落在這裡。未修之
理由是「什麼算格式錯誤的**回應**(相對於請求)」需要一條工單從未做出的裁定。

**引擎 v0.2.54 定版(2026-07-29)=增量**:top `70f9843`(squash 耐久對等目錄弧 +
oo 0.2.54 bump;故事提交 **"An observation cannot travel, a signature can"**)。
bump+lock `dev 07ebcf4`。squash 後先驗樹逐位元等同 dev(兩側 `HEAD^{tree}` = `00c3c685`)
再重測:workspace **1633/0/3**、conformance **143/143**、genesis **11/11**、
advert_persistence **19/0/0**、kademlia 17/17、discover_index 17/17、local_gc 17/17、
advertise_wire 19/19。條件閘一次成功;`touch build.rs` 重建後 `oo --version` =
**`oo v0.2.54`** ✓ 無髒尾且 `git describe --exact-match` 相符。dev tie-back **`7895021`**。
spec closure `local 941035f`。

**分類=增量**之依據:根不動;`.oo/peers/` 對舊引擎只是一個它不讀的檔案——**實測**
v0.2.53 在帶該目錄的倉庫上演化並提交成功,本版讀回該 commit 且目錄仍載入。

**一件驗收代修**(`dev dd7fa3c`)=**載入器一則簽章都沒驗**。實測:改掉儲存記錄中簽章的
16 個十六進位字元、重啟 ⟹ 節點回報「載入 1 筆、跳過 0 筆」**並將其轉發**。修法為把檢查
移至引擎建構之後(`peers::verify_loaded`),走與轉發記錄同一道階梯。已入規格
(REAL_02 §5.1.2 / SPEC_15 §7.1)。

**符合性觀測(2026-07-29)**:150 則廣告 **131,568 位元組 / 0 次壓實 / 877 B 每筆**,
對照被撤銷之全檔重寫設計同樣 150 則的 **14,380,000 位元組**(**109×**)。壓實另測
(50 行 / 10 活):**3 次、重寫 36,627 B、檔案 20,635 B**。A/B @ v0.2.53 = **8 綠 11 紅**
(校準 10 紅 + P8 代修守衛)。

**切版過程一件事故並修復(候選重測抓到)**:第一次 squash 之故事提交建於一棵會偶發失敗的
樹上——R5 的反事實用 `self_id = 全零`,而**全零在一半的情況下與正確 self_id 不可區分**
(桶 0 在 self=X 下是「最高位與 X 不同者」,在 self=0 下是「最高位為 1 者」;X 最高位為 0
時二者同集,溢出丟棄亦同)。故 **dev 上十次全綠、候選上失敗**。已改用「真 self_id 最高位
翻轉」為反事實(其桶 0 為正確者之補集,兩半皆溢出故存活集不可能重合),target 取自兩存活
集之對稱差;**十次連續乾淨**。top 之故事提交已重做於修正後之樹(舊 `c3f9167` 廢棄,未 tag)。

> **此事本身是一項發現,已寫入交付紀錄與 tag**:一個帶著**未種下之全零 self_id** 出貨的
> 引擎,在**一半的節點上**與正確實作行為完全相同——這正是該類缺陷得以存活的機制,
> 也正是探針不得依賴當次抽樣的理由。

**引擎 v0.2.53 定版(2026-07-29)=增量**:top `7a5ba30`(squash 本地 GC + 儲存格式
版本弧 + oo 0.2.53 bump;故事提交 **"Forgetting is a privileged act, and stays one"**)。
bump+lock `dev 878614b`。候選重測(squash 後、tag 前,樹與 dev 逐位元相同——
`git rev-parse HEAD^{tree}` 兩側皆 `3302531e`):workspace **1614/0/3**、
conformance **143/143**、genesis **11/11**、local_gc **17/17**、kademlia **17/17**。
條件閘 `[repo=nlang-tools]&&[branch=top]` 一次成功;`touch build.rs` 重建後
`oo --version` = **`oo v0.2.53`** ✓ 無髒尾且 `git describe --exact-match` 相符。
dev tie-back **`32f7352`**,`git diff --stat top dev` 空。spec closure `local a3385a2`。

**分類=增量**之依據:根不動;`oo gc` 為新子命令,v0.2.52 及更早無任何客戶端能依賴
其行為;`.oo/format` 對 v0.2.52 是一個它不讀的檔案——**實測** v0.2.52 引擎打得開一個
已 GC 且帶有 `.oo/format` 的倉庫,並能讀取、演化、提交,本版再讀回。

**零代修**(OODP 系列以來首次)。驗收採**行為驗證**而非可達性對可達性:探針的走訪器
與引擎的走訪器可能共用盲點,兩者相比不會察覺(此顧慮當場兌現,見下)。實測
**11 → 4 物件、釋出 1,681,325 位元組**,而現存歷史中每個 commit 仍讀得回、值仍取得回、
宇宙仍能演化並提交。A/B 對 v0.2.52 以交付方的探針檔重跑:**9 紅 8 綠**,與校準一致
(探針未被削弱)。

**驗收方自曝兩事**(皆為我寫的東西):

1. 校準紀錄稱 R12「今日平凡通過」為**假**——它在 v0.2.52 是紅的,原因與 GC 無關。
   CAS 同時裝值與 Commit,而 `oo inspect` 假設全是值,於是對**引擎自己剛寫下的
   Commit** 回 `#object_undecodable … (integrity unknown)`。交付順手修好;我另驗
   該修法未吞掉真損壞(擾動物件仍 `#object_undecodable`、竄改物件仍 `#caid_mismatch`)。
   裁決已入 REAL_03 §6.6「裁決必須為真」。
2. 工單稱「預定改變的釘:無」為**假**——本弧宣告 `.oo/format`,而 kademlia P4 是
   `.oo/` 耐久檔的允許清單,必須改(交付確實改了,最小且附註)。**那正是 v0.2.51
   工單犯過、v0.2.52 工單專為避免而寫的錯**。把教訓寫下來並未阻止我在一弧之後重犯,
   故改為機械檢查:**一弧新增耐久檔或新 op 時,grep 既有的釘,找出誰在斷言它不存在**。

**探針設計新規**(本弧掙來):全集掃描型探針**首位須放 control**。本檔的
`reachable_before_any_squash_is_everything` 當場逮到驗收方自己的可達性走訪器把整個
倉庫報成不可達(未處理以位元組陣列儲存的 digest)。走訪器靜默失效時,**每一支紅線都會
靠「刪掉全部」而通過**——以紅線開頭的全集掃描量到的是零。

**引擎 v0.2.52 定版(2026-07-28)=增量**:top `1ccce5e`(squash Kademlia 路由表弧
+ oo 0.2.52 bump;故事提交 **"A table that can be held accountable"**)。bump+lock `dev 148ad5d`。
候選重測:workspace **1597/0/3**、conformance **143/143**、genesis **11/11**、
kademlia **17/17**、discover_index 17/17、advertise_wire 19/19、oodp 13/13、
peer_fetch 12/12、node_identity 13/13。條件閘一次成功 `GATE OK: head=1ccce5e`;
tag 後重建 `oo --version` = **`oo v0.2.52`** ✓ 無髒尾且 `git describe --exact-match` 相符。
dev tie-back **`6b863c3`**,`git diff --stat dev top` 空。spec closure `local 334e565`。

**分類=增量**之依據:根不動(P3 於填滿並查詢過路由表的節點上實測相等);`#find_node`
對 v0.2.51 是**未知 op**,故此前無客戶端能依賴其行為(實測該版回 `#conflict`,新客戶端
乾淨處理);廣告雙向 `#success`。

**符合性觀測(2026-07-28)**:滿載 `#find_node` 回應實測 **20 筆 / 10,347 位元組**,
對 87 位元組之請求為 **118.9×**——在 REAL_02 §4.4.2 的 64 KiB 預算之內,約為 `#discover`
之四倍(k=20 對上限 8)。磨鑰匙成本實測 **0.280 ms/key**,佔滿桶 8 的 20 個槽位需
**10,928 把鑰匙 / 3.0 秒**(SPEC_15 §7.1 之表由此而來)。

**一件驗收代修**(`dev 54c07ec`)=交付將路由表與廣告目錄持久化至 `.oo/oodp_index.json`
(每受理一則廣告重寫全檔:150 則 → 索引 185,854 B、累計寫入 **14.38 MB**、77×、O(N²);
且跨行程存活)。**根因為工作單自相矛盾**(禁持久化 + 指定另一行程的 CLI 當唯一觀測面)。
已撤;觀測改讀 serve 自身日誌行。**副作用**:記憶體內表使「先到者鎖死某桶」止於重啟,
該緩解將於耐久狀態落地時消失。

**引擎 v0.2.51 定版(2026-07-28)=增量**:top `d2e3d28`(squash `#discover` 服務索引弧
+ oo 0.2.51 bump;故事提交 **"The directory learns to answer"**)。bump+lock `dev 5d8b88b`。
候選重測:workspace **1580/0/3**、conformance **143/143**(`scripts/run-conformance.py`)、
genesis **11/11**、discover_index **17/17**、advertise_wire **19/19**、oodp 13/13、
peer_fetch 12/12、node_identity 13/13。條件閘 `[repo=nlang-tools]&&[branch=top]`
一次成功 `GATE OK: head=d2e3d28`;tag 後重建 `oo --version` = **`oo v0.2.51`** ✓
無髒尾且 `git describe --exact-match` 相符。dev tie-back **`b59d936`**,
`git diff --stat dev top` 空。spec closure `local e681614`。

**分類=增量**之依據:根不動(P3 實測 quiet 與 busy 之根 digest 皆
`9ecb95b0c6088b348d582c8f0ed03fa499ff7b6d4cb0b71f3eba70bf9f339ae3`);
`#discover` 此前一律回 `#not_implemented`,無客戶端能依賴其行為;跨版本雙向實測——
廣告雙向 `#success`、新客戶端對 v0.2.50 節點發 `#discover` 得 `#not_implemented`
並**乾淨處理**、新索引成功轉發**一個 v0.2.50 節點廣告的記錄**。
`ttl` 範圍檢查(`0..=15`)為新增拒絕面,但 v0.2.50 之 CLI 只送 `ttl: 15`,
掃描確認無既有客戶端會被此拒。

**一件驗收代修**(`dev d2fa511`)=放大界只做在回應方。實測從不停頓之對端送 **67.1 MB**,
收方全數緩衝、峰值 **143 MB**、解析 **8156** 筆,**讀取逾時從未觸發**(逾時針對停頓非總量)。
驗證階梯全程守住(零接受)故為資源非繞過。反事實:**143,324→5,632 KB、2.38→0.02 s**。

**引擎 v0.2.50 定版(2026-07-28)=增量**:top `75e2932`(squash `#advertise` 上線弧
〔含一件驗收代修〕+ oo 0.2.50 bump+lock 同入),故事提交 **"A signature with no key to
check it"**,tag 於實測 commit(workspace **1563/0/3**、advertise_wire **19/19**、
oodp 13/13、peer_fetch 12/12、node_identity 13/13、store_boundary 20/20、cas 13/13、
identity 16/16、conformance **143/143**、genesis **11/11** 皆於候選重測;條件閘一次
成功 `GATE OK: repo=nlang-tools branch=top head=75e2932`;tag 後 touch build.rs 重建
`oo --version` = `oo v0.2.50` ✓ 無髒尾,`git describe --exact-match` = v0.2.50)。
dev tie-back `37c8d27`(dev/top 內容一致驗畢)。spec closure `local 6e9092d`。
**分類=增量**:根 digest `2e50005d…e301` **三來源零位移**(交付兩個全新工作區 +
v0.2.49);`#advertise` 由 `#not_implemented` 變為有本體,而**此前不存在任何會送
`#advertise` 的客戶端**,故無原本可行者失效;跨版 `#fetch` 雙向實測皆通。
**行為變更**:REAL_02 §4.2 落地(公鑰內嵌、`listen_port`、`ts`、簽章簽在本體 CAID 上
加 `oodp-advert:v1:` 域分隔);`%ad` 入請求;`#rejected` 新設 + `%reason` 當且僅當;
新增 `oo node advertise`;對等點目錄(引擎本地,**本版不為任何取物路徑所讀**)。
**驗收代修=未認證的遠端任意效果**:`serve_advertise` 以求值 `%ad` 為第一個動作,早於
五道檢查——實測未帶簽章/金鑰/身分之封包令節點寫檔,而後才回 `#rejected #malformed`
(**裁決是對的,效果已經發生了**);修法為 AST 白名單置於求值之前 + 深度上限,
**線上位元組不變**。REAL_02 **§4.2.3 新設**規範之。
**未觸及**:GPP(REAL_02 §7 / APP_02 §6 / APP_05 §5 / SPEC_15 §7)另立討論。
**掛帳**:`read_line` 無上限(v0.2.48 既有);兩條算 CAID 路徑不一致未獲解釋;
引擎留有除錯測試 `mod advert_debug`。前版 v0.2.49=`7e951fa`。

**引擎 v0.2.49 定版(2026-07-27)=增量**:top `7e951fa`(squash 節點身分弧〔含一件驗收
代修〕+ oo 0.2.49 bump+lock 同入),故事提交 **"Two copies are two nodes"**,tag 於實測
commit(workspace **1543/0/3**、node_identity **13/13**、oodp 13/13、peer_fetch 13/13、
identity 16/16、store_boundary 20/20、cas 13/13、conformance **143/143**、genesis
**11/11** 皆於候選重測;條件閘一次成功 `GATE OK: repo=nlang-tools branch=top
head=7e951fa`;tag 後 touch build.rs 重建 `oo --version` = `oo v0.2.49` ✓ 無髒尾,
`git describe --exact-match` = v0.2.49)。dev tie-back `0608d29`(dev/top 內容一致驗畢)。
**分類=增量,由跨版矩陣所判**(非由掃描推之):新客戶端→v0.2.48 節點**通**(`%from`
為加法);v0.2.47 客戶端→v0.2.48 節點**不通**且**與移除舊式接受後完全相同** ⟹ 無任何
原本可行者失效。**行為變更**:`%from` 上線;`%source` 由 `node:<port>` 改為 node_id;
舊式裸 CAID 請求移除(回 `#conflict`);新增 `oo node id`;`OO_NODE_HOME` 覆寫。
**位址面零位移**。**與 #6 之關係**:本弧證明 v0.2.48 那條「相容面」從未相容,已於
REAL_02 §3.2 更正。前版 v0.2.48=`d430493`。

**節點身分弧(2026-07-27,裁定 Q1/Q2/Q3,**一件驗收代修**,REAL_02 **§4.1.1 新設** +
§3.2 更新、REAL_01 **§7.5.4 新設**;**增量**,已切 v0.2.49)**:
**承重量測**:`let source_id = format!("node:{}", port)` ——**節點用監聽埠號自我介紹**;
不同機器的同一埠號是同一個 `%source`,同一節點換埠即另一個;`%from` 根本不存在;
`ladd.rs` 的 `node_caid` 是誤稱(裝的是被廣告**值**的 CAID)。
**決定材質的跨弧約束**:兩個全新工作區同源 ⟹ **同一個根 digest**(v0.2.45 刻意做到),
故宇宙**不能**當節點位址(同宇宙的節點全擠一個 DHT 槽)。**讓宇宙可聯邦的性質,恰好
取消它作為節點位址的資格**——內容定址回答「是什麼」,節點位址回答「眾多持有者中的
哪一個」。⟹ 身分是**金鑰對**,`node_id` = 公鑰之 CAID,同時補上 §4.1「那是什麼東西的
CAID」之規格洞。
**裁定**:Q1 金鑰住 `~/.oo/nodes/<工作區絕對路徑雜湊>`,**路徑是身分的一部分**——
引擎**分不出搬移與複製**(只看到路徑改變),故令路徑參與身分使**複製在結構上即為另一個
節點**,不靠偵測、不靠啟發式、不必問人;代價=搬移即換身分。Q2 每個上網的工作區都是
節點,惰性鑄鑰,`%from` 恆帶。Q3(我方)節點金鑰與操作者金鑰**獨立**,歸屬**刻意相反**
(操作者屬人且明確否決每工作區;節點**正是**每工作區,因為節點就是工作區)。
**`%from` 是主張不是認證**(不簽名,任何人可填),故不得有任何判定依賴它。
**分類=增量,由跨版矩陣所判**:v0.2.48↔v0.2.48 通、新↔新 通、**新客戶端→v0.2.48 節點
通**(`%from` 為加法);而 **v0.2.47 客戶端→v0.2.48 節點 不通**(`⊥ #caid_mismatch`),
**與移除舊式接受後完全相同** ⟹ 無任何原本可行者失效。
**驗收方自陳之更正**:v0.2.48 我把裸 CAID 寫成「已申報且有期限的相容面」,並要求
**必須以新信封作答**——**該要求使它在構造上不可能相容**。**一個以新格式作答的過渡通融,
不是過渡通融。** 已於 §3.2 更正並附實測。
**一件驗收代修**:**節點金鑰的保護是意外的**——§7.5.3 早已要求私鑰在語言層邊界之內
**且保護不得依賴路徑恰好含 `.oo` 元件**;實測 `read_file` 對節點金鑰回 `#none`
(**是允許,只是解不開**),它讀不到只因 PKCS#8 DER 非合法 UTF-8,距離毫無保護只差一個
讀位元組的 builtin。改為拒絕節點金鑰**目錄**(與操作者金鑰之**路徑級**刻意不同:
`~/.oo/` 尚有他物而 `nodes/` 只裝金鑰),補釘 P8 含對照組。
**探針 5 紅 8 綠**(P8 為代修所補);A/B 對 v0.2.48 **五紅全紅、七釘全綠**。
**對抗全過**:複製工作區得不同身分、`OO_NODE_HOME` 相對路徑被拒、含空白與非 ASCII 之
路徑可用、損毀金鑰拒絕且位元組不變、**併發 12 行程 ×3 輪 ⟹ 一把鑰匙**、搬移後
`nodes/` 出現第二個檔(路徑導出確認)、操作者金鑰與節點金鑰兩檔兩內容兩公開 id。
**交付順手補上的衛生**:`peer_fetch` 的 `oo_raw` 先前未設 `OO_IDENTITY`,自 v0.2.46
起該suite會寫進開發者真正的 `~/.oo/` —— 我方 v0.2.46 未蓋到,交付一併隔離。
**數字(驗收方獨立重跑)**:workspace **1543/0/3**、node_identity **13/13**、
oodp 13/13、peer_fetch 13/13、identity 16/16、store_boundary 20/20、cas 13/13、
conformance **143/143**、genesis **11/11**。
**掛帳**:`#advertise`/`#discover` 上線與廣告簽章;Kademlia(§4);委任(節點金鑰由
操作者金鑰簽署);控制面。

**引擎 v0.2.48 定版(2026-07-27)=破壞性(Layer 1 — 協定),破壞性條目 #6**:top `d430493`
(squash OODP 封包格式弧〔含一件驗收代修〕+ oo 0.2.48 bump+lock 同入),故事提交
**"The node knew, and said nothing"**,tag 於實測 commit(workspace **1530/0/3**、
oodp **13/13**、peer_fetch **12/12**、cas **13/13**、universe_determinism 12/12、
identity_persistence **16/16**、privileged_effect **14/14**、conformance **143/143**、
genesis **11/11** 皆於候選重測;條件閘一次成功 `GATE OK: repo=nlang-tools branch=top
head=d430493`;tag 後 touch build.rs 重建 `oo --version` = `oo v0.2.48` ✓ 無髒尾,
`git describe --exact-match` = v0.2.48)。dev tie-back `cd3a32f`(dev/top 內容一致驗畢)。
**破壞面**:對等取物線上格式由「裸 CAID + 裸 JSON 或 0 位元組」改為帶 `%op`/`%status`
之信封;`oo serve` 退役改 `oo node serve`。**新客戶端送信封、v0.2.47 節點讀不懂**,
故為協定不相容(節點側仍接受過渡期裸 CAID,已入規格為有期限之相容面,不使本次降為
相容變更)。**位址面零位移**:值 CAID / 宇宙根 / commit CAID 皆不在此路徑(P3/P4 綠)。
**核心結果**:四向客戶端可分——值 / `⊥ #missing_key` / `integrity #mismatch:…source=` /
`⊥ #peer_timeout`;線上七種對抗輸入**無一得到沉默**。
**與 #4/#5 同日**,ORDER_00 §5.1.4 時鐘起算日不變(仍 2026-07-27)。前版 v0.2.47=`6848bff`。

**OODP 封包格式弧(2026-07-27,裁定 Q1/Q2,**一件驗收代修 + 一條驗收補述**,
REAL_02 §3.2 重寫 + TAG_REGISTRY §1.3 新設 `#peer_timeout`;**破壞性條目 #6**,
已切 v0.2.48)**:
**承重量測**:兩引擎**今天就對接得起來**(先前那次失敗是我自己用具名參數呼叫位置參數的
builtin,同 v0.2.39 形狀);壞的是對等點交不出位元組時它有什麼可說的——
**未持有 → 0 bytes、持有但腐敗 → 0 bytes、接受後不回話 → 掛到被殺**。伺服端**知道**是
哪一種(它 log 了 `NDP Miss`,v0.2.44 起還 log `NDP integrity #caid_mismatch`),線上一
個字都不說。**線上的沉默是四件事**=REAL_03 §6.6 條款三往外一層,而 v0.2.44 明寫
「線上維持 0 bytes(留給 REAL_02 §3.2 弧)」。
**第二件量測(未預期)**:**LADD 已經實作了**——`ladd.rs` 的 GBB(mass/sketch/masa/nerve)、
`disc.advertise`、`disc.find` 都是真程式,但全部讀寫**行程內的 `RwLock<HashMap>`**。
⟹ **LADD 是實作成單機模擬的,封包格式就是把它變成分散式的那一步**;故信封第一天就帶
`%op`,另兩個 op 之後是增量而非二次破協定。
**裁定**:Q1 節點身分與 `%from` 屬**下一弧**(fetch 不需要知道誰在問,物件自驗證;
`%from` 真正承重在 `#advertise`/`#discover`);**注意其配置與 v0.2.46 相反**——操作者
金鑰屬人且明確否決每工作區,節點金鑰屬每個 `.oo/` 正因為**節點就是工作區**,且由此帶出
未裁定問題「複製倉庫=複製節點身分」。Q2 改名同刀收:**改名不花破壞性條目**(已量:
Layer 1 = 語義/文法/**協定**,REAL 之規範性為引擎互通,本機子命令拼法不涉),而協定這
一刀必砍,故讓對接方只跟一次。`oo node serve` **有出處**——REAL_01 §1.2 本就稱其為
**宇宙節點 (Universe Node)**,名詞一直在規格裡、從未有 CLI 拼法(用戶指出)。
**探針 5 紅 7 綠一次校準到位**;A/B 對 v0.2.47 **五紅全紅**(P8 亦紅=代修之記錄)。
Harness 有一處必要讓步並於檔頭聲明:命令名於同弧變更,故啟動器先試 `node serve` 再退回
`serve`,**只為使線上諸門在改名兩側皆可測**,名字由 R5 單獨決定。
**一件驗收代修**:**逾時標籤重用**——交付沿用既有 `BottomCause::Timeout`,而該碼自始
表示**本地運算**超出 `%timeout`,TAG_REGISTRY 給它的補救是「優化性能、減少嵌套、放寬
時限」,**對「對端握著連線不回話」而言那句話指向讀者自己的程式**。**一個以「四件事必須
可分」為全部論旨的弧,不能出貨第五件不可分的事**;新設 `#peer_timeout`(§1.3,障礙度數
與 `#timeout` 同列視界層,append-only 尾端故不動既有 CAID),REAL_02 四向表同步改,補釘 P8。
**一條驗收補述**:實作仍接受信封之前的**裸 CAID 行**,交付未將其當成決策申報;經量測
確認後入規格為**已申報且有期限**的相容面(移除隨節點身分弧),理由是一個概念兩種拼法
正是本規格反覆退役的東西。反向不相容仍成立,故不降為相容變更。
**線上對抗全過**:舊裸 CAID / 已知未實作 op / 非已知 op / 缺 `%hash` / 壞 CAID / 截斷 /
空行——**七種輸入無一得到沉默**,且 `#not_implemented`(已知未實作)與 `#conflict`
(根本不是已知 op)分得開。四向客戶端實測:值 / `⊥ #missing_key` /
`integrity #mismatch:…source=` / `⊥ #peer_timeout`。
**掛帳**:狀態集無專屬「請求格式錯誤」碼,malformed 一律 `#conflict`(判定危害低——
malformed 是客戶端自己造成的,它從自己這側就知道);`#discover`/`#advertise` 上線;
Kademlia(REAL_02 §4)。
**流程記帳(驗收方之錯)**:本弧工單把 **D5 規格改動寫進了交付範圍**,於是**由實作方
撰寫了替自己的變更分類的 CHANGELOG 條目**——與 v0.2.45「由被檢查者供給檢查名單者,其
檢查恆真」同形,低一層。內容經獨立核對屬實故保留並增補,但**常設律新增:規格收尾
(尤其 CHANGELOG 分類條目)不得進入交付範圍**。

**引擎 v0.2.47 定版(2026-07-27)=增量**:top `6848bff`(squash `#privileged_effect`
弧〔含三件驗收代修〕+ oo 0.2.47 bump+lock 同入),故事提交
**"A number that used to be a clock"**,tag 於實測 commit(workspace **1517/0/3**、
privileged_effect_audit **14/14**、universe_determinism **12/12**、
identity_persistence **16/16**、store_boundary **20/20**、pin **15/15**、
history_ops **15/15**、conformance **143/143**、genesis **11/11** 皆於候選重測;
條件閘一次成功 `GATE OK: repo=nlang-tools branch=top head=6848bff`;tag 後 touch
build.rs 重建 `oo --version` = `oo v0.2.47` ✓ 無髒尾,`git describe --exact-match`
= v0.2.47)。dev tie-back `b121157`(dev/top 內容一致驗畢)。
**分類=增量**,且係**先問「根會不會動」才下**(上一弧之教訓):A/B 對 v0.2.46
二進位,根 digest **3 種來源 0 位移**、一般提交元資訊鍵集與 kind 兩側相同、
一般值金 CAID 綠;`CommitMeta` 新欄位遵循手寫 `Debug` 缺席即省略之模式 ⟹
**既有 commit CAID 零位移**。全樹掃描乾淨(`--grant commit` 零使用;語料唯一
`runPure` 為 conformance L2/103 之未授權案例)。
**行為變更**:提交固化特權放行之內容須重新出示涵蓋其標籤之能力(新守護);
`--grant commit` 拒絕(退役拼法);`oo log` 之提交訊息改逐行加 `message: ` 前綴。
前版 v0.2.46=`ed15cc2`。

**`#privileged_effect` 弧(2026-07-27,裁定 Q1/Q2,**三件驗收代修**,
REAL_01 **§7.0 新設** + §7.3 補適用條件 + SPEC_08 §6.2 補三條;**增量**,
已切 v0.2.47)**:
**本弧不是佇列上寫的那一項**。原訂 REAL_01 §7.2 令牌+CRL;量測顯示**那把鎖沒有門**——
唯一能發動特權的是 CLI 由工作區擁有者親自呼叫、`oo serve` 唯讀、REAL_01 §2 整套
JSON-RPC 未實作故 §2.6 無對象、`oo repl` 不吃授予;且 SPEC_08 §6.3.3 已明文對帶外
竄改不提供保證,而擁有者正是帶外能力者。**更關鍵:§7.2 的 ≤24 小時持有者令牌比現行
機制更弱**(逐次出示的參數不留存,不留存者不會外洩),而引擎實際在用的機制在 §7 中
一字未提。**裁定 Q1**=令牌屬服務面、本機面之逐次出示寫入 §7.0.1 成為規範。
**「量測否決弧」第二例**(首例 `#ext:`)。
**量測找到的是從未被滿足的既有規範**:`evolve --grant effect_override:io` 後
`commit` **不帶任何能力**即成功,宇宙裡是 `v: 1785130396317`(一次 `~%Time.now`
被洗成整數),commit `kind=Standard`、元資訊僅 author/timestamp/message;對照組
(同源、evolve 不帶授予)提交 `v: ⊥ #privileged_required`。且放行來的 42 與手打的
42 **同一個 CAID**——這是對的,也正是 §6.2 把審計放 Commit 的原因。**裁定 Q2**=
提交期重新出示能力 + 標 `#privileged_effect`。
**三件驗收代修**:(1)**標記仍可偽造**——交付只為訊息**首行**加前綴,實測
`-m $'x\n    privileged_effect\n    pin'` 在無任何能力下使後兩行與真標記**逐位元組
相同**;**訊息不是一行**,改逐行加前綴並把 §6.2 審計可查驗性推廣為「使用者所能供給
之全部文字」。(2)**出示某個能力不等於出示該能力**——閘只問 `effect_override` 存在
與否,故放行 `io` 者可用 `--grant effect_override:nondet` 通過,而該能力當初根本
無法授權該放行(§6.1.4 軸二);改為 `.oo/effect_pending` 攜**標籤集**並於提交期檢查
涵蓋。(3)**標記了未曾發生的干預**——`runPure` 施於本已純的值不覆寫任何效果,交付
仍要求能力並蓋標記;§6.2 定其為「強制將**含副作用**節點標記為 `#pure`」,無效果即
無可強制。三條皆入規格。另**還原**交付縮掉的 run_log 註解(記錄該處為何是 `match`
而非 `if let Ok`——REAL_03 §6.6 條款四之棄判決形狀)。
**探針 5 紅 7 綠一次校準到位**;A/B 對 v0.2.46 二進位**五紅全紅**(P8 亦紅=代修之
記錄;**P9 在 v0.2.46 為綠,因其所擋之缺陷係交付引入,本就不可能是 A/B 紅**)。
**驗收方自強化探針**:R4 補多行訊息(我原本只試單行,才讓它漏到對抗階段才被抓);
`pin_commit_meta_debug_omits_absent_fields` 改為斷言**整串 Debug 渲染**而非逐欄位
點名——本弧正好示範了為何:字面值為了編譯必須補上新欄位,而斷言仍只認得 `abandoned`。
**分類=增量**:A/B 根 digest **3 種來源 0 位移**、一般提交元資訊鍵集與 kind 兩側
相同、一般值金 CAID 綠;依 v0.2.42 判例(新守護 + 全樹掃描無既有此形),掃描乾淨
(`--grant commit` 零使用;語料唯一 `runPure` 是 conformance L2/103 之未授權案例)。
**本次先問「根會不會動」才下分類**(上一弧之教訓)。
**數字(驗收方獨立重跑)**:workspace **1517/0/3**、本弧探針 **14/14**、
universe_determinism 12/12、pin 15/15、history_ops 15/15、runpure 6/6、
selective_discharge 15/15、conformance **143/143**、genesis **11/11**。
**掛帳**:服務面本身(REAL_01 §1.2/§2)及隨之的令牌/CRL/`.oo/audit.log`;
`oo evolve` 無 `--privileged` 而其餘子命令皆有之不對稱。

**引擎 v0.2.46 定版(2026-07-27)=破壞性(Layer 1),破壞性條目 #5**:top `ed15cc2`
(squash 身分持久化弧〔含三件驗收代修〕+ oo 0.2.46 bump+lock 同入),故事提交
**"The operator gets a name"**,tag 於實測 commit(workspace **1503/0/3**、
identity_persistence **16/16**、universe_determinism **12/12**、store_boundary **20/20**、
cas **13/13**、peer_fetch **12/12**、conformance **143/143**、genesis **11/11** 皆於候選重測;
條件閘一次成功 `GATE OK: repo=nlang-tools branch=top head=ed15cc2`;tag 後 touch build.rs
重建 `oo --version` = `oo v0.2.46` ✓ 無髒尾,`git describe --exact-match` = v0.2.46)。
dev tie-back `d0b9d79`(dev/top 內容一致驗畢)。
**破壞面**(三項,已於 CHANGELOG 逐條列):`~%Official./sign_refine` 自語言表面移除
(→ `⊥ #missing_key`),`~%Official` 保持掛載而成為空模組;**新建宇宙之根 CAID 位移**
(歸因實測:對 v0.2.45 二進位,兩根整體 inspect 對 diff **僅 9 行相異、全落在 `~%Official`
那一段**);供給了白名單之倉庫的 `--sign` 由恆遭拒絕變為可通過(放寬)。
**不受影響**:一般值 CAID(`identify_and_store` **7 種形狀 0 位移**,含空的開放與閉合
combo 及巢狀)、既有倉庫(v0.2.45 所建者實測 log/status/evolve/commit 皆正常)、
genesis 種子、conformance 143/143。
**核心結果**:白名單首次成為**可被滿足**的檢查——操作者以 `oo identity` 取得自身公鑰、
帶外置入名單,`--sign` 得 `verified`;名單不含該鑰者仍被拒(成對判別兩面皆實測)。
**與條目 #4 同日**,故 ORDER_00 §5.1.4 之 90 天時鐘起算日不變(仍為 2026-07-27)。
前版 v0.2.45=`fe5d4d1`。

**身分持久化弧(2026-07-27,冷啟動第二步,裁定 Q1/Q2/Q3,**三件驗收代修**,
REAL_01 **§7.5 新設** + SPEC_08 §6.3.1/§6.3.2 各補一條 + SPEC_10 §93 補「名單必須是可滿足的」;
**破壞性條目 #5**,已切 v0.2.46)**:
**承重量測**:把行程 1 的公鑰供給進 `.oo/architects.json` 後,`#refine` **兩個方向皆被拒**
(帶 `--sign` 得「簽署者不在名單中」,不帶得「非引導期缺 `%authority`」)——**沒有任何值可
寫入該檔案而此引擎會出示之**。§93 的權威判定分支**自始未曾被滿足過一次**:條目 #4 之前是
自任讓它恆真,之後是無鑰讓它恆假。**無法被滿足的名單不是更嚴格的名單,是同一個檢查**;
兩者皆為恆定值,只是常數不同。這正好證成佇列順序——**A 拆掉謊言,B 才讓真話可達**。
**第二件量測**:`~%Official./sign_refine` 於無任何授權下即可由普通 n/ 程式取得真實 Ed25519
簽章(效應僅 `#io`);`~%Official` 只有這一個鍵,且 n/ 層無任何建立 refine commit 之介面
⟹ 該 builtin 唯一能做的事就是把簽章交出去。**今日無害只因鑰匙不值錢,持久化正是把它上膛的
那一步。**
**其餘基線量測**:身分逐行程新鑄(同工作區三行程三把鑰匙)、`.oo/` 內零金鑰材料、
n/ 讀 `~/.oo/*` 已被 v0.2.42 邊界擋下(對照組可讀)、引擎完全不讀 `$HOME`、
身分在全引擎僅兩個消費點且皆為簽署。
**裁定**:Q1 身分屬**操作者**住工作區之外(`.oo/objects` 是設計來被取用與複製的成品,
秘密不得住在其中;ORDER_01 §7.1 的 `@Voter` 帶 weight/alias,那是**人**);
Q2 首次需要簽章時鑄造並持久化(**金鑰是名字,權威來自宣告;引擎得造名字,不得造宣告**
= 條目 #4 之度數分離高一層);Q3 `/sign_refine` **退役**(同 v0.2.42 判例),否決能力格
(`--grant` 是行程啟動時的意圖,簽章在求值中任意時刻,兩者間無可信通道 = v0.2.40 判例)。
**探針 8 紅 6 綠一次校準到位**;A/B **由構造成立**——校準時的引擎程式碼與 v0.2.45 tag
`git diff` **逐字元相同**,故 8 條紅門訊息即 v0.2.45 之行為,不必重建二進位。
**驗收方自改既有探針三處**:`store_boundary` 與 `universe_determinism` 共三個控制項原以
`/sign_refine` 當模組存活控制,退役會使其成為給交付的**假紅**,故由驗收方改寫並在工單
言明。改寫時另抓到**我自己的控制項是空洞的**:原寫「不是 ⊥」,而實測**模組被整個移除會得
`_`(Top,系統根是開放的)不是 `_|_`** ⟹ 該控制項會為「模組消失」放行,根本不是控制項;
三處一律改為斷言 `{{`。
**三件驗收代修**:(1)**併發首次鑄鑰使操作者拿到錯的鑰匙**(8 行程 ×3 輪 ⟹ 3 把鑰匙、
每輪 2 個行程印出不在檔案裡的公鑰);成因=「先寫暫存檔再改名取代」無條件覆蓋,且其註解
宣稱「敗者改讀勝者之檔案」而程式碼僅於寫入**出錯**時才重讀 ⟹ **描述了程式碼沒有的保證的
註解,即會說謊的審計面**(v0.2.41 判例)。改為原子性宣告路徑、檔案自建立即 `0600`;
共用且可預測的暫存路徑一併消失(該路徑既非 `.oo` 亦非身分檔,實測語言層讀得到)。
(2)**引擎變更操作者自有目錄之權限**(既有 `0750`→`0700`、刻意唯讀之 `0500`→可寫);
改為僅於引擎**建立**該目錄時設定。(3)兩者補綠釘 P7/P8;12 行程 ×5 輪 ⟹ 一把鑰匙。
**附帶修正**:空閉合 combo 原渲染 `{{ }` 無法回讀;因退役使 `~%Official` 成為系統根中第一個
空閉合 combo 而可見,故一併修。**`to_nlang` 在雜湊路徑上**(`Value::Thunk` 之 content_hash
與記憶鍵),故以 A/B 實測確認未動任何值 CAID,而非以「僅屬外觀」帶過。
**歸因量測(決定分類)**:根 CAID 位移。對 v0.2.45 二進位 A/B,兩根整體 inspect 對 diff
**僅 9 行相異,全部落在 `~%Official` 那一段**;`identify_and_store` **7 種形狀 0 位移**
(含空的開放與閉合 combo 及巢狀);v0.2.45 所建倉庫實測 `log`/`status`/`evolve`/`commit`
皆正常。
**驗收方自陳**:工單原預期分類「增量」,條件寫成「全樹掃描無既有此形」。該條件治的是
**程式**會不會壞(掃描確實乾淨),**治不了位址會不會動**——移除宇宙根的成員必然移動根 CAID,
與有沒有人用過那個拼法無關;條目 #4 正是同一形狀。**是量測改了結論,不是推理。**
**數字(驗收方獨立重跑)**:workspace **1503/0/3**、identity_persistence **16/16**、
universe_determinism **12/12**、store_boundary **20/20**、cas **13/13**、peer_fetch **12/12**、
conformance **143/143**、genesis **11/11**。
**掛帳**:既有宇宙遷移;冷啟動第三步(REAL_01 §7.2 令牌生命週期/CRL,引擎完全未讀);
金鑰輪替;對等節點身分(不可否認性,與簽署身分為兩件事)。
**本弧途中量到之既有掛帳(非本弧造成)**:`oo <任何子命令> | head` 會印出 Rust panic
(`failed printing to stdout: Broken pipe`)——Rust 預設忽略 SIGPIPE,故 `println!` 對
已關閉管線 panic;`log` 與 `identity` 皆實測命中,全引擎共通。管線接 `head` 是再尋常
不過的操作,而使用者看到的是 panic 而非靜默結束。

**對等取用位址驗證弧(2026-07-27,裁定 Q1/Q2,**兩件驗收代修**,SPEC_13 §6.1.1 新設)**:
**選弧理由**:REAL_03 §6.6 是**前一日**才寫進規格的,條款一寫「以 CAID 取得內容的
**每一條路徑**」、§6.6 非規範註記逐字點名「**對等取用**」是熱路徑之一——昨日入法的
MUST,引擎當下就違反。**合規缺口,不是規格變更**;排在既有掛帳的型別層急切展開之前。
**承重量測**:`remote_fetch`(`lib.rs:2249`)開 socket、寫出請求的 CAID、讀位元組、
`serde_json::from_slice`、`Ok(val)`——**請求的 hash 用來問,之後再也沒用過**。實測兩次:
(a) 對全零 CAID(從未存在的位址)請求,對等點回 61 bytes 捏造 JSON,程式拿到
`"ATTACKER_CONTROLLED_NEVER_EXISTED"`;(b) 問 `a80f42…` 拿回 `b80f42…` 的真實物件。
**任何 CAID 都能被任何已連線的對等點解析成任何內容。** v0.2.43 加固了本地庫——位元組
至少是自己的那個地方——放著位元組完全不是自己的網路路徑不驗;該版故事提交叫
「A path is not an identity」,而 **socket 就是 path**。
**地板疊在地板上**:SPEC_13 §7.2 的語義日蝕防禦要求引擎**主動**在信任格**之外**取用
(隨機跳出 1/64)。那只有在格外位元組能自我認證時才是加固,否則不是防禦,是把通道
交給不受信任的節點。REAL_02 §3.1 更直接把「來源不影響收斂結果」當**事實**斷言,
而引擎讓這句話是假的。
**裁定 Q1(用戶提問「peer1 和 peer2 是對等的還是偏序的」,未選項而指出真問題)**=
兩者皆是,在不同度數上:**偏序在「哪個 CAID」**(§7.1 信任偏序治理**別名**衝突、
挑的是名字解析到哪個身分 = 度數 ≥1 的權威與意義);**對等在「這個 CAID 的位元組」**
(度數 0 的驗證**自我認證**,信任最低之節點交出位址正確的位元組,與最高者所給逐位元
相同)。⟹ 說謊之來源跳過並續問;`⊥ #caid_mismatch` 只在無來源交出可驗位元組時出現;
裁決永不沉默丟棄。**config 旋鈕否決**:旋鈕得治可用性政策,不得治驗證是否發生或裁決
是否浮現(可關閉之 MUST 不成其為 MUST;且使語言可見結果取決於引擎本地設定 = R2 帳)。
**裁定 Q2 範圍 = D1–D5**:D1 網路不驗〔條款一〕/ D2 `oo serve` 把竄改報成 `NDP Miss`
〔條款三**逐字**〕/ D3 `disc.fetch`/`find` 五處使竄改≡缺席≡`⊥ #conflict`〔條款三〕/
D4 shadow 掃描靜默截斷〔條款四〕/ D5 `main.rs:417`。**明確排除並掛帳**:REAL_02 §3.2
封包格式、信任偏序實作、隨機跳出、絕對缺席的 `⊥ #conflict` 因由。
**探針 12 支**(6 red 全紅且**紅得對** + 6 pin);**兩組成對判別**:R5 基線 `Shadow: 2`
→ 竄改三個位元組後 `Shadow: 1`,措辭不變無警示(= v0.2.43 refine 判例再一次);
R6 **10 跑 6 次回傳說謊者的值**且兩個說謊者都贏過 ⟹ 實證 `peers` 是 `HashMap`、
迭代序逐行程變動、現行 fetch 結果**不決定**,而**驗證正是使無序對等集變安全的那樣東西**。
**四數**:workspace **1475/0/3**、peer_fetch 探針 **12/12**、conformance **143/143**、
genesis **11/11**;**位址零位移**:對 v0.2.43 二進位對跑 **25 種值形狀 0 位移**
〔**更正 2026-07-27**,原記「全語料 143/143 逐字相同」係空洞量測——見弧紀錄末〕。
**A/B**:代修後把探針搬回 v0.2.43 worktree,6 紅仍全紅、6 pin 仍全綠 ⟹ 門量的是交付
不是測具。
**驗收代修二件**:(1) **shadow 截斷記了互相矛盾的裁決**——依真實 kind 記一筆後,又以
**寫死的 `Mismatch`** 對同一位址再記一筆,致 `#object_undecodable` 造成之截斷被端成
`#caid_mismatch`;§6.6 條款三 要的正是三者可分,**主動宣稱錯的那一個比漏報更糟**
(同 v0.2.41 squash「無法憑檢視查驗的審計面不成其為審計面」,此處更進一步:審計面
在說謊)。改為單一紀錄、真實 kind、明說截斷。(2) **`oo repl`(工單 §4.4 逐字點名)
與 `oo eval`／`oo test` 未排空裁決紀錄**——條款四**不因裁決進了「值」而滿足**:
一來源說謊、另一來源答對時,值是對的,紀錄是謊言的唯一痕跡;`oo test` 須逐檔排空
且在 summary 之前,因該函式失敗時 `exit(1)`。
**交付品質**:diff 純度合格(探針只少 6 個 `#[ignore]`,工單只多一節交付紀錄);
`value_address_matches` 依工單復用未另寫比較器;`BottomCause::CaidMismatch` 走尾端
追加;未動 nlang-spec。
**分類=增量**:語言表面新增可分辨結果(原為 `#conflict` 之壓平),依 `#effect_violation`
判例;**全樹回歸掃描**(未截斷):僅 4 個 `.n` 用到 fetch/find(皆健康庫,其二在
`tests/pending/`)、合規向量零使用、無測試依賴 fetch 路徑之 `#conflict`。
**spec closure**:SPEC_13 **§6.1.1 新設**(來源在度數 0 上對等不得排序/語言表面三結果/
裁決不因取用成功而消滅/驗證不得為可組態)、TAG_REGISTRY §1.3 `#caid_mismatch` 補述
語言層 `%cause`、CHANGELOG 增量。**本弧無新增合規向量**(需真實 socket 與被竄改之庫,
非密閉)。工單 `nlang-tools/docs/peer_fetch_verification_handover.md`。
**本弧量到之掛帳**:**L1 stored 值帶未強制 thunk 與原始碼 span**——committed root 把
字面欄位存成帶 `span:{start,end}` 的 `Thunk`,兩後果皆實測:(1) shadow 掃描**只可能**
對上已強制的欄位(字面值來源恆得空報告);(2) **身分被排版污染**——同語義、只差兩空行
與一註解的兩份原始碼,`lattice_sketch` **完全相同**而 `content_digest` **不同**:譜特徵
認得出是同一個幾何,內容指紋不認得;REAL_03 §7.1 規定雜湊遍歷餵入「型別標籤、名稱與
譜特徵」,span 三者皆非。(須比**根值** CAID;commit CAID 含 `CommitMeta` 時間戳,必然
不同,證不了事。)與既有掛帳**型別層急切展開**相鄰——一個太急一個太惰,同一個問題:
**store 裡到底是什麼**。**L2 NDP 未實作 REAL_02 §3.2** 封包格式(規格 `{{ %op %hash
%from }}` / `%status`+`%result`+`%source`+`%hops`;實際裸 CAID 進、裸 JSON 出);
規格的 response 本就有可承載驗證裁決的 status 詞彙。**L3 `remote_fetch` 無讀取逾時**
(`connect_timeout` 有,`read_to_end` 無)——**實測**:對等點接受連線後永不回應,
`oo run` 無限期停住(25 秒後由外部砍掉)。單一惡意節點即可掛住取用。可用性非本弧的
驗證主題,但同屬對等信任面。

**更正與後續發現(2026-07-27,v0.2.44 切版後)**:本弧驗收所稱「**位址零位移**=對 v0.2.43
二進位逐一對跑全語料 **143/143 逐字相同**」係**空洞量測**——比較腳本取 `content_digest`,
而 commit 之 root 鍵名實為 `digest`,兩側每次皆得 `None`,故 143/143 恆等而**什麼都沒量到**。
**這是驗收方(我)自己犯下五弧來一直在校準的那一類錯誤,且是綠的方向。**
**重量(誠實)**:改比**值**的 CAID——25 種值形狀 **0 位移、0 測具失敗**,其中 **7 種攜 ⊥ 之值**
(`1/0`、`1&2`、繭合併違規、巢深 ⊥、`~%Io` 失敗等)直測 `BottomCause::CaidMismatch` 尾端追加之
唯一風險;genesis 11/11 含 `seed_caids_are_stable`;conformance 143/143 行為等價。
**增量之結論不變,證據更換**。且查明:語料層的**根**位址本就不可比——見 L4。

**L4(新,2026-07-27 實測)——宇宙根的 CAID 逐行程不決定,因為引擎身分被烘進了根**:
同一份原始碼、6 個新倉庫、6 個行程 ⟹ **6 個不同的根 digest**;對照組(`identify_and_store`
一般值)6 個行程 ⟹ **1 個**。經 key-order 正規化比對兩根,唯一實質差異是
`~%Official.data.architects` 之字串(`dc6dc995…` vs `0314c0f8…`)= **`Identity::new_random()`
每次引擎啟動所鑄之隨機身分**。故**雜湊沒錯,內容真的不同**——錯的是**一個隨機數是宇宙的
一部分**。**違反 SPEC_13 §4.1.2 規格義務 #1**(「相同的內容在相同的格式版本下,產生的 CAID
**必須**全宇宙唯一且決定」)。**後果**:兩個引擎讀同一份原始碼永遠得不到同一個宇宙身分 ⟹
根層級的聯邦、commit 互認、跨引擎共享在原則上不可達;既有掛帳「身分持久化」與此為同一件事
的兩面(持久化只解決「跨行程誰說的」,不解決「隨機值不該在宇宙裡」)。
**旁測**:`oo fmt --write` 後重提交,根 digest 改變而 `lattice_sketch` **完全相同**;惟此差異
被 L4 掩蓋(根本每次都不同),故 **`oo fmt` 是否真的不保身分,須待 L4 修好後方能判定——
尚未證實,不得據以行動**。
**同批量測(型別層急切展開,原佇列首位)**:成長律為**線性且不相乘**——遞迴型別 1/2/3 個
分別 +8,533 / +17,072 / +25,599 bytes,且 `@B: { a: @A, … }` 嵌套**不複合**(+17,066 = 2×)。
每個遞迴型別固定約 2 KB(壓縮後,展開 3 層、JSON 深度 17)。**降級為常數浪費**。真正的重量
在**基線根 251,841 bytes**:壓縮後約 77 KB,其中 `system` 70,983(26 個創世模組)+ `types`
5,918 = **92% 是每個倉庫都逐位元相同的創世內容**;磁碟 3.3× 膨脹來自**縮排**(序列化用
pretty-print)。三者(急切展開/創世重複/縮排)皆為儲存量問題,與 L4 之身分問題不同層。

**引擎 v0.2.43 定版(2026-07-26)=增量**:top `e217d3a`(squash CAS 讀路徑位址驗證弧
〔含一件驗收代修 + 一支探針由驗收方自修〕+ oo 0.2.43 bump+lock 同入),tag 於實測
commit(workspace **1463/0/3**、conformance **143/143**、cas 探針 **13/13**、
store_boundary **20/20**、genesis **11/11** 皆於候選重測;條件閘一次成功;tag 後
touch build.rs 重建 `oo --version` = `oo v0.2.43` ✓ 無髒尾)。dev tie-back `736e310`
(dev/top 內容一致驗畢)。**增量**:**位址零位移**(genesis 與全語料重測逐字不變,
既有完好倉庫行為不變);觀測面變動僅及**已被竄改或無法解碼**之物件(原靜默回傳→
具名拒絕)與 `oo run` 不再自動入庫(該迴圈零依賴,實測停用後全綠)。前版
v0.2.42=`3aa5710`。

**CAS 讀路徑位址驗證弧(2026-07-26,裁定 R-1~R-4,**一件驗收代修 + 一支探針由驗收方自修**,REAL_03 §6.6 新設)**:
**量測起因**:`oo inspect` 印出 CAID 與譜特徵,然後端出**不是那個身分**的值——就地
改寫物件位元組(檔名即 digest 不動),同一命令同一 CAID,輸出由 `b: "two"` 變
`b: "XXX"`。同族:竄改 commit 本體後 `oo log` 當真跡走;**digest 為真、sketch 偽造**
的 CAID 解析到真物件(路徑僅由 digest 導出,正是 §9.2 描述的縫);masa_ref 同理。
**開弧前量測(可否決本弧的那件)**:若既有物件重算位址不等於檔名,開啟驗證等於當場
砸掉所有倉庫——全合規語料 143 向量灌入單一庫逐物件重算,**125/125 可解析物件穩定**。
另確認儲存定址用**無鹽** `content_hash()`(`SystemTime` 鹽只餵 lib.rs:1889 觀測面
`%id`),`#blur` 不致位址不確定;**commit 為 v1(無 sketch)、值為 v2**,故驗證範圍
天然分流。
**量到的第二件(重塑本弧)**:126 個物件中**有一個根本無法解碼**——5,091,205 bytes、
JSON 深度 **646**、超過反序列化預設上限 128;來源是 **shipped 且綠燈**的合規向量
`L2-20`,**預設配置**,兩行即可觸發。二分定位:只需型別定義,不需 meet 不需導航;
且分成兩段——`evolve+commit` 給 260 KB/`next`×3/深度 20(讀得回),**`oo run` 給
5.09 MB/`next`×128/深度 646(讀不回)**。差的 20 倍來自 `run_one_shot` 的 store-put
迴圈(`observe` = 強制固化)。**違反 SPEC_04 §158**(導航保持惰性、**不得**為吸收
強制固化 union,條文**逐字點名** `@Tree | ()`)與 **SPEC_12** `#recursive_lazy`。
規格早已寫死,故為 bug 非設計。(觀測 `@Tree` 本身 5 分鐘不終止——§158 那句「否則
發散」不是假設語氣,只是沒有向量站在那個位置;L2-20 標題為「遞迴型別**終止**」、
觀測 `t.v`,測的是終止性且確實成立。**惰性才是沒有任何向量測的那條**。)
停用迴圈實測:workspace 1450/0/3、conformance 143/143、不可讀物件消失、**零依賴**。
**裁定**:R-1 本弧=驗證+迴圈,**型別層急切展開上帳**(用戶);R-2 迴圈**移除**而非
改惰性(`oo run` 契約為 one-shot **純**宇宙,寫持久儲存屬範疇錯誤;其產物為建構上
的孤兒即 GC 弧要掃的垃圾;零依賴;能力本就有 `~%Engine./save`——**讓它明說而非自動**,
同 `#squash` 弧對遺忘的裁定);R-3 值驗**全 v2**(digest+sketch+masa_ref,承 §9.2
譜引擎條款);R-4 **三種結果非布林**(verified/`#caid_mismatch`/`#object_undecodable`,
今日 `run_inspect` 把三者全壓成 "CAID not found")。後三為驗收方裁量,明列供否決。
**探針校準**:8 red + 4 pin;**一支第一版假紅**——只斷言「三結果兩兩不同」,而
**缺陷本身即滿足**(corrupt 靜默回傳被竄改的值、absent 報 not found),改為釘住每個
結果的**形狀**。連續第五弧同類,連續第五次因查「為什麼紅」而非「有沒有紅」抓到。
**交付首次回報驗收方錯誤而未遷就**(此前兩例皆為交付遷就:v0.2.39 `ContentHash::parse("_")`、
v0.2.42 `disc.connect` 的 `remote:`):`red_a_run_does_not_force_*` 我寫「最大物件
< 100_000」**量錯對象**——探針自己的 `seeded()` 就留下 **251,839 bytes** 的 committed
root(創世系統模組,即 R-1 上帳的型別層重量,比本弧老),故缺陷修好門仍紅。獨立
複驗其數字後,改為斷言**跨 run 的 delta**(更精準且更強:**純 one-shot 宇宙必須對
持久儲存零新增**),並開 worktree 對 **v0.2.42 A/B** 確認**修好的門在基線仍紅**
(`before 2, after 4`)。**本次零退回成本。**
**驗收代修(竄改可買到 refine 單調性跳過)**:按工單要求列全每個 `get_value`/
`get_commit` 呼叫點後抓到——`refine` 步驟 1 為 `if let (Ok, Ok)`,**任何**載入失敗
皆靜默跳過幾何檢查。成對判別:未竄改的違反方向被 `new ⋢ old` 拒;**改幾個位元組後
同一方向穿過步驟 1**,只在授權關才停。**關鍵區分:§9.1 不透明模式適用於「引擎算不
出來的 CAID」,不適用於「會說謊的位元組」**;缺席可跳,損毀不行。已改三分類分流,
新增驗收門 `acceptance_corruption_does_not_buy_a_refine_monotonicity_skip`。
**其餘同類已全數列舉、明確劃界(非默默修一個)**:`universe.rs:831/835`(shadow scan
報告靜默截斷)、`disc.rs:133/146/158/312/323`(peer fetch/find,損毀對使用者顯示為
不存在;NDP 供給原樣)、`main.rs:225/417`。皆為「本弧使損毀可偵測,而這些地方丟棄
偵測」;無一如 refine 經實證可利用,而改動 discovery 錯誤語義跨五個呼叫點,另裁。
**四數**:workspace **1463/0/3**、conformance **143/143**、genesis **11/11**、
cas 探針 **13/13**、store_boundary **20/20**。
**過程記錄**:交付自行提交了 TAG_REGISTRY(spec `8c10bd4`)——內容正確且命名確由我請
其提出,但**規格收尾屬驗收方步驟**,我的工單此點含糊;另 `#caid_mismatch` **本就存在
於規格**,我工單稱其為新增係我方之誤。
spec closure:REAL_03 **§6.6 新設**(重算義務/驗證範圍/三結果可分/消費端不得丟棄裁決/
位址不得位移 + 快取不得以被驗證物本身為鍵之非規範註記)、§8 錯誤表補兩碼、TAG_REGISTRY
§1.3、CHANGELOG 增量。**本弧無新增合規向量**(runner 不涉庫竄改,CLI 探針為法定測具)。
工單 `nlang-tools/docs/cas_integrity_handover.md`。
**掛帳**:**型別層急切展開**(evolve 期 260 KB/`next`×3,惰性表示應為數百 bytes;
觸及型別合一與可能之 CAID/向量,另一量級的弧);discovery 五處等丟棄裁決之呼叫點;
GC(**須純本地**);身分持久化;`.oo` 比對大小寫不敏感 FS 未測。

**引擎 v0.2.42 定版(2026-07-26)=增量**:top `3aa5710`(squash 儲存信任邊界弧
〔含一件驗收退回 + 一支驗收方自修既有探針〕+ oo 0.2.42 bump+lock 同入),tag 於
實測 commit(workspace **1450/0/3**、conformance **143/143**、store_boundary 探針
**20/20**、pin 探針 **15/15**、genesis **11/11** 皆於候選重測;條件閘一次成功;
tag 後 touch build.rs 重建 `oo --version` = `oo v0.2.42` ✓ 無髒尾)。dev tie-back
`43b7f5f`(dev/top 內容一致驗畢)。**增量分類依判例**(對齊 `#effect_violation`
arc 3):觀測面影響僅及「以路徑指涉儲存」之呼叫,由靜默成功變 ⊥;一般檔案存取、
CAID 定址存取、引擎自身路徑全不動;**回歸掃描確認全樹無既有此形**(n/ 語料唯一
命中 `../.oo_peer_a` 為不同名且已入 pin;合規語料與 `add_architect` 皆零命中)。
CAID 不動。前版 v0.2.41=`0ab489e`。

**儲存信任邊界弧(2026-07-26,裁定 R-A~R-E,**一件驗收退回**,SPEC_08 §6.3 新設)**:
**開弧前量測**(v0.2.41 實機端到端,非讀碼):未授權 n/ 程式 `~%Io./write_file
".oo/HEAD"` 即取得與 `#rollback` **完全相同**的效果,而 `oo rollback` 無 `--grant`
被 `#privileged_required` 拒絕——**同一效果,合法路徑拒、後門通,且後門留下的審計
痕跡比合法路徑更少**(無放棄紀錄)。同類三件:偽造 `.oo/abandoned`(下一個合法
commit 把「從未存在過的提交被放棄」封進 CAID,**永久**)、偽造
`.oo/architects.json`(refine 信任根)、**物件位元組就地竄改而引擎照單全收**
(改 `x:1` 為 `x:999`,檔名即 digest 不動;載入後宇宙根成為從未提交過的值,
再演化真值反得 `#conflict`)。**論點**:v0.2.40 為 `#pin` 寫的 §6.2「授權時點」
條款只施行於該操作、從未推廣;**§6.2 每道閘都裝在 CLI 動詞上,每道都有檔案系統
後門 ⟹ v0.2.38/40/41 的能力格在此洞未補前是裝飾性的**。
**承重框架(→ SPEC_08 §6.3.1)**:儲存**不是一層而是兩層**且所需機制**恰好互斥**
——物件層(內容定址,自我認證)需**驗證不需權限**;斷言層(HEAD/暫存/意圖/白名單,
是宣稱非內容)需**認證而無從驗證**。引擎原先對兩層都只做「信任」。此線同時回答
三問:進程可否寫(物件可、斷言不可)、鏡像斷在哪(精確於物件,**必然斷於 HEAD**
因其為索引性事實、全球格無 HEAD 即無全域截面)、GC 為何不對稱(無全域可達性根
⟹ **全球 GC 原則上不可能**;既有分散式 GC 結論,n/ 的貢獻是把它接到 `#squash`
的特權地位)。詳見 `docs/discussion/025`(超專案 top `881df75`)。
**裁定**:R-A 沙箱模型(使用者)、R-B 授權層單弧 CAS 讀取完整性另弧(使用者)、
R-C **保留路徑元件**(解析 `.`/`..`/symlink 後元件精確等於儲存名;非字串前綴、
非 base_dir 比對)、R-D **無條件**(任何能力皆不解鎖)、R-E 讀寫一致(驗收方,
均已明列供否決)。**A1 `~%Official./add_architect` 退役**:自實作起恆 ⊥ `#conflict`
(apply 只搬位置鍵、builtin 對整個引數取 `to_string_plain()`,同 v0.2.39
`check_oml` 之縫),而其 builtin 是白名單持久化的**唯一呼叫者**⟹**可偽造的檔案
曾是信任根唯一活著的寫入路徑**;裁為退役非修復(它是本弧正關後門的同一信任根的
**前門**,且 REAL_01 §7.2 本就規定帶外供給),全樹掃描零引用。
**探針校準**:15 red + 5 pin。**兩支第一版假紅**——payload 寫成 `"[\"bb\"]"` 求值
為 ⊥,`write_file` 從未被 apply,紅得與邊界無關;改 `~%Json./stringify` 後重驗
`tgt: #true` 確認基線寫入確實成功。**教訓入探針註解:紅門要查的是「為什麼紅」,
不是「有沒有紅」**(連續第四弧的同類校準)。最鋒利者 `red_a4_...` 為三路判別
(後門擋掉/前門未授權仍拒/前門授權仍通——缺第三路則「弄壞 rollback」亦會通過)。
**驗收**:diff 純度 ✓(探針僅移 15 個 `#[ignore]`);四數 ✓ workspace **1450/0/3**、
conformance **143/143**、genesis **11/11**、store_boundary **20/20**、pin **15/15**。
對抗:尾斜線/雙斜線/`./`/深層 `..`/絕對路徑/symlink 逃逸/`--privileged`/`--grant`
全拒;`.oo_peer_a`/`.oomisc`/`foo.oo`/`.ooo` 全可寫。
**一件退回(範圍外,根因在我方)**:交付另行讓 `disc.connect` 接受 `remote:` 前綴
——**該 scheme 不存在**,是**工單寫錯了前綴名**(實際只有 `tcp://`),而交付**遷就
驗收方的錯誤而非回報**。新增位址 scheme 是無規格條款、無向量、無測試的語言表面
變更,已退回並於呼叫點留註。**與 v0.2.39 `ContentHash::parse("_")` 同型**:驗收方
的手滑被交付方當成需求;**首要責任在我方**。累計此類兩例。
**兩點使規格文字更準(非推翻)**:(1)**邊界作用於「路徑定址」而非儲存內容**
——`~%Engine./save` 與 `disc.fetch` 仍以 CAID 觸及物件且**正確地保持開放**(自我
認證,無可保護之物),此即兩層結果在程式碼裡的顯影,也是比 R-E 原話更好的表述;
(2)**R-C 的代價大於裁定原文**——實測:位於任何名為儲存目錄之目錄**底下**的工作區,
其語言層檔案存取**全數**被拒(連 `ordinary.txt` 亦然),而非僅該目錄不可及;引擎
自身照常。規格採實測版本而非較軟的原話(§6.3.3 誠實範圍聲明)。
**驗收方自修一支既有探針**:`pin_probe_test::pin_intent_file_is_not_authority` 的
**前提**「未授權程式**可以**寫意圖檔」已因本弧為假(交付正確地回報而未擅改)。改為
**兩層皆測**:層一(本弧)語言層根本碰不到該檔;層二(v0.2.40)**檔案若仍以他途存在
則不構成授權**——由測具帶外植入,即 R-A 明言沙箱不及之處。
spec closure:SPEC_08 §6.3 新設(原 §6.3「設計理由」順延 §6.4;ENGINE_SYNC
L1822 的舊 `§6.3` 指涉隨之過時,屬編輯性)、TAG_REGISTRY §1.5 `#store_boundary`、
CHANGELOG 增量。**本弧無新增合規向量**(runner 不涉檔案系統邊界,CLI/語言層探針
為法定測具)。工單 `nlang-tools/docs/store_boundary_handover.md`。
**掛帳**:CAS 讀取完整性(A3;**經 025 重新定性=不是安全修補,是讓 n/「衝突不是
錯誤」整套立場站得住的地基**——引擎現在於 0 階信任位元組,其上每條語義保證都附帶
一個沒寫出來的條件「只要檔案系統沒被動過」);身分持久化(`Identity::new_random()`
每次啟動重生 ⟹ **n/ 現無法跨行程回答「這是誰說的」**,屬 REAL_01 §7/REAL_02;
簽章的用途是**不可否認性而非存取控制**,並兼作「兩個引擎跑同一個 `.oo/`」的偵測器);
位元組回收 GC(**必須定義為純本地,且不得表述成「把值從 n/ 刪掉」**);`.oo` 比對
為逐位元組,**大小寫不敏感檔案系統(macOS/Windows)之行為未測**,需實機定案。

**引擎 v0.2.41 定版(2026-07-26)=增量**:top `0ab489e`(squash `#rollback`+
`#squash` 弧〔含一件驗收代修〕+ oo 0.2.41 bump+lock 同入),tag 於實測 commit
(workspace **1429/0/3**、conformance **143/143**、history_ops 探針 **15/15**、
genesis **11/11** 皆於候選重測;條件閘一次成功;tag 後 touch build.rs 重建
`oo --version` = `oo v0.2.41` ✓ 無髒尾)。dev tie-back `627a983`(dev/top 內容
一致驗畢)。**增量**(純增兩子命令 + `CommitMeta.abandoned` 可略欄 +
`CommitKind::Squash`;**跨版雙向相容經實測**,舊 commit 雜湊與反序列化不變;
普通 evolve/commit/log 路徑未動)。**SPEC_08 §6.2 五操作至此全數有本體**。
前版 v0.2.40=`51b8837`。

**`#rollback` + `#squash` 弧(2026-07-26,裁定 R1+R2,**一件驗收代修**,
§6.2 收尾)**:兩者**皆不碰格**(與 `#pin` 相對),只移動 HEAD 與改寫 commit 鏈;
且皆為**單一命令**,故 `#pin` 弧的「意圖≠授權」陷阱不重演(能力與效果同行程)。
§6.2 五操作至此**全數有本體**(`#commit` 已於 `#pin` 弧退役)。**裁定 R1**:
原條文「無(由歷史鏈追蹤)」**經量測在 n/ 不成立**——回溯後 log 自新 HEAD 沿
parent 走,**被放棄的整段離開歷史**(物件仍在 store 但無介面可列舉);git 敢如此
宣稱是因另有 reflog,n/ 無,且 **n/ 中鏈本身即紀錄**(git 把軌跡留本地、推乾淨
成果)。故:rollback 本身不建 commit,但**其後的下一個 commit 記錄被放棄的
HEAD**(多次回溯全數記錄),存 **CommitMeta**、**不入值**。**推論**:歷史圖有
兩類邊(`parent` 收斂血緣 / **放棄邊** 分歧標記),仍為 DAG;放棄邊 = **反單調
操作(n/^op 上箭頭)在歷史上的顯影**(disc/021)。**裁定 R2**:squash **得**壓過
放棄紀錄,其 `#privileged_squash` 標記承接事實——**細節可失、事實不可失**;
且 squash **必須同時斷開 parent 與放棄兩類邊**,否則被放棄 commit 永久可達、
可達性回收永不生效 ⟹ **squash 是唯一能使物件不可達的操作**,故「使之不可達」
永遠是受特權且自我標記的行為,其後回收位元組得為機械無特權掃描——**遺忘不得
自動發生**(git 讓遺忘自動發生〔reflog 過期〕,n/ 併成同一件受審計的事)。
交付 `229e58a`,**本弧為三個特權弧中交付品質最高者**(機制/邊角/序列化相容
一次到位)。**序列化相容經實測非推理**:`CommitMeta` 加欄後以**自訂 Debug**
保 `Commit::content_hash`(走 `format!("{:?}", meta)`)位元穩定(`abandoned==None`
時輸出與舊三欄 derive 逐字同);**跨版實測**——以 `v0.2.40` 二進位另建 worktree
建倉三提交 → 新版讀取 **CAID 逐字相同、鏈長一致**;新版於其上續提交 → **舊版
仍能讀完整四提交**;`CommitKind::Squash` 標籤字節 3(0/1/2 不變)。**對抗全過**:
髒暫存兩操作皆拒/非祖先基底拒/基底=HEAD 空區間拒/**兩次回溯兩條放棄紀錄皆入
帳**/紀錄由第一個後續 commit 消費且不外洩至第二個/**squash 壓過放棄紀錄後
`abandoned` 消失而 squash 標記仍在**/squash 一個 squash 標記依然在/被壓 commit
已離開可達鏈而物件仍在磁碟(位元組回收另案)。**驗收代修(審計面可查驗性)**:
squash 自動訊息原為**裸字 `"squash"`**,而 `oo log` 的 kind 標記行亦印
`    squash` ⟹ **兩行字串全同**,讀者無法分辨「機器設定的審計標記」與「恰好
這樣寫的人類訊息」,**驗收方紅門亦因此無法區分**(單靠訊息即通過,測不到標記
本身)。**一個無法憑檢視查驗的審計面不成其為審計面**。修=訊息改為
`compressed <n> commit(s) onto <base>`(新增 `Universe::commits_after`);探針
強化為斷言**恰好一行** `squash` 標記 + 訊息含 `compressed`,並補 R2 紅門的
「放棄紀錄確已消失」前置斷言(使 R2 兩面皆壓住)。四數:探針 **15/15**、
workspace **1429/0/3**、conformance **143/143**、genesis **11/11**。**spec
closure**:§6.2 表修訂(rollback 審計改「放棄紀錄」、squash 說明改「使其脫離
可達鏈」)+ 新增 R1/R2 兩段規範性條文 + **審計可查驗性**條款;CHANGELOG 增量。
**無新增合規向量**。**增量**。工單 `nlang-tools/docs/history_ops_handover.md`。
**掛帳**:位元組回收(GC)另案(本弧只使不可達成為可能,store 仍 append-only);
`.oo/abandoned` 屬**審計紀錄非授權**(與 `#pin` 的 pin_pending 性質不同,偽造
只會加假紀錄不取得能力),store 完整性仍屬 REAL_02;`.oo/` 對程式可寫的通盤
複查(跨弧殘留)。

**引擎 v0.2.40 定版(2026-07-26)=增量**:top `51b8837`(squash `#pin` 弧
〔含兩件驗收代修〕+ oo 0.2.40 bump+lock 同入),tag 於實測 commit
(workspace **1414/0/3**、conformance **143/143**、pin 探針 **15/15**、
genesis **11/11** 皆於候選重測;條件閘一次成功;tag 後 touch build.rs 重建
`oo --version` = `oo v0.2.40` ✓ 無髒尾)。dev tie-back `262859e`(dev/top
內容一致驗畢)。**增量**(純增 `oo evolve --pin` 與 `oo commit --grant`;
未 pin 的演化與提交路徑逐字未動)。CAID 不動——審計僅 commit kind,值內無痕。
前版 v0.2.39=`fa99626`。

**`#pin` 弧(2026-07-26,SPEC_08 §6.2 第一個操作本體,**兩件驗收代修,其一為
特權升級**)**:`#pin`=唯一動及**格本體**的特權操作(其餘三個只移動歷史鏈),
即 discussion/021「被檢疫的一劑 n/^op」。**表面由量測定**:`oo run` 明文為
one-shot pure universe、永不載入已提交狀態,故根衝突在該處不會發生;`oo evolve`
才是持久宇宙命令,且軸別正確(SPEC_00 §1.2 改變宇宙=演化軸)。**兩步式**:
`--grant pin` 授權 + `--pin` 請求。**審計落點由規格推導**:§6.2「特權改變收斂
過程而非幾何指紋」⟹ 審計不得入值(否則 CAID 位移)⟹ 落 Commit
(`CommitKind::Pin`,`Standard` 仍 `#[serde(other)]`,舊 commit 反序列化不變)。
交付 `5a1ea6b`。**驗收代修 1(範圍洩漏)**:commit 在 pin_pending 時對**整個
staged** 做 replace_merge——實測根有 `y:5` 時,一個**普通**放寬寫入 `y:@int`
(G2-S 允許,`meet(5,@int)=5`)在對照組提交後仍為 `5`,但同批次只要有任一 pin
就被取代成 `@int`:**只碰 x 的特權操作改變了未受特權的 y 的語義**。修=新增
`Universe.pin_coords`(實際 pin 的座標集,隨意圖檔以 JSON 持久化),commit 走
`pin_commit_merge`——**只取代 pin_coords,其餘照常 meet 且衝突照常大聲失敗**;
不可解析/舊格式意圖檔 → **空集合**(安全側,不得讀成全部)。**驗收代修 2
(特權升級,§6.1.2 後門)**:`.oo/pin_pending` 的**存在**即驅動 commit 端取代
語義與 Pin 標記,而 commit **完全不重驗能力**;`.oo/` 是**任何 n/ 程式可寫**的
目錄(`~%Io./write_file` 對 n/ 開放、`~%Json./stringify` 可產合法 JSON)。
**端到端證實**一支全程未授權的程式(`lst: ["y"]` / `~%Io./write_file
".oo/pin_pending" (~%Json./stringify lst)`)即取得 #pin 覆寫語義**且**其 commit
被**假標記為 pin**——正是 §6.1.2 明禁之無令牌後門(程式自授權)。修=`oo commit`
加 `--grant`/`--privileged`,`pin_pending` 且無能力 → 大聲拒
`#privileged_required`;**意圖檔記錄意圖、不是授權**,授權須於**施加特權效果的
當下**經可信通道重新出示。修後同一 exploit 被拒、格未動;合法流程
(`evolve --grant pin --pin` → `commit --grant pin`)完好。**探針修改權行使**:
三處 commit 呼叫改攜 `--grant pin`(工作流因代修正當改變)+ 補升權迴歸釘
`pin_intent_file_is_not_authority`(exploit 原封寫入探針)+ 範圍洩漏迴歸釘兩支。
四數(兩次代修後):探針 **15/15**、workspace **1414/0/3**、conformance
**143/143**、genesis **11/11**。**spec closure**:§6.2 新增兩條**規範性**條款
——**授權時點**(跨階段特權每個施加階段各自出示;**意圖 ≠ 授權**,實作必須
假定本地儲存可被非特權程式寫入)與**作用範圍最小化**(特權僅施於被指名座標,
不得因共處一次提交而外溢);語義保證增列推論「審計標記不得存於值內」;
**`#commit`(含衝突)退役**(裁定:改規格文字)——量測顯示其描述無對應閘位
(含 ⊥ 值本就可提交不需特權;真正被拒的根×staged 衝突拒於 evolve 邊界,而在
該邊界強制覆寫者即 `#pin`,故為重複條目)。CHANGELOG 增量。**無新增合規向量**。
**增量**(未 pin 的演化與提交路徑逐字未動)。工單
`nlang-tools/docs/pin_handover.md`。**掛帳**:`#rollback`/`#squash` 本體;
**殘留**=偽造意圖檔若搭上一次**合法** pin commit 其座標仍會被套用,徹底解法
需意圖記錄**可認證**(HMAC 等),而令牌鑄造/生命週期依 §6.3 屬 **REAL_02**;
另 `.oo/` 對程式可寫本身值得單獨檢視(本弧只堵 pin 這條路,其他以 store 狀態
為據的機制應同樣以「檔案≠授權」重讀)。

**引擎 v0.2.39 定版(2026-07-25)=修正**:top `fa99626`(squash 具名參數
可達性弧〔apply 層搬具名欄 + 驗收代修〕+ oo 0.2.39 bump+lock 同入),tag 於
實測 commit(workspace **1399/0/3**、conformance **143/143**、具名參數探針
**14/14**、genesis **11/11** 皆於候選重測;條件閘一次成功;tag 後 touch
build.rs 重建 `oo --version` = `oo v0.2.39` ✓ 無髒尾)。dev tie-back `7de6ede`
(dev/top 內容一致驗畢)。**修正**(非增量亦非破壞):修的是**引擎未實作
規格已寫的拼法**——SPEC_08 §3.5 文字不變,既有可用行為零改變(A/B 逐字元
證實四條既有路徑不動),改變的是**原本不可用者變為可用**。CAID 不動。
**首度**有合規向量(L2-104)檢驗 §3.5。前版 v0.2.38=`a98a684`。

**具名參數態射不可達弧(2026-07-25,一件驗收代修 + 一件探針修正)**:修
**規格 × 引擎合規缺口**。**缺陷**:`apply_morphism` 組 builtin 參數時**只搬位置
(數字)鍵**,參數的**具名欄永遠到不了 builtin** ⟹ 凡讀頂層具名欄的 builtin
**在 n/ 源碼層以任何拼法皆不可達**(`f #x`→`{0:#x}`、`f {k:#x}`→`{0:{k:#x}}`
巢狀、`f {0:#x}`→`{0:#x}`)。**而 SPEC_08 §3.5 明文以具名參數規定**
`project_down { target, masa }`／`project_up { sections }`——故規格站在 builtin
那邊,是合規缺口非引擎疣。**影響**:`check_oml`(a,b)=**對任何輸入皆
`#oml_valid` 的恆真驗證器**〔靜默假保證,最危險〕、`project_up`(sections)=
builtin 回 Top ⟹ apply 回 partial、`project_down`/`set_strategy`=⊥ #conflict
(死但大聲)、`disc` fetch/find(target)=直查模式永不觸發靜默退化為相似度搜尋。
未受影響:`diff.rs`(讀清單**元素**欄)、`query.select`(位置優先)、
`equivalence_map`(真 nullary)。**為何從未被抓到**:既有測試(`bohr_test.rs` 等)
**直接自 registry 取 builtin 呼叫**、手工餵具名欄組合,**繞過 apply**——registry
層契約與 apply 層契約不一致而**無測試踩在那條縫上**;本弧探針故一律走 **n/ 層
(CLI)**。**裁定(使用者):修在 apply 層**(一處修全家族,且讓引擎符合 §3.5
已寫的拼法,毋須改規格)。交付 `69dbbe1`:`unified_arg` 加搬參數之非 `%`、非
數字具名欄,衝突規則**參數優先**;位置鍵語義不動。**爆炸半徑以 A/B 實證**(非
推理):另建 worktree 編出交付前二進位逐式對跑,`%rules`／pattern-dispatch(含
range 鍵)／ks-lookup／curry 四路徑**新舊逐字元相同**,含「具名欄放發散值於被
丟棄路徑」一例。**兩項申報的範圍外變更一收一退**:(收)`oml.rs` 同文短接
`a.digest==b.digest → Valid`——數學成立(任何正交模格中 $a=b$ 使 OML 平凡為真,
無須先算 $\neg a$,正是 Int 等無 orthocomplement 原子落 `Approximate` 的出口),
判準取 digest(REAL_03 最細元件)=內容同一,不過度放寬;(**退,代修**)
`ContentHash::parse("_")`→32 零字節——理由「對齊 MasaRef Display」**不成立**:
REAL_03 §3.1 之 `_` 是 **masa_ref 元件**的編碼(出現在
`hash:sha256:v2:_:<sketch>:<digest>` **之內**),§2.1/§2.2 定義的 CAID 全形從不是
裸 `_`、`ContentHash::Display` 亦從不吐裸 `_`,故非任何 Display 的逆;其影響是
**身分層的靜默放寬**(13 個 `parse` 呼叫點含 `storage.rs` 自磁碟讀 ref——雜散 `_`
將不再報錯而靜默成零摘要 CAID,與「說謊即崩潰」相反),A/B 證實確改行為。
**根由是驗收方探針**:`masa: "_"` 為我隨手選的佔位字串、本身不合 REAL_03;交付方
為滿足它而**放寬引擎**而非回報探針有問題(探針修改權在驗收方),**首要責任在
驗收方**——紅門校準不實。**探針已修**(改用正規 v2 CAID + 正向 `#blur` 斷言),
還原後 14/14 仍全綠,**證明引擎讓步本就非必要**。四數:探針 **14/14**、workspace
**1399/0/3**、conformance **143/143**、genesis **11/11**。**合規向量:新增
L2-104**(`project_down` 具名參數 → `#blur` 局部截面;hermetic 已驗〔同目錄重跑
與全新目錄逐位元相同〕)——**SPEC_08 §3.5 首次可被合規套件檢驗**;**不為
`check_oml` 建向量**(全樹 grep 確認它**不在規格任何一處**=引擎額外品,為未規範
行為建向量等於把引擎專屬語義鎖成規範)。**`check_oml` 誠實特徵化**(修後實測):
同文→`#oml_valid`／真序對(`1 ⊑ @int`)→`#oml_approximate`／非序對→`#oml_vacuous`
——不再恆真,惟 `Valid` 目前僅經同文短接可達(真 OML 路徑因 `orthocomplement`
在這些值類未定義而落 `Approximate`,既有限制非本弧引入)。工單
`nlang-tools/docs/named_arg_reachability_handover.md`。**掛帳**:`orthocomplement`
未定義於多數值類／`check_oml` 無規格歸屬(要嘛入規格要嘛明列為引擎擴充)／
**具名欄為 eager force**(發生在兩條早退分支之前而它們丟棄 `unified_arg`;A/B 證
今日不可觀測故不列代修,但屬 CbO 惰性偏差,廉價護法=把搬運閘在
`%builtin` 存在之後)。

**引擎 v0.2.38 定版(2026-07-25)=增量**:top `a98a684`(squash 選擇性
discharge 弧〔特權能力格〕+ oo 0.2.38 bump+lock 同入),tag 於實測 commit
(workspace **1385/0/3**、conformance **142/142**、選擇性 discharge 探針
**15/15**、genesis **11/11** 皆於候選重測;條件閘一次成功;tag 後 touch
build.rs 重建 `oo --version` = `oo v0.2.38` ✓ 無髒尾)。dev tie-back
`9857cc4`(dev/top 內容一致驗畢)。**增量**(`--privileged` 語義不變=全授,
既有程式與腳本零影響;新增的是更窄的 `--grant` 授予)。CAID 不動——能力
屬 horizon,實測同程式跨不同授權 `--format` 輸出逐位元相同。前版
v0.2.37=`aa1eb8e`。

**引擎 v0.2.31 定版(2026-07-20)**:top `e6d6e5c`(squash 序波
W3 弧 + oo 0.2.31 bump+lock 同入),tag 於實測 commit(1288/0/3、
語料非 pending 75/0、125/125 皆於候選重測;條件閘一次成功;tag
後重建 `oo --version` = `oo v0.2.31` ✓)。dev tie-back `bc1d848`。

**引擎 v0.2.30 定版(2026-07-20)**:top `ef9aeee`(squash 序波
W1+W2 弧 + oo 0.2.30 bump+lock 同入),tag 於實測 commit
(1278/0/3、語料非 pending 75/0、123/123 皆於候選重測;條件閘
一次成功;tag 後重建 `oo --version` = `oo v0.2.30` ✓)。dev
tie-back `bc7bde7`。origin/top 已同步至 v0.2.29(用戶已推)。

**引擎 v0.2.29 定版(2026-07-20)**:top `1537e09`(squash 空洞
真弧 + oo 0.2.29 bump+lock 同入),tag 於實測 commit(1267/0/3、
語料非 pending 75/0、123/123 皆於候選重測;條件閘一次成功;tag
後重建 `oo --version` = `oo v0.2.29` ✓)。dev tie-back `b773f10`。
註:切版時發現 origin/top 已同步至 v0.2.28(用戶已推)。

**引擎 v0.2.27 定版(2026-07-20)**:top `60e3a8c`(squash effect-
meta 弧 + oo 0.2.27 bump),tag 於實測 commit(1249/0/3、語料非
pending 75/0、123/123 皆於候選重測;首次 tag 後 `--version` 出
`v0.2.27+` 髒尾=Cargo.lock 未入 squash——amend 入 lock、重打 tag
於 `60e3a8c` 後三套件**全數重測**一致;條件閘成功;重建
`oo --version` = `oo v0.2.27` ✓)。dev tie-back `b4ed3c4`(+lock
同步 `caa3575`)。**切版教訓:squash 前驗 Cargo.lock 與 bump 同
入,或 bump commit 時一併 `git add Cargo.lock`**。

**引擎 v0.2.26 定版(2026-07-19)**:top `1592a80`(squash 前向×
spread 弧 + oo 0.2.26 bump),tag 於實測 commit(1236/0/3、語料非
pending 74/0、121/121 皆於候選重測;條件閘一次成功;tag 後重建
`oo --version` = `oo v0.2.26` ✓)。dev tie-back `16399c4`。

**前向引用×spread 弧結案(2026-07-19,一件代修=驗收代修)**:
交付 dev `6822ff3`(形制 b:pending_spreads thunk 佇列、四觸發點
擴張同律、unify 保留 pending、交付期自抓 root-unify 消耗病+C4
擴張路徑武裝染色)、驗收代修 `f072e6b`。**抓漏=cocoon 目標面**:
繭構造 force_recursive 於 evolve 期把「尚未定義」當「永不定義」
消耗 + 重建丟 pending → `{{...later, b:1}}` 前向 #missing_key vs
倒序 7。代修=in_evolve 相位旗標(evolve 期 closed 回佇 Top 源;
開放 combo 保基線消耗守 never-eq)+重建保留 pending。終態:
**1236/0/3**、**121/121**(L2-81/82 翻綠)、語料 74/0。對抗:
CAID 前向 vs 實心孿生 #true(身分收斂)、聯集支擴張後正典序、
去重坍縮、cross-dep `src:{a:q.b}` → 1(逐座標惰性理想)。共責
教訓入紅線:**容器雙形({}/{{}})與拼法雙形同級,門要雙釘**。
既有債另案:evolve 期急切計算×pending 開放 combo(out 先於源=
基線同形)。展開碰撞 Q3 凍結案清結。

**引擎 v0.2.25 定版(2026-07-19)**:top `c04fd9d`(squash 態射體
`^` 弧 + oo 0.2.25 bump),tag 於實測 commit(1224/0/3、語料非
pending 74/0、119/119 皆於候選重測;條件閘一次成功;tag 後重建
`oo --version` = `oo v0.2.25` ✓)。dev tie-back `fa21a8d`。

**態射體內 `^` 綁定弧結案(2026-07-19,零代修第二十四例;協議
全淨)**:交付 dev `e6e6331`(單點修=apply_single_rule 載 %closure
前 scopes.clear(),嵌合鏈源頭斷;hop/裸名/$/overshoot 全復用)、
驗收見 dev log。獨立重跑:**1224/0/3**、**119/119**(L2-79/80
翻綠)、caret RHS 13/13、語料 74/0。對抗:別名呼叫定義側不變/
遞迴/雙平面合成/$+^ 共存/**巢內態射梯全自洽**(inner ^=外層
參數世界〔^.n→1、嚴格 miss 誠實 _〕、^^=持有、^^^=root=字面量
局部性逐層成立)。三通道各一法完工:裸名=詞法/$=動態/^=定義側。

**引擎 v0.2.24 定版(2026-07-19)**:top `0422e80`(squash %kind B3
弧 + oo 0.2.24 bump),tag 於實測 commit(1213/0/3、語料非 pending
74/0、117/117 皆於候選重測;條件閘一次成功;tag 後重建
`oo --version` = `oo v0.2.24` ✓)。dev tie-back `be6273a`。

**%kind B3 弧結案(2026-07-19,零代修第二十三例;協議全淨)**:
交付 dev `0d3aded`(兩鑄造點 #type、is-marker=%kind #type ∧ 載荷欄
Some、:126 同遷;引擎 "type_constraint" 字串歸零)、驗收 `ea8f7ae`。獨立重跑:**1213/0/3**、**117/117**、語料 74/0。對抗:
marker 結構面/@option/密封 nominal 模板/雙重精化冪等/精化後等值;
`#ok & @result` ⊥=v0.2.23 反事實同形非回歸。marker 繭 CAID 一次性
合法位移。**B1–B4 全數落地,%kind 超級衝突調和完結**(B5
%super/%predicate 實作掛帳 §4.10/L3 波)。

**引擎 v0.2.23 定版(2026-07-19)**:top `3030563`(squash cocoon
調和弧 + oo 0.2.23 bump),tag 於實測 commit(1206/0/3、語料非
pending 74/0、117/117;**宿主中途崩潰重啟,依崩潰恢復協議檢兩倉
無 lock 無殘留後三套件從頭重測**,前後一致;條件閘一次成功;tag
後重建 `oo --version` = `oo v0.2.23` ✓)。dev tie-back `685249d`。
同日 %kind 超級衝突裁定=**B 全套**(B1 軸語正名/B2 nominal %type
欄宣告內部表示/B3 %kind 標籤統一 **#type 勝出、#type_constraint
全面退場**(規格書應僅剩 REAL_01 L224)/B4 REAL_03 §288 範例改寫
bn_serial v2 實態;B5 %super/%predicate 實作掛帳 §4.10/L3 波)。

**cause cocoon 調和弧結案(2026-07-19,代碼零修;協議代修一筆
第二連)**:交付 dev `e337095`(別名臂移除=⊥落F1/blur落#5 無特例、
兩鑄造點刪 %type、`is_engine_scaffold_field` 顯示出口剝鷹架)、驗收
`80824e2`。獨立重跑:workspace **1206/0/3**、conformance **117/117**
(L2-78 翻綠)、語料 74/0。對抗:conflict/missing_key 繭類變形淨
(後者鑄 %path,§1 示例列補筆)、`{_:5}` 照印、`{_:_}=(){}` #false
語義保欄。角落記帳:用戶顯式 `_: _` 與鷹架表示同一不可區分——
顯示隱藏、語義完整,非違規。協議:交付方單方遷移 probe×6+語料×3
`.%type` 期望(忠實改寫、申報誠實)=協議代修第二連;共責=驗收方
開單只掃 conformance 漏 probe 樹+語料。**新紅線:退役拼法開單時
全樹 grep(probes+corpus+conformance)**。cause 繭 CAID 一次性合法
位移(%type 欄移除)入帳。

**blur 顯示序鍵去鹽弧開單(2026-07-18)**:SPEC_01 §2.4.1 #5 修訂
=blur 族內鍵 (%cause 名稱字典序, 剩餘燃料升序, 策略),明確排除
%caid/鹽,平手穩定保序(起草洞修正:原「顯示字串字典序」經內嵌
%caid 滲鹽)。探針形制=**鹽證明雙排列門**(兩輸入順序都須出法定
序,字串排序必在一排列上強加 caid 序 → 決定性紅,不靠鹽運氣);
2 紅+5 釘(lucky-salt 校準巧合綠轉釘)。conformance 載不了跨行程
非決定面,矩陣 116 不動。工單 docs/blur_display_key_handover.md
(tools dev `07e8f50`);基線 1190/0/5,目標 1192/0/3。模型 #3 已派。

**引擎 v0.2.22 定版(2026-07-18)**:top `5fc6939`(squash 正典顯示
序+blur 鍵去鹽兩弧 + oo 0.2.22 bump),tag 於實測 commit(1192/0/3、
語料非 pending 74/0、116/116 皆於候選重測;條件閘一次成功;tag 後
重建 `oo --version` = `oo v0.2.22` ✓)。dev tie-back `fbced75`。

**blur 顯示序鍵去鹽弧結案(2026-07-18,零代修第二十二例)**:交付
dev `7686649`(族階 4 獨立臂,鍵=(cause, fuel, strategy),全等
Equal 穩定保序)、驗收 `31b6907`。獨立重跑:workspace **1192/0/3**、
conformance **116/116**、語料 74/0。病灶面直測:雙 blur 聯集 CLI
8 次 caid 相對序 6 升 2 降=鹽已非鍵(修前必全升);身分鹽/顯示
文字不動。§2.4.1 起草洞收口,正典顯示序家族完結。

**正典顯示序弧結案(2026-07-18,代碼零修;協議代修一筆)**:交付
dev `7a515bb`(value.rs 顯示層排序 helper + to_nlang Union 臂單點;
穩定排序、禁 digest 遵守)、驗收 `9948b9f`。獨立重跑:workspace
**1185/0/3**、conformance **116/116**(L2-75/76/77 翻綠)、語料
74/0。對抗全正(combo 欄內嵌/nav 合成 `2 | 9 | _`/int-float 同值
int 前/TopCaused 殿後/combo 顯示字串序/區間)。協議記帳:交付方
單方遷移兩「相遇序」舊釘(內容合法、申報誠實)→ G3 弧「下次計
代修」預告兌現;共責=驗收方開單掃描漏遷×2(盤點輸出可見)。
曝光另案(法案起草洞,驗收方責):**雙 blur 聯集顯示序跨行程
非決定**——§2.4.1 blur 族內鍵「顯示字串字典序」經內嵌帶鹽 %caid
滲鹽入排序鍵(兩次 CLI 實測先後翻轉);修法候選=blur 族內鍵改
(%cause, 視界參數);單 blur 不受影響。

**引擎 v0.2.21 定版(2026-07-17)**:top `e94864b`(squash math×
聯集分配弧 + oo 0.2.21 bump),tag 於實測 commit(1168/0/3、語料
非 pending 74/0、114/114 皆於候選重測;條件閘一次成功;tag 後重建
`oo --version` = `oo v0.2.21` ✓)。dev tie-back `f547be6`。

**引擎 v0.2.20 定版(2026-07-17)**:top `048998c`(squash G4 惰性
⊥ 剔除+染色作用域兩弧 + oo 0.2.20 bump),tag 於實測 commit
(1151/0/3、語料非 pending 74/0、112/112 皆於候選重測;tag 走條件
閘 `[repo=nlang-tools]&&[branch=top]` 一次成功、無事故;tag 後重建
`oo --version` = `oo v0.2.20` ✓)。dev tie-back `16f4fbf`。

**引擎 v0.2.19 定版(2026-07-17)**:top `1bdbb54`(squash `^` 解析
+R6 lint+eq×thunk 釘三弧 + oo 0.2.19 bump),tag 於實測 commit
(1122/0/3、語料非 pending 78/0、107/107 皆重測;tag 後重建
`oo --version` = `oo v0.2.19` ✓)。dev tie-back 見 dev log。
**誤 tag 事故第二次**:倉別檢查印了警訊但 `&&` 鏈照跑,tag 再進
spec 倉,當場撤銷無殘留——教訓升級:**檢查與 tag 不同呼叫,或用
條件閘 `[ repo = nlang-tools ] && [ branch = top ] && git tag`**
(本次已用閘,成功)。

**引擎 v0.2.18 定版(2026-07-17)**:top `bec8542`(squash cause
正典審計弧 + oo 0.2.18 bump),tag 於實測 commit(1087/0/3、語料
非 pending 78/0、104/104 皆重測;tag 前驗倉別+branch〔上次事故
對策〕;tag 後重建 `oo --version` = `oo v0.2.18` ✓)。dev
tie-back 見 dev log。

**引擎 v0.2.17 定版(2026-07-16)**:top `1ae49fa`(squash Blur
展開源+系統軸所有權兩弧 + oo 0.2.17 bump),tag 於實測 commit
(1078/0/3、語料非 pending 78/0、101/101 皆重測;tag 後重建
`oo --version` = `oo v0.2.17` ✓)。dev tie-back `5795c99`。切版
過程誤 tag 事故一筆:tag 兩度誤打 spec 倉(cd 鏈錯),當場撤銷
無殘留——教訓:tag 前先驗 `git branch --show-current`+倉別。

**引擎 v0.2.8 定版(2026-07-13)**:top `2c3face`(squash G3 弧 + oo
0.2.8 bump),tag 於實測 commit(871/0/3、語料 74/0、61/61 皆重測;
tag 後重建 `oo --version` = `oo v0.2.8` ✓)。dev tie-back `ace1dc5`。

**剖析器天花板弧(a_limit_you_cannot_catch,2026-08-11,引擎交付
`dev def7157`)**:規格側新增 TAG_REGISTRY §2.7.4(上限住在每一個遞迴
階段)、§1.3 登記 `#request_too_large`、REAL_02 §3.2.3(收方必須在
處理之前先設界)。

*符合性量測(某版引擎做到了沒有,故歸此檔而不入規格)*:

- 交付前:`oo fmt` 於 `{{a: …}}` 巢狀 **debug 131 層 / release 1336 層**
  exit 134 abort,無 ⊥、無 `%cause`;分組 `(…)` 每層 ×2,24 層 >120 秒;
  線上 69 位元組請求使節點停擺 >90 秒且並行合法客戶端餓死,8000 個 `!`
  的請求使 serve 行程中止;單行讀取無位元組上限。
- 交付後:文法左因子分解(`paren_expr` 共享 `( expr` 前綴)、`unary_expr`
  改迭代(AST fold 亦迭代)、剖析前深度閘 **256**、剖析後 AST 深度閘
  **4096**(顯式 worklist)、線上讀取上限 **64 KiB**。
- 餘裕(驗收方 spike,量後即撤):剖析器執行緒完整閉包(pest 剖析 +
  `parse_expr`)每層 **525–532 KB**,線性;堆疊 64/128/256/512 MiB 對應
  可達深度 **123/248/498/997**。出貨堆疊 **512 MiB** ⟹ 閘 256 對天花板
  997 = **3.89×**。剖析延遲 3.8 ms(64 MiB 時 4.2 ms),256 層巢狀峰值
  RSS 141 MB ⟹ 保留為位址空間,惰性提交。
- 線上對抗(實測):兩種攻擊向量皆 **0.01 秒**回 `#stack_overflow`,節點
  存活;128 KiB 單行 **20/20** 回 `#request_too_large`。
- 閘:本弧探針 15/15、全 workspace **1869/0/3**、×5 穩定、跨版本雙向
  (新讀舊、舊讀新所寫)。

*掛帳(未修,留待下一個剖析器弧)*:`with_parser_stack_using` 將
**剖析器執行緒的 panic** 與 spawn 失敗一併映射為 `#stack_overflow`。
真正的堆疊溢位會 abort 而到不了 `join()`,故 join 失敗意味內部 bug——
**把 bug 報成無能為力**正是 §2.7.1/§2.7.3 要消除的那類錯標,且使剖析器
panic 變靜默。

*跨弧回退(驗收方修復)*:AST 閘使 `limit_you_cannot_choose`(v0.17.0)
的 `chain(5000)` 於剖析即被拒 ⟹ C1 紅、**R2 空綠**(其三個斷言全為
「不存在」,空宇宙盡數滿足,求值器硬上限未被執行到)。兩處 fixture 改為
可抵達求值器之長度,並依常設規則為 R2 補「存在」斷言(反事實已驗)。
另 `nesting_doubles_the_universe`(v0.17.1)之 R5 因首輪閘設 100 而紅
——**低於前一版已交付之能力**,為選定上限時未先 grep 全樹釘住該量之
斷言所致;裁定改為「先定承諾(256)再配資源(512 MiB)」。

**引擎 v0.18.0 定版(2026-08-11)**:top `5e1b9e3` 故事提交
"A limit you cannot catch"(squash 剖析器天花板弧 + oo 0.18.0 bump),
tag `v0.18.0` 於實測 commit(workspace **1869/0/3**、conformance
**143/143**、genesis **11/11** 皆於候選上重測;tag 前驗倉別+branch;
tag 後 `touch build.rs` 重建,`oo --version` = `oo v0.18.0` ✓、
`git describe --exact-match` = `v0.18.0` ✓)。dev tie-back `3975350`,
dev 與 top 樹逐位元同一。規格同步切 **v0.18.0-draft.1**。
**增量,零破壞性**——身分面完全不動,故走 minor 而非 major
(VERSIONING §6「語義變更逐 minor」)。切版清單一筆:deps 全零頭檢查
命中一個 `.tmp*` 殘留(中斷建置留下),清除後複驗零命中。

**燃料計費弧(the_meter_reads_two / D2,2026-08-11)**:規格側新增
REAL_01 §9.1「算子應用」範圍釐清、SPEC_08「AST 有界工作不計 MBU」,
更正 SPEC_08 計費交叉引用(§10→§9.1)與 SPEC_09 §6 `%timeout` 列。

*符合性量測(歸此檔)*:

- 交付前:最低可行燃料在巢狀 2 層與 200 層**同為 2**;觀測原子、`1+1`、
  單次態射應用、8 段管道鏈、**升寫到 20 個元素**——全部 **2**(每個 fixture
  的值都先驗過:9 / 13 / `[2..21]`);合併 4。機制=`force_recursive` 兩處
  `check_resources(0)`,且 `value_is_fully_solid_combo`(整棵子樹遞迴走訪)
  發生在任何收費之前。
- 交付後:按 §9.1 語義計費;memo 命中扣與 miss 同額 MBU。
- **交付主動找到並關掉一個未被要求的缺陷**:此前暖快取留下較多燃料 ⟹
  視界落點隨快取狀態改變 ⟹ **`#blur` 的 CAID 取決於該值先前是否被觀測過**。
  `stage5_r1` 原本的前置條件 `warm > cold` 即為「快取狀態可從燃料帳觀測到」
  之證據。屬 O42 類。
- 閘:本弧探針 12/12、workspace **1883/0/0**(零 ignored)、conformance
  143/143、genesis 11/11、×5 穩定、跨版本雙向。

*驗收方裁決與更正*:

- **算術不計費一度被我判為缺陷,判錯**。O41(用戶,2026-08-09)已裁 `%fuel`
  是「唯一一個拿掉之後觀測不再必定終止的旋鈕」⟹ 其職責是**保證終止**,
  而有限 AST 求值一次必定終止 ⟹ 交付的讀法是對的。
- **我另一處說錯**:曾稱 SPEC_09 規範預設 `%timeout: 1000` 而引擎未套用。
  實為 O41 已改創世預設為 `#_`、引擎正確;我讀到的是**同檔另一張過期的表**
  (§6 未隨 O41 更新)。該列已修。
- **`<<_.>>` 粒度改變接受為暫時**:耗盡不再使整體結構觀測坍縮為單一 blur,
  而是每個成員各自具名(61 個)。查證非違規——SPEC_08 §3.2.4 寫的是
  「**節點**會根據 `%strategy` 進行語義坍縮」,新行為更貼合;決定性已驗
  (五行程、兩工作區逐位元同一)。成因是 `eval.rs:915` 由 `check_resources(1)`
  改為 `(0)`,**blur 出現在哪裡等於 `handle_resource_exhausted` 在哪裡被呼叫**
  ——「錶在哪轉」與「結果報在哪」今天是同一條路徑,該分開者留待 `~%Observe` 弧。
- **驗收方改動七支既有測試**(交付未動,符合 §10.6):三支粒度改觀測 `v`;
  `cycle_test` 兩支由字面算術改為態射應用(算術已不可能抵達視界);
  stage4/stage5 四支由「燃料差」改用 `force_memo_hit_count()`,並**同時斷言
  燃料在冷暖之間相等**——比原斷言更強。反事實已驗:停掉計數器四支立刻紅。
- **工單自身缺陷**:§10.4 要求交付「re-point those four」而 §10.6 又要求
  「交付不得編輯任何測試」,二者矛盾;交付選了約束、提供儀器並把測試留給
  驗收方,**這是對的**。根因記在工單側。

*掛帳*:`~%Observe`(暫態觀測結果之家;連帶 SPEC_08 §117 之 MUST NOT 違反
——逾時仍鑄 `#blur` 且 `#incomplete` 在引擎中從未存在)。排在完整設計與
savepoint 之後。

**引擎 v0.19.0 定版(2026-08-11)**:top `9878f48` 故事提交
"The meter reads two"(squash 燃料計費弧 + oo 0.19.0 bump),tag `v0.19.0`
於實測 commit(workspace **1883/0/0**〔**零 ignored**,三支假缺陷清除後首次〕、
conformance **143/143**、genesis **11/11** 皆於候選上重測;tag 前驗倉別+branch;
tag 後 `touch build.rs` 重建,`oo --version` = `oo v0.19.0` ✓、
`git describe --exact-match` = `v0.19.0` ✓;deps 全零頭檢查零命中)。
dev tie-back `2976522`,dev 與 top 樹逐位元同一。規格同步切
**v0.19.0-draft.1**。**破壞性條目 #12**(計費改語義計費 ⟹ 燃料側 `#blur`
位址移動;快取暖度離開燃料帳),90 天時鐘自本日重啟——距 #11(v0.17.0,
2026-08-10)一日,深水期的正常代價。**破壞性走 minor 而非 major**
(major 保留給 v0.500.0 委員會錨點,VERSIONING §6)。

---

## Q-010a — every byte or none(2026-08-13,尚未切版)

**主張**:同一個 CAID 的 CAS 物件,磁碟位元組必須相同。規格側落於
**REAL_03 §6.7**(§6.6 的對偶:那節治「位元組決定位址」,本節治「位址決定
位元組」;二者合起來才是雙射)。

**⚠ 符合性主張的正確措辭**——**不得**只寫「O48 成立」:

> **O48 對本版之後寫入的 CAS 物件成立;原地升級的倉沿用其 format-1 物件的
> 位元組。**

理由是用戶 2026-08-13 裁定 **(a) 宣告限制,不遷移**:`write_object` 在位址已
存在時提早返回,故舊物件永不改寫。〔量〕把帶 span、pretty 的物件與 `format: 1`
偽造成舊倉再提交一次:`format` 升到 `2` 而**舊物件原封不動(4 個物件裡 1 個
仍帶 span)**。Q-010b 是紀元弧、會以新位址重寫全部,今日寫的遷移程式兩弧後即為
丟棄品——**這是排程判斷,不是「已解決」**。

**交付**:CAS 專用正準 JSON(字典序、緊湊)＋型別驅動的 span 剝除
(`Value::for_cas_storage()` 複製後沿型別走訪,置 `Span::unknown()`,由 AST 的
serde 省略)＋`STORE_FORMAT_VERSION` 1→2。**`.oo/staged` 未動**(O51:工作階段
保留 Thunk,強制發生在 commit)。

**量測**:本弧探針 14/14;形狀覆蓋掃描(14 種值形一次提交)全樹 `"span"` 零命中
且 14/14 欄位讀得回來;**workspace 1897/0/0(零 ignored),五次全同**;根物件
**252,435 → 67,913 B(−73.1%)**、換行 0、**位址 `16ba5683…` 未動**。跨版本以
**真的 v0.19.0 二進位**(worktree＋獨立 target)雙向實測:舊倉→新引擎讀得開且
值正確;新倉→舊引擎回
`store format version 2 is not supported by this engine (understands format 1);
refusing to open`——**誠實拒絕,不是 serde 錯誤**。

**破壞軸**:**格式／讀相容,非身分**。P1 釘住根 CAID 未移動;而 `ast.rs` 四處
`pub span: Span` 零 serde 屬性 ⟹ 舊引擎無法讀無 span 的物件,**這不是相容層能
補的**。切版時須記一條破壞性條目並註明其軸別與 #12 不同。

**一件代修**:首版以**序列化後的 JSON 形狀**判定語法節點(帶 `span` 且帶
`kind`／`key`+`value`／`left`+`op`+`right`／`anchor`+`segments`),而**使用者
Combo 的欄位名恰好落在同一位置**——四個判別式全部摧毀使用者資料,`commit`
回報成功而物件從此 `#caid_mismatch`。判例已入 REAL_03 §6.7 實作註記。

**驗收方自動的三支釘**(皆為「倒數計時器型」而非不變量):
`atomic_write_probe_test` 的 `p2`(釘 `.oo/format == "1"`)、`local_gc_probe_test`
的 `r7`(同上,且以 `"2"` 當未知格式的對抗值——而 O48 剛好把 2 變成現行值)、
以及新增 `p4`(釘 `serde_json::Map` 的字典序:正準序**依賴無人開啟
`preserve_order`**,cargo feature 跨圖統一,一個新相依即可靜默推翻 R2)。
`affiliation_claim` 與 `seat_order` 的同類釘用的是**相對**寫法(讀 before →
動作 → 斷言未變),全域升版動不到——**那是對的寫法**。

**規格 v0.20.0-draft.1 / 引擎 v0.20.0 定版(2026-08-14)**:引擎 top `55e5975`
故事提交 "The address decides the file",tag `v0.20.0` 於實測 commit(候選上重測
workspace **1897/0/0**〔零 ignored〕、conformance **143/143**、genesis **11/11**;
tag 前驗倉別＋branch;tag 後 `touch build.rs` 重建,`oo --version` = `oo v0.20.0` ✓、
`git describe --exact-match` = `v0.20.0` ✓;deps 全零頭檢查零命中)。dev tie-back
`4cb85a0`,dev 與 top 樹逐位元同一。**破壞性條目 #13:軸別為格式／讀相容,非身分**
——根 CAID 一位元未動(`app: { k1: 1 }` 前後皆 `16ba5683…`),故 **90 天時鐘不因本條
重啟**(時鐘所防者為使用者的 CAID 失效);前次身分破壞為 #12(v0.19.0,2026-08-11)。

---

## Q-010b — a value, not a recipe(2026-08-14)

**弧**:提交時強制／`%closure` 僅捕捉自由變數／根以單一摘要指名標準根。
三者皆進入雜湊 ⟹ **一個紀元或零個**。裁定 O35＝A、O49 重述、O50、**O52**、O51。

**規格側**:REAL_03 **§6.8 新設**、§6.7 補第二則判例、REAL_02 §5.1.1 去字面版本號、
SPEC_05 §3.3(前置弧)。破壞性 **#14,身分軸,90 天時鐘自 2026-08-14 重啟**。

**符合性量測(引擎 v0.20.0 → v0.21.0)**

| 項 | v0.20.0 | v0.21.0 |
| :--- | :--- | :--- |
| 根物件(`app: { k1: 1 + 2, f: x -> x + v1, v1: 10, v2: 20, v3: 30 }`) | 72,555 B | **1,511 B** |
| 其中標準根 | 67,329 B(system 61,912／types 5,186／rules 231) | 一個 64-hex 摘要 |
| 根 CAID(`app: { k1: 1 }`) | `16ba5683…` | **`6e5ad5e3…`**(BN/ 與印表機兩路徑同值) |
| `.oo/format` | 2 | **3** |
| workspace | — | **1908/0/0**(193 套件,零 ignored) |

**三輪驗收,三件代修,而三件是同一個病的三種形態**——在一個地方做了決定,別處還照舊。

1. **D1 用形狀猜型別**。`expand_root_system_json` 對任何位於 `"Combo"` 鍵下、缺
   `"system"` 的物件插入 `"system": {}`;使用者把座標命名為 `Combo` 即中彈,
   **`commit` 報成功而物件讀不回**。第二輪把判準收窄為 `object.len() == 1`——
   **仍是形狀判準**,使用者的軸映射剛好一筆時逐位元組相同:`app: { Combo: 7 }` 壞、
   `app: { Combo: 7, z: 1 }` 好,五軸皆然。第三輪依裁定把兩道純外觀的 JSON 手術
   整個刪除(sentinel 留在型別形),代價 +117 B 於 1,394 B。**判例已入 §6.7。**

2. **D2 重建 `ComboVal` 時漏了四軸,且收窄沒取不動點**。`capture_free_fields` 自
   `ComboVal::default()` 起手只指派 `data`／`local` ⟹ `%u`(meta)、`/u`(rules)、
   `@u`(types)全部失聯;且只取本體的自由名,不跟被捕捉的值自己的依賴 ⟹
   深層兄弟與相互遞迴斷在第二跳。**全部靜默回 `_`,不報錯。**
   修法為逐軸判準＋遞移不動點;實測 `{d, e, k}` 入閉包而 `junk` 不入。

3. **D3 加了第二個解碼器卻沒搬所有讀者**。`get_root` 正確,但 `gc.rs`、
   shadow scan、OODP `#fetch` 仍走 `get_value` ⟹ **`oo gc` 在健康倉上指控它自己
   損壞**(違 REAL_03 §6.6「裁決必須為真」,亦即 v0.2.55 弧修掉的那一類)。
   修法為**所有讀者共用一個解碼器**,不逐處補。

**驗收方處理的 12 支預定改變**(交付未動任何既有探針,正確)。九支共因為
`every_byte_or_none` 的 `root_object` ＝ `max_by_key(len)`:**根縮小到比 commit 小
之後,這些 fixture 開始量 commit**——C0 說「525 B 太小不像根」、R2 看到兩個 commit
不同就宣告非決定性、R6 讀到 commit 就報告使用者資料被毀。改為「以 `{"Combo":`
開頭且必須恰好一個」。

順帶發現 **R1 的存在半自始是弱的**:它要求磁碟上有 Thunk,而 `app: { k1: 1 }`
自己從無 Thunk——找到的是**內嵌標準庫裡的**,即被弧控制不到的內容滿足;
對一個把 fixture 的 span 與值全丟掉的交付也會是綠的。已改為用含態射的 fixture
要求磁碟上有 `Code`。**R4 亦然**:它取根的 `system` 用第一個出現處,而根自己的是
**第七個**(前六個是巢狀空的),靠交付碰巧壓縮掉空的那些而綠了兩輪——
**儀器量的是它所測試的那個實作的巧合**。已改為「恰好一個 64-hex 摘要,竄改之
必須得到指名的拒絕」,校準:v0.20.0 的根 0 個、v0.21.0 的根 1 個。

**跨版本(真 v0.20.0 二進位)雙向**:新倉→舊引擎
`store format version 3 is not supported by this engine (understands format 1
through 2)`;舊倉→新引擎讀得開,**且讀不升級 format**。

**五次重跑:四次 1908/0/0,run 4 掛一支** `kademlia_table_probe_test::p4_nothing_persisted`
(`Address already in use`)。**成因在交付之外**:該檔 `git diff HEAD` 為空、單獨重跑
12 次 0 次重現、失敗發生在綁埠而非任何讀取路徑;`free_port()` 綁 `:0` 取得埠後**放掉
listener** 再交給子行程,空窗由另一個並行的測試二進位取走。已入 WORK_QUEUE Inbox。

**新增掛帳(皆已入 Inbox)**:創世頂層規則軸只有 `/add` 一個算術態射且**使用者因此
無法在自己的宇宙頂層定義 `/add`**(`#missing_key at /add.%kind`,而 `/sub`／`/mul`／
`/frobnicate` 皆成功);SPEC_09 §2.1 與 §2.5 兩張標準型別表名單互不相同而引擎只兌現
`list`／`option`／`result` 三個,**其餘憑名字現造**(`@zzz` 與 `@int` 印出逐字同形的
值而兩者 `.%kind` 皆為 `_`);`free_port()` 的 TOCTOU。

---

## Q-011 — a store you did not write(2026-08-15)

**弧**:`.oo/format` 只宣告佈局且自描述／新增 `.oo/objects.format` 宣告物件編碼／
缺席即拒絕且讀取路徑永不寫／只 hydrate 帶標準根摘要的根。
裁定 **O23**(A′)、**O36**(A)、**O53**(B)、**O54**(C)。**O55 另立一弧。**

**規格側**:REAL_02 **§5.1.1 改寫**(佈局格式版本 → 儲存的兩份宣告)、
REAL_03 **§6.8.1 新設**。破壞性 **#15,格式／讀相容軸,90 天時鐘不重啟**。

### 符合性量測(引擎 v0.21.0 → v0.22.0)

| 項 | v0.21.0 | v0.22.0 |
| :--- | :--- | :--- |
| `.oo/` 宣告 | `format` 一個裸數字,兩軸共用 | `format`=`layout=2` ／ `objects.format`=`encoding=3` |
| `.oo/format` 缺席 | **唯讀路徑蓋上 `1`** 並開啟 | **拒絕,且不寫** |
| 空的 `.oo/` 目錄 | 開得起來 | 開得起來(判別式改問 `HEAD`／CAS 物件是否存在) |
| 裸數字 `1`/`2`/`3` | 開啟 | 開啟(明文舊制規則),**讀後不改寫** |
| `layout=99`／`0`／`abc`／空 | — | 全部具名拒絕,**且不寫檔** |
| workspace | — | **1917/0/0**(194 套件,零 ignored),**五次全同** |

### 三輪驗收

1. **論旨成立、M1 入口關上**;**D1**:`init` 以 `.oo` 是否存在當判別式,
   **一個空的 `.oo/` 目錄被誤判成別人的倉** ⟹ `oo node serve` 在一個只有
   `discovery.n` 的目錄上開不起來(11 支失敗)。**又是拿代理量當性質。**
2. D1 修好(判別式改問 `HEAD` 與 CAS 物件是否存在);**O54 完全沒做**——
   `git diff | grep -c hydrate` = **0**,而**九支探針全綠、workspace 1917/0/0**。
3. 通過。

### O54 由三個真二進位驗證,不由探針

**該項在樹內不可滿足**——分辨「有沒有 hydrate」需要兩個標準根**不同**的引擎,
而測試造不出第二個標準根。故工單 §6 明記「本項無探針」,§7.5 列為驗收步驟。
儀器先驗:兩個引擎的標準根摘要 `65f52e2d…` / `571669af…` 確認不同。

| 倉 | 讀者 | 修前 | 修後 |
| :--- | :--- | :--- | :--- |
| format-2 | 交付(控制組) | 開 | 開 |
| **format-2** | **交付＋一筆標準根條目** | **`corrupt (integrity failure)`** | **開** |
| format-3 | 交付＋一筆 | 指名拒絕 | 指名拒絕 |

**驗收步驟抓到了它,而九支探針沒有。** ⟹ 常設規則:**工單裡凡有「本項無探針」者,
必須逐字標在該項目旁邊**,不能只寫在探針表的註腳——交付方讀的是射程表。

### 那條界線付了它不是為了付的紅利

〔量〕舊二進位的蓋章行為**修不掉**:v0.20.0 對一個宣告被刪的儲存仍蓋 `1` 並開啟。
故本弧能保證的是「新引擎不再製造那個狀態」。而新引擎讀一個**已被舊引擎貼上假標籤
`1` 的編碼-3 儲存**:**讀得回來、零則完整性指控、且不改寫標籤**。

原因是 O23 的界線落在 O54 上——物件層的決定**由物件自帶的摘要驅動,不由宣告驅動**。
一個說謊的標籤因此只能影響「這個倉是不是給我讀的」,影響不到物件怎麼被讀。
**該界線是為了讓 §6.7 與 A′ 相容而裁的,它順帶把舊二進位造成的傷害擋在物件層之外。**

### 驗收方處理的七支預定改變

`atomic_write::p2`／`every_byte_or_none::r5`(字面釘)、
`local_gc::r7`(改為逐軸驗證,不釘字面值;順帶移除說謊的相容別名 `STORE_FORMAT_VERSION`)、
`local_gc::p4`／`advert_persistence::r2`／`kademlia_table::p4`(`.oo/` 檔案集合)、
本弧自己的 `p1`。**後四支我在工單裡寫的是「`.oo/` 檔案集合的斷言(若有)」——
寫了「若有」而沒有去 grep。** ⟹ 常設規則:**工單裡凡寫下「若有」「應該沒有」
「大概不影響」處,都是一次沒有做的 grep。**

---

## Q-025 — a library you no longer ship(2026-08-15)

**弧**:引擎依根所指名的摘要**在一個集合裡查找**標準根,不再拿自己那一份去比對。
實作 **O55**;規格依據 REAL_03 **§6.8.2 第二條 MUST**(多重具備)。
**本弧不動標準根的內容**——`/add` 孤兒與 SPEC_09 兩張型別表屬 §6.8.2 **第一條**,另一弧。

**規格側**:REAL_03 **§6.8.2 新設**(標準根是版本綁定之物／多重具備／「不具備」改指
沒有任何規格版本公佈過／實作不得自行擴充),**含未兌現宣告**;SPEC_09 §2.5 佔位符
明文標註。裁定 **O56**(走 L3,先立框架不填清單)。

### 為什麼是現在

〔量 2026-08-15〕`root_with_system()` 在 v0.20.0 → v0.22.0 之間**逐位元組未動**,
摘要恆為 `65f52e2d…` ⟹ **至今只存在過一份標準根,表只有一列**,現在是裝這道門最便宜的時刻。
而〔量,三個引擎〕多**一筆**內建即造成兩個引擎**雙向互相讀不了對方的倉**——
牆照 §6.8 是對的,缺的是門。

### 符合性量測(引擎 v0.22.0 → 本交付)

| 項 | v0.22.0 | 本交付 |
| :--- | :--- | :--- |
| 解析判準 | `digest != expected` 即拒絕,`expected` 來自單一 `root_with_system()` | `StandardRootSet::get(digest)`,查不到才拒絕 |
| 新增一版歷史標準根 | 不可能(只持有一份) | `shipped_standard_roots()` 多一個元素,**解析邏輯零改動** |
| 拒絕訊息 | `… is unavailable (this engine has {單數})`——**持有量 > 1 時即為假** | `… is unavailable`,仍指名所缺者 |
| 「這隻引擎開不開得了這個倉」 | 只能開開看然後讀錯誤 | `oo status` 直接報 available／unavailable／self-contained |
| workspace | 1917/0/0 | **1921/0/0**(195 套件,零 ignored),**五次全同** |
| conformance／genesis | 143/143 ／ 11/11 | **143/143 ／ 11/11** |

### 主證據由三個真二進位給出,不由探針

樹內測不到「集合大小 > 1」(需要兩個標準根不同的引擎),**該事實於工單射程表逐字標明**。
驗收建 **PLUS**(交付＋一筆內建,只持有新的)與 **PLUS+H**(同上,**且仍持有 `65f52e2d…`**):

| 倉 | 讀者 | 結果 |
| :--- | :--- | :--- |
| 本交付寫 | 本交付 | `commit …74a2b07f`(控制組) |
| 本交付寫 | PLUS | **拒絕**,指名 `65f52e2d…` ⟹ §6.8 第三條 MUST 仍在 |
| 本交付寫 | **PLUS+H** | **`commit …74a2b07f`,與控制組逐字元相同** ⟹ **門成立** |
| v0.20.0 寫 | 三者 | 皆 `commit …81eeabeb`,**完全相同** ⟹ O54 不回歸 |

**§2.1 的性質在建構過程中自證**:PLUS 與 PLUS+H 的原始碼差異**只有 `from_roots([…])`
裡多一個元素**。一張表的判準就是「加一列不必改讀表的人」。

### 破壞性:無

〔量,對真 v0.22.0 二進位雙向實測〕**讀相容雙向成立**——v0.22.0 讀本交付寫的倉、
本交付讀 v0.22.0 寫的倉,commit 位址皆與各自控制組逐字元相同。
**身分軸未移動**:同一份源碼 `app: { k1: 1 + 2, v: 10 }`,兩個引擎寫出的**根位址**
皆為 `6a7b18de…`。⟹ **本版不記破壞性條目,90 天時鐘不重啟。**

### 一輪通過,但驗收工具自己壞過一次

交付**一輪即通過**(探針 4/4、diff 純度乾淨——探針檔只少兩行 `#[ignore]`)。

值得記的是驗收方這一側:上一輪背景建置被中斷,在 `q025-plus-target` 留下一個
**37 MB、有執行位元、看起來完全正常**的 `oo`,實際是 `Exec format error`;
同目錄還留了損毀的 `serde_json` 中間產物,使重建也失敗,得整個清掉。
**若未先驗它能不能執行,「PLUS 讀 → 拒絕」那一列會因為每一次呼叫都失敗而變綠。**
⟹ 常設教訓:**驗收用的工具自己壞掉時,矩陣照樣填得滿**——跨版本矩陣的每一個
二進位,使用前必須先問它一個**已知答案**的問題(此處為 `--version`)。

---

## Q-026 — a port you did not bind(2026-08-16)

**兩輪。無規格變更。** 交付 `nlang-tools 1aa87c2`。

**弧**:節點必須報告它**實際綁到**的埠;而測試不該猜埠,該問節點。
〔量 v0.23.0〕`oo node serve --port 0` 綁得起來,橫幅印 `serving at port 0`,
而 `/proc/<pid>/fd` → `/proc/net/tcp` 顯示**實際在 40707** ⟹ **唯一告訴你節點在哪的
那一行,在 OS 選埠時是假的**。與 `.oo/format` 同族:標記報告的不是它量的東西。

### 符合性量測

| 項 | v0.23.0 | 本交付 |
| :--- | :--- | :--- |
| `--port 0` 的橫幅 | `serving at port 0`(假) | 實得埠 |
| 測試如何取埠 | 14 份 `free_port()`,**10 種逐字不同**,門檻漂移到 21000–35000 | **零份**;子行程綁 `:0`,橫幅即權威 |
| `serve()` 助手 | **11 種形狀**,一個檔根本沒有 | **1 份**(`tests/common/mod.rs`) |
| 子行程死亡 | 等滿 4 s 才報「never came up」 | `try_wait` 立即偵測並帶 log 報錯 |
| workspace | 1921/0/0 | **1924/0/0**(196 套件),**五次全同** |
| conformance ／ genesis | 143/143 ／ 11/11 | **143/143 ／ 11/11** |

**測試函式 1918 支,交付前後不變**——未新增、未刪除;無斷言被刪(全跑差異 −441/+70 行皆為取埠與啟動樣板)。

### 這條缺陷的成因被改寫過一次

Q-010b 記為「`free_port()` 的 TOCTOU 空窗」。**該說法量不出來**:隔離該空窗,
14 行程 × 200 次 × 三檔空窗,**2800 次綁定 0 次 EADDRINUSE**(Linux 輪替配發 ephemeral port)。
實測成立的是**兩個別的**:**H1** 探測問 `127.0.0.1:0` 而子行程綁 `0.0.0.0:{port}`
——**不是同一個問題**〔量:持有 `127.0.0.1:P` 時 `0.0.0.0:P` 得 EADDRINUSE〕⟹
**碰撞對手不必是另一支測試**,機器上任何持有該埠的行程都算,**這解釋了為何單獨重跑從未重現**;
**H2** `std::net::TcpListener::bind` 不設 `SO_REUSEADDR`,TIME_WAIT 拒絕重綁。
⟹ 原本 Inbox 提的「全域埠仲裁」**修不好 H1**,已一併更正。

### 一輪代修,一個根因

**把每一個 `free_port()` 都當成「我要一個埠來綁」。** 18 個呼叫點裡 15 個確實是,
另外三個不是:**D1** 新增的 `os_chosen_port() -> 0` 被呼叫端**照舊拿去撥**
(`connect(127.0.0.1, 0)` 永遠失敗,五次全紅)——**生產者換了,消費者沒換**,
與 Q-010b D1/D2/D3、Q-011 D1 同族;**D2** `advertise_wire` r7 的那個號碼是塞進
**簽名廣告**裡的 `listen_port`(對方宣稱自己在哪聽),註解逐字寫著「nobody is listening
there」而交付**留著註解只換掉值**,引擎對 `listen_port: 0` 回 `#malformed`,
於是該探針的**控制組**先垮、主張根本沒被測到。

**工單的責任**:§3.2 只寫「刪除全部 14 份 `free_port()`」,**未要求先按用途分類呼叫點**。
⟹ 常設規則:**要求移除一個被到處呼叫的助手時,工單必須先列出呼叫點清單並逐一標註用途。**

### 主證據不是「壓測不再失敗」

這條缺陷**從來無法按需重現**(Q-010b 12 次、Q-025 3 次、本弧 2800 次,皆 0)。
14 路併發壓測 3 輪 **0 次 EADDRINUSE**,但**該壓測不具代表性**——〔量〕它在 12 核上
推到最多 **168 個並行測試**,而 `cargo test --workspace` 一次只跑一個二進位;
其每輪 1–2 支失敗經查皆非交付缺陷(`seat_order` 自陳前提不成立;
`advert_persistence` 逾時,而〔量〕無負載時橫幅 **60 ms** 出現、助手的窗 **6000 ms**、
且該檔原本的窗只有 4000 ms ⟹ **交付把窗拉長了**,單獨重跑 3/3 綠)。

**⟹ 主證據是機制被移除**:`grep 'fn free_port'` ＝ 0,沒有任何測試再挑埠,
H1 與 H2 都失去發生條件。

### 順帶入 Inbox 一則

`identity_persistence_probe_test::pin_concurrent_first_mint_yields_one_key` 五次中一次
(`not a valid PKCS#8 Ed25519 key`),該檔本次逐位元組未動、與埠無關 ⟹ 疑似鑄鑰非原子寫入,未定位。

---

## Q-027 — a fallback that wins(2026-08-16)

**四輪。** 交付 `nlang-tools 1abb832`。裁定 **O57**(A／B／C／D 四則)。

**弧**:**當引擎說不出一筆資料是什麼時,那筆資料不得因此獲勝。**

### 承重量測:同一個寫法,在同一個檔案裡往兩個相反方向倒

〔量 v0.23.1〕`peers.rs` 的耐久記錄解析,每個欄位都用 `…and_then(as_T).unwrap_or(X)`:

| 退回值 | 後果 | 方向 |
| :--- | :--- | :--- |
| `ttl`→0 | `ttl == 0` ⟹ 不轉發 | **輸** ✅ |
| `services`→空 ／ `observed_host`→"" ／ `listen_port`→0 | 不匹配 ／ 位址不可撥 | **輸** ✅ |
| `provenance`→`Unknown` | **帶註解**「never promote to direct」 | **輸** ✅ |
| `capacity`→0 ／ `hops`→0 | 未進任何決策 | 中性 |
| `ts`→0 ／ `received_at`→`ts` ／ `admission_seq`→0 | epoch／主鍵／次鍵,皆排最前 | **贏** ❌ |

**`provenance` 是唯一有人選過方向的一處**;其餘由巧合決定 ⟹ 「**意外的性質不是性質**」
(§4.3.5.1 自己的話)。**一次關掉兩條寫下來的 MUST 違反**(§5.1.2 與 §4.3.5.1)。

### 符合性量測

| 項 | v0.23.1 | 本交付 |
| :--- | :--- | :--- |
| 缺席 vs 不可解析 | **併成同一個退回值**〔量:5 候選 3 席位,不可解析那筆**拿到席位**,排在真實序號 7／8 之前〕 | 以獨立布林欄位分開;不可解析成為**主鍵**故排最後,**記錄仍保留** |
| 熵取不到 | `return 0` ⟹ 抽樣退化為**目錄序前 k 個**(模擬確認);註解逐字 `treat as 0` | `#rejected` `%reason: #entropy_unavailable`,**不附樣本** |
| 隨機來源 | 不可注入 ⟹ 該失敗路徑**無任何測試到得了** | `RandomSource` trait;交付附單元測試,**驗收方拿掉注入確認它會紅** |
| 客戶端讀不出 `%status` | 兩處 `unwrap_or("#conflict")` ⟹ 記成 **`#peer_refused`** | 兩處皆 `#peer_unknown_status` |
| workspace | 1927/0/2 | **1933/0/0**(197 套件),**五次全同** |
| conformance ／ genesis | 143/143 ／ 11/11 | **143/143 ／ 11/11** |

**§1.1 表中「輸」與「中性」七處逐字未動**(驗收方逐一 `git diff` 確認)。

### 規格側

REAL_02 **§4.3.5.1 新增正面條款**(該節原本只有「不得靜默退回固定序」這條禁令,
**沒有它的正面對應**,於是實作自己選了一格);**§3.2 共用理由表新增一列**
——那是**該表第一列說「收方做不到」**的,先前每一列不是「你的請求有問題」就是「我沒有」;
`TAG_REGISTRY` 登記 `#entropy_unavailable`。**狀態集未增長**,符合 §130。

### 四輪,而三輪的漏是驗收方造成的

1. **只做了排序那半。** 非交付方之過:本工單**漏了「交付方自檢」章節**(Q-025 有,
   Q-026 與本弧沒有——驗收方在 Q-025 之後弄丟的),而**本弧是第一次有整整一半的射程沒有探針**;
   且**完成條件被放在標題寫著「交付方不必做」的章節之後**。⟹ 已補回自檢章節並置於驗收之前。
2. **D1** `ts` 未做——**它是射程列的三處之一,卻是唯一沒有探針的一處**,故以「其餘全綠」通過。
   **D2** 熵拒答用了 `#conflict`,而依 §3.2.2 提問者會記為 `#peer_refused`
   ——**修「說錯話的退回值」的那次修改自己說錯了話**。D2 亦為工單之過:
   原文寫「**`%reason` 不得重用 `#malformed` 或 `#rejected`**」,而 `#malformed` 是 reason、
   `#rejected` 是 **status**——**一句話跨了兩層**,故「換新 reason、留舊 status」完全符合字面。
3. **D1** `ts_unparseable` 被**無條件**併入 `received_at_unparseable`,但 `received_at`
   只有缺席時才退回 `ts` ⟹ 一筆 `ts` 壞而 `received_at` 完好的記錄被降到最後,
   **引擎知道它何時到達卻報告「我不知道」**。方向安全故不違反本弧主張,
   但**本弧的整個論旨就是「值必須說真話」**,用戶裁定算代修。
4. 通過。

### 常設規則(本弧賺到五條)

*   **「交付方自檢」是必備章節**;**完成條件不得放在標題寫著「交付方不必做」的章節之後**。
*   **射程列了 N 處,探針就必須逐處對應**——少一處,那一處會以「其餘全綠」通過。
*   **約束分層的協定欄位時,必須逐層分別寫明**(status 與 reason 不可寫在同一句)。
*   **驗收前先提交交付**;未提交的工作不得是唯一副本。〔本弧實例〕驗收方為驗「拿掉注入會不會紅」
    以 `git checkout` 還原暫改,**那把整個檔案退回已提交狀態**,交付方在該檔的全部未提交工作被清除;
    `git diff --stat` 回空被誤讀為「還原成功」,實意為「與 HEAD 無差異」。僅因完整 diff 恰在紀錄裡而得以重建。
*   **全跑進行中不得改動樹**。〔本弧實例〕第三輪電池執行期間加入 P6,run 4／5 重編譯後多出一個 ignored,
   該次 ×5 因此不算數。

---

## Q-029 — a refusal that only covers reading（第一層，2026-08-16）

**交付 `nlang-tools 30abd55`（第一層）。規格零變更。裁定 O59。**

**論旨**：REAL_03 §6.8 第三條的拒絕**只蓋住了讀取路徑**。

〔量，兩個真二進位、未竄改任何位元組：`q025-plus`（標準根 `a63ef70b…`）建倉，
`v0.24.0`（只有 `65f52e2d…`）操作它〕——`log`／`inspect` 正確拒絕，而 `evolve` 靜默 staged、
`commit` 回報成功、`refine` 提交並移動 HEAD、`squash` 回答 `no HEAD to squash`。
事後倉裡有**兩個 `app` 相同、標準根摘要不同的根**與**兩個 `parent: null` 的提交**，
HEAD 在後者，**原引擎從此讀不了自己建的倉**。

### 成因是一行，六個症狀

`crates/oo/src/main.rs:1538`：

```rust
Err(_) => Universe::new(None, engine.root_with_system()),
```

`Universe::new(None, engine.root_with_system())` **就是「自身的標準根」**、`Err(_) =>`
**就是「代入後繼續」**——§6.8 第三條的 MUST NOT 被寫成了一個 fallback。
`Universe::load`（`universe.rs:275`）本身是對的（它呼 `get_root(…)?`），
**`oo rollback` 也一直是對的**——`Universe::rollback` 自己又呼了一次
`get_root(&target_commit.root, &engine.standard_roots)?`，繞過了那個 fallback。
⟹ 工單因此寫成「讓其他幾支得到 rollback 已經有的東西」，不是發明新機制。

### 驗收

探針 **10/10、0 ignored**，diff 純度乾淨（探針檔逐位元組只少六個 `#[ignore]`）；
workspace **1943/0/0（198 套件）五次全同**，conformance 143/143，genesis 11/11。
**主證據是兩個真二進位**：四條寫入路徑全部具名拒絕、HEAD 未動、物件數 2→2、
無任何根帶入侵引擎的摘要、**原引擎照常讀得回自己的倉**。
另驗**首次使用無迴歸**（全新目錄無 `.oo/`：`status`／`evolve`／`commit`／`log` 皆正常）——
那是拿掉 fallback 最容易打破的一格。

### 未完成（第二、三層）

*   §2.2 五個 `| None` 分類點（`universe.rs:989`／`:1063`／`:1082`、`disc.rs:200`、`oodp.rs:388`）
*   §2.3 線上那一格（`not_held` 仍為假）

**且第一層蓋不住它們**〔量〕：把一個外來根物件放進**一個開得起來的倉**，
`oo refine --source <該外來根> --target <我自己的根>` **照常提交**——
閘裝在**宇宙**上，而單調性檢查讀的是**運算元**。
**對照組**：運算元真的不在時 refine 亦照常提交（REAL_03 §9.1 的不透明設計）
⟹ **壞的是混同，不是跳過本身**。

---

## Q-030 — a digest that was not there（2026-08-16）

**交付 `nlang-tools 1ceff6c`。規格零變更（工單即如此預測）。裁定 O60。**

**論旨**：`hash:sha256:v1:`——digest 為空的 CAID——**parse 得過**。
`ContentHash::parse` 只檢查冒號段數 ≥ 4、前綴、hex 可解碼性，而 `hex::decode("") == Ok(vec![])`，
**全程無人驗長度**；`storage.rs:476` 隨後切它的前兩個字元。

〔量，真節點真封包〕`{ %op: #fetch, %hash: "hash:sha256:v1:", %from: "x" }`——
**47 個位元組、遠端、未認證、單一封包**，`oo node serve` 行程消失（rc=101）。
同一次執行的控制組（64 hex）得到正常的 `#not_held`。
**非交付所致**——對交付前的 v0.24.0 基線二進位逐字重現。

### 射程量到的，比 Inbox 那一列準

| | 到得了 | 到不了 |
| :--- | :--- | :--- |
| 線上 | **`#fetch`** | `#discover`（正常回應）、`#find_node`（**已經**回 `#malformed`） |
| CLI | `inspect`、`rollback`、`refine` | `squash`（先被祖先檢查擋下）、`node discover/find-node` |

洞比「空」大：**`hash:sha256:v1:ab` 被當成合法 sha256 CAID 收下並查倉**；
v1 與 v2 是**兩個各自的 `hex::decode` 呼叫**，只修 v1 會留下 v2。

### 修法幾乎是自己浮出來的

〔量〕`oodp.rs` 全檔 `unwrap`／`expect`／切片／`panic!`／`unreachable!` **共 0 處**——
協定層是防禦性寫成的，panic 來自它底下的儲存層。
而**正確的線上答案早就寫在那裡且只是到不了**：`oodp.rs:371` 的
`(None, Some(raw)) => refuse(Conflict, "unparseable_caid")`。
⟹ 工單明文禁止「把防禦加回協定層」，並讓 **P1 逐字斷言 `unparseable_caid`**。
交付即一個 `parse_sha256_digest` helper（decode ＋ `len() != 32` 即 bail），v1／v2 各呼一次。

**規格因此變成真的，而不是被改**：REAL_02 §3.2 第 141 行早已寫著
「`#conflict` ／ `#unparseable_caid` ／ `%hash` / `%target` 存在但不是 CAID」——
在此之前，`hash:sha256:v1:` 對 `parse` 而言**就是**一個 CAID，故該列對這個輸入不可達。

### 驗收

探針 **7/7、0 ignored**，diff 純度乾淨（探針檔只少五個 `#[ignore]`）；
workspace **1950/0/0（199 套件）五次全同**，conformance 143/143，genesis 11/11。
另掃全樹剩餘 `[0..n]` 切片：`lattice_sketch.rs`×2 與 `disc.rs`×1 皆在
`Sha256::finalize()` 的固定 32 位元組上，安全；`storage.rs:193` 的孿生依指示未動。

### 一個順帶的證據

`bohr_test.rs` 有**四個 fixture 在用 `hash:sha256:v1:00` 與 `:ff`**（一個位元組的 digest），
本弧後加寬為 64 hex。**它們四個之所以能存在，就是因為型別沒有履行它名字的承諾。**

### 常設規則（本弧賺到一條，是驗收方的錯）

*   **探針要釘性質，不要釘拼法——而「訊息含某子字串」就是拼法。**
    〔本弧實例〕探針斷言 `contains("Invalid CAID")`，而產品訊息是
    `"Invalid rollback CAID"`／`"Invalid source CAID"`／`"Invalid target CAID"`
    ——**不含**那個子字串。交付方唯一能滿足它的辦法就是改產品，於是三個使用者面訊息
    被合併成 `"Invalid CAID"`。**射程裡沒有這一項。**
    用戶裁定保留該合併（違規的 CAID 本身仍印在訊息裡，角色標籤因此冗餘；
    且新的內層理由 `expected 32 bytes, got 1` 比舊的 `Invalid CAID format` 有用）——
    **但探針已改為釘行為**：命令失敗 ＋ **從未到達倉**（`not found in local store` 不得出現）。
    改寫後逐一手工對基線二進位重新校準：長度那支**不靠 panic 就在基線上是紅的**，
    控制組三個形在基線上是綠的。

---

## Q-031 — held but unopenable（＝ Q-029 第二、三層，2026-08-16）

**交付 `nlang-tools 2ca1d2f`。規格：REAL_02 §3.2 共用理由表新增一列。裁定沿用 O59，無新裁定。**

**論旨**：Q-029 第一層把閘裝在**宇宙**上；閘的底下，**五個呼叫點**仍把
「我持有這些位元組，而我打不開它」折進另一個答案。成因同一個——拒絕是 `anyhow!` 字串
而非 `StoreReadError`，`downcast_ref` 得 `None`，五處都把 `None` 併進 `NotFound`。

### 一輪通過，五格各自處理

交付採建議做法（新增 `StoreReadError::StandardRootUnavailable`，**讓編譯器找齊**）：

| 點 | 落到哪 |
| :--- | :--- |
| `universe.rs:989`（refine 運算元） | `Err("refine operand cannot be opened")` |
| `universe.rs:1063`（shadow-scan 讀 commit） | `return Err(…)`，中止 |
| `universe.rs:1082`（shadow-scan 讀 root） | `return Err(…)`，中止 |
| `disc.rs:200` | 新 `enum LocalRead { Mismatch, Absent, StandardRootUnavailable }` |
| `oodp.rs:388` | `refuse(NotFound, "standard_root_unavailable")` |

**〔量，真節點真封包，驗收方獨立複驗〕**

```
持有但開不起來 → %status=#not_found  %reason=#standard_root_unavailable
真的沒有       → %status=#not_found  %reason=#not_held
```

**狀態集未增長**（REAL_02 §130；O57-C 已據此裁過一次）。

### 驗收

探針 **6/6、0 ignored**，diff 純度乾淨（探針檔逐位元組只少四個 `#[ignore]`）；
workspace **1956/0/0（200 套件）五次全同**，conformance 143/143，genesis 11/11。

**最重要的是那支綠的**：控制組 `C1`——運算元**真的不在**時 refine 仍照常提交
（REAL_03 §9.1 的不透明設計）。**修的是混同，不是跳過**；工單 §3 明文標出這是唯一
能毀掉本弧的方向，而它沒有被毀掉。

### 探針怎麼在樹內造出「持有但開不起來」

樹內無第二個二進位。靠兩個實測到的、互相對稱的事實：

*   **root 物件在驗位址之前先解標準根** ⟹ 放在錯位址上的根仍回
    `refusing root: … is unavailable` 而非 `#caid_mismatch`。**C0 逐字斷言這一點**——
    這個順序若變了，C0 先紅，而不是讓另外四支安靜地測別的東西。
*   **commit 物件會驗位址**〔量：`#caid_mismatch`〕 ⟹ 混合歷史走兩趟，**祖先先定址**
    （head 的內容含祖先的位址）。

**兩支紅一開始紅在 harness 上**（`own_root` 把探針自己種下的算成第二個根；一個暫時
位址用了非 hex 的 `h`），開單前修掉——**紅在 harness 上什麼都不證明**。

### 規格側

REAL_02 §3.2 新增 `#not_found` ／ `#standard_root_unavailable` 一列，並附註
**本表現有兩列說「收方做不到」而刻意落在不同 `%status` 上**：`#entropy_unavailable`
是 `#rejected`（我不作答），本列是 `#not_found`（我交不出來，去問別台）。
順帶更正 `#entropy_unavailable` 那列的「本表上唯一一列」——加了第二列後不再為真。

**`TAG_REGISTRY` 刻意未加**，並在規格裡寫明理由：〔量〕該檔今日只收了本表理由的一個
不一致子集，逐筆補會讓下一個新理由再問一次同樣的問題；一般性問題已進 Inbox。

### 兩則記錄（非缺陷，但要有人知道）

*   `disc.rs` 把「開不起來」映到 `BottomCause::Conflict`。**工單未指定該值**（只要求
    「不得判為不存在」）⟹ 那是交付方選的。下次有人問「為什麼是 conflict」，答案是
    **沒有人裁過**。
*   交付新增**兩個 `unreachable!()`** 到 `universe.rs`（真不可達：外層 arm 先 return，
    內層 match 只為窮盡性）。在剛確立「`oodp.rs` 全檔 panic 形為 0」之後，
    **方向相反**，記一筆。它們在 CLI 的 refine 路徑上，不在節點的 serve 路徑上。

## Q-032 — the half that was never written（2026-08-17，v0.26.0）

**弧**：O58＋O61＋O62，repair 時新增並裁 O63。標準根不再 `⊕` 進每一個根，改為根
指名一個可定址的標準根物件；引擎傳染算出的有效效果搬入參與 CAID 的 `%effect`；
`#pure` 以欄位缺席作正準形；拆開前後的位址規則由物件容器編碼閘分辨。

初次交付 `nlang-tools a71a69b`；Repair 1 `d779586`。初次交付的四項結構改動與歷史
標準根列方向正確，但新讀法套到舊根得到 `#caid_mismatch`，且 workspace 有 21 支紅未分類。
Repair 1 依 O63 讓 `encoding=3` 保留舊讀寫規則、`encoding=4` 使用新規則，並逐支把紅分成
授權改變與真回歸；最終無未定類。

### 交付形狀

*   新根物件只保存使用者殘差與一個進入雜湊的標準根 digest；標準根以 packed CAS
    物件保存、可由 `inspect`／`#fetch` 定址。GC walker 把該 digest 視為真邊。
*   使用者根先查、標準根後查，故 `/add`、`@list`、`@option`、`@result` 四個原先被
    標準根閉合值佔住的座標皆可遮蔽；沒有加入任何名字特例。
*   寫下的 `%effect` 與引擎傳染的效果仍可分開計算，但耐久值只留一個有效欄位。
    只有 `#pure` 省略；`#cached` 不是豁免，仍須落成欄位。正規化在守衛之後。
*   標準根 `65f52e2da48baa550d7340c0fdc214fd1f9925577a96ffec59bc34f8b2bcbe72`
    → `2da5b71371649291cfa5dc5d0cd019464d248e98645b3901938e1c08d2172c2c`。

### 驗收

Repair 1 最終樹：workspace **1964/0/0（201 套件）**，conformance **143/143**，
genesis **11/11**，Q-032 探針 **8/8、0 ignored**。26 個 genesis seed 中實際移動
**8 個**（Math／Discovery／Time／Io／Env／Process／Query／Csv），其餘 18 個未動。

主證據由兩個真二進位給出：v0.25.0 建倉並提交後，v0.26.0 可讀、可追加提交，舊根
位址不動，容器保持 `layout=2`／`encoding=3`；v0.25.0 再回讀兩筆提交亦全綠。新引擎
自建倉宣告 `encoding=4`。因此本弧是**身分軸破壞**但讀相容雙向成立；規格 changelog
記為破壞性條目 #16，90 天時鐘重啟。

### 規格側與未完成

REAL_03 §6.8／§6.8.1 補上拆開與格式閘判例；SPEC_08 §4.1 寫入「兩個住處是一個有效
欄位」及 `#pure` 正準形；STATUS 新增 O63。**未做且不得算作本弧殘欠**：`#23`
靜態守衛看不穿態射應用、使用者 `%builtin` 偽造。兩者回 WORK_QUEUE 另排。

驗收旁量另入 Inbox：`oo --version` 的 build script 未監看目前分支 ref，可能以舊 commit
自報身分；`advert_persistence::r5_the_rebuilt_index_matches_an_insertion_replay` 在 workspace
並行負載下間歇紅，單獨 20 次全綠，尚未完成弧前／弧後同負載歸因。兩者均未因發布而結案。

---

## v0.26.1（2026-08-19）— 一個名字不得有兩種解析

**起因不是新弧，是 Q-033 偵察的複驗。** 偵察由代班代理執行
（`nlang-tools/docs/a_root_only_one_engine_can_build_recon.md`），驗收方複驗時
（`…_audit.md`）翻出一則 Q-032 回歸。

### 缺陷

O58 工單 §2.1 已裁查找方向並明文「不得改變這個方向」：使用者的根在標準根之前。
Q-032 交付 `a71a69b` 新增**兩處**查找，只做對一處：

| 路徑 | 順序 | 位置 |
| :--- | :--- | :--- |
| 裸名 | … → `ctx.root` → `ctx.standard_root` | `lib.rs:3673` → `:3700`（正確，且附了寫對的註解） |
| 投影 | … → `ctx.standard_root` → `ctx.root` | `lib.rs:3813` → `:3840`（**反了**） |

⟹ **同一個名字在裸解析與投影解析下是兩個值**：

```nlang
/add: { mine: 1 }
app: { bare: /add,        ;; → { mine: 1 }      使用者的
       app_: /add(1, 2),  ;; → ⊥ #conflict      使用者的（無 %builtin）
       proj: /add.mine }  ;; → ⊥ #missing_key   標準根的閉合繭
```

〔量〕使用者的欄位**確實進了提交後的根物件、確實進了雜湊**，而寫下它的那台引擎
讀不回來——**不是拒絕，是靜默地回答了別人的值**。與 Q-031「持有但打不開」同形，
粒度由整倉降到座標。

### 為什麼 Q-032 的 P1 是綠的

`the_half_that_was_never_written_probe_test.rs:174` 只斷言 `evolve` 的輸出不含
`Error`。`evolve` 確實成功；失敗在**觀測**。而 O58 要的「四個孤兒變成可遮蔽」
**是觀測性質**。

> **常設教訓（新增）：斷言「沒有報錯」的探針，只見證了沒有那個報錯。**
> 本弧內第三則同族——另兩則為「綠而無見證」（Q-032 P3）與「斷言訊息子字串
> ＝釘拼法」（Q-030）。**探針由驗收方寫並校準，這三則都是驗收方的漏。**

### 修正

`crates/interpreter/src/lib.rs` 投影路徑兩區塊對調並補註。**產品碼 diff 僅此一處**
（15 增 11 刪）。未開 implementation 工單：方向已裁，開單只是把已裁事項再繞一圈。
但保留「探針先寫、先對未修改的二進位校準成紅」。

### 驗收

探針 `crates/oo/tests/a_name_that_resolves_two_ways_probe_test.rs`：
**4 綠（控制組）／4 紅 → 8/8**。四支紅**每一支都觀測**。C4 刻意存在：E4
（12 個保留驗證器名不可遮蔽）管 `&` 那條軸，本次不得碰。

*   workspace **×5 皆 1972/0/0（202 套件）**；基線 1963/1（201 套件）＋8＋1 ⟹ 零回歸。
    已知的 `advert_persistence` 間歇本次五跑未發作。
*   conformance **143/143**。
*   **身分不移動**：標準根 `2da5b713…`、`app: { v: 1 }` 的根 `426d5186…`
    修前修後逐位元組相同 ⟹ patch 形狀（先例 v0.24.1）。
*   對 `nlang-baselines/v0.26.0-verify-target` 真二進位並排：四個座標
    `⊥ #missing_key` → `1`／`2`／`3`／`4`；控制組 `@zzz.mine` 兩版皆 `9`。

### 規格側

`spec/CHANGELOG` v0.26.0-draft.1 的「拆開後四者皆可遮蔽」加更正框（**當時為假，
自本版起為真**）；SPEC_00 新列並移動「(目前)」；REAL_03 §6.8 自陳缺口第一項
（使用者無法定義自己的 `/add`）**解除並註明症狀出於順序而非清單**——**清單本身
的缺口不受影響**，第二項（SPEC_09 §2.1／§2.5 兩表不一致）仍在，屬 Q-033 D2。

### 旁量入 Inbox（不併射程）

*   **去前綴 fallback 使模糊比對贏過精確比對**：`app: { add: 7, use: /add(1,2) }`
    → `⊥ #conflict`。**對 v0.26.0 並排逐字相同 ⟹ 既有，非本版造成**；但本版
    使兩路徑同向，危害隨之由裸名擴散到投影。需裁「`add:` 是否本來就該遮蔽 `/add`」。
*   **SPEC_09 §5.1 六列引擎只兌現兩列**（`~%Logic`／`~%Str`／`~%Option`／`~%Result`
    皆 `_`）。屬 Q-033 D2 的直接輸入，不獨立升 Ready。
*   **`~%Official` 現值 `{{ }}` 違反 SPEC_13 §135**（該節已裁，正解為 `⊥ #missing_key`）。
    **它在標準根裡 ⟹ 移除會移動 digest**，必須搭 D2 的 digest 移動一起做。

---

## Q-035 implementation — 派送去查根（2026-08-23，v0.30.0 之後）

**裁定沿用 O68 Q3.B／Q4.C，無新裁定。** 工單
`nlang-tools/docs/a_name_is_no_longer_a_credential_handover.md`；
repair 工單 `…_repair_1.md`。交付 `nlang-tools 4d047f4`，repair `1f6c2ec`；
規格側 `nlang-spec 6da71f7`（交付方，見下）＋本次驗收方補完一句定義。

### 交付形狀

`lib.rs:3064` 派送點在查 `builtin_registry` **之前**先查表，三個新的具名 `%cause`
（`BottomCause` 尾端追加，既有 discriminant 未動）：

*   `#no_standard_root` —— 脈絡從未安裝表（`standard_root_installed: bool`）
*   `#unprojected_builtin` —— 表有裝，不投影這個名字
*   `#unprovided_builtin` —— 表投影了，而本引擎 registry 沒有（六個死名）

`EvalContext` 另加 `projected_builtins: HashSet<String>`，於安裝時算好。
**兩個欄位都不進序列化，不動身分。** S4：`oo inspect` 對非標準根物件且帶
`meta.builtin` 者印 `note: user-authored %builtin`，只顯示、不拒絕、不改寫。

### 驗收

**一輪 repair。** 三階段增量各自等於當步解除的探針數：
交付前 2018 → 交付 **2024**（＋4 解除 ＋2 新 S2 測試）→ repair **2026**（＋1 解除）
⟹ **零回歸**。全跑 ×5 逐字全同（209 target、err=0），conformance **143/143**，
主探針 9/9、repair 探針 2/2、S2 2/2，皆 0 ignored。

**探針完整性**：交付那輪 `cargo fmt` 重排了探針檔，驗收方去空白、去逗號後
**逐字元比對確認語義未動**（差異僅 5 個 trailing comma），四個 `#[ignore]` 全移除；
repair 那輪探針檔 **0 insert / 1 delete**。

**身分紅線（兩個真二進位）**：同一份源碼，PRE（`ebc0a5a`）與 repair 後
**根物件 CAID 逐字元相同**（`1bf4798a…`，497 B，`cmp` 逐位元組相同），
標準根 digest 兩邊皆 `7038e250…`；交叉讀互通。

### repair 的論旨

`universe.rs:159` `standard_for_root` 對**不指名摘要**的根回傳空表，註解寫著
「Formats 1/2 were self-contained」。閘之前無害（派送不查表）；閘之後
「已安裝的空表」投影零個名字 ⟹ **那個宇宙的標準庫自己也被判為未投影**。

〔量，三個真二進位、同一個倉（`/home/gali/nlang/.oo` 的複本，HEAD 2026-08-14，
根 67,494 B；原倉未寫入，HEAD 前後逐字元相同）〕

| 引擎 | `lib: ~%Math./add (3,4)` |
| :--- | :--- |
| v0.20.0（造它的） | `7` |
| PRE `ebc0a5a` | `7` |
| 交付 `4d047f4` | **⊥ `#unprojected_builtin`** |
| repair `1f6c2ec` | `7` |

**倒下的是合法的標準庫呼叫，不是偽造。** 歷史打得開、名字解析得到、`oo status`
照印——什麼都算不出來，即 REAL_03 §6.8.1 中**可讀性**那一半。

**在野不是空集合**：全機 15 個持有 Combo 物件的倉，10 個的根帶
`__nlang_system_digest`、5 個沒有；其中 4 個為本次量測所造，**第 5 個是超專案自己的 `.oo/`**。

**修法**：`with_standard_root` 在表為 `is_blank()` 時改由使用者根的
`system`／`rules` 軸收集投影名，**不走 `data`**。閘不因此變弱——
〔量〕同一個舊宇宙裡憑空發明的名字仍得 `#unprojected_builtin`；
使用者寫的 `/evil` 亦然（`projected_builtins` 在安裝當下由 HEAD 的根算好，
staged 進不去；提交後亦擋）。

### 規格側

*   **交付方做了規格收尾**（`6da71f7`：`TAG_REGISTRY` §1.6 新設三碼、§2.1 計數 50→53、
    CHANGELOG 增量）。**分工上那是驗收方的事**，已列常設規則。內容經查正確，
    且**明文寫著本弧不關閉 SPEC_05 §3.3 的 MUST NOT**——沒有去改自己沒滿足的條款。
*   **驗收方補完一句定義**：`#unprojected_builtin` 原措辭「憑證是脈絡裡那份**被指名的表**」，
    而自足的根**沒有被指名的表** ⟹ 依原措辭整個舊宇宙的庫都算未投影。
    已改為「表有兩種存放方式，兩種都算」，並明寫 `data` 不是表。

### 本弧買到什麼、沒買到什麼

**沒買到**：SPEC_05 §3.3 的 MUST NOT 仍未滿足。〔量〕七個危險名字**全在標準根裡**
⟹ 閘依 Q3.B 放行，`{{ %builtin: "process.exit" }} 7` 仍 exit 7。**探針 C3 逐字釘住這條界線。**
關它要靠 **Q2a（寫入層）**，仍未裁，乾淨解在弧 D 下游。

**買到**：① 三個今天共用 `#conflict` 的事實分成三個具名答覆（**Q-031 類別第七個呼叫點**）；
② 把巧合換成機制——〔量〕`registry(245) ＼ 標準根(251) = ∅` 而 `標準根 ＼ registry = 6`；
③ O55 的版本綁定第一次對 `%builtin` 生效。**③ 今天量不到差異**：四個歷史標準根
投影的名字集合相同，連 v0.20.0 那個舊根也是 **251 個、與今天完全一致**
（`今天有、舊根沒有 = 0`）。它買的是**下一次標準根變動時**舊宇宙自動保有舊名字集合。

### 旁量入 Inbox（不併射程）

*   **往沒有標準根摘要的舊宇宙寫入，會把它變成讀不回來的倉**：commit 成功，
    下一次 evolve 得 `Error: refusing root: standard root digest 47dc540c… is unavailable`。
    〔量〕**v0.26.0／PRE／repair 後三者同一個 digest、同一句話** ⟹ **至少自 v0.26.0 既有，
    與本弧無關**。
*   **`genesis_test::eval_context_new_has_no_timeout` 現在建的不是 `new()`**
    而是 `new().with_standard_root(…)`，函式名比它實際構造的窄。交付方已自行點名；
    覆蓋未失（`with_standard_root` 只碰三個欄位，不碰 `timeout_deadline`）。
*   **三個新碼沒有 conformance 向量，而且其中兩個不該有**：`#unprovided_builtin`
    取決於各引擎 registry 的缺口，**不是符合性性質**；`#no_standard_root` 在 CLI 上不可達。
    只有 `#unprojected_builtin` 可向量化，**但它與 SPEC_05 §3.3 相牴觸**——
    §3.3 要求實作拒絕使用者資料中的 `%builtin`，而該向量必須讓引擎**求值**一個使用者
    `%builtin` 才能觀測到派送理由。⟹ **本弧不補向量，理由記於此**；Q2a 落地時一併處理。

---

## Q-036 —— 匯入就是 spread（2026-08-24，v0.31.0 之後）

**✅ 已驗收，一輪通過。** 交付 `nlang-tools db9ccea`；裁定沿用 **O72**，**無新裁定**。
工單 `nlang-tools/docs/import_is_spread_handover.md`。**規格收尾另做，見 §規格側。**

### 開單時射程被量測改變

工單原本被排成**純規格**（O72 的三項條文工作）。開單量測推翻了那個排法：
〔量 2026-08-24，v0.31.0〕**兩處正典範例今天沒有任何拼法能跑起來**——
`_: ~%Cond`（規格今天的拼法）、`...~%Cond`（O72 的正準拼法）、`_: { ...~%Cond }`
三者的下一行 `result: /if (…)` **全部未求值**；而 `~%Cond./if (…)` 與別名
`c: ~%Cond` ＋ `c./if (…)` **都通**。
⟹ 只改條文等於把一個跑不動的範例寫進規格，正是 **§2.4** 那一類病。

### 本弧不必發明任何東西

〔量〕**裸名解析今天就會動**，但只在「根座標、且從根層使用」那一格：
`/if: ~%Cond./if` ＋ `result: /if (#true, …)` → **`"yes"`**；
`/double: (x -> x+x)` ＋ `out: /double 21` → **42**。
巢狀同層（`{ /double: …, out: /double 21 }`）與由巢狀向外**都不解析**。
⟹ **缺的只有「把模組展平進根」那一個動作**，不是一條新的查找規則——
這正是 **O72 ⑦**「求值路徑決定局部脈絡」的實測形狀。

### 頂層 spread 有三種錯法，而 Inbox 只記到一種

〔量 2026-08-24，v0.31.0〕同一個拼法，**依前一行而定**：

| 前一行 | 結果 | 性質 |
| :--- | :--- | :--- |
| 無 | 落成一個叫 `"..."` 的鍵，內容未展開 | 看得見（**Inbox 原列只記這個**） |
| `a: 1` | `a: 1..#_["~%Cond"]` | **靜默**——spread 被 `..` 吃掉 |
| `a: "x"` | `a: "x"..#_["~%Cond"]` | 靜默 |
| `a: 1..5` | `a: ⊥ #conflict` | **靜默塌陷** |
| `a: 1,`（逗號） | 恢復成第一種 | 逗號會斷開，換行不會 |

**成因是兩個，不是一個**〔讀〕：(a) `field_start = _{ field_key ~ ":" }` **要求冒號**，
裸 spread 沒有 ⟹ 各處 `!field_start` 護欄擋不住它，`range` 於是吃掉下一行；
(b) 展開分支只住在 Combo 建構（`eval.rs:1227`），`Universe::evolve` 從來沒有 spread 分支。
**(b) 與 D38 同族**：引擎做得出來，然後在另一個邊界上沒有接線。

### 交付形狀

`n.pest` 兩處：`range` 加 `!"."`（第三個點是 spread 不是 range）、
`field_start` 加 `| "..."`（否則 range 讓開之後改由並置吞掉下一行）。
`universe.rs` 新增 `is_spread_field` 與 `evolve_spread`，後者**重用
`expand_combo_pending`**——與 Combo 建構同一條路徑、同一套法則。

### 驗收

**一輪通過。** 全跑 **×5 逐字全同：`targets=210 passed=2034 failed=0 ignored=0 err=0`**；
conformance **143/143**；探針 **7/7、0 ignored**。

**增量對得起來**：弧前（無探針檔）2026／209 target → 加探針檔 2029／210（4 紅 ignored）
→ 交付後 2034 ＝ 2029 ＋ 4（解除的紅）＋ 1（交付方指名的 `golden_top_level_spread_is_not_a_range`）
⟹ **零回歸**。

**身分紅線**（兩個真二進位，PRE 由 `git archive c38e1c6` ＋ 獨立 `CARGO_TARGET_DIR` 建於
`/home/gali/nlang-baselines/q036-pre`，未動倉）：同源碼 `app: { k1: 1 }` 的根物件
`932a9f9d…` 與標準根 `7038e250…` **PRE 與 POST 逐位元組相同**，且與開單當下所釘一致。

**diff 純度**：把 `c38e1c6` 版的 `universe.rs` 先 `rustfmt` 再與交付版比對——
**95 行新增、實質刪除 0 行**（唯一「刪除」是一個空行）⟹ 那批 fmt 重排**語義為零**。

### 驗收方自行補做的量測（交付報告未答工單 §2.1 的三個交互）

工單要求「報告中逐項回答」三個交互，交付報告未答。驗收方自量，**三項全過**：

1.  **Q-035 派送閘**：`...~%Math` 進根後 `/add (3,4)` → **7**（合法呼叫通）；
    憑空發明的名字 → **⊥ `#unprojected_builtin`**（偽造仍擋）。
    `process.exit` 偽造仍 exit 7 —— **那是 O68 Q3.B 的既定放行**（該名字在標準根裡），
    Q-035 探針 C3 逐字釘住，**非迴歸**。
2.  **`~` 私有性**：`p: { ~s: 1, a: 2 }` ＋ `...p` ⟹ 根只得 `a: 2`，`~s` **沒有**進根。
3.  **根層碰撞**：`/add: 99` ＋ `...~%Math` ⟹ **`/add: ⊥ #conflict` 而其餘 48 個成員全部存活**
    （O72 ④：碰撞即 ⊥，不得覆寫）。

**另補三組迴歸量測**（PRE／POST 對照，皆 SAME）：
14 個合法 range 形式、7 個巢狀 spread 形式、
以及**一般（非 spread）座標碰撞**——`Error: Evolution Conflict … at a` / exit=1 /
staged 未動，**PRE 與 POST 逐字相同** ⟹ 交付方「順手改動 #3」確實只在新路徑內。

**commit round-trip 已驗**：`...~%Cond` ＋ `r: /if (…)` 提交後，
CAS 根物件 `data` ＝ `[r]`、`rules` ＝ `[cond, if, match]` ⟹ 展平後的成員確實入了歷史。
（`oo eval '_.r'` 回 `_` 是**既有**的 Q-018 可見性問題——不用 spread 的對照組與 PRE 皆同。）

### 交付方未指名的兩處（都不是缺陷，但依「順手改動須逐項指名」記在這裡）

*   **`universe.rs` 的一批 `cargo fmt` 重排**（`new_with_standard` 簽章、三處 `get_root`、
    五處 `StandardRootUnavailable` match 臂）。已如上證明語義為零，但報告未提。
*   **畸形輸入的行為改變**：`1...5` 由**靜默的 `_`** 變成**響亮的 parse error**；
    `{ a: 1....5 }` 由 `1..#_..5`（引擎自己發明的三段 range）變成 parse error。
    〔量〕全機語料 `[0-9]\.\.\.` **0 命中**，14 個合法 range 形式全部未動。
    ⟹ **判為改善而非迴歸**（靜默的胡說 → 響亮的拒絕），但它是 `!"."` 的後果而非孤立選擇，
    報告應當指名。

### 規格側

**本弧交付方未改規格（工單明令），規格收尾由驗收方另做**——即 O72 §7.2 的三項：
(i) `SYNTAX_05` §3 與 `SPEC_09` §5.2 的範例改 `...`；(ii) `...` 三性質入規格；
(iii) `_:` 作為預設分支入規格。**皆須補向量。**

⚠ **向量現況已重量並更正**：先前記「三者皆 0 向量」不精確——
spread 有 **12 個 L2 向量**（`36`–`42`／`57`–`59`／`63`／`81`–`82`），
釘住碰撞即交集、`~` 私有性、循環、blur 吸收與前向參照；
**但 O72 指名的三個性質各自 0 向量**：spread 一個 cocoon `{{}}` **0**、
可交換性 **0**、`.%effect` 逐欄位保留 **0**。匯入 **0**、`_:` 預設分支 **0**、頂層 spread **0**。

### 旁量入 Inbox（不併射程）

*   **⚠ 同一個 `oo evolve`，兩種碰撞給兩種答案，而其中一種無聲**：
    〔量 2026-08-24〕一般座標碰撞 → `Error: Evolution Conflict … at a`、**exit=1**、staged 未動；
    spread 碰撞（`/add: 99` ＋ `...~%Math`）→ **無輸出、exit=0**，⊥ 靜默寫進 staged 的 `/add`。
    **這是 D33／D40 那一類的新實例**——「收斂撞 ⊥ 必須停下並回報」，而這裡沒有報。
    **不判為本弧缺陷**：工單未要求回報，且 spread 若比照一般碰撞升為 Evolution Conflict，
    會為了 1 個衝突丟掉 48 個好成員，那更糟；per-field ⊥ 正是 **O72 ④** 所裁。
    ⟹ **屬 W3′-b／Q-017 的類別**（阻塞於 Q-016），**依「修類別不修個案」不在本弧修**。
*   **`evolve_spread` 的 `local_fields()` 迴圈疑為死碼**：〔量〕`expand_combo_pending`
    已把私有成員排除在 incoming 之外（交互 2 實測 `~s` 不進根），故該迴圈觀測不到觸發。
    它與公開欄位那個迴圈同形，是防禦性寫法，**不是缺陷**；記此以免日後誤讀為有意義的路徑。
*   **頂層 `...zzz`（解析不到的名字）靜默得 `{}`**：與 `..._` 同形，落在既有的
    「未知 ⟹ 未知」那一列（該列本身仍是 §2.5 首例，規格 0 條文、向量 0）。
