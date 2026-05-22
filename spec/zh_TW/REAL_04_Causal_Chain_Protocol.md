# REAL_04：因果鏈協議 (OODP Causal Chain Protocol)

> [!NOTE]: [Standard / 規範性標準]  
> 本協議統一定義 **OODP (Ouroboros Discovery Protocol)** 中 `%cause` 元欄位的物理結構與所有標準化的因果標籤（Cause Tags）。

基於 **觀測對偶性 (Observation Duality)**，`%cause` 既是一個可直接比較的標籤，也是一個包含豐富診斷資訊的封閉結構。

**本文定位**：
- **層級**：OODP 跨層級基礎設施（用於 L3-L5 的錯誤傳播與診斷）
- **上游**：SPEC_13 (發現語義)、SPEC_08 (視界管理)
- **下游**：REAL_02 L3 (收斂層衝突處理)

> 關於 OODP 五層架構的完整定義，請參閱 **[SPEC_13: 銜尾蛇發現協定](./SPEC_13_Ouroboros_Discovery_Protocol.md)** §0。

---

## 1. 標準結構 (Standard Structure)

`%cause` 是一個 **Cocoon**（封閉結構）。為了支援對偶觀測，它必須包含 `%val` 欄位。

```nlang
%cause: {{
    ;; 核心對偶欄位 (Duality Core)
    %val:       #Tag           ;; 衝突型別標籤 (如 #conflict)。直接觀測 %cause 時返回此值。
    message:    @str           ;; 人類可讀的錯誤描述
    
    ;; 定位欄位 (Location)
    path:       @str           ;; 觸發衝突的絕對路徑 (如 "_.user.profile.age")
    source:     @str           ;; 來源標識，檔案路徑或 CAID (如 "file:./main.n" 或 "hash:sha256:v1:...")
    line:       @int           ;; 行號 (若適用)
    column:     @int           ;; 欄號 (若適用)
    
    ;; 語境欄位 (Context)
    operation:  #Tag           ;; 觸發衝突的操作型別 (如 #merge, #observe, #lift)
    operands:   [@any]         ;; 參與運算的節點值或路徑 (用於重現)
    
    ;; 鏈結欄位 (Chaining)
    parent:     %cause | #none ;; 父層因果 (用於複雜合併的遞迴診斷)
    trace:      [@str]         ;; 堆疊追蹤 (用於遞迴或管道鏈)
    
    ;; 擴展欄位 (Extension)
    details:    {{}}           ;; 特定標籤的額外封閉資訊 (結構依 %val 而定)
}}
```

---

## 2. 因果標籤分類 (Cause Tag Taxonomy)

所有標準 `#cause` 標籤分為六大類別：

### 2.1 格論衝突 (Lattice Conflicts)

| 標籤 | 定義 | 典型觸發場景 | 關聯章節 |
| :--- | :--- | :--- | :--- |
| `#conflict` | 靜態邏輯不相容 | `1 & 2`、`@int & @str` (不相交型別) | **[SPEC_06](./SPEC_06_Unification_Logic.md)** |
| `#numerical_error` | 數值運算異常 | `NaN` 產生、浮點數溢位 | **[SPEC_02](./SPEC_02_Lexical_Structure.md)** |
| `#divergent` | 動態非終止 | `a: a + 1` (無限遞迴)、循環定義無法收斂 | **[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** |
| `#incomplete` | 視界內無法完全收斂 | 燃料耗盡但結果仍為聯集狀態 | **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** |

### 2.2 視界與資源邊界 (Horizon Boundaries)

| 標籤 | 定義 | 典型觸發場景 | 關聯章節 |
| :--- | :--- | :--- | :--- |
| `#fuel_exhausted` | 觀測燃料耗盡 | `%fuel` 配額用完，中斷收斂 | **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** |
| `#timeout` | 時間半徑超標 | 運算耗時超過 `%timeout` 或時鐘限制 | **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** |
| `#max_nodes_exceeded` | 匹配節點數超標 | `%max_pattern_nodes` 限制觸發 | **[SPEC_06](./SPEC_06_Unification_Logic.md)** |
| `#max_depth_exceeded` | 統一化深度超標 | `%max_unification_depth` 限制觸發 | **[SPEC_09](./SPEC_09_Standard_Library.md)** |
| `#max_branches_exceeded` | 聯集分支數超標 | `%max_branches` 限制觸發 | **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** |
| `#out_of_horizon` | 視界過度穿透 | 導航符號 `^` 超出實際嵌套層級 | **[SPEC_07](./SPEC_07_Logic_and_Pipe.md)** |

---

## 3. 標籤特定詳細結構 (Tag-Specific Details)

### 3.1 `#conflict` 詳細結構
```nlang
details: {{
    left:       @any        ;; 左運算元值
    right:      @any        ;; 右運算元值
    left_type:  @any        ;; 左運算元型別約束
    right_type: @any        ;; 右運算元型別約束
    merge_path: @str        ;; 衝突發生的相對路徑
}}
```

### 3.2 `#out_of_horizon` 詳細結構
```nlang
details: {{
    requested_depth: @int    ;; 請求的穿透深度 (如 ^^^^ 為 4)
    actual_depth:    @int    ;; 當前環境中可供穿透的最大深度
}}
```

---

## 4. 因果鏈組合規則 (Causal Chain Composition)

當收斂過程中多個衝突同時發生時，引擎必須選出一個作為「主因果標籤」返回。優先級如下：
1. `#divergent` > 2. `#effect_violation` > 3. `#conflict` > 4. 資源邊界標籤 > 5. `#not_found`。

---

## 5. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_03](./SPEC_03_Combo_System.md)** | Cocoon 結構定義 `%cause` 的封閉性。 |
| **[SPEC_05](./SPEC_05_The_Trinity_Isomorphism.md)** | `%val` 如何驅動觀測對偶性。 |
| **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** | 運行時如何生成本標準定義的報告。 |
