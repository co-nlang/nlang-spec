# ROADMAP — 工作路線圖

> 更新：2026-07-05。取代 `spec/zh_TW/README.md` §4 的舊 TODO 表（其 P0「銜尾蛇量子化」
> 早已完成，見「已完成」節）。狀態標注若與現況不符，以使用者修正為準。
>
> **角色釐清（2026-08-13）**：本檔只保存里程碑與長程 gate，不再兼任引擎施工
> 佇列；其中「進行中／排隊中」是歷史策展，可能落後於現版。當前工作與唯一
> 下一弧見 [`WORK_QUEUE.md`](WORK_QUEUE.md)，引擎實際交付史見
> [`ENGINE_SYNC.md`](ENGINE_SYNC.md)。

---

## 1. 里程碑門檻（gating）

| 里程碑 | 門檻 | 備註 |
| :--- | :--- | :--- |
| **對外宣傳（intro 發表）** | **= v0.2.0 分水嶺（版號政策已裁 2026-07-11，`meta/VERSIONING.md`）**——本輪 merge review 定版即解鎖 | 素材：`meta/history_origins.md` ＋ workspace 側 intro 草稿（兩版未完成） |
| **Changelog 啟用** | **= v0.2.0 起筆（已就位：`spec/CHANGELOG.md` 含分水嶺策展條目，merge review 時定日期）** | 版號政策：規格/引擎共用 major.minor、patch 各自；引擎裸核＝REAL_05 門檻；**fmt v2 自 v0.2.0 凍結**（合法差異窗口關閉，SPEC_00 §4.4 註 2） |
| **Epoch 0 起點** | v1.0.0 正式發布之物理時刻 | ORDER_00 §5、ORDER_01 §1.1 |

## 2. 進行中

| 流 | 項目 | 說明 |
| :--- | :--- | :--- |
| 規格 | **SYNTAX_01–10 語法細則** | **01–12 全數 `[穩定]`（2026-07-05 定稿完成）**；macro、import、`%effect` 均已除名（`%effect` 屬語義域，2026-07-06）——**SYNTAX 系列無待排項**；`$` **P1–P5 全定案**——超級惰性語義成為語義要求（路徑導向觀測；ENGINE_SYNC #16）。關鍵路徑瓶頸**轉移**：規格已釘死 → **引擎已同步（2026-07-06，ENGINE_SYNC #1–#16 急切範圍全銷；殘留＝惰性引擎半邊）** |
| 引擎 | **oo／nlang-tools stdlib 與協定 phases** | Phase 47+（~%Set/~%Stat/~%Csv/~%Url/~%Toml 已入；後續 phase 由引擎側排程）。**惰性引擎 Stage 1+2+3 ✅（2026-07-07 整治後驗收通過：交付 `705bfb1` → 驗收代修 `db83eb8` → 整治 `272b180`；`v.w.x.a → "Logic"` 完成定義達成，銜尾蛇向量全五行綠）**；F2 ✅ 結案（`97a0bcd`：OOM 真兇＝探針助手克隆遞迴，量測證偽 sub_context 之說；Arc root 保留＝效能收益）——殘留＝memo Stage 4+／快照語法另案 |
| 審計 | **claims ledger 後續** | L11 Path 2（進行中）：**handover doc ✅（2026-07-07）→ Tier 1 實作 ✅ → 驗收 ✅（2026-07-07，`nlang-tools/crates/oo`：`nlint` + `oo lint`；R1/R2/R3 + ω(G) + K4/K5 candidate sites + JSON tier1-v1 + 防火牆；驗收含三修正〔原子形態 Tier C、tier U 發射、見證可解索引〕；oo 24 測試、workspace 84 套綠；`1f73d76`）** → 對規格自身 lattice 量 Ouroboros nerve 的 ω(G)（`meta/claims_ledger.md` N2；另一前提＝規格書 Combo 化）。三條靜態規則＝discussion/019 §4（rerun-safe、正片段、密封×加鍵） |

### 2a. SYNTAX 定稿衝刺（關鍵路徑提案，2026-07-05，待裁）

現況的依賴鏈：**SYNTAX `[草稿]`→`[穩定]` → 引擎可無返工實作 → 規格書 Combo 化 →
（自我驗證里程碑 ＋ ledger Path 2 實驗）→ intro 門檻**。瓶頸在第一環，且九章草稿已存在，
缺的是定稿。提案分波：

| 波 | 章節 | 解鎖什麼 |
| :--- | :--- | :--- |
| **Wave 1（資料面）** | 01 詞法、02 字面量、03 路徑、04 容器、05 前綴、08 元數據 | spec-Combo 化的 parse/serialize；linter Tier 1 實驗只需要這一波 |
| **Wave 2（語義面）** | 06 比較/子型別、07 觀測對偶、09 態射應用 | 自我驗證（收斂檢查）、引擎執行語義 |
| **Wave 3** | 10 Enum/Poset；之後視需求：態射定義、管道、import、%effect | — |

每章的定稿審查 pass = 模板合規（SYNTAX_00 §4）＋ §4 邊界情況完備性 ＋ 跨章一致性
（syntax-minimalism 原則、`$` 凍結條款）＋ **引擎現況對照**（草稿 vs oo 已實作行為的
diff → 產出「待裁清單」：品味決定歸使用者、機械修正直接改）。

> **素材標記（2026-07-07，使用者）**：discussion/018（Kleisli 拆解）與 019（nucleus 三層
> 分類）標為未來 **n/ 自己的 paper**（語義／實作論文，非數學系列）之素材。

## 3. 排隊中（依賴或時機未到）

| 項目 | 依賴／時機 | 說明 |
| :--- | :--- | :--- |
| 規格書 Combo 化（自我驗證） | 引擎 SPEC_17 支援（現 0%） | 舊 TODO 的 P1；也是 Path 2 實驗的前提之一 |
| 增量收斂引擎原型（GUIDE_03） | 引擎側 | 舊 TODO 的 P0；**現況已確認（2026-07-07 審計）**——Route A（unify memo）**存在且已加固**（略）；Route B（DAG）**0%**（略）；惰性基底 **Stage 1+2+3 ✅**（整治後驗收通過 2026-07-07：F1 deref-$框架 ✓、F2 ✅ 結案（根因實為探針助手；Arc root 保留）、F3 衛生筆記 ✓）。**Stage 4 ✅（2026-07-08 驗收通過：交付 `8a00b4d`＋驗收代修 `8229676`——紅線探針揪出 memo key 漏觀測方綁定分量的 soundness bug，改有效綁定；root CAID 惰性快取；§11.3 實作註記補上）；**Stage 5 ✅（2026-07-08 驗收通過：交付 `13f6464` 紅線全綠＋驗收代修 `fe4522b`——實測洞＝engine 內部語境繞閘參與 memo，補 `memo_enabled`；hit-float／雙形式座標＝縱深防禦誠實標注）——增量收斂引擎 Route A＋B＋惰性基底全線落地**；殘留＝快照語義（已暫裁「＝Commit/CAID，不加語法」，SPEC_10 §1.2，2026-07-08；source-level 重開條件併入下方「首次使用複審」）、`Atom(Top)` unify bug（✅ 2026-07-08 結案）**。 |
| 想法 D Tier 2：linter 讀真 ω/q | CAID v2 symplectic fingerprint 實作（SPEC_13 §1.3） | Tier 1（純圖論）不需等。**APP_02 兩軌重寫（2026-07-11）後同一指紋兼任 GPP 驗證軌證明對象**——fingerprint 工程一次解鎖 linter Tier 2 ＋ ZK 身分電路（APP_02 §6.7.1：fmt v3 封套雙承諾接口） |
| APP_02 兩軌重寫的衍生 TODO | 規格側小項 | (a) SPEC_15 §7.1 ✅ 兩軌改寫（2026-07-11；**成本量化仍 TODO**，條目內明文）；(b) REAL_02 §7 ✅（封包改 fingerprint_commitment/identity_proof＋mass_hint 退出驗證義務）；(c) fmt v3 時 CAID 封套納入 ω/q 摘要（雙承諾；REAL_03 §0 框注已預告）；(d) APP_05 §5/§6 ✅ 重寫（2026-07-11：GPP=身分證明〔指向 APP_02 §6〕＋confidence 執行軌；CIP claim＝收斂鏈粒度 (CAID_in,q,H)→(CAID_out,fuel)，良定義由視界決定論承保；證明分級 L1 樂觀 trace 抽查／L2 遞迴 STARK；§6.2.1 L-S 段刪除，乙太坊類比正名——fuel=gas、CIP=rollup proof）；(e) 第二/三波標注件（audit #6–#11）✅（2026-07-11：APP_04 新增 §5 特徵二影子指針節〔原 §5–7 改號 §6–8〕＋關係表一列；APP_06 §4 封套/本體補句；COSMOLOGY/01 §8 半句；GLOSSARY GPP/CIP 條＋COSMOLOGY/GLOSSARY 繞射/鎖定條；APP_01/GUIDE_02 執行軌框注；SPEC_08 fuel 表 GPP 500 註記待 𝔽₂ 校準）。**衍生 TODO 僅餘 (c) fmt v3 雙承諾＋SPEC_15 成本量化** |
| **✅ 引擎 bug〔已結案 2026-07-08〕：`Atom(Top)` 不走 unify 的 Top arm** | 引擎側小刀；工單 `docs/atom_top_unify_handover.md`；探針預置 `1e12872`（含跨模型驗收章）→ **完成 `04df5c4`＋忠實別名整治**（外部 agent 交付 A＋B，驗收方 Opus 補別名臂忠實化＋帳務） | Stage 5 探針構造時撞見（2026-07-08）：`t: {flag: _}` 後 refine `t: {flag: 2}` → `Conflict`——字面量 `_` 求值為 `Atom(AtomKind::Top)`，unify 么元臂只匹配 `Value::Top`。**修法（預裁決 A）**：eval 正規化 `Atom(Top) → Value::Top`（`eval.rs`＋`lib.rs` `_` 臂），另加 unify `Atom(Top)` 別名臂（縱深防禦，**重入 `Value::Top`** 保 Union 正規化忠實）。驗收：三探針 unignore 全綠、workspace 94 套 612 綠、Stage 4/5 memo 紅線原樣、ENGINE_SYNC 補列。CAID 注意：`_` 回印不變、bn_serial 位元改（合法差異）。 |
| **✅ 引擎:Range 語義補完 E1–E3〔已結案 2026-07-11〕**；E4 待派 | 工單 `docs/range_gaps_handover.md`；探針 `17f8399` | **E1**：`validate_value` 對 Range 驗非錨點界；`type_constraint_meet` 鏡像雙向（Combo×Range，非僅 Combo×Combo）；界不改寫。**E2**：`%val` 常值規則；`resolve_pattern` 解析 range 鍵；`filter_minimal` 比 pattern 不比 unified；`apply_morphism` 走 pattern 表（排除 `%builtin`/curry 數字鍵）。**E3**：meet 語境 `x & !(range)` 成員否定（Union 分配）；standalone `!(range)` 仍 ⊥。**驗收(驗收方,2026-07-11)**:通過+一件代修 `2991096`(E1 早臂 marker×ANY 搶佔 Union 分配——臂序蟲族**第四例**,縮權至 marker×Range;revert 非目標區假前提編輯)。探針 26/26;workspace **693/0/3**。**✅ E4 nominal `@Name`〔已結案 2026-07-11,零代修〕**(交付 `9db9090`+驗收 `52353d1`:內建保留集標記/其餘查找鏈/查無直通;README 範例端到端首次通過;708/0/3)。**Range 語義補完 E1–E4 全數結案,引擎派工隊列空**。遺留另案:Union 通用去重、use-before-def lint(想法 D Tier 1)、步進∩步進 CRT、§4.10。 |
| **SYNTAX 缺口:動態鍵(`@{expr}` 作鍵位)無語法裁決章** | 規格側;**RFC-0001 候選** | 語義有家(SPEC_03 §3.2:模式匹配鍵)、語法無家:SYNTAX_04 只裁值位(集合強制+透明),鍵位懸空——鍵內合法表達式類、與 `a[expr]`/tag 鍵(SYNTAX_03 §10)的分工、分派極小元判定。同家引擎債:E2(分派鍵 Range cmp)、field_key path-vs-named 另案。**開放設計題:list/tuple 作鍵**(積座標/複合鍵)——依「勿先發明語法」緘默,已起案為 **RFC-0001(Draft)**:rfcs repo 骨架已建(2026-07-11,`/mnt/d/Workspace/ai_ai/rfcs`,README 含 v0.500.0 前過渡治理條款+模板;起案人傾向選項 C 緘默等使用證據);GitHub 上線(`gh repo create co-nlang/rfcs`)與 submodule 掛載待使用者。 |
| **✅ REAL_05 合規矩陣〔2026-07-11〕** | 45 向量(L1×25/L2×20)+ `conformance/` 語料庫 + runner 契約 + 參考 runner | 裸核閘門自此可機檢(VERSIONING §3);全向量先經 beta.2 引擎驗證拼法;引擎現況 **45/45〔2026-07-12 L2-17 結案,零代修〕——裸核門檻達成**(交付 `3db91f1`;ENGINE_SYNC 結案條;**引擎 v0.2.0 裸核版已定 2026-07-12**,tag 於 45/45 實測 commit);**2026-07-12 矩陣擴至 47**(L1-26/27 前向引用 = SPEC_03 交換律可執行化)——**前向引用結案 2026-07-12,零代修第四例**(`f9dd657`;**v0.2.1 已定版**,tag 於 47/47 實測 commit);**同日矩陣擴至 48**(L1-28 聯集冪等)+ **Union 去重×R4 lint 雙子單結案 2026-07-12,一件代修**(`0b0a788`+多參態射誤報代修;762/0/3、**48/48**;R4 全語料掃描零誤報,真陽性反哺語料清理清單;想法 D Tier 1 之 use-without-def 儀器化落地);**`.n` 語料清理完結 2026-07-12**(11 件舊期望歸零,unit 65/0;曝光缺口 **G1 combo 等值/G2 `/`柯里定義打包/G4 去重×導航**→ENGINE_SYNC 量測);**G2 重診斷並開單 2026-07-12**(G2 解體為 G2-M 多參糖未去糖/G2-S root 內建 `/add` 影蓋毒宇宙/G2-C 原子×態射繭吸收,`/` 非變因;新曝 **G5 tuple 參數解構未實作**另單;工單 tools `docs/g2_shadow_multiparam_handover.md`,11 紅門+12 釘;矩陣擴至 **50**,L1-29 開單時紅 = 工單門、L1-30 即綠);**G2 三件同日結案(零代修第四例,`05e62ca`/驗收 `60cdf44`:parser 去糖+root 影蓋 evolve 攔截+原子×態射 ⊥;785/0/3、conformance 50/50)**;**v0.2.3 已定版**(top `8d97c4f`,tag 於 50/50 實測 commit);**G5 tuple 解構同日結案(零代修第五例,`8de3144`/驗收 `27d84fe`:`%params` 打包+分派側位置解構;800/0/3、conformance 51/51;Union 引數逐支解構驗證)**;**v0.2.4 已定版**(top `09ef211`);**G4 重診斷+同日結案(零代修第六例,`fef564c`/驗收 `c8bc908`:navigate_segments Union 臂逐支投影;813/0/3、conformance 52/52;真相=Union 導航從未實作、去重紅鯡魚)**;**v0.2.5 已定版 2026-07-13**(top `d4cc816`,tag 於 52/52 實測 commit);**G1 裁定批准入法 2026-07-13**(Q1=`==` 誤用 ⊥ #conflict、Q2=效果參與;SYNTAX_06 §4 #11–13;矩陣擴至 **56**,L1-33~36 開單時四紅 = G1 工單門,工單 `docs/g1_combo_equality_handover.md`);**G1 同日結案(零代修第七例,`f5e71fc`/驗收 `c37bca1`:固化+統一等值關係+家族邊界 ⊥;838/0/3、conformance 56/56;校準曝 G6 混血觀測另案)*;**v0.2.6 已定版**(top `309ce3f`,tag 於 56/56 實測)****G6 值語境統一律入法+開單 2026-07-13**(SYNTAX_06 §4 #6+SYNTAX_07 §4 #6 對偶;L1-37~39 三紅=門,矩陣 59;工單 `docs/g6_hybrid_collapse_handover.md`,8 紅+10 釘)**G6 同日結案(一件代修,`ce7a2cc`+驗收代修:值語境剝殼+觀測投影+結構標記;導航透明化代修由反事實抓回;856/0/3、59/59)**;**v0.2.7 已定版**(top `acaa6cf`,tag 於 59/59 實測;`oo --version` 綁 git tag)****G3 重診斷+裁定入法+開單 2026-07-13**(帳載第五次修正:視界抹除非 cause 精化;SPEC_08 §3.2.2 視界傳播律;L2-21/22 兩紅=門,矩陣 61;工單 9 紅+6 釘;test_canonical 出 pending 併單)**G3 同日結案(零代修第八例,`2811437`:值語境 Blur 吸收全臂+深度門 FuelExhausted+CLI 64MiB;871/0/3、61/61、語料 74/0;協議違規註記第二次)**;**視界參數劃家 ~%Config 入法 2026-07-13**(SPEC_08 §3.1 規範家+節點提示降級;**收斂單已開**:裸名化/max_lifting_depth/策略併家/R5 lint;L2-23 紅=門,矩陣 62);**v0.2.8 已定版**(top `2c3face`,tag 於 61/61 實測);**config 收斂弧結案 2026-07-14(零代修第九例,dev `7763bb3`:七欄裸名+max_lifting_depth 佈線+策略三家併一〔死展示欄移除〕+R5 lint=想法 D 儀器第二件;887/0/3、62/62、語料 74/0)**;**v0.2.9 已定版 2026-07-14**(top `ceb08db`,tag 於 62/62 實測;`--version` ✓);**Blur 邊界律入法+開單 2026-07-14**(SPEC_08 §3.2.2 #5 座標吸收/#6 `=` 二段律〔同 CAID→#true 決定論+去重一致;其餘吸收,twin 量測證 #false 為謊〕/#4 擴 %caid;`===` 否決;`<`/`<=`×blur 歸 §4.10 變因隔離;L2-24~27,三紅=門,矩陣 66)**Blur 邊界同日結案(一件代修,`646269d`+`ceaef12`:吸收臂跳出段迴圈破導航合成性 x.a.b≡(x.a).b,內聯/綁定歧異——代修續迴圈+釘;907/0/3、66/66;既有債曝光=nav×⊥ 同形合成性歧異另案)**;**⊥ meta 觀測整流+#invalid_path 廢止入法+開單 2026-07-14**(F1 合成性/F2 %cause Cocoon 補 %val=對偶自動歸位/F3 無因回 _/F4 廢鑄:原子開放.^溢出=#out_of_horizon 正典上崗.聯集全⊥=REAL_04 §4 主因果;G4 條款修訂 ({a:1}|7).a→1|_;L2-28~31 四紅=門,矩陣 70;同日曝光記帳:私有軸未實施/G4 惰性⊥支未剔/^解析觀測語境未接/cause 正典審計)**;**⊥ meta 整流同日結案(一件代修,`81dd138`+`085fe9a`:排序移除破 (1|2)=(2|1)——代修=Union 多重集等值,SPEC_01 歸位;門×釘可滿足性聯檢教訓;930/0/3、70/70)**;**v0.2.10 已定版 2026-07-14**(top `0d97df1`,tag 於 70/70 實測;`--version` ✓);**私有軸實施+~.錨廢止入法+開單 2026-07-15**(SPEC_04 §3.1 #4 顯示剝除/#5 幾何內外判準新增、§2.2 ~.廢止=與裸名冗餘;量測=私有軸全面反轉:外阻全通/內通全斷含規格自身範例/~%系統軸豁免陷阱;L2-32~35 四紅=門,矩陣 74)**私有軸同日結案(零代修第十例,`dc1a807`:seal_defining_scope+攔 ~ 段+strip_local_axis;948/0/3、74/74;曝光記帳=spread 滲出/新)**;**v0.2.11 已定版 2026-07-15**(top `407bc32`,tag 於 74/74 實測;`--version` ✓);**spread 私有保全開單 2026-07-15**(SPEC_03 §3.1 既有法引擎追法;內外判準沿 SPEC_04 #5 幾何路線;L2-36/37 紅=門、38 綠=法釘,矩陣 77;同場曝光=展開碰撞未依法交集合併 `{a:1,...{a:2}}`→覆寫 另案+態射體內根名解析 另案)**;**spread 同日結案(零代修第十一例,`6a06716`:insider 幾何判準+外部跳過 local;偽造對抗全正;959/0/3、77/77)**;**v0.2.12 已定版 2026-07-15**(top `b6da107`,tag 於 77/77 實測;`--version` ✓);**展開碰撞弧入法+同日結案 2026-07-16(零代修第十二例,dev `af2e989`:SPEC_03 §1.1 重複鍵合併新法+§3.1 ⊥ 展開因果傳播修訂;merge_field_into 碰撞交集全寫入點+原子殼 {%val,_}+C4 復用 computing 零新狀態;L2-39~42 四紅=門,矩陣 81;984/0/3、81/81;別名繞道→#divergent 超單改善;協議違規一筆=交付紀錄缺席驗收方代記;曝光=Blur 展開源靜默 no-op 另案+前向引用×spread 另案)**;**v0.2.13 已定版 2026-07-16**(top `158bdb0`,tag 於 81/81 實測;`--version` ✓);**詞法雙弧 2026-07-16(帳載修正第七次:態射體內根名不再重現,真病灶=公有 combo 詞法鏈全斷〔seal local 空跳過門誤傷〕+遮蔽錯值謊言;詞法作用域弧一件代修=跨層 %id 分裂→%id 走 force_recursive 固化,L2-43~46 矩陣 85;補完弧零代修第十三例=lexical_forcing 軟再入+cocoon 先 seal 後 force+單段 seal 語料耗時淨改善,L2-47~49 矩陣 88;動態作用域洩漏對抗兩形皆淨;曝光另案=cocoon 本徵態預設 ⊥ 未實施/互指自指裁定候選)**;**v0.2.14 已定版 2026-07-16**(top `0e83268`,tag 於 88/88 實測;`--version` ✓);L3 向量波 v1.0.0 前補 |
| **首次使用複審（commit/evolve 人體工學 ＋ 快照 source 語法）** | 觸發＝引擎有可實際驅動的 REPL、有人真正跑過 observe／evolve／commit／collapse | 兩件事是**同一問題**（皆取決於實際使用體感，非紙上設計）：(a) 現行 git-式 commit/evolve 模型（SPEC_10）的人體工學是否真的順手——目前設計為對 n/ 的想像，尚無人用過；(b) 是否值得為 **Staged 中間態快照**／歷史 Commit 值嵌入 source 付一個新語法（SPEC_10 §1.2 有意留白）。**在真實使用證據出現前，勿發明語法**（反轉不對稱：晚加可逆、早加沾黏）。 |
| **Parser 靜默變形掃描（fuzz／golden-AST）** | ✅ 全 SYNTAX 向量＋EOI 護欄（2026-07-09）；**驗收通過（2026-07-10）** | **已交付**（`08c0fd5`＋`2885ed7`）：golden 20 套（SYNTAX_01–12 §4 形狀＋拒絕向量）、roundtrip 語料擴充、fuzz 800×d3（含 TypeAnn／Range）。**本輪新修**：(1) `parse_expr_only` 改 `expr_toplevel=SOI~expr~EOI`——堵住 `a <=> b <=> c`／`x: leftover` 等**尾隨靜默丟棄**；(2) TypeAnnotation 印 `@` 非 `:`；(3) Apply 對 `/g` 引數加括號；(4) 巢狀三元 else 強制括號。**驗收（2026-07-10，重跑＋diff-read＋量測）**：102 套 640 綠 0 敗（3 ignored 皆既存已知）、Stage 4/5＋Atom(Top) 紅線原樣、無空提交且交付方自帶 ROADMAP 記帳。**驗收補帳三筆**：(a) CAID 合法位移——Thunk bn_serial 走 `expr.to_nlang(0)`（`bn_serial.rs:78`），印表機正規化＝含 Float／純虛複數／TypeAnn／新括號策略之 thunk 舊 CAID 已變（一次性合法差異，見 ENGINE_SYNC #19）；(b) `1..10` 行為位移——交付前 parse 大聲報錯、現在 parse 成功但 eval 無 Range 臂 → 萬用臂 ⊥Conflict，`{x: 1..10}` 觀測 `x: _|_` **全靜默**（合法字面量偽稱 Conflict；見下方 Range eval 另案）；(c) `@{}` 落地暴露 Atom(Bottom) 吸收律違反（見下一列）。殘留＝cargo-fuzz 外掛（可選）、field_key path-vs-named 語意另案。 |
| **✅ 引擎 bug〔已結案 2026-07-10，驗收含代修〕：`Atom(Bottom)` 吸收律違反（Atom(Top) 之對偶）** | 探針 `e7d2fcb` → 交付 `9727f1a` → 驗收代修 `26b31fb` | **修法 A**（同 04df5c4）：`eval.rs` `AtomKind::Bottom` → `BottomCause::Conflict.into()`；`resolve_path` `_|_` 臂同；`unify_internal` 別名臂重入（忠實別名，同 5b501e5）。交付照預裁決、探針未弱化。**驗收抓到回歸並代修**：正規化讓 ⊥ 抵達 `LatticeEq` 吸收早退，但 `=` 家族**不塌縮不吸收**（SYNTAX_06 §4.1）——`_|_ = 3` 基線 `#false`→修後 ⊥（worktree 對照量測；基線正確靠的正是同一隻 Atom 漏洞）。代修＝`LatticeEq` ⊥ 作空集運算元：(⊥,⊥)→`#true`、(⊥,x)→`#false`（stash 反事實武裝確認）。終態 **103 套 648 綠 0 敗**；探針 8 活（含 `=` 家族 2 新無回歸線）＋紅線清畢。CAID：含字面 `_|_` 的 bn_serial 改走 `Value::Bottom`（合法差異）。**教訓**：修法移動兩家族邊界時探針須釘住兩側。 |
| **✅ 引擎 bug〔已結案 2026-07-10〕：`<`/`<=`/`>`/`>=` 極值端違 SYNTAX_06 §4.2** | 工單 `docs/cmp_extremes_handover.md`；探針 `09ec048` | **修法**：`eval_binary_cmp` 按 `CmpOp` 分流——Eq/Ne 吸收不動；Lt/Gt/Lte/Gte 先 force 兩側、collapse 後極值表（Gte≡Lte 鏡像、Lt＝嚴格子集），有限路徑不變；永不回 `_`/⊥。**驗收**：`cmp_extremes_probe_test` 8/8 綠（5 紅 unignore＋3 活護欄）；workspace **656 過 0 敗 3 ignored**（工單目標吻合）。`3 <= 5` 仍 `#true`（§4.10 另案防火牆）。ENGINE_SYNC 補列。 |
| **✅ Range／`@{ expr }` 求值語義〔已結案 2026-07-10〕** | 工單 `docs/range_eval_handover.md`；探針 `16db350` | **落地**：`Value::Range {start,end,step}`；eval `Range`／`AnonSet`（`@{e}≡e`）；unify 成員（閉端＋步進）＋無步進交集（空⊥／單點塌縮原子；步進∩步進→⊥ 另案）；parser 缺界→TagStart/TagEnd；golden 三條授權改錨點。**驗收（2026-07-10，含代修 `b3f9316`）**：交付面全對（探針等同、golden 恰授權三條、真值表手驗）；對抗量測抓到 **Union 分配被 `(Range,_)→Conflict` catch-all 搶先**——`(1\|7) & 1..3` 實測 Conflict 應為 `1`（SPEC_07 §4；`5b501e5` 同族臂序蟲）。代修＝catch-all 讓位（decline），Union/Thunk/Combo 交回既有機制；分配護欄入永久套件、stash 反事實確認。終態 **667 過 0 敗 3 ignored**。bn_serial `TAG_RANGE=0x18`（無既存 CAID）。`~%List./range` 半開不動。臂序教訓（第二次同款）：unify 早臂 catch-all 預設 decline 而非 Conflict。ENGINE_SYNC 補列。 |

## 4. 已完成（自舊 TODO 表以來的大項）

- **想法 C 落檔（2026-07-07，research `a438a91`）**——C-O 地層銳化，對 ar5iv 全文核對：
  維度公式（Prop 2.7，僅 N>2n）與 genericity 構成性（連 sign invariants 都要非零 ω）驗證；
  **修正我方舊措辭**（「pairwise-transverse」→ C-O 相鄰 Lagrangian 本就共享 (n−1) 維）；
  正交性升級為**結構性**：pentagram 的 K₅ 關聯型 vs C-O 循環型＝不同配置範疇、參數域
  N=5<2n=8 在其定理範圍外、域 F₂ 被排除——「不是他們 modulus 的影子，是他們不進的地層」。
  co_reduce.py 的「正交非化約」拿到回溯性的 why。**研究側四想法 A–D 至此全數落檔。**

- **想法 A 落檔（2026-07-07）**——binarity 設計契約：Paper N §3 remark（形式版，research `be0cd0a`，編譯 9pp 乾淨）＋ APP_07 §4 工程句（spec `140bde7`）。兩個精確化內建：契約管相位代數生成元非語法元數；強度不對稱（binarity⟹ceiling 定理級、逆向未證——放棄保證≠必然障礙）。順帶補上想法 B 的 Paper N 尾款（圖說「虛線遵循 1+2^i、4 是結構洞」一句）。語法極簡主義自此有上同調理由書。A＋B 至此互為表裡地收攏（頻譜 note §3 ↔ Paper N remark 互引）。

- **想法 B 落檔（2026-07-07，research/insight/hbar_spectrum_sparsity.md）**——「degree 4
  雙重封死」＋公開面預測（下一階 H⁵/arity-6/K₇，永不 H⁴）＋ ⚠️ 自相似猜想（允許線性度
  k ∈ 1+2^j；四線性結構性空缺），kill conditions 與升級路徑載明。§3 與想法 A（binarity
  契約，仍排隊）互為表裡。

- **GUIDE_03 §11：Call-by-Observation 求值模型補章（2026-07-07）**——惰性引擎施工圖：
  thunk 四欄設計（expr/frame/context/effect，對照引擎現況三缺口）、memo key＝(語法 CAID,
  框架 CAID, context CAID)、019 tier 分級 memo 策略（C 永久／M 按 fuel 代／Q 不跨觀測）、
  force＝觀測原語＋fuel 記帳、Cocoon/tuple＝固化邊界、驗收＝pipe_laws＋context_dollar
  原樣重跑＋銜尾蛇向量。惰性化完成的定義＝`v.w.x.a` 通過。**Stage 1+2+3 全完成（2026-07-07，含一輪驗收代修＋一輪整治）**——`v.w.x.a → "Logic"` ✓（deref 再入供 `$` 框架，scope 限定不污染兄弟）；自指全量觀測視界誠實截斷 ✓。殘留＝memo Stage 4+。 **升規範層完成（2026-07-22）**：CbO 語義本體升為 **SPEC_04 §6「按需觀測」**，與 CAID 平起（CAID＝SPEC_13 §1 語義＋REAL_03 協議；CbO＝SPEC_04 §6 語義＋本節工程協議）。散落語義指標（SPEC_01 §2.4.2／SPEC_07 §4.2／SPEC_12 §3.2／SYNTAX_07／SYNTAX_12 §4）全數改指 §6。新增 Yoneda 對偶框架（CbO＝觀測極 `hom(A,X)`／CAID＝身分極；惰性 ⟺ 無全域截面 ⟺ 障礙非零，接 APP_07／KS）。 |

- **`|>` 範疇論重拆（2026-07-06，docs/discussion/018）**——`|>` ＝ 疊加 monad 的 Kleisli
  bind（效應分級）；三形態＝兩個嵌入（Kleisli 箭頭／精煉箭頭＋常數特例）；tuple 角落＝
  精煉箭頭定理。定律表引擎全驗（`pipe_laws_test.rs`），順手修兩處違規（ENGINE_SYNC #18：
  可加性、原子交集）。衍生排隊項均已落地（見下）。
- **精煉箭頭 nucleus 判準（2026-07-06，docs/discussion/019）**——重跑安全性三層分類：
  Tier C（$-free：恆冪等，nucleus 型）／M（正片段：單調縮小、迭代收斂紀律、冪等不保證）／
  Q（布林化・`!`・分支：非合流，只在觀測點收斂）。兩個 tier 邊界皆語法可判 → linter
  Tier 1 規則清單累計 3 條（019 §4）；meet-同態步＝LADD 分片友善（先演化後合併不失語義）；
  tier ＝ GUIDE_03 增量重算的靜態調度依據。引擎迴歸 +3（pipe_laws_test 尾段）。

- **銜尾蛇量子化重構**（舊 P0）——APP_06 定稿＋2026-06 spec ladder cleanup（COSMOLOGY 16→7、
  SPEC_00 §4.2 權威矩陣、Paper N 白皮書、spec 回寫 SPEC_13 §1.3／SPEC_17 §4.3／ORDER_00 §1.1）。
- **論文系列 I–XXII ＋ Paper N** 全數上傳 Zenodo；series open list = item 21 ＋ comparison map 的 16-cell 腿。
- **claims ledger 第一輪**（2026-07-03）：15 列初審通過；N1 comparison-map 考古定案（四處修復）；
  L11 Path 1 掛牌（SPEC_17 §4.3）。
- **APP_07 兩欄語意**（survivor/differential）＋ consensus note H⁰/H¹ 修正＋post-XXII 反轉。
- **forcing chain 兩鏈分家**（Paper N §1 ledger、APP_06 §3 補註）。

## 5. 長期／擱置

| 項目 | 狀態 |
| :--- | :--- |
| **取代 pest 剖析器** | 長期。自成專案，不是一弧——v0.18.0 的 fence 已把輸入界擋住，故非安全項；動機是文法可控性與 v0.18.0 殘留的錯標（`WORK_QUEUE` Q-002 只治錯標，不治剖析器選型）。**2026-08-13 落檔**：此前只活在對話與記憶裡 |
| Paper XXIII（item 21 的 arity-5 lid 正式證明） | PARKED（reduction 已到位，等 M5/FFT 級投入） |
| comparison map 的 16-cell 腿（frontier items 1＋7＋DD lift） | open（2026-07-03 自 item 23 名下析出） |
| 𝔽₂→char-0 之牆（item 11/12 τ-end、amplituhedron 線） | 刻意不開（新 program，非 backlog） |
| **終期願景：n/ × LLM 神經符號迴圈**（M1 實驗驗證 → M2 交換協定 → M3 統一推理；出處 research_review §8＋`insight/transformers_bohrification.md`） | 長期。post-XXII 重估（2026-07-05）：M3 原設門檻「Q⊣B 至少於 Pauli 特例成立」**已由 item 14 交付**（D^b adjunction、free⊣forgetful、mod Kudo）；新增維度條件——adjunction 為 **equivalence iff n=4**（counit defect = n_a），即 LLM↔n/ 往返無損 ⟺ 自我描述一致的同一條件；XXII ceiling ⟹ M2 的 obstruction-degree 標籤僅需 {1,2,3}＋序列外（2-bit）；item 24 ⟹ 協定語意用「認證深度」非「能力等級」。對應表整體 R2-corr／R3 級（ledger 紀律）；M1 = LLM 側的 Path-2 儀器（與引擎側 linter 為同一字典的兩台測量儀）。 |
