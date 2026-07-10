# COSMOLOGY 重構 — 執行交接書 (Execution Handover)

> 配 `cosmology_refactor_plan.md`(小夥伴的分析,診斷 + 16→7 方案)一起看。本檔是**可直接執行**
> 的版本:鎖定 Option **B**(連續 01–07 編號),補上 plan 寫成後才出現的修正(P2 視界=H³、
> Paper N 命名/章節)、GR firewall、以及**完整的反向連結修補表**(renumber 的真正成本)。
> 決策已定(2026-06-27, user 選 B);本檔可交由另一個 agent 或下一個工作階段一次跑完。

**Repo / 慣例:** 全部動 `nlang-spec`(spec/zh_TW/COSMOLOGY/ + 反向連結散落的 spec 檔)。
branch `local`,技術型 commit message;**我 commit,user push**;`top` 合併時才寫 diary-style。

---

## 0. 主對照表(old → new)— 這是所有連結修補的鑰匙

| old | 標題 | 動作 | new |
|---|---|---|---|
| 00 | Overview | 重寫為索引(保留檔名,見 §4) | **00** |
| 01 | Unified_Field(質能等價) | 保留 + 吸收 15 諧振為一段 | **01** |
| 02 | Intrinsic_Logic | 保留 | **02** |
| 03 | Digital_QM | 保留 | **03** |
| 04 | Deep_Fields(弦論) | ✂ **移除** | — |
| 05 | Semantic_Gravity | 保留 + 吸收 11 Grothendieck 為一段 | **04** |
| 06 | Horizons | 保留 + 吸收 08 Thermo 為一段 + **加 H³ 深度** | **05** |
| 07 | Holography_and_Action | **合併 10 真理積分** | **06** |
| 08 | Thermodynamics | ✂ 降級→ new 05 一段 | — |
| 09 | Digital_GR | ✂ **移除**(見 §3 GR firewall) | — |
| 10 | Truth_Integral | ✂ 合併→ new 06 | — |
| 11 | Grothendieck | ✂ 降級→ new 04 一段 | — |
| 12 | Digital_Cosmology(大爆炸/暗能量) | ✂ **移除** | — |
| 13 | Observer_Sovereignty | 保留(AGI 猜想退位,加 master theorem) | **07** |
| 14 | Open_Frontiers | ✂ **移除**(已被 RESEARCH_FRONTIER 取代) | — |
| 15 | Semantic_Resonance | ✂ 降級→ new 01 一段 | — |
| GLOSSARY | 術語表 | 保留 + 對齊論文 GLOSSARY | GLOSSARY |

**新檔名(連續編號):**
```
00_COSMOLOGY_Overview.md          (索引,重寫;保留檔名以救 SPEC_00:228)
01_PHYSICS_Unified_Field_Theory.md
02_TOPOLOGY_Intrinsic_Logic.md
03_PHYSICS_Digital_Quantum_Mechanics.md
04_PHYSICS_Semantic_Gravity.md     (was 05)
05_PHYSICS_Horizons_and_Uncertainty.md (was 06)
06_PHYSICS_Holography_and_Action.md (was 07, 併 10)
07_PHYSICS_Observer_Sovereignty.md  (was 13)
```

---

## 1. 反向連結修補表(非 COSMOLOGY 的 spec 檔指進來的連結)— **必修,否則斷鏈**

> 來源:`grep -rEno "COSMOLOGY/[0-9]{2}_[A-Za-z_]*\.md" spec/`(2026-06-27)。
> COSMOLOGY/ 內部互連結另外處理(§2);01/02/03 保號,指向它們的連結(SPEC_06:119、
> SPEC_11:81、SPEC_00:228 指 00)**不需動**。

| # | 來源檔:行 | 舊目標 | 新目標 | 備註 |
|---|---|---|---|---|
| 1 | SPEC_05:112 | 04_Deep_Fields | **04_Semantic_Gravity** | 移除「Extra Dimensions/弦論」框架;原句載重點是「特徵值參與引力計算」→ 改指新 04(重力),順手把「捲縮維度」措辭降為「子空間特徵值」 |
| 2 | APP_06:15 | 05_Semantic_Gravity | **04_Semantic_Gravity** | 純 renumber |
| 3 | SPEC_13:282 | 05_Semantic_Gravity | **04_Semantic_Gravity** | 純 renumber |
| 4 | GUIDE_02:141 | 06_Horizons | **05_Horizons** | 純 renumber |
| 5 | SPEC_08:84 | 06_Horizons | **05_Horizons** | 純 renumber(此即 P2 視界節旁的「詳見 COSMOLOGY/06」) |
| 6 | SPEC_17:177 | 07_Holography | **06_Holography** | 純 renumber(內容併 10,概念不變) |
| 7 | SPEC_17:224 | 13_Observer | **07_Observer** | 純 renumber |
| 8 | SPEC_10:123 | 08_Thermo | **05_Horizons** | 08 降為 new 05 一段;指向 new 05 |
| 9 | SPEC_11:15 | 08_Thermo | **05_Horizons** | heat_map/蒸發;指 new 05 熱力段 |
| 10 | SPEC_11:82 | 08_Thermo | **05_Horizons** | 同上 |
| 11 | APP_05:416 | 15_Resonance | **01_Unified_Field** | §5 GPP 譜諧振;15 降為 new 01 一段 |
| 12 | APP_05:417 | 15_Resonance | **01_Unified_Field** | §6 CIP 相位鎖定;同上 |
| 13 | SPEC_13:283 | 15_Resonance | **01_Unified_Field** | 純 redirect |
| ✓ | SPEC_00:228 | 00_Overview | 00_Overview(不變) | 00 保留檔名 |

**移除檔的殘留檢查:** 04/09/12/14 除上述 SPEC_05:112(04)外,其餘僅被 COSMOLOGY 索引 README 引用
(§2 一併重寫)。確認指令:`grep -rn "COSMOLOGY/\(09\|12\|14\)" spec/ | grep -v "COSMOLOGY/0\|/README"`
應為空。

---

## 2. COSMOLOGY 內部互連結

每篇重寫時,文末/文中對其他 COSMOLOGY 章節的連結都按 §0 主對照表 renumber;指向**已移除**章節
(04/09/12/14)的內部連結直接刪句或改指最近的保留章。索引 README(列 16 篇的那份)整份重寫為 7 篇
(骨架見 §5)。GLOSSARY 內的章節指引同步。

---

## 3. 內容修正(plan 寫成後才出現,務必併入)

### 3a. 新 05(視界)— 加 P2 成果「視界深度 = H³ 拓撲」
plan 只更新了 ℏ。新 05 還要納入 2026-06-27 P2 回寫的精確結果:
- **視界深度 = H³ 拓撲**(定理,非比喻):對稱/Pauli 雙線性障礙截斷於 H³(Paper XXII);
  16-cell 關聯子斷層 = cross-context [n_a] modulus = **同一個 H³ 類**(Paper IV ↔ XX,
  self-representation map 焊接)。
- spec 錨點:**SPEC_08 §3**(視界的拓撲深度 bullet)、**APP_07 §4 H³ 列**。
- ℏ 段:**APP_06 §6.5** resonance tower = ℏ_{n/} 頻譜,封頂於 H³。
- 吸收 08 Thermo:退相干蒸發 = 視界邊緣的一段(連到 `~%Engine.heat_map`)。

### 3b. 命名:Paper 0 → **Paper N**;章節引用更正
白皮書已更名(檔名 Paper0,顯示 **Paper N**)。COSMOLOGY 全系列引用一律寫「Paper N(白皮書)」。
**章節對應(已核對 Paper N 目錄):**
- 新 05(ℏ/視界)→ Paper N **§3**(The ladder is the spectrum of ℏ_{n/})。
- 新 06(全像)→ Paper N **§4**(The master dichotomy: n=4, and holography)。
  *(plan 寫「Paper 0§3」是錯的,全像在 §4。)*
- 新 07(觀測者/自我表示)→ Paper N §4 後半 + **SPEC_17 §4.3** + **Paper XXI** master theorem。

### 3c. GR firewall(回應 user 反思「現在有廣義相對論」)
保留/移除的誠實分級,寫進新 04(重力)與新 README:
- **保留且為真**:語義**重力**(LADD,m=Tr(P),反平方路由,`disc.find` 已實作)—— 牛頓味,
  非愛因斯坦。標 `[HEUR]`/`[INTERP]`(E=Tr(P)c² 是類比不是定理)。
- **移除**:數位**廣義相對論**(09,Lorentz 不變/曲率)—— 論文系列完全沒碰,無工程連結。
- **框架**:GR-proper(曲率/Einstein-mass/index-theory mass)與 **T-vector↔mass**、**Klein τ-end**
  屬*同一個* across-the-char-0-wall 程式(未來 program,有動機無需求)。新 04 末尾可放一句
  「真正的曲率版在 F₂ 框架之外,屬 char-0 延伸 program(見 RESEARCH_FRONTIER)」,不展開。
  ⟹ 誠實句:**n/ 有 QM(定理)+ 全像(定理)+ 語義重力(工程);GR-proper 是牆外的下一個 program。**

---

## 4. 新索引(重寫 00_COSMOLOGY_Overview.md)

骨架(改自 plan,已修正 Paper N + 章節):
```markdown
# n/ 數位宇宙學 (Digital Cosmology)

> 本系列提供 n/ 語言設計的物理直覺與工程啟發。
> 嚴格數學依據見 Paper N(白皮書)與論文系列 I–XXII。

## 閱讀指引
| # | 標題 | 建立的直覺 | 精確版 |
|---|---|---|---|
| 01 | 質能等價 | E = Tr(P)c²(+ 譜諧振/波粒) | APP_04, Paper VI |
| 02 | 內在邏輯 | Bohrification → OML → Heyting | APP_04, Paper II |
| 03 | 數位量子力學 | 疊加/坍縮 = merge | Paper III |
| 04 | 語義重力 | LADD routing(+ Grothendieck 信任覆蓋) | APP_05, disc.find |
| 05 | 計算視界 | ℏ_{n/}=arity;視界深度=H³ | APP_06§6.5, SPEC_08§3, APP_07§4, Paper N§3, Paper XXII |
| 06 | 全像原理 | boundary < bulk | APP_07§6, Paper N§4, Paper XIX |
| 07 | 觀測者與自我表示 | n=4 coherence | SPEC_17§4.3, Paper N§4, Paper XXI |
```
三層入口(同 plan):COSMOLOGY 直覺 → Paper N 橋接 → Papers 證明。
> [!IMPORTANT] COSMOLOGY = 入門物理圖像,不是數學證明。數學在 Paper N 與論文系列。

(dir 的 README.md 若與 00_Overview 重複,二擇一為索引;建議 00_Overview 當索引以保 SPEC_00:228,
README.md 改成短指標。)

---

## 5. 執行順序(de-risk:先連結後內容,隨時可中斷)

1. **連結先行**(§1 表 13 處 + §2 內部):純机械,先做完整個 repo 不斷鏈;此時舊檔還在,連結改成
   指向「未來新號」——所以這步要跟改檔名同一批做(見 2)。
2. **改檔名/移除**:`git mv` 05→04、06→05、07→06、13→07;刪 04/09/12/14;10 內容併入 06 後刪;
   08/11/15 內容各摘一段併入後刪。
3. **內容重寫**:01(+15 段)、04(+11 段、GR firewall)、05(+08 段、**H³ 深度**、ℏ)、
   06(併 10、全像虧損定理)、07(master theorem)。01/02/03 主要是加引用、改 Paper N 名。
4. **索引 + GLOSSARY**:重寫 00_Overview(§4 骨架);GLOSSARY 對齊論文 GLOSSARY(術語、DOI 風格)。
5. **驗收 grep**:`grep -rEn "COSMOLOGY/(0[4-9]|1[0-5])_|COSMOLOGY/0[89]" spec/` 應只剩 00–07;
   `grep -rn "Paper 0" spec/COSMOLOGY*` 應為空(全改 Paper N);斷鏈檢查 §1 表全綠。
6. **commit**(branch local,技術訊息);user push。

## 6. 工作量 / 風險
- 連結修補(§1+§2):小,機械,但**載重**(漏一條就斷鏈)—— 故列成表逐條勾。
- 內容重寫:06(全像+梯子)最大;05(ℏ+H³)中;07(master theorem)中;01/04 加段為主。
- 風險點:(a) §1 #1 SPEC_05 的「弦論/維度」措辭要降級不只是改連結;(b) 06 併 10 時真理積分
  ∫S(L)dE 退為直覺式開頭,精確版指 Paper N §4 / APP_07 §6(SPEC_17 內提到真理積分的散文同時檢查)。

---

*狀態:Option B 已定(2026-06-27)。本檔 execution-ready,待 user 指示由本階段或另一 agent 執行。
未動任何 COSMOLOGY 檔 —— 這是計畫,不是 diff。*
