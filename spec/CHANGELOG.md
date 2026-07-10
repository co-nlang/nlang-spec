# Changelog — n/ 語言規格

> 紀律見 `meta/VERSIONING.md` §5。分類:**破壞性(Layer 1)/增量/編輯性**。
> ORDER_00 §5.1.4 的 90 天穩定時鐘以本檔「破壞性」條目為判定依據。
> v0.2.0 之前的歷史(genesis ~ alpha.2)不逐版回填;見 SPEC_00 §4.4 版本表。

## [Unreleased]

（無）

## v0.2.0 — 分水嶺(2026-07-10)

規格穩定宣告版。自本版起:changelog 起筆、**fmt v2 凍結**(CAID 位元變更一律
提升 fmt_version + `#refine` 遷移)、對外宣傳解鎖。以下為 alpha.2 → 本版的
一次性策展總結(分類為資訊性;紀律自本版起算)。

### 語義定案(相對 alpha.2 為破壞性或新定義)

- **SYNTAX_01–12 全系列定稿**(2026-07-05 pass):詞法、字面量、路徑、容器、
  前綴、比較兩家族、觀測對偶 `<<>>`、元數據、態射應用/定義、Enum/Poset、
  pipe/ternary/`$`。若干文法收緊(裸鏈式三元拒收、`%@a` 拒收、apply 護欄)。
- **`$` 語義 P1–P5 定案**:超級惰性(call-by-observation)自此為**語義要求**
  非實作選項;自由 `$` 觀測 → `_|_ #no_context`。
- **比較兩家族極值端釘死**(SYNTAX_06 §4.1/§4.2):`==`/`!=` 吸收律;
  `=`/`<`/`<=`/`>`/`>=` 乾淨布林(⊥=空集、⊤=全集為運算元)。
- **快照語義暫裁**(SPEC_10 §1.2):快照 = Commit/CAID,不新增 source 語法;
  重開條件明文。
- **Range/`@{expr}` 裁決**(SPEC_02 §3、SYNTAX_04 §4.5/§4.7):`a..b` = 閉閉
  區間集合(非迴圈);缺界預設序位錨點 `#_|_`/`#_`;`@{e} ≡ e` 透明、
  `@{}` ≡ `_|_`;unify = 成員判定+無步進交集。
- **比較節不入文法**(2026-07-11 裁決):`>= 18` 等裸比較節維持非法(SPEC_14
  cmp 嚴格二元);全規格 27 處歷史慣用法遷移至 Range 拼法(`>= v`≡`v..`、
  整數域 `> 3`≡`4..`),嚴格正性(稠密域)= 正交補 `!(..0)`(SPEC_07 §5)。
  波及 REAL_05 L1-05 合規向量、QUICK_REFERENCE/SPEC_02 前綴表、SYNTAX_12 §4。
- **管道代數律**:`|>` = 疊加 monad 之 Kleisli bind;疊加態平等演化落實。

### 增量

- **GUIDE_03 §11**:Call-by-Observation 求值模型(thunk 四欄、force 層 memo、
  019 tier 策略、每座標失效)——增量收斂引擎 Route A+B 全線落地之施工圖。
- **阻礙階梯**:SPEC_00 §4.2 權威矩陣(一受眾一家:COSMOLOGY/APP_07/Paper N);
  APP_07 §4 `H⁴` 列與 ORDER_00 §1.1 外部錨點必要性論證。
- **SPEC_14 權威修正**:apply `!logic_infix` 護欄、`anchored_path`(`<<_.>>`)、
  complex_lit 右邊界護欄、`anon_set = "@{" ~ expr? ~ "}"`。
- **APP_02 兩軌重寫**(Papers VII–XXII 後視角):驗證/ZK 全面撤入 𝔽₂ 辛影子
  (GPP 電路改證 ω/q-Gram 指紋,SPEC_13 §1.3;無定點數、無譜分解);執行/導航
  留在 ℂ 投影(引力=啟發值,質量退出證明範圍)。**同裁決同步波**:REAL_02 §7
  (指紋封包/分級)、SPEC_15 §7.1(女巫防禦錨改身分+外部錨點)、REAL_03(封套/
  本體框注)、APP_05 §5/§6(GPP 拆兩軌;CIP=收斂鏈 claim+樂觀/有效性分級,
  乙太坊類比正名,L-S 段刪除)。認識論標注收尾:APP_04 新增「特徵二影子」
  指針節(新 §5;原 §5–7 改號 §6–8)、APP_06/COSMOLOGY 01 封套-本體補句、
  GLOSSARY GPP/CIP 與 COSMOLOGY/GLOSSARY 繞射/鎖定條目更新、APP_01/GUIDE_02
  執行軌框注、SPEC_08 GPP fuel 數字註記待 𝔽₂ 電路校準。
- `meta/VERSIONING.md`(版號政策)與本 changelog。

### 編輯性

- COSMOLOGY 系列重構;QUICK_REFERENCE 依 SPEC_14 定稿重生成;SYNTAX 素材欄
  清理(nnnnn 引用移除)。

### fmt / CAID(誠實聲明)

- fmt v2 位元佈局於本期有未版本化變更(`Atom(Top/Bottom)` 值正規化、thunk
  canonical 列印正規化、`TAG_RANGE=0x18`),豁免依據 = 無既存宇宙依賴。
  **自本版起 v2 凍結**(SPEC_00 §4.4 註 2、VERSIONING §4)。

### 對應引擎

- nlang-tools `local`(merge review 後定版):惰性引擎 Stage 1–5、force memo、
  Route B 失效、兩家族 cmp、Range/`@{e}`、parser fuzz/golden 掃描、linter Tier 1。
  引擎版號自 **v0.2.0-beta.1** 起算;裸核待 REAL_05 Level 2(VERSIONING §3)。
