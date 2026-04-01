# REAL_03：CAID 物理協議與規範化細則

> [!NOTE]: [Standard / 規範性標準]

## 1. 正式語法 (BNF)
```bnf
<caid>          ::= "hash:" <algo> ":v" <fmt_version> ":" <digest>
<algo>          ::= "sha256" | "blake3" | <ext_algo>
<fmt_version>   ::= <nonzero_digit> { <digit> }
<digest>        ::= <hex_digit> { <hex_digit> }
<ext_algo>      ::= <ident_char> { <ident_char> }
<hex_digit>     ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" 
                  | "a" | "b" | "c" | "d" | "e" | "f"
<nonzero_digit> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<digit>         ::= "0" | <nonzero_digit>
```

---

## 2. 規範化規則 (Canonical Rules)

為了計算決定論的 CAID，AST 必須序列化為唯一的位元流。

### 2.1 基礎正規化
1.  **Unicode**：所有識別碼與標籤必須轉換為 **NFC** 形式。
2.  **空白與註解**：在計算 CAID 的序列化過程中，**禁止**包含任何空白、換行或註解。
3.  **數值**：
    - 整數不含前導零。
    - 浮點數統一使用小寫 `e`，且小寫正規化（如 `0.50` 變為 `0.5`）。

### 2.2 Combo 排序演算法
欄位必須具備決定論順序：
1.  **第一維度 (前綴優先級)**：
    *   順序：`%` > `~%` > `~` > `@` > `/` > (無前綴 Data)。
    *   **複合前綴判定**：若欄位同時具備多個前綴符號（如 `~%@`），以 **最左側 (最外層)** 之符號作為排序依據。例如 `~%@foo` 的優先級等同於 `~%`。
2.  **第二維度 (名稱)**：相同優先級內，按實體名稱之 Unicode 代碼點遞增排序。
3.  **數字鍵**：純數字鍵（List 索引）始終排在最後，按數值大小遞增。

### 2.3 聯集分支排序 (Union Branch Sorting)
為了確保 `A | B` 與 `B | A` 產生相同的 CAID，引擎在序列化聯集節點前，**必須**：
1.  計算每個分支自身的 CAID。
2.  按 **CAID 字符串之字典序** 對分支進行升序排列。
3.  對排列後的序列進行冪等化簡（移除重複 CAID）。

---

## 3. 引擎實作建議

### 3.1 串流雜湊 (Streaming Hash)
對於大型 Combo 或 List，建議採用串流雜湊而非先拼湊巨大的字串。
- **演算法**：使用遞迴下降遍歷 Canonical AST，將每個節點的型別標籤、名稱與值依序傳入雜湊更新器。

### 3.2 中間節點快取 (Merkle-style Cache)
由於 `n/` 的節點是不可變的，引擎應快取每個子節點的雜湊值。
- 當父節點內容不變時，直接復用子節點的 CAID 參與計算，這能將 CAID 計算複雜度從 $O(N)$ 降至 $O(\text{變動路徑深度})$。

### 3.3 #blur 狀態與 CHS (Canonical Horizon Snapshot)
計算 `#blur` 節點的 CAID 時，**必須**將具備決定論的視界參數序列化為 **CHS 封套** 並納入雜湊輸入。

1.  **強制納入參數**：`[%fuel, %strategy, %max_branches, %max_unification_depth, %max_pattern_nodes]`。
2.  **嚴禁納入參數**：`%timeout`（物理時間不穩定）與任何非標準的 `#ext:` 標籤。
3.  **序列化格式**：`node_content + "#horizon:" + canonical_json([params])`。
---

## 4. 跨實作驗證
官方提供 `oo caid-test-suite` 包含一組標準 AST 與其預期的 `v1` CAID，實作者應通過此測試套件以保證相容性。

---

## 5. CAID 驗證的邊界條件

### 5.1 不透明 CAID 處理
當引擎遇到無法計算的 CAID（如使用未知演算法或格式版本）時：

1.  **語義不透明模式**：
    - 若該 CAID 出現在 `#refine` Commit 的 `target_caids` 欄位中。
    - 引擎將其視為**不透明字串**，僅進行字串匹配，不進行雜湊驗證。
    - 信任來源：`#refine` Commit 的簽署權威。
2.  **嚴格驗證模式**：
    - 若該 CAID 出現在一般內容引用中（如 `deps` 欄位）。
    - 引擎**必須**能計算並驗證該 CAID，否則回傳 `#unsupported_ca_algo` 錯誤。

### 5.2 錯誤代碼 (Boundary Errors)

| 錯誤代碼 | 說明 |
| :--- | :--- |
| **`#unsupported_ca_algo`** | 引擎不支援該 CAID 使用的雜湊演算法或格式版本。 |
| **`#refine_authority_missing`** | `#refine` Commit 缺少有效的治理權威簽署。 |
| **`#refine_source_unverifiable`** | `#refine` Commit 的 `source_caids` 無法在當前引擎下驗證。 |
