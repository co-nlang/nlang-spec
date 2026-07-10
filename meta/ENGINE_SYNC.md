# ENGINE_SYNC — n.pest 對 SPEC_14 的同步清單

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
| 5 | tuple ＋ `list_sep`（`,`/`;`、尾隨可省） | ✅ `ExprKind::Tuple`；求值＝**定長密封**數字鍵 Combo——密封只及 arity，`%effect` = 元素 max（2026-07-06 裁決：效應屏蔽為 Cocoon 專屬；SYNTAX_04 §2.5） |
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

## Range 語義補完缺口(2026-07-11,比較節遷移驗證時曝光;引擎側待派)

比較節裁決(`>= 18` 等裸比較節不入文法,全規格 27 處遷移至 Range 拼法)後,
以引擎實測遷移後向量,曝光四個未實作面。舊文本不過 parser,故皆為**首次曝光**
而非回歸;`10 & 6..`→`10`、`@{ 6.. } & 10`→`10`、`@{ 5 }: …` 分派均正常。

- **E1 型別標記 × Range**:`@int & 6..` → ⊥Conflict(應為 `6..` 之整數精化)。
  `@int & 10`→`10` 正常,標記 unify 缺 Range 臂——「新值種 × 既有機制」**第三例**
  (同 5b501e5/Union 分配蟲族)。REAL_05 合規向量 L1-05(`@{ @int & 6.. } & 10`→`10`)
  需此修。
- **E2 分派鍵含 Range**:`f: { @{ 4.. }: "A" }` 後 `/f 5` → ⊥Conflict
  (SPEC_03 §、SPEC_06 §、SPEC_07 §5 範例全依賴)。極小元判定需 Range 序比較——
  即既排 backlog「Range 子集 cmp」,現在有規格級需求向量。
- **E3 Range 正交補**:`!(..0)` 單獨求值即 ⊥Conflict(SPEC_07 check_pos 新拼法
  `x -> @{ $ & !(..0) }`,嚴格正性之稠密域唯一拼法)。Not × Range 未實作。
- **E4 `@Name` 引用不攜帶定義**:`@Adult: {…}` 後 `x & @Adult` 中 `@Adult` 解為
  `{{%kind: #type_constraint, %type: "Adult"}}` nominal 標記,欄位約束不進合併
  (README 門面範例因此不 enforce;裸名模板 `T: {…}` 則正確坍縮)。nominal 型別
  解析未接線,件級較大,宜獨立工單。
