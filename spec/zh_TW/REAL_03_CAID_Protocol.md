# REAL_03：CAID 物理協議 - L2 定址層 (OODP L2 Identity Layer)

> [!NOTE]: [Standard / 規範性標準]

本協議定義 **OODP (Ouroboros Discovery Protocol)** **L2 定址層**的核心元件：**CAID** 的物理結構與規範化流程。

CAID 旨在保留結構抗碰撞性的同時，內建幾何譜特徵以支援 L3+ 的全球引力路由。關於 OODP 五層架構的完整定義，請參閱 **[SPEC_13: 銜尾蛇發現協定](./SPEC_13_Ouroboros_Discovery_Protocol.md)** §0。

**本文定位**：
- **層級**：OODP L2 (定址層 Identity Layer)
- **上游**：SPEC_13 (語言語義) → 本文 (物理編碼)
- **下游**：REAL_02 L3 (收斂層)、APP_05 L3+ (譜幾何優化)

---

## 1. 正式語法 (BNF)

```bnf
<caid_v1>        ::= "hash:" <algo> ":v1:" <content_digest>
<caid_v2>        ::= "hash:" <algo> ":v2:" <masa_ref> ":" <lattice_sketch> ":" <content_digest>

<algo>           ::= "blake3" | "sha256" | <ext_algo>
<masa_ref>       ::= "_"                                ;; Top：無父脈絡（MASA 自身 / v1 兼容）
                   | <hex_digit> { <hex_digit> }         ;; MASA 的 content_digest
<lattice_sketch> ::= <base64_char> { <base64_char> }
<content_digest> ::= <hex_digit> { <hex_digit> }

<ext_algo>      ::= <ident_char> { <ident_char> }
<hex_digit>     ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
                  | "a" | "b" | "c" | "d" | "e" | "f"
<base64_char>   ::= "A".."Z" | "a".."z" | "0".."9" | "+" | "/" | "="
```

---

## 2. CAID 版本

CAID 有兩個並行版本。**v1** 僅用於 ORDER_00 創世 commit 的原點自舉。
**v2** 是當前宇宙的標準格式。

### 2.1 v1（創世原點）

```
hash:sha256:v1:<content_digest>
```

僅有內容摘要。無 MASA 來源、無光譜特徵。
保留 v1 純粹是為了創世 Commit $C_0$ 的歷史完整性——此時尚無 MASA 覆蓋來定義光譜。

### 2.2 v2（當前標準）

```
hash:sha256:v2:<masa_ref>:<lattice_sketch>:<content_digest>
```

三個組件從左到右構成「從粗到細」的篩選鏈：

| 位置 | 組件 | 角色 | 篩選粒度 |
|:---:|------|------|:-------:|
| 1 | `<masa_ref>` | 此 Combo 從哪個 MASA 觀測 | 最粗——脈絡過濾 |
| 2 | `<lattice_sketch>` | 投影算子 $P_A$ 的複數譜特徵 | 中等——幾何形狀比對 |
| 3 | `<content_digest>` | 規範化 BN/ 的密碼學哈希 | 最細——精確身分驗證 |

**順序的工程理由：**

| 原因 | 說明 |
|------|------|
| **路由預過濾** | LADD 從左到右讀取：先過濾 MASA 脈絡，再比對幾何形狀，最後驗證精確身分 |
| **字典序分組** | `&` 合併時 union branch 按 CAID 字典序排列（§3.2.2）。`masa_ref` 在最前 = 按脈絡自然分組 |
| **串流解析** | 解析器可先讀 `masa_ref` 和 `lattice_sketch` 做路由決策，最後才驗證 `content_digest` |
| **前綴匹配** | 「找出 MASA $X$ 中所有 CAID」的查詢依賴 `masa_ref` 是前綴 |

---

## 3. 三組件結構與語義

### 3.1 MASA 來源 (masa_ref)

*   **物理意義**：定義該投影算子 $P_A$ 是從哪個 MASA（古典觀測語境）提取的。
    $H^1$ 幾何相位的參考系由此組件決定。
*   **編碼**：
    *   `_`：無父脈絡（Top），用於 MASA 自身的 CAID 或 v1 相容模式。
    *   `hex_digest`：MASA 的 `content_digest`（對 sha256 為 64 hex chars）。
*   **非遞迴保證**：`<masa_ref>` 只存 MASA 的 `content_digest`，不存完整 CAID。
    這避免了巢狀 CAID 解析問題。MASA 本身的 CAID 使用 `<masa_ref> = _`。
*   **路由行爲**：LADD 依此值做第一級過濾——只有相同 MASA 的 CAID 才能直接比較相位。

### 3.2 幾何摘要 (Lattice Sketch / Spectral Signature)

*   **物理意義**：子空間正交投影算子 $P_A$ 的 **複數譜特徵摘要 (Complex Spectral Summary)**。
    相較 v1 的純振幅譜，v2 增加了來自 MASA 參考系的相位資訊。
*   **複數譜量化方式**：
    ```
    for each eigenvalue λ_i with phase θ_i (from MASA reference frame):
        quantized_amplitude = float32_to_fixed128(λ_i)
        quantized_phase     = float32_to_fixed128(θ_i / π)   // 歸一化到 [-1, 1]
        output := DeltaEncode(quantized_amplitude)
              ++ DeltaEncode(quantized_phase)
    ```
*   **特性**：
    *   支援無須下載完整內容的氣味搜尋（幾何距離比對）。
    *   相位資訊讓兩個不同 MASA 的 CAID 可以計算干涉效應。
    *   相容純實數譜（相位設為 $0$）。

### 3.3 內容指紋 (Content Digest)

*   **物理意義**：規範化 AST 位元流經 `<algo>` 指定演算法計算後的加密雜湊。
*   **特性**：精確身分驗證與絕對抗碰撞。

---

## 4. CAID 版本的合併操作

v2 格式讓 `&` meet 操作可以根據障礙程度做出更精細的決策，
取代「全域 _|_ 不可合併」的二元邏輯。

### 4.1 相位感知合併

當引擎合併兩個 CAID-combo $A$（MASA $X$）和 $B$（MASA $Y$）：

```
1. compute masa_overlap = MASA_X & MASA_Y
   if overlap == _|_ → SPLIT (H² obstruction, incompatible MASA contexts)
   → 此為 §7（原 §6）非嚴格性分支

2. compute geometric phase:
   θ_AB = phase_difference(P_A, P_B) in masa_overlap
   where phase_difference = arccos(Tr(P_A P_B))  in overlap subspace

3. decision:
   if θ_AB < ε_coherent    → MERGE (coherent superposition, H¹ is small)
   if θ_AB ≥ ε_coherent    → SPLIT (decoherent, H¹ survivor created)
   if θ_AB ≈ π/2            → ⟂ (orthogonal — pure H¹ survivor recorded)
```

- `ε_coherent` 是工程參數，預設建議 0.1 rad。
- H¹ survivor 記錄在 `%cause` 中以供 LADD 路由修正。

### 4.2 與非嚴格性的關係

原 §7（非嚴格性）是通用保護——它在 `_|_` 發生時保留分支。
本節的相位感知規則是其細化：在 `overlap ≠ _|_` 時，依據 $H^1$ 相位差決定合併或分支。

---

## 5. 規範化規則 (Canonical Rules)

為了計算具備決定論的 CAID，子空間本體必須序列化為唯一的位元流。

### 5.1 基礎正規化
1.  **Unicode**：所有標識符轉換為 **NFC**。
2.  **複數數值**：原子數值序列化為 `(real+imag i)` 形式。
3.  **整數**：不含前導零（`42` 而非 `042`）。
4.  **浮點數**：統一使用小寫 `e` 表示指數，且進行正規化（如 `0.50` 變為 `0.5`，`1E3` 變為 `1e3`）。
5.  **空白移除**：計算時嚴禁包含任何空白、換行或註解。

### 5.2 決定論排序演算法
1.  **基底排序 (Base Sorting)**：
    *   第一維度 (前綴優先級)：`%` > `~%` > `~` > `@` > `/` > (無前綴 Data)。
    *   第二維度 (名稱)：按實體名稱之 Unicode 代碼點遞增排序。
    *   **複合前綴判定**：若欄位同時具備多個前綴符號（如 `~%@`），以 **最左側 (最外層)** 之符號作為排序依據。例如 `~%@foo` 的優先級等同於 `~%`。
    *   **數字鍵**：純數字鍵（List 索引）始終排在最後，按數值大小遞增。
2.  **聯集分支排序 (Union Sorting)**：
    *   為了確保 $A \mid B$ 與 $B \mid A$ 產生相同的 CAID，引擎在序列化聯集節點前，必須：
        1. 計算每個分支自身的 CAID。
        2. 按 **CAID 字符串之字典序** 遞增排列。
        3. 進行冪等化簡（移除重複 CAID）。
3.  **態射規則排序 (Morphism Rules)**：
    *   當一個態射具備多個分支規則（存儲於 `%rules` 元欄位）時：
        1. **投影轉換**：將每個分支的「輸入模式 (Input Pattern)」序列化為 **規範化投影字串**（遵循本章 §3.1 之 NFC 與空白移除規則）。
        2. **字典序排列**：按輸入模式的投影字串之 **Unicode 代碼點** 進行遞增排序。
        3. **序列化**：依排序後的順序將分支規則（Pattern + Body）傳入雜湊更新器。

4.  **EML 表達式排序 (EML Canonicalization)**：
    *   EML 樹（由 `/eml` 與常數 `1` 構成的數學表達式）在序列化前必須進行**穩定規範化**，以確保語義等價的表達式產生相同的 CAID。
    
    **規範化規則**：
    | 規則 | 說明 | 範例 |
    | :--- | :--- | :--- |
    | **常數摺疊** | 預先計算常數子表達式 | `eml(1, 1)` → `1` |
    | **左結合化** | 二元運算統一為左結合 | `eml(a, eml(b, c))` 維持原狀 |
    | **變數排序** | 自由變數按字典序排列（僅限純常數表達式） | - |
    | **冗餘消除** | 移除單位元運算 | `eml(x, 1)` 保持（因 `1` 為核心常數）|
    
    **決定論保證**：
    - EML 表達式的 CAID 計算必須在展開為基本運算（`exp`, `ln`）**之前**進行，以保留高層語義結構
    - 兩個數學等價的 EML 表達式（如 `eml(x, 1)` 與 `exp(x)`）可能產生不同 CAID，這是預期行為——CAID 反映**語法結構**，而非數學語義

---

## 6. Binary-n/ 序列化格式 (BN/)

為了確保 CAID 計算的**位元級決定論**，本節定義標準的 Binary-n/ (BN/) 序列化格式，將規範化後的 AST 轉換為確定的位元流。

### 6.1 基本編碼

#### 整數編碼 (LEB128)
採用 **LEB128** (Little-Endian Base 128) 可變長度編碼：
- **無符號**：標準 LEB128，每 byte 低 7 位為資料，第 8 位為延續標記
- **有符號**：Signed LEB128，使用補充表示法

```
Unsigned LEB128: 624485 (0x0F8125)
┌─────────┬─────────┬─────────┐
│ 10010101│ 10000010│ 00001111│
│ └─ 21   │ └─ 128  │ └─ 0+15 │
│ 0x95    │ 0x82    │ 0x0F    │
└─────────┴─────────┴─────────┘
```

#### 字串編碼
- **編碼**：UTF-8 (RFC 3629)
- **格式**：`[長度: u32_LEB128] [內容: UTF-8 bytes]`
- **長度**：以 byte 為單位（非字元數），最大 $2^{32}-1$

#### 浮點數編碼（定點數）
參見 §3.1 的 128-bit 定點數表示：
```
[整數部: i64_LEB128] [小數部: u64]
```
- 小數部：無符號 64-bit，代表 $0$ 到 $1-2^{-64}$ 的範圍

### 6.2 Combo 序列化結構

#### 欄位排序優先級
在序列化前，Combo 欄位必須按下列**嚴格順序**排序：

| 優先級 | 前綴類型 | 說明 |
| :---: | :--- | :--- |
| 1 | `~%` | 系統元資訊（~%system 優先） |
| 2 | `%` | 一般元資訊 |
| 3 | `@` | 型別約束 |
| 4 | `/` | 邏輯算子 |
| 5 | (無前綴) | 純數據欄位 |
| 6 | `~` | 私有欄位 |
| 7 | `~local` | 局部私有（最後） |

**同優先級排序**：按欄位名稱之 Unicode 代碼點遞增。

#### 序列化格式

```
Combo ::= [類型標記: u8] [欄位數: u32_LEB128] [欄位列表]

類型標記:
  0x01 = Combo (開放) `{}`
  0x02 = Cocoon (封閉) `{{}}`
  0x03 = List `[]`
  0x04 = Tuple `()`

欄位列表 ::= 欄位 [欄位 ...]
欄位     ::= [鍵: 字串] [值: 值編碼]
值編碼   ::= [類型標記: u8] [內容]
```

#### 值編碼類型

| 類型標記 | 類型 | 編碼 |
| :---: | :--- | :--- |
| 0x10 | Atom | `[長度: u32_LEB128] [內容: bytes]` |
| 0x11 | Tag | `[長度: u32_LEB128] [標籤名: UTF-8]` |
| 0x12 | Int64 | `[i64_LEB128]` |
| 0x13 | Float | `[i64_LEB128 整數部] [u64 小數部]` |
| 0x14 | Complex | `[Float: 實部] [Float: 虛部]` |
| 0x15 | Bool | `[0x00=f/\|_ , 0x01=t/_]` |
| 0x16 | 引用 | `[字串: CAID]` |
| 0x01-0x04 | Combo/Cocoon/List/Tuple | 見 Combo 序列化 |

### 6.3 範例

```nlang
@point: { x: 3, y: 4 }
```

序列化（Hex 表示）：
```
01              ;; 類型標記: Combo
02 00 00 00 00  ;; 欄位數: 2 (小端 u32)

;; 第一欄位: ~%type
05 00 00 00 00  ;; 鍵長度: 5
7E 25 74 79 70 65 ;; 鍵: "~%type"
0x11            ;; 值類型: Tag
06 00 00 00 00  ;; 值長度: 6
70 6F 69 6E 74  ;; 值內容: "@point"

;; 第二欄位: x
01 00 00 00 00  ;; 鍵長度: 1
78              ;; 鍵: "x"
0x12            ;; 值類型: Int64
03              ;; 值: 3

;; 第三欄位: y
... (y: 4) ...
```

### 6.4 與 Lattice Sketch 的區分

BN/ 與 **[APP_05](./APP_05_LADD_Global_Logic_Lattice.md)** §3.5 定義的 Lattice Sketch 編碼**互相獨立**。

| 特性 | BN/ (Binary-n/) | Lattice Sketch |
| :--- | :--- | :--- |
| **輸入** | 規範化後的 AST | 投影算子譜特徵 |
| **輸出** | CAID content_digest | CAID lattice_sketch |
| **編碼流程** | LEB128 (整數)、定點數 (浮點) | Delta → ZigZag → LEB128 → Base64 |
| **用途** | 內容唯一性雜湊 | 譜幾何相似性搜尋 (LADD) |
| **驗證方式** | 雜湊比對 | 譜距離計算、熱帶距離篩選 |

**共用機制**：
- 兩者雖共享 LEB128 與 128-bit 定點數格式，但 Lattice Sketch 專為譜特徵的**低維摘要**設計
- BN/ 是**完整 AST** 的序列化；Lattice Sketch 僅是**投影算子特徵**的壓縮
- 兩者在 CAID 中並列存在：
  ```
  <caid_v2> = hash:<algo>:v2:<masa_ref>:<lattice_sketch>:<content_digest>
  <caid_v1> = hash:<algo>:v1:<content_digest>
  ```

**不相交原則**：
- BN/ 輸出進入 SHA256/BLAKE3 產生 `content_digest`
- Lattice Sketch 經過獨立壓縮管道後直接編碼為 Base64 字串
- 兩者計算路徑嚴格分離，避免循環依賴

### 6.5 完整性驗證

引擎實作應通過官方 `bn_test_suite` 驗證：
- 給定輸入 Combo 必須產生完全相同的位元流
- 跨平台（x86_64, ARM64, WASM32）的位元一致性
- 錯誤輸入的明確錯誤代碼

---

## 7. 譜序列化實作建議

### 7.1 串流雜湊 (Streaming Hash)

對於大型 Combo 或 List，建議採用串流雜湊而非先拼湊巨大的字串。

*   **演算法**：使用遞迴下降遍歷規範化子空間 AST，將每個節點的型別標籤、名稱與譜特徵依序傳入雜湊更新器。
*   **優勢**：記憶體效率高，支援漸進式計算大型幾何體的 CAID。

### 7.2 中間節點快取 (Merkle-style Cache)

由於 `n/` 的節點是不可變的，引擎應快取每個子節點的雜湊值。

*   **機制**：當父節點內容不變時，直接復用子節點的 CAID 參與計算。
*   **複雜度**：這能將 CAID 計算複雜度從 $O(N)$ 降至 $O(\text{變動路徑深度})$。
*   **物理意義**：類似於量子系統的「糾纏快取」——子空間的譜特徵一旦確定即永恆不變。

### 7.3 #blur 狀態與 CHS (Canonical Horizon Snapshot)

計算 `#blur` 節點的 CAID 時，**必須**將具備決定論的視界參數序列化為 **CHS 封套** 並納入雜湊輸入。

**CHS 封套格式**：
```
node_content + "#horizon:" + canonical_json([params])
```

**強制納入參數（共 5 項）**：

| 參數 | 量子語義 | 說明 |
| :--- | :--- | :--- |
| `%fuel` | 譜能量預算 | 允許消耗的計算資源上限 |
| `%strategy` | 坍縮策略 | `#eager` / `#lazy` / `#balanced` |
| `%max_branches` | 最大疊加分支 | 聯集展開的最大分支數 |
| `%max_unification_depth` | 最大收斂深度 | Meet 運算的遞迴深度限制 |
| `%max_pattern_nodes` | 最大模式節點數 | 態射模式匹配的最大節點數 |

**嚴禁納入參數**：
*   `%timeout`（物理時間不穩定，不具備決定論）
*   任何非標準的 `#ext:` 標籤

---

## 8. CAID 驗證與錯誤代碼

| 錯誤代碼 | 說明 |
| :--- | :--- |
| **`#unsupported_ca_algo`** | 引擎不支援該 `<algo>` 或 `<fmt_version>`。 |
| **`#refine_authority_missing`** | `#refine` Commit 缺少有效的權威簽署。 |
| **`#refine_source_unverifiable`** | 精煉來源無法在當前引擎下驗證。 |

---

## 9. 譜驗證邊界條件

### 9.1 不透明 CAID 處理

當引擎遇到無法計算的 CAID（如使用未知演算法、格式版本或譜特徵無法解析）時：

1.  **語義不透明模式 (Opaque Mode)**：
    *   **觸發條件**：該 CAID 出現在 `#refine` Commit 的 `target_caids` 欄位中。
    *   **行為**：引擎將其視為**不透明字串**，僅進行字串匹配，不進行雜湊驗證或譜特徵重構。
    *   **信任來源**：`#refine` Commit 的簽署權威。
2.  **嚴格驗證模式 (Strict Mode)**：
    *   **觸發條件**：該 CAID 出現在一般內容引用中（如 `deps` 欄位）。
    *   **行為**：引擎**必須**能計算並驗證該 CAID（包括譜特徵重構），否則回傳 `#unsupported_ca_algo` 錯誤。

### 9.2 譜特徵相容性

當引擎收到包含 `lattice_sketch` 的 CAID 時：
*   若引擎不支援譜幾何，可選擇僅驗證 `content_digest`（向後相容）。
*   若引擎支援譜幾何，應同時驗證譜特徵與內容指紋的一致性。

---

## 10. 跨實作驗證

官方提供 `oo caid-test-suite` 包含一組標準子空間 AST 與其預期的 `v1` / `v2` CAID，實作者應通過此測試套件以保證相容性。

*   **v1 測試**：驗證基礎雜湊與規範化規則。
*   **v2 測試**：額外驗證 `<masa_ref>` 編碼、複數譜特徵、及相位感知合併邏輯。

---

## 11. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_01](./SPEC_01_Foundation_and_Lattice.md)** | **CAID** 被定義為聯集疊加態的分辨器。 |
| **[SPEC_06](./SPEC_06_Unification_Logic.md)** | 相位感知合併 (§4) 細化 `&` meet 操作。 |
| **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** | **CHS** 參數與 `%fuel`、視界管理。 |
| **[APP_02](./APP_02_Formal_Verification.md)** | **GPP** 證明使用 128-bit 定點數運算。 |
| **[APP_04](./APP_04_Mathematical_Foundations.md)** | **譜特徵**的數學基礎（投影算子、跡、相位）。 |
| **[APP_05](./APP_05_LADD_Global_Logic_Lattice.md)** | **Lattice Sketch** 驅動全球引力路由。 |
| **[APP_06](./APP_06_Unified_Field_Theory.md)** | v2 的 `<masa_ref>` 和複數譜由 $H^1$ obstruction 定理保證。 |
