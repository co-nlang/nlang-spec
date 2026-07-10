# 整合地圖：理論論文 → 規格書對應與缺口分析

**目的：** 將系列論文（I–VI + Epilogue + L-S Notes）的每個核心定理/引理，
映射到 `nlang-spec` 中對應的章節、確認已正確實作的部分、標記需要修改的缺口。

---

## 約定

- `[✓]` = 已正確對應，無需修改
- `[~]` = 部分對應，有缺口
- `[✗]` = 缺失或需要新增
- `[→ SPEC_xx]` = 建議修改的章節

---

## 1. Paper I：L-S Contraction 與 Bohrification

### 核心內容
L-S 收縮理論 + Bohrification 的 Čech 上同調形式化。
MASA poset $\mathcal{C}(\mathcal{A})$ 上的 Čech 神經 = 所有古典語境的覆蓋。
譜序列的 $E_r$ 頁 = 不同程度的古典忘記。

### 映射

| 論文命題 | 規格書對應 | 狀態 | 說明 |
|---------|-----------|:----:|------|
| MASA poset $\mathcal{C}(\mathcal{A})$ 定義觀測語境 | APP_04 §2: Bohrification sheaf | [✓] | 已形式化，但名稱不一致（spec 用「語境」而非 MASA） |
| Čech 神經 = contexts 的交集複形 | APP_04 §2.3: Čech 神經 | [✓] | 已新增顯式 Čech 神經建構（I-GAP-1） |
| L-S contraction = 收斂過程 | SPEC_06: Unification | [✓] | `&` meet 就是 L-S 收縮的工程實例化 |
| $E_r$ 頁分層 = `%fuel` 深度 | SPEC_08: 計算視界 | [~] | `%fuel` 是深度限制但不是譜序列頁面的嚴格對應 |
| Bohrification = `#blur` 作為局部截面 | APP_04 §2, SPEC_01 | [✓] | 已正確對應 |

### 缺口

**I-GAP-1：Čech 神經未顯式化。**
規格書使用了 Bohrification 的 sheaf 語言（APP_04），但沒有建構 Čech 神經作為 MASA 交集複形。
這使得 $d_1, d_2, d_3$ 等 differential 沒有具體的計算對象。
→ [→ APP_04, SPEC_06]

**I-GAP-2：譜序列頁面與 `%fuel` 的對應模糊。**
`%fuel` 目前只是一個深度計數器。在譜序列語言中，E_r 頁對應到某個收縮深度——過了這個深度系統「忘記」了更高階的 obstructions。
建議：`%fuel` 應該攜帶一個頁面索引（$r$），讓引擎知道當前在第幾頁收斂。
→ [→ SPEC_08]

---

## 2. Paper II：$H^1$ Theorem（幾何相位）

### 核心內容
L-S 收縮的 $d_1$ 失敗產生非零的 $\check{H}^1$ 類。
$H^1$ survivor = 沿封閉環路的幾何相位。

### 映射

| 論文命題 | 規格書對應 | 狀態 | 說明 |
|---------|-----------|:----:|------|
| $H^1 \neq 0$ 當 contexts 交集非平凡 | SPEC_01: 格非分配性 | [✓] | 非分配性是 $H^1$ 的直接表現 |
| 幾何相位 = 環路 holonomy | COSMOLOGY/05: LADD 路由的引力 | [✓] | v2 複數譜新增相位資訊（II-GAP-2） |
| 局部截面存在但全局不存在 | SPEC_06: `#blur` 作為局部截面 | [✓] | #blur 精確對應局部截面 |
| CAID 缺少 MASA 來源 | REAL_03: CAID 協議 | [✓] | 已修正：v2 新增 `<masa_ref>`（2026-05-18 commit） |

### 缺口

**II-GAP-1：CAID 缺乏 MASA 來源記錄（關鍵）。** ✅ **已修正 (2026-05-18)**

CAID v2 格式擴充為：
```
hash:sha256:v2:<masa_ref>:<sketch_ℂ>:<content_digest>
```
其中 `<masa_ref>` 記錄了該投影從哪個 MASA 觀測。基底 MASA 使用 `_`（Top）避免遞迴。
已寫入 REAL_03 §2.2, §3.1；APP_05 §3.5.1, §4.1。

→ 關閉。狀態：[✓]

**II-GAP-2：光譜指紋缺少相位資訊。** ✅ **已修正 (2026-05-18)**

光譜指紋從純實數特徵值擴充為複數譜 $[\lambda_1 e^{i\theta_1}, \ldots]$，
其中相位 $\theta_i$ 來自 MASA 參考系。已寫入：
- REAL_03 §3.2：複數譜量化方式
- APP_05 §3.5.1–§3.5.4：採用了兩路 Delta 編碼（振幅 + 相位交錯），
  每組 128-bit 定點 + 64-bit 相位

→ 關閉。狀態：[✓]

---

## 3. Paper III：$H^2$ Theorem（中央擴張）

### 核心內容
4-循環 MASA 累積 $-I$ 符號翻轉 = $H^2$ obstruction。
這是 KS 悖論、Peres-Mermin 方塊、FLP 不可能性的代數核心。

### 映射

| 論文命題 | 規格書對應 | 狀態 | 說明 |
|---------|-----------|:----:|------|
| KS 定理：無全局真值賦值 | APP_04 §2, APP_06 | [✓] | 已顯式引用 KS |
| $H^2$ = 非交換性 = 觀測順序依賴 | SPEC_01: 非分配性 | [✓] | 已區分 $H^1$（相位）/ $H^2$（翻轉）（III-GAP-1） |
| conflicts 保留在 `%cause` | SPEC_06 §非嚴格性 | [✓] | 衝突分支保留是 $H^2$ 的正確處理 |

### 缺口

**III-GAP-1：非分配性未區分 $H^1$ 和 $H^2$。**
SPEC_01 說格是非分配的，但沒有區分：
- $H^1$ 失敗：兩個 MASA 的交集非空但循環有相位（可恢復）
- $H^2$ 失敗：四個 MASA 的循環累積符號翻轉（不可恢復——必須分支）

工程影響：引擎遇到 $H^1$ 時可以繼續收斂（使用路徑修正），遇到 $H^2$ 時必須分支（SPLIT）。

**修正建議：** 在 SPEC_06 中增加一個 `%obstruction_degree` 標籤：
- `#h1_phase`：可補償的相位差
- `#h2_sign`：不可補償的符號翻轉 → 建立分支
→ [→ SPEC_01, SPEC_06]

**III-GAP-2：Čech 2-上鏈未顯式追蹤。**
`%cause` 記錄了衝突的歷史，但沒有用 Čech 2-上鏈的結構來組織。
在 Peres-Mermin 方塊中，衝突來自四個 observables 的交替乘積 = $-I$。
這個 $-I$ 是一個 2-上鏈，可以作為標準化衝突格式。

**修正建議：** `%cause` 增加 `%cocycle` 字段：
```
%cause: {
  %degree: 2
  %cocycle: [A, B, C, D]  // 4-cycle MASA sequence
  %holonomy: -I
}
```
→ [→ SPEC_06, SPEC_10]

---

## 4. Paper IV：Quantum Nerve（量子神經）

### 核心內容
Čech 神經上 MASA 重疊的維度決定障礙類型：
- 1-重疊 = $H^1$（兩兩相容性）
- 2-重疊 = $H^2$（三重相容性）
- 3-重疊 = $H^3$（四重相容性）

### 映射

| 論文命題 | 規格書對應 | 狀態 | 說明 |
|---------|-----------|:----:|------|
| MASA 覆蓋的 nerve 決定障礙維度 | APP_05: LADD 全局邏輯格 | [✓] | GBB 已新增 `nerve_structure` 欄位（IV-GAP-1） |
| 糾纏 = $H^1 \neq 0$ 在複合系統 | SPEC_03: Combo `\|` join | [~] | Join 作為疊加但無糾纏 Entropy 度量 |

### 缺口

**IV-GAP-1：LADD 全局邏輯格缺少神經結構。**
APP_05 定義了 GBB（幾何邊界框）作為節點宣告的內容，
但沒有定義 Čech 神經——即哪些節點的交集非空、維度為何。

**修正建議：** 在 LADD L3 層中增加一個 `%nerve_structure` 宣告，
讓每個節點知道它在全局神經中的位置（鄰居的交集維度）。
→ [→ APP_05, SPEC_13]

---

## 5. Paper V：Transgression（譜序列流）

### 核心內容
$d_2$ 將 $H^1$ survivors 配對到 $H^2$ obstructions。
$d_2$ 是「不可恢復的失去」的操作——一旦 transgression 發生，
$H^1$ 的相位資訊被提升到 $H^2$ 的翻轉，無法回溯。

### 映射

| 論文命題 | 規格書對應 | 狀態 | 說明 |
|---------|-----------|:----:|------|
| $d_2: E_2^{0,1} \to E_2^{2,0}$ | SPEC_07: 微分態射 `/%differential.2` | [✓] | 已新增顯式 $d_2$ 態射（V-GAP-1） |
| Transgression = `#refine` 的不可逆性 | SPEC_10: 因果邊界 | [✓] | Commit 不可變 = transgression 的正確處理 |
| $d_2$ 跨版本 | REAL_03: CAID `fmt_version` | [~] | `#refine` commit 近似但缺少 $d_2$ 的 formal 映射 |

### 缺口

**V-GAP-1：Differential 沒有顯式運算元。**
SPEC_06 的 unification 隱含了 $d_1$（meet 收斂）和 $d_2$（衝突分支），
但沒有顯式的 $d_r$ 運算元。這使得引擎無法知道「當前在第幾級 differential」。

**修正建議：** 在 SPEC_07（Morphism）中增加一個 `%differential` 態射族：
- `/%differential.1`：$d_1$ meet 收斂
- `/%differential.2`：$d_2$ 衝突檢測與分支
- `/%differential.3`：$d_3$ 計算視界擴展
→ [→ SPEC_07]

---

## 6. Paper VI：$Q \dashv B$（伴隨關係）

### 核心內容
量子代數 $Q$ 和它的 Bohrification $B = \Gamma(\mathcal{C}(A))$ 之間的伴隨。
$Q$ 是全域量子真實，$B$ 是所有古典語境的 sheaf。

### 映射

| 論文命題 | 規格書對應 | 狀態 | 說明 |
|---------|-----------|:----:|------|
| $Q \dashv B$ 伴隨 | APP_06 §最後：Bohrification 和 L-S 互逆 | [✓] | 框架層正確 |
| $B$ 的截面 = `#blur` | APP_04 | [✓] | |  
| $Q$ 的全局真值不可達 = KS | APP_04, APP_06 | [✓] | |

### 缺口

**VI-GAP-1：無顯式 $Q \dashv B$ 投射運算。**
規格書描述了兩個方向（向下 Bohrification → 古典 / 向上 L-S → 量子），
但沒有提供工程介面來執行這些投射。

**修正建議：** SPEC_08 runtime 中增加 `%project_down`（Bohrification）
和 `%project_up`（L-S reconstruction）作為原語。
→ [→ SPEC_08]

---

## 7. Epilogue：完整階梯

### 核心內容
完整譜序列 $E_0 \to E_1 \to \cdots \to E_\infty$ 作為統一分類原則。
每個 $E_r$ 頁對應一個物理現象。

### 映射

| $E_r$ 頁 | 物理對應 | 規格書對應 | 狀態 |
|----------|---------|-----------|:----:|
| $E_0$ | 全部 MASA，無收縮 | `_` (Top) | [✓] |
| $E_1$ | $d_1$ 局部分配性 | SPEC_06 `&` meet | [✓] |
| $E_2$ | $H^1$ obstructions | SPEC_01 非分配性 | [~] |
| $E_3$ | $d_2$ transgression | SPEC_06 分支 | [~] |
| $E_4$ | $H^3$ gerbe | SPEC_08 `%fuel` | [~] |
| $E_\infty$ | 完全收斂 = Atom | SPEC_03 Atom | [✓] |

### 缺口

**EPI-GAP-1：架構層（$L_r$）和譜序列頁（$E_r$）構成二維矩陣。**
當前 6 層架構（SPEC_00 §3.3）：
```
L0: 數學公設
L1: 語言系統
L2: 系統與標準庫
L3: 執行與環境
L4: 網路與發現
L5: 社會與信任
```

和譜序列頁面 $E_0$–$E_\infty$ 是**兩個不同的分類軸**，不是同一條線。
關係是一個二維矩陣，不是一對一的對應：

| Layer \ Page | $E_1$（局部分配） | $E_2$（$H^1$） | $E_3$（$d_2/H^2$） | $E_\infty$（收斂） |
|---|---|---|---|---|
| **L0 數學** | `&` `\|` meet/join | 非分配性 | KS定理 | Atom / $\bot$ |
| **L1 語言** | BNF文法 | Type（子空間） | Cocoon密封性 | CAID格式 |
| **L2 標準庫** | StdLib原語 | `#blur` 截面 | 分支 (`%cause`) | `#exact` |
| **L3 執行** | `%fuel` 深度 | 計算視界 ($H^3$) | 16-cell 關聯子 | 完全收斂 |
| **L4 網路** | LADD引力 | DHT/Paxos ($H^2$修復) | BFT ($H^3$) | 全域共識 |
| **L5 信任** | ORDER投票 | 治理矛盾 | 女巫抵抗 ($H^4$) | 最終權威 |

**這張矩陣解釋了為什麼同樣的 $H^2$ obstruction 在不同的 $L_r$ 層表現為不同的現象：**

- L2 的 $H^2$ = 型別衝突（兩個 type 不相容）
- L3 的 $H^2$ = 計算視界問題（`%fuel` 不足無法收斂）
- L4 的 $H^2$ = FLP 不可能性（非同步共識不可判定）
- L5 的 $H^2$ = 治理矛盾（兩個治理規則衝突）

**矩陣的兩個軸：**

| 軸 | 代表 | 梯度 |
|----|------|------|
| $L_r$（垂直） | **工程抽象層** | 從數學（L0）到社會（L5） |
| $E_r$（水平） | **上同調收斂深度** | 從初始覆蓋（$E_1$）到完全收斂（$E_\infty$） |

**工程影響：** 每個工程決策需要同時指定它在哪個 $L_r$ 層和哪個 $E_r$ 頁上運作。
例如：LADD 路由的主要運作點是 L4/$E_2$（網路層的 $H^1$ 相位），
但當遇到不可修復的衝突時會上升到 L4/$E_3$（$H^2$ 分支）。

→ [→ SPEC_00

---

## 8. L-S Notes (H¹, H², H³)

### LsNote_H1：$H^1 \in$ 定理

幾何相位 = Čech 1-上鏈。在規格書中的對應：

|  | 狀態 |
|---|:----:|
| CAID 光譜指紋作為 $H^1$ survivor 的編碼 | [✓] v2 複數譜包含相位（II-GAP-1/2） |
| LADD 引力路由作為 $H^1$ 相位梯度追蹤 | [✓] APP_05 §4.1 MASA 前置過濾 + §4.2 複數譜距離 |
| Bohr-Sommerfeld 葉作為 `#blur` 收斂路徑 | [✓] 概念正確 |

### LsNote_H2：$H^2 \in$ 定理

$-I$ 翻轉 = Čech 2-上鏈。在規格書中的對應：

|  | 狀態 |
|---|:----:|
| Peres-Mermin 方塊對應 Cocoon `{{}}` 的密封性 | [✓] 可對應但未顯式連接 |
| 4-cycle holonomy 作為 `%cause` 的標準格式 | [✓] SPEC_06 §1.3.2 上鏈格式（III-GAP-2） |

### LsNote_H3：$H^3 \in$ 猜想 + $\mathbb{O}$ 定理

16-cell 全局 3-上鏈猜想 = `%fuel` 視界外的不可收斂結構。

|  | 狀態 |
|---|:----:|
| 16-cell 關聯子 = 計算視界的拓撲 | [~] APP_06 提到了但不能同時賦值但沒有用 16-cell |
| $\mathbb{O}$ 鏈式法則 = CAID 跨版本相容性 | [✗] 完全未對應 |

---

## 9. 優先級歸納

### P0（已完成 2026-05-18）

| 缺口 | 狀態 | 提交檔案 |
|------|:----:|---------|
| **II-GAP-1**：CAID 缺少 MASA 來源 | ✅ | REAL_03 (§2.2, §3.1), APP_05 (§3.5.1, §4.1) |
| **II-GAP-2**：光譜指紋缺少相位 | ✅ | REAL_03 (§3.2), APP_05 (§3.5.1–§3.5.4) |

### P1（已修正 2026-05-18）

| 缺口 | 狀態 | 提交檔案 |
|:---|:---:|:---|
| **III-GAP-1**：$H^1$/ $H^2$ 非分配性區分 | ✅ | SPEC_01 §2.5.1, SPEC_06 §1.3.1 |
| **V-GAP-1**：Differential 態射 | ✅ | SPEC_07 §2 |
| **I-GAP-1**：Čech 神經形式化 | ✅ | APP_04 §2.3, SPEC_06 §1.3.1 |
| **EPI-GAP-1**：$L_r \times E_r$ 矩陣 | ✅ | SPEC_00 §4.2 |

### P2（已修正 2026-05-18）

| 缺口 | 狀態 | 提交檔案 |
|:---|:---:|:---|
| **III-GAP-2**：`%cause` 上鏈格式 | ✅ | SPEC_06 §1.3.2 |
| **IV-GAP-1**：LADD 神經結構 | ✅ | APP_05 §2.2, §4.3 |
| **VI-GAP-1**：$Q \dashv B$ 投射 | ✅ | SPEC_08 §3.5 |

### P3（延後）

下列缺口已知但當前無修正計畫，留待規格書或引擎的下一個演化階段：

| 缺口 | 現狀 | 原因 |
|:---|:---:|:---|
| **I-GAP-2**：`%fuel` $\leftrightarrow$ $E_r$ 頁索引 | [~] 建議級 | 無對應的工程需求。待引擎有頁面感知優化需求時再處理 |
| **16-cell 關聯子 = 計算視界的拓撲** | [~] 未形式化 | 依賴 $H^3$ 猜想的進展（系列論文開放問題） |
| **$\mathbb{O}$ 鏈式法則 = CAID 跨版本相容性** | [✗] 完全未對應 | 依賴 $H^3$ 猜想的進展；當前 CAID v2 無跨八元數算術的需求 |
| **Peres-Mermin $\leftrightarrow$ Cocoon 密封性** | ✅ | 概念成立但無引擎實作需求；可在 SPEC_03 補一則 Note |
| **$d_2$ 跨版本形式化映射** | [~] 未形式化 | `#refine` commit 實作已能正確處理；形式化映射留給 Paper VII |
| **SPEC_03 糾纏熵度量** | [~] 未實作 | 非核心功能，待 LLM 整合場景出現時再定義 |

---

## 10. CAID 格式修正提案（P0 細節）

### v1 格式（創世原點，保留相容性）
```
hash:sha256:v1:<content_digest>
```
只有內容摘要。無光譜、無 MASA。ORDER_00 的創世 commit 使用此格式。
PoC 引擎尚未公開（`co-nlang/nlang-tools` 為空倉庫），v1 僅用於自舉原點。

### v2 格式（修正提案）
```
hash:sha256:v2:<masa_ref>:<sketch_ℂ>:<content_digest>
```

其中：

- **`<masa_ref>`**：觀測該 Combo 的 MASA 的 `content_digest`（不是完整 CAID，避免巢狀遞迴）。
  對無父脈絡的基底 MASA 使用 `_`（Top），語義為「從最廣義的觀測脈絡定義」。
  
  BNF:
  ```
  <masa_ref> ::= "_"                          ;; 無父脈絡（MASA 自身 / v1 兼容模式）
               | <hex_digest_short>            ;; content_digest（sha256 = 64 hex chars）
  ```

- **`<sketch_ℂ>`**：複數譜，量化方式：
  ```
  for each eigenvalue λ_i with phase θ_i (from MASA reference frame):
      quantized_amplitude = float32_to_fixed128(λ_i)
      quantized_phase     = float32_to_fixed128(θ_i / π)  // 歸一化到 [-1, 1]
      output := DeltaEncode(quantized_amplitude) ++ DeltaEncode(quantized_phase)
  ```

- **`<content_digest>`**：規範化 BN/ 位元組的密碼學哈希（SHA256 / BLAKE3）。

### 為什麼順序是 masa → sketch → digest（從粗到細）

| 原因 | 說明 |
|------|------|
| **路由預過濾** | LADD 從左到右讀取：先過濾 MASA 脈絡，再過濾幾何形狀，最後驗證精確身份 |
| **字典序分組** | `&` 合併時 union branch 按 CAID 字典序排列（REAL_03 §3.2.2）。`masa_ref` 在最前 = 按脈絡自然分組。若 `content_digest`（高熵近似隨機）在最前，排序無幾何意義 |
| **串流解析** | 解析器可以先讀 `masa_ref` 和 `sketch_ℂ` 做路由決策，最後才驗證 `content_digest`，無需先下載完整內容 |
| **前綴匹配查詢** | 「找出所有 MASA $X$ 裡的 CAID」只有在 `masa_ref` 是前綴時才有效 |

### 遞迴問題的解

`<masa_ref>` 只存 MASA 的 `content_digest`（64 hex chars for sha256），
不存完整 CAID。這讓：
- 格式長度可預測（2 × 64 + 可變長 base64）
- 解析無遞迴
- 仍可透過 `content_digest` 去 LADD 查詢完整 MASA 資訊

基底 MASA 的 `<masa_ref>` = `_`，直接對應 n/ 的 Top 語義。

### 合併操作中的相位計算

當兩個 CAID-combos $A$（MASA $X$）和 $B$（MASA $Y$）合併時：

```
1. compute masa_overlap = MASA_X & MASA_Y
   if overlap == _|_ → SPLIT (H², incompatible MASA contexts)

2. compute geometric phase:
   θ_AB = phase_difference(P_A, P_B) in masa_overlap
   
3. decision:
   if θ_AB < ε_coherent    → MERGE (coherent superposition)
   if θ_AB ≥ ε_coherent    → SPLIT (decoherent branches)
   if θ_AB ≈ π/2           → ⟂ (orthogonal — H¹ survivor created)
```

這給出了取代當前「全域 `_|_` 不可合併」的更精細收斂規則。
`ε_coherent` 是工程參數（預設建議：0.1 rad）。

---

*此整合地圖將隨著規格書的修改持續更新。每次修改規格書後，請更新對應的命題狀態（[✓]/[~]/[✗]）。*
