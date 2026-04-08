# n/ Language Specification - 測試與證明 (Testing & Proof)

本章節定義 `n/` 語言中的測試哲學與驗證機制。在一個基於格論收斂的數據中心語言中，測試不再是「執行與斷言」，而是「**約束與觀測**」。

---

## 1. 測試即合併 (Testing as Merge)

在傳統語言中，測試通常透過 `assert(actual == expected)` 來進行。在 `n/` 中，驗證的本質是**合併運算（`&`）**。

### 1.1 相容性測試 (Compatibility Test)
當我們對兩個節點進行合併時，若結果未產生衝突（即不等於 `_|_`），則代表「實際結果符合預期約束」。

```nlang
~%test.math: {
    ;; 測試 1 + 1 是否與 2 相容
    case1: (/add 1 1) & 2

    ;; 測試結果是否符合特定型別約束
    case2: (/add 2 3) & @int
}
```
*   若 `/add 1 1` 的結果為 `2`，則 `2 & 2` 收斂為 `2`，測試通過。
*   若結果為 `3`，則 `3 & 2` 產生衝突，收斂為 `_|_`，測試失敗，引擎將透過 `%cause` 記錄失敗原因。

### 1.2 負向測試 (Negative Test)
有時我們需要驗證某個操作*必定*會失敗或產生特定錯誤。此時可以利用 `_|_` 觀測機制或標籤：

```nlang
~%test.error_handling: {
    ;; 測試除以零是否會產生空集合 (發生衝突)
    case_div_zero: (/div 1 0) <= _|_
}
```

---

## 2. 測試框架與工具 (`oo test`)

`n/` 的官方工具鏈提供 `oo test` 指令，用於自動發現與執行測試。

### 2.1 測試發現 (Discovery)
`oo test` 會掃描工作區中所有的 `.n` 檔案，並自動尋找符合以下路徑模式的節點：
*   所有以 `test_` 或 `~%test` 為前綴的 Combo。

### 2.2 觀測與報告
對於每個找到的測試案例（Combo 內的欄位），`oo test` 會獨立對其進行觀測：
1.  **通過 (Pass)**：若節點收斂為任何非 `_|_` 的值（Atom, Combo, List 等），且沒有在過程中拋出未捕獲的異常。
2.  **失敗 (Fail)**：若節點最終收斂為 `_|_`。引擎會自動提取該節點的 `%cause` 元資訊，並產生錯誤報告（如：路徑不匹配、型別衝突、不相容的值）。

### 2.3 靜態違規檢測 (Static Violation Detection)

部分反模式（如 **[SPEC_15](./SPEC_15_Anti_Patterns.md)** 中定義的隨機性注入、隱性環境依賴等）無需動態觀測即可透過靜態分析檢測。`oo test` 支援僅進行靜態分析的快速檢測模式：

```bash
oo test --static-only    ;; 僅進行靜態分析，不動態觀測
```

---

## 3. 屬性測試與空間覆蓋率

由於 `n/` 的型別即集合，測試不再侷限於單一值的比對，而是對整個**集合空間**的覆蓋。

### 3.1 集合空間覆蓋率 (Spatial Coverage Metrics)
在傳統語言中，我們衡量「行覆蓋率」；在 `n/` 中，我們衡量「集合空間的覆蓋率」。當執行 `oo test --coverage` 時，引擎會針對每個型別約束報告：
*   **正向覆蓋率 (Positive Coverage)**：被測試的原子佔該約束總原子空間的比例或代表性。
*   **負向覆蓋率 (Negative Coverage)**：測試了哪些邊界衝突。

---

## 4. 系統證明介面 (`~%Proof`)

在 `n/` 中，證明不是附加的註解，而是宇宙中可觀測的幾何物件。所有的證明邏輯與合約均透過 `~%Proof` 系統物件進行反映。

### 4.1 證明合約 (`~%Proof.@Proof`)
任何宣稱具備形式化證明能力的節點，均應滿足此型別約束。使用者可透過 `<~%Proof.@Proof>` 觀測其完整結構。

```nlang
~%Proof.@Proof: {
    %kind:     #proof
    %target:   @any         ;; 證明的對象 (如某個態射或 Combo)
    %property: #Tag         ;; 證明的性質標籤 (如 #commutativity, #totality)
    %verifier: #Tag         ;; 負責驗證的引擎 (如 #lean4, #coq, #oo_internal)
    %evidence: @str | b""   ;; 證明的證據實體 (如外部 CAID 或原始碼)
}
```

### 4.2 驗證原語 (`~%Proof./verify`)
這是驅動證明檢查的核心態射。

*   **輸入**：一個滿足 `~%Proof.@Proof` 約束的節點。
*   **語義**：引擎根據 `%verifier` 標籤調用對應的驗證器插件，對 `%evidence` 進行核對。
*   **結果**：
    - **成功**：回傳該節點本身，並在元資訊中疊加 `#proven` 標籤。
    - **失敗**：收斂為 `_|_`，標記 `%cause: #verification_failed`。

### 4.3 證明節點範例 (交換律證明)
```nlang
/add_comm_proof: </add> & ~%Proof.@Proof: {
    %property: #commutative
    %verifier: #lean4
    %evidence: "hash:lean4:v1:9f86..."
}

;; 進行驗證
status: ~%Proof./verify /add_comm_proof  ;; 若 Lean 4 驗證通過，結果為 #proven
```

---

## 5. 證明的幾何傳遞 (Proof Propagation)

由於 `n/` 是基於格論的，證明具備天然的單調傳遞性：

1.  **合併保全 (Merge Preservation)**：
    若節點 $A$ 已被證明具備性質 $P$，則對於任何合併 $C = A \sqcap B$，結果 $C$ 在 $A$ 的維度上依然繼承性質 $P$ 的保證。
2.  **證明即約束 (Proof as Constraint)**：
    觀測者可以將證明對象直接作為約束應用：`my_logic & /add_comm_proof`。若 `my_logic` 的結構與已證明的幾何矛盾，則收斂為 `_|_`。

---

## 6. 測試、證明與演化循環

在 `n/` 的開發生命週期中，驗證被視為演化的一環：

1.  **Staged 階段**：執行 `oo test`（動態觀測與合併測試）。
2.  **Check 階段**：調用 `~%Proof./verify`（形式化證明核對）。
3.  **Commit 階段**：僅當所有驗證節點均不為 `_|_` 時，宇宙才允許狀態推進。

---

### 哲學思辨 (Philosophical Synthesis)

> 結語：觀測即證明。在 `n/` 的世界裡，正確性不是被測試出來的，而是當約束完整收斂時，真理自然顯現的必然結果。透過 `~%Proof`，我們不僅看見了程式碼的運作，更看見了支撐這份運作的永恆幾何公理。
