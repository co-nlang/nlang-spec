# 數學宣稱帳本 (The Claims Ledger)：spec ↔ 論文系列的關係審計

**目的：** `integration_map` 系列的姊妹篇（也是它的深化）。integration_map_2 的框架句——
「n/ 是工程在前、數學在後補依據」——是對的，但「補依據」一詞把好幾種**不同強度的關係**
壓成了一種。本帳本把「論文系列支撐工程決策」逐條拆開、標明每條宣稱實際的關係等級，
使任何一條都不能再向鄰居借力。

**觸發事件（2026-07-03）：** 同一種範疇混用在一個 session 內被抓到三次——
(1) forcing chain（發現鏈穿邏輯鏈的修辭，Paper N §1 已修）；
(2) APP_07 survivor/differential 兩欄混排（已修）；
(3) n=4↔自演化：工程化的迴圈（ORDER_01 治理，住 consensus 梯）與數學化的迴圈
（self-representation map，住 quantum 梯）**同名而不同物**。本帳本是對 (3) 型問題的系統性排查。

**狀態：R 級經使用者初審通過（2026-07-03，「分類沒太大問題」）。L6/N1 考古定案並修復；
L11 Path 1 掛牌完成（SPEC_17 §4.3），Path 2 排入規劃。**

---

## 1. 分類法

| 級 | 名稱 | 定義 | 引用紀律 |
|---|---|---|---|
| **R0** | 普通工程 | 決策有獨立的工程理由，不需要（也不宣稱）數學支撐 | 不得倒過來宣稱「數學迫使此設計」 |
| **R1** | 推導 (Logic) | 數學迫使設計 | 必須逐環掛強度標籤（[DESIGN]/[CONDITION]/[THEOREM]/[ECHO]），範本：Paper N §1 |
| **R2** | 座標／邊界 (Type) | 數學命名並限界失敗模式；設計自負其責 | 可作設計的*邊界條件*引用，不可作*理由*引用 |
| **R3** | 共鳴 (Data，待見證) | 先有設計、數學後來押韻 | 在 Path 1（掛牌）或 Path 2（儀器化）完成前，**不得作為設計依據被引用** |

R2 子型：
- **R2-corr**：correspondence-level 對應（同形不同係數；嚴格鄰居須點名，如 HKR）。
- **R2-neg**：負面陳述形式（「內部不可能 ⟹ 外部手段必要」）——不需工程實例化任何類即成立，
  是 R3 升級的首選路徑（範本：Sybil／ORDER_00，見 L9）。
- **R2-cond**：條件於字典實例化（引擎實際攜帶 ω/q 資料之前，宣稱只對紙上的影子成立）。

R3 的兩條出路：
- **Path 1（誠實化）**：掛牌。措辭範本＝Paper N §4：「a theorem *relative to* this identification」。
- **Path 2（儀器化）**：讓宣稱變可測（CAID v2 symplectic fingerprint per SPEC_13 §1.3 ＋
  contextuality linter）。完成後升級 R2 或降級退役。

> **一條 R3 註記（自娛，但掛牌）：** 本分類法疑似同構於 n/ 自己的三位一體——
> R1=Logic（態射／必然）、R2=Type（邊界）、R3=Data（存在宣稱，待見證）；
> SYNTAX_00 正在用同一組描述。好看，但不承重；若它開始承重，請先把它自己升級出 R3。

---

## 2. 裁決規則（本 session 判例的提煉）

1. **同名兩物檢查**：每條宣稱必須點名它借力的梯子實例——
   **語意梯**（Combo/ω/q，quantum/stabilizer 讀法）、**分散式梯**（LADD/consensus，
   correspondence-level）、**反身梯**（自我描述）。跨實例借力＝自動降 R3。
2. **Sybil 判例**：後加的解釋不是原罪；改寫成負面陳述（R2-neg）可以比正面宣稱更穩固。
3. **survivor/differential 判例**：同一梯子內部還有欄位之分（classification vs obstruction）；
   引用時欄位錯置＝範疇錯誤。
4. **Paper VI 判例**：宣稱「感覺卡在嚴格度中間」時，先查系列是否早已證過嚴格版——
   缺的可能不是數學，是記憶。
5. **comparison-map 判例（命名紀律）**：一詞多指是誤傳播的載體。「comparison map」專指
   IV↔XX 水平比較（Paper XX 原始指涉，open）；垂直橋 $\partial\Delta^4\to BV$ 一律稱
   self-representation map。新名字誕生時，舊名字必須正式退役或收窄指涉——否則舊名的
   殘留連結會把新指涉的進度誤傳給舊指涉（N1 即此案例）。

---

## 3. 帳本（R 級皆草案，待裁決）

| # | 決策／宣稱 | 家 | 發現鏈（真實起源） | 數學實際給的 | 梯子 | R（草案） |
|---|---|---|---|---|---|---|
| L1 | CAID 粒子面（內容定址、抗碰撞） | SPEC_13 §1 | **供應鏈攻擊防禦**（套件發佈） | 標準密碼學，與梯子無關 | — | **R0** |
| L2 | CAID 波動面（相位／干涉，smell 的前提） | SPEC_13 §1, APP_06 §2 | 氣味搜尋需要「取件前的距離」 | forced-quantization 鏈（Paper N §1 ledger：Solèr+Paper VI 鉗形，EML=echo） | 語意 | **R1**-mod-flags（[DESIGN]+[CONDITION]） |
| L3 | CAID symplectic fingerprint（ω/q-Gram） | SPEC_13 §1.3 | 論文語言的回寫（2026-06） | XI（β/quadratic refinement）＋字典 | 語意 | **R2-cond**（Path 2 的錨點格） |
| L4 | LADD 格論路由（XOR→交集） | SPEC_13 §2/§6, APP_05 | 把 Kademlia 式 DHT 格論化 | 格論（成熟數學）；譜幾何 smell 問題（Laplacian/Weyl/interlacing）仍 open | — | **R0** ＋ open-math 附註 |
| L5 | `&` = context/MASA；#split 語意 | SPEC_13 §7 | 格論化的自然行為，字典後對齊 | Bohrification（成熟）＋「context=Lagrangian」字典（modeling id） | 語意 | **R2-cond** |
| L6 | 視界深度 = H³（%fuel 拓撲） | SPEC_08 §3, APP_07 §4 L3 列 | 計算視界為工程機制，H³ 解釋後對齊 | XIX/XX/XXII（數學側真）＋ IV↔XX comparison map | 語意→反身 | **R2-cond**（定案）；註 N1（考古紀錄） |
| L7 | ℏ_n/ 頻譜＋認證深度封頂（≤ H³／5-context） | APP_06 §6.4–6.5 | 從 L-S 圖像起家，後由 XXII 錨定 | XXII ceiling 定理（數學側真；bound 型結論） | 語意 | **R2-cond**（最有工程價值的 R2） |
| L8 | CAP/FLP/Byzantine 對應 | APP_07 §4 | 後加的工程翻譯（Paper VI 時代 insight） | correspondence（嚴格鄰居=HKR；已掛牌 2026-07-03） | 分散式 | **R2-corr** |
| L9 | ORDER_00 外部錨定必要性（Sybil 層） | ORDER_00 §1.1, APP_07 §4 | **冷啟動機制**（比特幣創世類比）；H⁴ 解釋**後加** | item 21 reduction 的負面陳述：內部無 H⁴ 類可偵測／修復 | 分散式＋語意(負面) | **R2-neg**（升級範本）；旗標：item 21=reduction |
| L10 | ORDER_01 治理（紀元、投票、躍遷） | ORDER_01 | spec 以套件形式發佈 ⟹ 需人為推進 | 無直接數學宣稱（L5 列的 H² 對應僅 R2-corr） | 分散式 | **R0**（機制本身） |
| L11 | **n=4 ↔ Ouroboros 自演化一致** | SPEC_17 §4.3 | 「自演化就是自描述」的直覺 | master theorem（數學側真）＋ modeling identification（**未證**） | 反身 | **R3**；Path 1 ✅（掛牌 2026-07-03）、Path 2 規劃中（註 N2） |
| L12 | EML = math LUCA（單一種子自舉） | SPEC_09, APP_06 §2 | EML 論文的召喚（**發現鏈的樞紐**） | [ECHO]（Paper VI 自己的歸檔；等價性 open=RF item 4） | — | **R0**（stdlib 設計）＋ R3-echo（勿再當支柱） |
| L13 | `!` 正交補／orthomodular 邏輯 | 邏輯層 spec | 設計公理（否定的對合性） | R1 的 [DESIGN] **輸入**，非結論（推導 orthomodularity 本身=RF item 5, open） | 語意 | **R1-輸入**（公理，明列不假裝推導） |
| L14 | 全像讀法（≤4-context 邊界對 bulk 盲） | APP_07 §6 | 工程剪影後加 | XIX modulus 定理（數學側真） | 語意 | **R2-cond** |
| L15 | L_r×E_r 大一統矩陣（同一 degree 跨層顯形） | SPEC_00 §4.2, APP_07 §5 | 統一敘事的需求 | 字典在各層的重複套用（各列繼承各自的 R 級） | 全部 | **R2-corr**（矩陣格位各自審） |

---

## 4. 註記（需要展開的列）

**N1（L6——考古定案 2026-07-03）：**「comparison map」本身就是同名兩物（規則 1 抓到了
自己的數學側）。Paper XX 的原始指涉＝IV↔XX **水平**比較（16-cell/Čech vs Maslov–Wall
兩個實現＋Dixmier–Douady coefficient lift；XX §future work **明文 deferred**，
`Paper20:477-478`）；Paper XXII 把同一個詞借給**垂直**橋 $\partial\Delta^4\to BV$
（item 23 closed-mod-Kudo 的是這個；research 側 2026-06-20 已改名 self-representation map）。
感染源＝Paper N §6 的「This is *also* the comparison map」括號句；2026-06-28 的 spec 回寫
沿共享名字把 item 23 的閉合誤傳播成「IV↔XX 已焊接／視界深度=H³ 為定理」（APP_07 §4、
SPEC_08 §3——後者甚至寫成「self-representation／comparison map」斜線同義）。
實況：水平比較＝兩條垂直腿＋遞移性——五角星腿 ✅（item 23，mod Kudo）；16-cell 腿 **open**
（= RESEARCH_FRONTIER items 1＋7＋coefficient lift）；「同一個類」目前為現象級證據
（同一個 $n=4/n\ge5$ 邊界、同一台 collapse machine）。**裁決（使用者確認 2026-07-03）：降級**
——APP_07 §4／SPEC_08 §3 改回 await 措辭、Paper N §6 括號句改寫、frontier item 23 加
命名紀律段（皆已修）。L6 定案 **R2-cond**；「封頂於 H³」那一半（XXII）不依賴此比較，仍為定理級。
附帶後果：系列的 open 清單實為 **item 21 ＋ comparison map 的 16-cell 腿**（後者先前藏在
item 23 的名字底下未被單獨點名）。

**N2（L11，帳本的動機列——裁決 2026-07-03：先 Path 1，Path 2 排程）：**
- *Path 1* ✅（2026-07-03）：SPEC_17 §4.3 已補掛 Paper N §4 同款旗標——(i) 數學側定理 vs
  (ii) modeling identification（CONDITION 級）分開陳述、「相對於此認同的定理」措辭、
  範疇分際條款（工程機制在分散式梯、宣稱在反身梯，不得借力）、Path 2 預告。
- *Path 2*（規劃中，未排入近期）：linter Tier 1 跑 **spec 自己的 Combo lattice**——算 Ouroboros
  nerve 的 incidence graph 與 clique number ω(G)。
  ω(G) < 4 ⟹ 實際迴圈的 ceiling ≤ 1，n=4 問題對*這個*迴圈不啟動（宣稱退役為純數學）；
  存在 K₅ 配置 ⟹ n 首次成為可測量，modeling identification 從 CONDITION 走向 empirical。
  無論結果為何，「連不起來」都被一個計算取代。前置：linter Tier 1 handover doc。

**N3（L2/L12 的分工提醒）：** 發現鏈裡 EML 是樞紐、邏輯鏈裡 EML 是 echo——兩鏈已在
Paper N §1 與 APP_06 §3 補註分家。本帳本引用時一律用邏輯鏈。

---

## 5. 待辦

- [x] 使用者裁決各列 R 級（2026-07-03 初審通過；L6/N1 考古定案並修復四處；L11 = Path 1 先行）。
- [x] R3 列完成 Path 1 掛牌（L11：SPEC_17 §4.3，2026-07-03）。
- [x] 口述歷史落檔（2026-07-05：`meta/history_origins.md`——定位為未來 intro 的素材庫；
      intro 發表門檻見 `meta/ROADMAP.md` §1）。
- [x] Path 2 首件之一：linter Tier 1 handover doc ✅（2026-07-07，`docs/linter_tier1_handover.md`——三條靜態規則＋context graph／ω(G) 交付定義、$-掃描邊界、措辭紅線）；接續：
- [x] linter Tier 1 實作 ✅（2026-07-07，`nlang-tools/crates/oo`：`nlint` 二進位 + `oo lint`
- [x] Tier 1 驗收 ✅（2026-07-07，含三項驗收修正：原子形態入 Tier C〔019 命題 2〕、tier U 發射〔GUIDE_03 §11.3 調度介面〕、K₄/K₅ 見證可解索引〔JSON context_nodes 表＋人讀 coord_path@span〕；nlang-tools `1f73d76`，oo 24 測試、workspace 84 套綠）。剩餘前提＝規格書 Combo 化 → spec-lattice 實驗。
      子命令；R1/R2/R3 + context graph ω(G) + K4/K5 candidate sites + JSON tier1-v1 schema
      + 防火牆措辭；21 項 acceptance 測試 + 全 workspace 579 測試綠。`static_analyzer.rs`
      接入 lib（孤兒檔修復——靜態部分保留、動態部分移除因對到舊 interpreter API））。
      接續：spec-lattice 實驗（量 Ouroboros nerve 的 ω(G)）。
- [x] 帳本目錄歸屬（2026-07-05：與 integration_map 系列同歸 `meta/`；README §4 留快照與指標）。
