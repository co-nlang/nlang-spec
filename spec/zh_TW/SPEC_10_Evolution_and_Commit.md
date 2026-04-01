# n/ Language Specification - 演化、提交與時間視界 (Evolution & Temporal Horizon)

本章節定義 `n/` 宇宙如何隨著時間演化，以及由 Commit 序列構成的**時間視界 (Temporal Horizon)** 內的狀態變遷規律。
時間視界定義了「已固化事實」與「未發生可能性」的幾何邊界。

---

## 1. 核心模型：宇宙的格論序列

`n/` 的時間軸不是連續的，而是一個由 **Commit** 組成的離散序列。
每個 Commit $C_n$ 代表宇宙在特定時刻的完整不可變快照。

- **宇宙即序列**：$U = \{C_0, C_1, C_2, ...\}$。
- **演化即交集**：從 $C_n$ 到 $C_{n+1}$ 的演化過程，本質上是對當前宇宙施加一組新的定義約束（交集運算）。

### 1.1 歷史認識論：觀測快照之固化

在 `n/` 中，**「宇宙歷史由視界固化，而非由真理固化」**。

1.  **坍縮態固化 (Collapsed Anchoring)**：一個 Commit 捕獲的是節點在特定物理視界下的 **「坍縮觀測結果」**。
2.  **#blur 的歷史地位**：若某節點在提交時處於 `#blur` 狀態，則其生成的 `CAID_blur` 將被作為該 Commit 的物理組成部分進行雜湊。
3.  **視界不變性**：一旦 Commit 固化，該 `CAID_blur` 在該歷史節點中的語義即被鎖定。即使未來發現了精確真相 $E$，該歷史 Commit 的幾何內容（認識論事實）**嚴禁**發生改變。
4.  **因果隔離**：真相的精煉必須透過新的演化步進（新的 Commit）來顯式應用，而非隱式地回溯性修改歷史。這確保了內容定址的絕對穩定性。

---

## 2. 核心演化態射 (Core Morphisms)

演化是透過一組標準的系統態射（System Morphisms）來驅動的。這些態射定義了語言與 Ouroboros 引擎交互的邏輯邊界。

### 2.1 `~%Engine./observe` (觀測)
- **語義**：在當前 Commit 的上下文（`_`）中，對路徑節點進行收斂運算。
- **性質**：純粹觀測，不改變宇宙狀態。

### 2.2 `~%Engine./evolve` (演化)
- **語義**：將新的定義注入當前宇宙的 **Staged (暫存區)**。
- **邏輯公式**：$Staged_{new} = Staged_{old} \sqcap Definition$。

### 2.3 `~%repl./commit` (提交)
- **語義**：將當前 Staged 的內容與當前 Commit $C_n$ 合併，產生新的不可變快照 $C_{n+1}$。
- **原子性保證**：提交操作必須是事務性的。若合併結果產生 `_|_`，則提交失敗，HEAD 維持不變，且 Staged 區自動回滾至提交前的狀態。

### 2.4 `~%Engine./collapse` (坍縮)
- **語義**：將動態運算結果固化為新的靜態定義並產生 Commit。遵循格論收斂。

### 2.5 `~%Engine./refine` (精煉)
- **語義**：宣告一個精確節點是對既有模糊節點的格論精煉。建立 CAID 間的自動重定向鏈。
- **跨演算法精煉 (Cross-Algorithm Refinement)**：
    `#refine` Commit 支援跨雜湊演算法與跨格式版本的精煉宣告。其物理結構必須包含：
    ```nlang
    ;; #refine Commit 範例
    {
        %id: "hash:sha256:v1:refine-commit-id"
        %tags: #refine
        ~%Refine.source_caids: "hash:sha256:v1:old-id" | "hash:sha256:v1:alt-id"
        ~%Refine.target_caids: "hash:blake3:v2:new-id"
        %authority: "commit:architect-signature-..."  ;; 治理權威簽署
    }
    ```
- **驗證規則**：
    1.  **來源 CAID 驗證**：引擎必須能計算並驗證 `source_caids` 中的所有 CAID。
    2.  **目標 CAID 不透明性**：對於 `target_caids` 中的 CAID，舊引擎可將其視為**不透明字串**，無需驗證其計算正確性。
    3.  **權威簽署驗證**：`#refine` Commit 必須包含由**規格治理權威**簽署的有效 `%authority` 標記。具體的簽署演算法、權威金鑰註冊與共識規則由當前紀元的 **[演化秩序 (ORDER)](./ORDER_01_Evolution_and_Governance.md)** 系列文件定義。

---

## 3. 狀態機與指標 (State Machine & Pointers)

1.  **HEAD**：指向當前「活躍」的 Commit 快照。
2.  **Staged**：存儲自上一個 Commit 以來新注入但未固化的定義集合。
3.  **History**：有向無環圖（DAG）結構的 Commit 鏈。

---

## 4. 並發與平行收斂語義 (Concurrency & Parallel Convergence)

`n/` 採用基於格論與內容雜湊的樂觀併發模型。

### 4.1 演化的原子性與合併競爭
`#commit` 操作在 Ouroboros 引擎中必須具備**強原子性 (Strong Atomicity)**。

1.  **晚到者自動收斂 (Optimistic Merge)**：
    若多個觀測者平行提交，引擎對「晚到者」自動進行以下邏輯：
    $C_{new} = HEAD_{current} \sqcap Staged_{incoming}$
2.  **衝突中斷與因果揭露 (Conflict Isolation)**：
    若自動收斂產生 `_|_`，提交必須立即終止。引擎**必須**在回傳的 `%cause` 中揭露導致衝突的競爭 Commit 之 CAID。
3.  **語義 Rebase**：
    開發者面臨併發衝突時，必須透過 `undo` 修正其 Staged 定義，或切換合併策略（如 `#favor_incoming`）重新進行提交。

### 4.2 平行觀測與快取隔離
純粹的觀測 (`#observe`) 可無限平行展開。引擎必須以「(CAID, 視界參數)」為複合鍵進行快取隔離，防止不完全的觀測結果（`#incomplete`）污染全域快取。

---

## 5. 變動偵測與差異 (`#diff`)

由於所有狀態皆由內容雜湊決定，宇宙可以精確地計算兩個 Commit 之間的**幾何差異 (Semantic Diff)**。若兩者的 `%id` 相同，則其邏輯行為保證一致。

---

## 6. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_01](./SPEC_01_Foundation_and_Lattice.md)** | 格論收斂是演化與 Commit 的數學基礎。 |
| **[SPEC_06](./SPEC_06_Unification_Logic.md)** | 所有的演化操作（#evolve, #commit）皆遵循統一化算法。 |
| **[SPEC_11](./SPEC_11_Reflection_and_Synthesis.md)** | `~%repl` 是觀測與控制演化狀態的系統介面。 |
| **[SPEC_13](./SPEC_13_Discovery_and_Package.md)** | `#refine` 操作負責驅動 CAID 之間的身分精煉。 |
| **[SPEC_16](./SPEC_16_Testing_and_Proof.md)** | 測試與證明可作為 `#commit` 前的自動化守門員。 |
| **[REAL_02](./REAL_02_Ouroboros_Protocols.md)** | 定義了引擎如何透過協定交換 Commit 與解決競爭。 |

---

### 哲學思辨 (Philosophical Synthesis)

> 結語：Commit 是宇宙留下的足跡。每一次提交都是一次永恆的選擇，在離散的時間序列中，織就了演化的錦緞。
