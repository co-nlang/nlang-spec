# COSMOLOGY 重構方案

## 現狀診斷

COSMOLOGY/ 共 16 篇（00–15，缺 14 → 14 是 Open Frontiers）+ README + GLOSSARY。
寫於 LADD 早期，用**物理類比**（質能等價、弦論、廣義相對論、大爆炸...）建立 n/ 的工程直覺。
每篇結構一致：警告標籤 → 物理類比 → n/ 對應 → 工程啟發 → 與 spec 的對應表。

### 好的部分（保留）
- **物理圖像的教學價值**：讀論文前先建立直覺，很有用
- **每篇都有 spec 對應表**：已經做了 grounding
- **警告標籤系統**：`[MATH]` `[INTERP]` `[HEUR]` `[HYP]` `[!!RISK!!]` — 誠實分級

### 過時/需更新的部分
- **真理積分 $\int \mathcal{S}(\mathcal{L}) dE$ 是核心方程式**（00§1, 10 整篇）：
  現在有了 obstruction ladder，真理積分可以被精確化為「沿著 context-nerve 的 cohomology」，
  不再是一個 vague 積分公式
- **全像原理**（07 整篇）：Paper XIX 已經給了精確的全像虧損定理，
  07 還在用 Yoneda「邊界編碼本體」的概念版
- **KS 與 ℏ_{n/}**（06）：ℏ_{n/} 在 APP_06§6.5 已有精確定義 = resonance tower 的 arity，
  06 還在用「類比式離散不確定性」
- **自觀測循環**（13）：Paper XXI 已證 coherent self-representation ⟺ n=4，
  13 還在用「AGI 湧現指標 σ」的猜想版
- **弦論/暗能量/GR**（04, 09, 12）：這些物理類比在論文系列中**完全沒有被碰觸**，
  和實際工程也沒有連結，是最 speculative 的部分

## 重構原則

1. **前段保留**：01–03 + 05–06 的物理圖像仍有教學價值（先讀直覺，再讀數學）
2. **後段指向 Paper 0**：數學細節不在 COSMOLOGY 重述，直接引導到 Paper 0
3. **過時內容精確化**：用論文系列的定理替換猜想版描述
4. **無依據的類比砍掉**：弦論/暗能量/GR 沒有論文支撐，降級或移除

## 方案：從 16 篇壓縮到 7 篇

### 保留（更新描述）

| 新編號 | 原編號 | 標題 | 動作 |
|---|---|---|---|
| **01** | 01 | 統一場論（質能等價） | 保留框架，更新 $E=\mathrm{Tr}(P)c^2$ 的 spec 錨定 |
| **02** | 02 | 內在邏輯與正交模格 | 保留，加 Paper VI 的 Solèr-Cohomology 引用 |
| **03** | 03 | 數位量子力學（疊加/坍縮） | 保留，加 Bohrification → context → nerve 的精確版 |
| **04** | 05 | 語義重力與 LADD | 保留，工程核心（disc.find 已實作） |
| **05** | 06 | 計算視界與 KS 測不準 | 保留，ℏ_{n/} 更新為 APP_06§6.5 的 resonance tower |
| **06** | 07+10 | 全像原理與障礙梯子 | **合併+重寫**：用 Paper XIX 的全像虧損定理取代概念版，真理積分退為直覺式開頭，精確版指向 Paper 0§3 |
| **07** | 13 | 觀測者主權與自我表示 | 保留框架，AGI 猜想退位，加 Paper XXI master theorem（n=4 = coherent self-representation） |

### 移除/降級

| 原編號 | 標題 | 處置 |
|---|---|---|
| 00 | COSMOLOGY Overview | → 重寫為新的 7 篇 README |
| 04 | 弦論與對稱性破缺 | **移除**：無論文支撐，和工程無連結 |
| 08 | 熱力學與幾何蒸發 | **降級**：GC = 退相干蒸發的類比可以一段話放在新 05（視界） |
| 09 | 數位廣義相對論 | **移除**：洛倫茲不變性類比在論文系列中沒有被使用 |
| 10 | 真理積分 | **合併到新 06**：精確版在 Paper 0§3 |
| 11 | Grothendieck 拓撲與信任覆蓋 | **降級**：信任覆蓋的內容已在 SPEC_13 §7，一段話放在新 04（LADD） |
| 12 | 數位宇宙學（大爆炸/暗能量）| **移除**：最 speculative，無論文支撐 |
| 14 | 開放邊境 | **移除**：內容過時，open frontiers 現在在 RESEARCH_FRONTIER.md |
| 15 | 語義諧振 | **降級**：CAID 波粒二象性可以一段話放在新 01 |
| GLOSSARY | 術語表 | 保留，對齊論文 GLOSSARY |

### 新的 README（取代 00）

```markdown
# n/ 數位宇宙學 (Digital Cosmology)

> 本系列提供 n/ 語言設計的物理直覺與工程啟發。
> 嚴格數學依據見 Paper 0（白皮書）與論文系列 I–XXII。

## 閱讀指引

| # | 標題 | 建立的直覺 | 精確版 |
|---|---|---|---|
| 01 | 質能等價 | E = Tr(P)c² | APP_04, Paper VI |
| 02 | 內在邏輯 | Bohrification → OML → Heyting | APP_04, Paper II |
| 03 | 數位量子力學 | 疊加/坍縮 = merge | Paper III |
| 04 | 語義重力 | LADD routing | APP_05, disc.find |
| 05 | 計算視界 | ℏ_{n/} = arity | APP_06§6.5, Paper XXII |
| 06 | 全像原理 | boundary < bulk | APP_07§6, Paper XIX |
| 07 | 觀測者與自我表示 | n=4 coherence | SPEC_17, Paper XXI |
```

## 工作量估計

| 任務 | 複雜度 | 說明 |
|---|---|---|
| 新 README | 小 | 上面已寫好骨架 |
| 01–03 更新 | 小 | 加引用，不改結構 |
| 04（原 05）更新 | 小 | 已有 disc.find 實作錨定 |
| 05（原 06）更新 | 中 | ℏ 重新定義段需重寫 |
| 06（合併 07+10）| 大 | 最重要的一篇，全像 + 梯子 |
| 07（原 13）更新 | 中 | AGI 猜想退位，master theorem 進位 |
| 移除舊檔 | 小 | 但需確認無外部連結 |
| GLOSSARY 對齊 | 小 | 和論文 GLOSSARY 同步 |

## 核心設計決策

> [!IMPORTANT]
> **COSMOLOGY 的角色是「入門物理圖像」，不是「數學證明」。**
> 數學在 Paper 0 和論文系列裡。COSMOLOGY 只需要做到：
> 讀者看完直覺後，知道去哪裡找嚴格版本。

這和 Paper 0 的關係：
```
COSMOLOGY → 直覺（物理類比，中文）
Paper 0   → 橋接（spec ↔ 論文，LaTeX）
Papers    → 證明（純數學，英文）
```

三層入口，三種讀者，同一個故事。
