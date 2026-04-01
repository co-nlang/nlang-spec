# APP_02：形式化驗證戰略藍圖 (Formal Verification Strategy)
## 1. 驗證架構：分層可信計算基 (Layered TCB)

我們將 `n/` 的形式化驗證分為三個維度，對應語言的六層架構，以避免複雜度爆炸。

### 1.1 數學核心層 (Layer 0) - 公理證明
*   **對象**：**[SPEC_01](./SPEC_01_Foundation_and_Lattice.md)** (格論公設), **[SPEC_09](./SPEC_09_Standard_Library.md)** (代數憲法)。
*   **工具**：**Lean 4**。
*   **目標**：建立 `n/` 的「數學黃金參考」。
    *   證明合併 (`&`) 的交換律、結合律與冪等律。
    *   證明 Top (`_`) 與 Bottom (`_|_`) 的單位元與吸收律。
    *   證明**函子 (Functor)** 與**單子 (Monad)** 定律在 Combo 結構下的正確性。

### 1.2 語義邏輯層 (Layer 1) - 匯流性與進展性
*   **對象**：**[SPEC_06](./SPEC_06_Unification_Logic.md)** (統一化邏輯), **[SPEC_07](./SPEC_07_Logic_and_Pipe.md)** (態射與管道)。
*   **工具**：**K Framework** 或 **PLT Redex**。
*   **目標**：驗證收斂演算法的運算特質。
    *   **匯流性 (Confluence)**：證明對於同一個定義，無論收斂順序如何，最終 CAID 一致。
    *   **進展性 (Progress)**：證明只要運算未達終態且燃料充足，收斂總能繼續。

### 1.3 運行時與狀態層 (Layer 2/3) - 守恆定律
*   **對象**：**[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** (計算視界), **[SPEC_10](./SPEC_10_Evolution_and_Commit.md)** (演化、提交與時間), **[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** (遞迴與驗證)。
*   **工具**：**TLA+** 或 **Alloy**。
*   **目標**：驗證狀態變遷與不變性。
    *   **Invariant 檢查**：將 **[SPEC_00](./SPEC_00_Introduction.md)** 的五大不變性建模為 TLA+ 的 `INVARIANT`。
    *   **併發安全**：證明平行 Commit 在不同合併策略下的安全性。

---

## 2. 關鍵驗證挑戰與對策

### 2.1 從「停機」轉向「有界收斂」
由於 `n/` 承認統一化是 NP-hard 且不可判定，我們不追求證明「全域終止」。
*   **策略**：證明 **「有界終止性 (Bounded Termination)」**。
*   **命題**：證明在給定 `%fuel` 與 `%max_unification_depth` 下，任何觀測行為必在有限步內收斂至 `{值, _|_ , #incomplete}` 三者之一。

### 2.2 三位一體同構的一致性
*   **策略**：在 Lean 4 中定義三種觀測視角（Views），證明轉換函數是**雙射 (Bijection)**，並驗證 `%kind` 推斷邏輯的互斥性與完整性。

### 2.3 CAID 穩定性 (Idempotency)
*   **策略**：證明 `oo fmt` 的冪等性與語義保全。
*   **方法**：結合 **Property-Based Testing (PBT)**（如 Rust 的 `proptest`）進行大規模隨機驗證。

## 3. 運行時發散偵測與優化建議 (Heuristics)

針對 **[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** 定義的發散偵測義務，建議實作者採用以下高效啟發式演算法：

### 3.1 狀態指紋快取與 k-閾值判定
為了在 $O(1)$ 時間內偵測潛在發散：
1.  **快取結構**：引擎應維護一個 Thread-local 的雜湊表，鍵為 `(Morphism_CAID, Input_CAID)`。
2.  **k-閾值**：若同一路徑連續進入 $k$ 次（預設 $k=16$）且 `Input_CAID` 持續變遷，則啟動**度量檢查**。
3.  **度量檢查 (Measure Check)**：計算輸入節點的「格論高度」。若高度未呈現遞減趨勢（或反而增長），則立即坍縮為 `#divergent`。

### 3.2 資訊單調性的跳躍式驗證 (Leaping Verification)
為了平衡安全性與性能：
1.  **CAID 快速對照**：若下一層輸入與當前輸入 CAID 一致，判定為靜止循環（Static Cycle），直接回傳 $\top$。
2.  **Checkpoint 機制**：不需要每層進行 $Result \sqsubseteq Input$ 的合併驗證。建議每隔 $N$ 步（如每 32 步）進行一次完整合併檢查。
3.  **失敗傳播**：一旦 Checkpoint 發現違反單調性，利用因果鏈回溯所有相關快取並標記為 `_|_`。

---

## 4. 自我演化的自指保護 (SPEC_17)

為了解決「用規格驗證規格」的循環依賴：
*   **層級理論 (Universe Levels)**：驗證器位於 Layer $N$，被驗證的規格位於 Layer $N-1$。
*   **核心凍結**：規定驗證器的核心數學庫（Layer 0）永久凍結，即使上層規格演化，底層邏輯亦保持不變。

---

## 5. 實作路線圖 (Implementation Roadmap)

1.  **Phase 1: 核心格論庫 (The Lattice Kernel)**：使用 Lean 4 實作數學公理庫。
2.  **Phase 2: 語義模擬器 (Unification Simulator)**：使用 K Framework 實現可執行語義。
3.  **Phase 3: 不變性守護者 (Invariant Checker)**：使用 TLA+ 對 Commit 模型進行建模檢查。
4.  **Phase 4: 實作精化 (Refinement)**：驗證 Rust 引擎核心程式碼是否為規格的正確精化。

---

## 6. 終極目標：內容定址證明 (CAID-linked Proofs)

未來，每一個經由 `oo verify` 產生的形式化證明都將擁有自己的 **CAID**。
*   **不可變證明**：證明永久綁定至該 Commit 的幾何指紋。
*   **零知識證明 (Future)**：利用 ZK-SNARKs 進行隱私驗證。

---

## 7. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_00](./SPEC_00_Introduction.md)** | 不變性守恆定律是證明的基礎。 |
| **[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** | 遞迴終止性證明與不動點計算。 |
| **[SPEC_16](./SPEC_16_Testing_and_Proof.md)** | 測試作為動態證明的實踐維度。 |
| **[SPEC_17](./SPEC_17_Self_Evolution.md)** | 規格自舉演化的形式化基礎。 |
