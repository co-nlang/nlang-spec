# 整合地圖（II）：論文 VII–XXII → nlang-spec

**目的：** 延續 `integration_map.md`(只覆蓋 I–VI + L-S),把 VII–XXII 的核心
結果映射回規格書,標記「已有依據 / 可補強 / 解凍的 P3 缺口」。

**重要框架（工程主導）:** n/ 是工程在前、數學在後補依據。VII–XXII 大多*不是*新功能,而是
*為既有決策補上嚴格證明*,或*解凍原本卡在「H³ 猜想未定」的 P3 缺口*。所以多數條目是
「[✓] 為既有 spec 主張提供嚴格依據(無需改 spec)」或「[~] 可補一則 Note」,真正*新的*整合
機會集中在 §C(XVIII–XXII 的 H³ 弧)與 §D(P3 解凍)。

約定:`[✓]` 已有對應/依據　`[~]` 部分/可補強　`[✗]` 缺失或 backlog　`[verify]` 待核對具體章節

---

## §A. Papers VII–IX：twistor 橋、Φ functor、3-qubit 幾何基底

| 論文 | 核心結果 | spec 對應 | 狀態 | 說明 |
|---|---|---|---|---|
| VII | googly = H² 障礙;Φ*([f])=c₁(O(1)) mod 2 | APP_06/07 的 H² 層;Cocoon 密封性 | [~] | 理論延伸;為「H² = 不可恢復翻轉」提供 twistor 側佐證,非引擎需求 |
| VIII | Φ=ℓ∘τ∘ι*;**PM nerve = K_{3,3}**;Z/2-gerbe∈H²(CP³);MASA 數 (4ⁿ−1)(4ⁿ⁻¹−1)/3 | integration_map I-GAP/Čech nerve;APP_05 全域格 cardinality | [~] | **K_{3,3} = PM nerve** 與 XXII §7「family B」是同一物(見 §C);MASA 計數可作 APP_05 全域格基數的依據 [verify APP_05] |
| VIII | twisted Penrose / gerbe non-vanishing | — | [✗] backlog | RESEARCH_FRONTIER item 11;開放問題,非引擎需求 |
| IX | W(5,𝔽₂) 為 3-qubit MASA 幾何;GL(3,𝔽₂)↪PSp(6,𝔽₂);Klein quartic | APP_04 數學基礎(symplectic polar space 作為 MASA poset 幾何) | [~] | W(2n−1,𝔽₂) 是 n/ MASA poset 的*幾何底座*,值得在 APP_04 補一則明確 Note [verify] |
| IX | Klein quartic / Ramanujan 路線 | — | [✗] backlog | RESEARCH_FRONTIER item 12;數學上很美但與引擎無關,純 backlog |

---

## §B. Papers X–XVII：五邊形精算 = 把 H²(KS) 從「引用」升級成「無枚舉代數證明」

這一整塊的工程意義是**單一的**:它把規格書一直*概念性引用*的 KS/H² 障礙,變成*嚴格、無枚舉
的代數定理*。也就是 APP_04/06 裡「KS 定理:無全域真值賦值」和 APP_07 裡「H² → `#split`」這兩個
主張,現在有了 3-qubit 的完整證明後盾。

| 論文 | 核心結果 | 撐住的 spec 主張 | 狀態 |
|---|---|---|---|
| X | K₅ ⇔ equiangular ⇔ Mermin;10-ray cap;collinearity 只是 shadow | PM/KS 配置的幾何刻畫(APP_04) | [✓] 依據 |
| XI | **β-formula** s(C)=(−1)^{β/2};quadratic refinement;β_sum≡2 mod4 | **CAID v2 複數譜的「相位/符號」結構**(REAL_03 §3.2;integration_map II-GAP-2) | [✓] 依據 — β/quadratic-refinement 正是複數譜要編碼的 sign/phase 來源 |
| XII | **T-vector** ω(T,r)=1;symplectic characteristic element(類 Wu class) | **LADD 語意質量 m=Tr(P_C) / gravity**(APP_05 §3.1) | **[✗ / 跨牆]**(2026-06-27 已核對):**非同源**。T-vector = F₂ 上同調層的 Wu/特徵元素(向量,per-config,witness −I holonomy);m=Tr(P_C) = ℂ-Hilbert 值層的維度/測度(純量,per-object,資訊體積)。type/level/domain 三重不符;唯一重疊是「characteristic」一詞的雙關。深層版(mass ↔ 特徵類 via index theory/η-invariant)= char-0 幾何故事,**跨 F₂ 牆**,與 Klein τ-end 同類,delegate 不展開。 |
| XIII–XIV | Maslov/Kashiwara;k-profile 定理;stabilizer(O₁=ℤ₂,O₂₃₄=S₃);Orbit-4 anomaly | — | [~] 內部結構,精煉理解,無引擎需求(可選 Note) |
| XV | **Weil representation** of Sp(6,𝔽₂) on ℂ⁸;metaplectic;S₃ lifting | **APP_06「為何是 ℂ」/量子化必然性**;Bohrification 的算子實現 | [✓] 依據 — Weil rep 是「Bohrification 投影算子」在 3-qubit 的具體載體 |
| XVI | **Weyl Product Identity** W_C=s(C)·I;∏_C W_C=−I(12,096/12,096) | **H² 障礙 = `#split` 的代數核心**(APP_07;integration_map III) | [✓] 依據 — 把「4-cycle holonomy = −I」變成 Weyl-代數恆等式 |
| XVII | **Cross-context anticommutation**;Petersen K(5,2);N_anti | 同上;且 N_anti 是 XVIII–XXII 的入口 | [✓] 依據 — 「∏=−I 無枚舉」用鴿籠(10>2³−1=7),正是全系列最常用的工具 |

> Note:整塊 X–XVII 對 spec 的淨效應 = **把 integration_map 第 3 節(Paper III, H²)的依據從
> 「概念引用 KS」升級為「3-qubit 完整代數證明」**。建議在 APP_04/APP_07 的 KS/H² 段落加一句
> 「嚴格證明見 Papers XVI–XVII」。

---

## §C. Papers XVIII–XXII：H³ 弧 —— 真正新的整合機會(解凍 P3)

這是 integration_map 當初寫不出來的部分。原文 P3 多項標「依賴 H³ 猜想的進展(開放問題)」——
那個進展就是這五篇。

| 論文 | 核心結果 | spec 對應 / 影響 | 狀態 |
|---|---|---|---|
| XVIII | n=4 普遍 N_anti=10(B0/B1/B2) | H² 障礙在 4-qubit 是*穩健*的 → spec 依賴 H²/`#split` 的合理性 | [✓] 依據 |
| XIX | **n≥5 modulus**:arity≤4 不足以分類 N_anti mod2 | **= 全像陳述**:邊界(arity≤4)資料*無法*決定 bulk(H³ 類)。直接對應 n/「全像原理」比喻 | [✓] 新依據 — 見 §E |
| XX | H³ opens at n≥5;n_a=δμ at n=4 | **把 Epilogue/APP_07 的 H³ 從「Paper IV 猜想」升級為定理** | [→ APP_07 §4, SPEC_00 §4.2] H³ 列可改標「theorem (XX–XXII)」 |
| XXI | master theorem(N_anti=10 ⇔ n=4);even/odd carrier dichotomy | H³ 障礙的精確邊界 | [✓] 依據 |
| XXII | **arity-resonance ceiling**;truncation(H³ 封頂);clique criterion;two families | 見下三條 — 最大的整合價值 | [→ 多處] |

XXII 的三個具體落點:

1. **Truncation(H³ 封頂)→ `%fuel`/計算視界 = H³ topology**(解凍 P3「16-cell 關聯子 = 計算視界拓撲」)。
   精確版:對稱/Pauli(雙線性)資料的障礙*止於 H³/BFT*;再上去搆不到。對應 SPEC_08 計算視界
   與 APP_07 的 L3/H³ 列。[✓ DONE 2026-06-27 — 見 §H-1]
2. **Truncation → ORDER_00 必須存在**(候選依據,strikingly parallel)。「arity-5 需要*非雙線性*
   datum」⟷ APP_07 H⁴/Sybil「身分層無法用內部格論修復,需外部物理錨點」。若焊得起來 = 「ORDER_00
   為何不可省」的數學依據,正中 research 動機。[✓ DONE 2026-06-27 — 見 §H-2]
   *caveat(已解除)*:原卡在 Paper IV(16-cell/Čech)↔ XX(Maslov–Wall)的 comparison map(= Direction D
   那道牆);該牆現已倒 —— self-representation map na=⟨Sq¹ω,[K5]⟩ closed-to-Kudo(item 23),
   IV↔XX 確認為*同一個* H³ 類(XX–XXI;[[project_paper20_h3_borromean]])。C-1 因此 theorem-backed;
   C-2 依賴 item 21(reduction,非封閉),已誠實標記。
3. **arity = ℏ_n/**(新橋):XXII 的 obstruction degree = APP_06 §6.4 的 effective ℏ_n/(「描述一個
   Combo 要幾個信任 context」)。resonance tower 即 n/ 的 ℏ 頻譜。[→ APP_06 §6.4 補一則對應 Note]

---

## §D. P3 缺口重估(被 XVIII–XXII 解凍的)

對照 integration_map §9 P3:

| 原 P3 缺口 | 原因(當時) | 現狀(XVIII–XXII 後) |
|---|---|---|
| 16-cell 關聯子 = 計算視界拓撲 | 依賴 H³ 猜想 | **可解凍** — XXII truncation 給「視界止於 H³」的精確版;待 IV↔XX comparison |
| 𝕆 鏈式法則 = CAID 跨版本相容 | 依賴 H³ 猜想 | 仍 [✗] — H³ 已懂,但 octonion/H⁴ 那層 XXII 證明*封頂*了(無 arity-5),所以這條可能*不該*用 H³ 而要重新定位 |
| `%fuel` ↔ E_r 頁索引(I-GAP-2) | 無工程需求 | 仍 [~],但 §C-3 的 arity=ℏ 給了「頁索引 = arity/ℏ」的候選定義 |

---

## §E. 新橋與框架對應

- **n/ = 全像原理(精確化)。** XIX modulus 是一句全像陳述:bulk 的 H³ 類*無法*從 arity≤4 的邊界
  資料重建。obstruction ladder 量的就是「邊界→bulk 重建」的失敗;H³ 是第一個邊界資料*原則上*不足
  的層級。建議 APP_07 或 COSMOLOGY 收一則「全像 / boundary-underdetermines-bulk」說明。
- **neuro-symbolic 分工(transformers_bohrification + truncation)。** LLM 天然算到低頁(RoPE=H¹,
  standard≈d₂,CoT≈E₃),高 degree(H³/H⁴)*證明上*搆不到;那正是 n/ 引擎(精確 Bohrification)
  接手的部分。→ 未來 LLM 整合場景的架構切點,有 ladder 依據。
- **T-vector ↔ LADD 語意質量**(§B XII):**已核對(2026-06-27)→ 非同源**。APP_05 §3.1 的
  m=Tr(P_C) 是 ℂ-Hilbert 維度/測度(值層);T-vector 是 F₂ Wu/特徵元素(上同調層)。type+level+
  domain 三重不符,「characteristic」只是雙關。深層的 mass↔特徵類(index theory)版本跨 char-0 牆,
  與 Klein τ-end 同 delegate。**結論:不寫回 APP_05。**

---

## §F. 優先順序(建議)

- **P0 ✅ DONE (2026-06-14):** APP_07 H³ 段 + SPEC_00 §4.2 已改標「theorem (Papers XX–XXII)」
  (H³ 於 n=4 消滅、n≥5 開啟、截斷於 H³;master rigidity);APP_04 §2 + SPEC_00 §4.2 已補
  KS/H² 無枚舉代數證明引用 (∏_C W_C=−I,12,096 Mermin pentagram,Papers XVI–XVII)。
  *未 commit;落點低風險。*
- **P1 ✅ DONE (2026-06-14):**
  - APP_06 新增 §6.5「resonance tower = ℏ_n/ 離散頻譜」(arity=ℏ 橋,Paper XXII;ℏ 譜封頂於 H³);
    *順手修了 L-S 依賴*:§6 開頭加文獻狀態註 —— L-S 2026「古典作用量→量子波函數*精確*重建」
    已被 Vattay Comment (arXiv:2605.02621) 駁倒(漏量子勢,實為 WKB);Paper I 只當動機,
    n/ 嚴格依據在 Bohrification + 系列論文,L-S 穩固的只有 contraction theory(1998)。
    §6.1/§6.2.3/§6.4 的「精確」字樣已就地降級+指回該註。
  - APP_07 新增 §6「全像原理:邊界資料不足以決定 bulk」(XIX modulus = 全像虧損的精確版,
    H³ 封頂;COSMOLOGY 質量圖像降為入門級物理直觀)。
  - *未 commit。*
- **P2 ✅ DONE (2026-06-27):** §C-1/2 —— truncation → `%fuel`=H³ topology + ORDER_00 必要性。
  原卡在 IV↔XX comparison map(整個系列當時真正的牆);該牆已倒(Direction D = self-representation
  map closed-to-Kudo, item 23;IV↔XX = 同一 H³ 類, XX–XXI)。回寫見 §H。*未 commit。*
- **backlog(均已收口,非待辦):**
  - Klein quartic/Ramanujan(item 12):**✅ harvested**(F₂ 半邊 steps 1–3 落在 Direction D 內);
    τ-end char-0 半邊跨牆 delegate。見 `open_problems.md` §B0。
  - twistor gerbe(item 11):**主線吸收**(F₂-linear gerbe 非消滅 = [n_a]≠0,master theorem 已控);
    Kodaira/holomorphic 半邊跨牆 delegate。見 `open_problems.md` §B0。
  - T-vector↔mass:**✅ 核對完畢 → 非同源**(§B XII / §E),不寫回 APP_05。
- **COSMOLOGY 重構(規劃中,user):** COSMOLOGY 系列是 LADD 早期、用質量類比寫的(後隨規格書量子化)。
  嚴格數學定義現已都在規格書/論文系列。計畫:**保留前段**(讀論文前的物理圖像建立 + 工程啟發,
  仍很有用),**後段直接接論文**。全像說明因此先放 APP_07(見 P1),COSMOLOGY 待此重構時再對齊。

---

## §G. 規格書回寫項目（Paper 0 Overview 浮現,先列項目;並行任務）

Paper 0 白皮書(`research/papers/Paper0_nlang_whitepaper.tex`)在銜接 spec↔論文時浮現兩個
「規格書落後於論文」的缺口。這原本就是論文系列做完要回頭處理的 spec 更新,只是 Overview 現在
卡在中間 —— 當作**並行任務**,先列項目,與既有 [→ SPEC_xx] 標記一起收口。

### G-1. CAID 擴展到 symplectic 指紋（spec 目前停在 I–VI 視角）
- **現狀**:`nlang-spec/integration_map.md` 的 CAID 只錨定 Paper I–VI;SPEC_13/REAL_03 的
  CAID = 投影算子 $P_A$ 的譜指紋(Yoneda 關係定身分),沒有 VII–XXII 的 $\Sp(2n,\F_2)$ 語言。
- **論文依據**:XI(β/quadratic-refinement = CAID v2 複數譜的 sign/phase,§B 已列)、
  XV(Weil rep = Bohrification 投影算子)、XVII(cross-context ω-Gram)。
- **回寫**:SPEC_13/REAL_03 補一則「CAID 的 symplectic 指紋」Note —— 關係指紋在 char-2/Pauli
  影子裡 = ω/q-Gram。[→ SPEC_13, REAL_03]
- **狀態**:[✓] DONE (2026-06-25) —— SPEC_13 §1.3「CAID 的 symplectic 刻畫」已新增(ω/q-Gram;
  XI sign/phase、XV Weil rep、XVII cross-context);Paper 0 §2 flag 改指向該節。REAL_03 物理封套
  暫不動(複數譜實作不變,symplectic 是數學本體)。*未 commit。*

### G-2. SPEC_17 自我演化 coherence = n=4 master theorem
- **現狀**:SPEC_17 §4 描述銜尾蛇自觀測循環(n/ 用自己的格論描述/演化自己),但*沒有*把
  這個循環的 coherence 釘到 $[n_a]=0 \iff n=4$。
- **關鍵區分(Paper 0 §4)**:OODP 引擎(CAID+LADD)*不*釘 $n$ —— 它要識別整條梯子
  (APP_07 §4:H¹ CAP / H² FLP / H³ Byzantine / H⁴ Sybil);**維度無關**。**只有自我演化**
  (Ouroboros, SPEC_17)需要 n=4 —— coherent 自我表示 = master theorem(XXI)= why_the_ladder
  (∞-Yoneda 在 n=4 free);**維度選擇**。
- **回寫**:SPEC_17 §4 補一則「自我描述/演化的 coherence = n=4(master rigidity, Paper XXI);
  引擎跨整條梯子,自我表示選維度」。[→ SPEC_17 §4]
- **狀態**:[✓] DONE (2026-06-25) —— SPEC_17 §4.3「自我表示的相干性 = n=4」已新增(引擎維度無關
  vs 自我演化選 n=4;APP_07 §4 區分;XX–XXI 後盾);Paper 0 §4 flag 改指向該節。*未 commit。*

> 其餘 spec 更新已散見既有標記:P0/P1(2026-06-14 已做,未 commit:APP_06 §6.5、APP_07 §4/§6、
> SPEC_00 §4.2、APP_04 §2);P2 ✅(2026-06-27,見 §H)。
> G-1/G-2 是 Overview 新浮現、優先級接在 P1 之後的兩項。

---

## §H. P2 回寫(2026-06-27,Direction D 牆倒後落地;並行任務收口)

§C-1/2 兩項在 Direction D 解決(self-representation map closed-to-Kudo,item 23;IV↔XX = 同一
H³ 類,XX–XXI)後可落地。回寫對齊 §G 的 G-1/G-2 格式。

### H-1. 計算視界深度 = H³ 拓撲(C-1)
- **論文依據**:Paper XXII(截斷:對稱/Pauli 雙線性障礙止於 H³);Paper IV(Čech/16-cell H³)↔
  Paper XX(Maslov–Wall na)= 同一 H³ 類(IV↔XX comparison map,由 self-representation map 焊接;
  XX–XXI 後盾)。解凍原 P3「16-cell 關聯子 = 計算視界拓撲」缺口。
- **回寫**:
  - SPEC_08 §3 新增「視界的拓撲深度(Papers IV, XX–XXII)」bullet —— 視界深度 = H³ 拓撲(定理非比喻);
    16-cell 關聯子斷層 = [na] 同一 H³ 類;`%fuel` 量坍縮 H³ bulk 的能量(指回 APP_06 §6.5 ℏ 封頂)。
  - APP_07 §4 H³ 列新增「與計算視界的對應」bullet —— L3 的 16-cell 關聯子斷層即此 H³ 類;指回 SPEC_08 §3。
- **狀態**:[✓] DONE (2026-06-27)。theorem-backed,無 caveat。*未 commit。*

### H-2. ORDER_00 必要性 = 無內部 arity-5/H⁴ 修復(C-2)
- **論文依據**:item 21 reduction —— 框架內部(symplectic/Pauli 雙線性)無 genuine arity-5/H⁴ 障礙類
  (ambient degree-4 環 = ⟨q²⟩ 可分解 = family B,Paper XXII;無 exotic 不變量)。⟹ 身分層(H⁴/Sybil)
  證明上超出內部格論,修復必須外部(物理創世錨點)。
- **回寫**:
  - APP_07 §4 H⁴ 列新增「必要性狀態(item 21, reduction)」bullet —— 外部錨點有數學必然性;誠實標記
    item 21 = reduction(modulo §3 reframe + Witt + polarization + resonance,不依賴 Kudo)。
  - ORDER_00 §1.1 新增「必要性(為何外部錨點不可省)」Note —— 指回 APP_07 §4 H⁴ 列;誠實標記。
- **狀態**:[✓] DONE (2026-06-27)。依賴 item 21(reduction,非封閉);定性結論穩固,完整封閉待 item 21 收尾。
  *未 commit。*

> 兩項 spec edits 在 nlang-spec branch `local`(SPEC_08 §3、APP_07 §4 H³/H⁴、ORDER_00 §1.1)。
> commit 後待 user push;`top` 合併時改 diary-style 訊息。

---

*本檔即 `integration_map_2.md`,延伸 `integration_map.md`(I–VI)涵蓋 VII–XXII;由 nlang-spec git
維護(branch `local`)。當初設想的「併入 integration_map.md」現已不採——兩份分工清楚(I–VI vs VII–XXII)、
且 VII–XXII 弧已自成體系,併入反而較難。少數落點仍標 [verify],待與最新 spec 逐節核對。
研究側伴生檔 `open_problems.md`、`inner/directionD_bridge.md`(均為 research local-only,不隨此檔公開)
仍是內部全貌來源。*
