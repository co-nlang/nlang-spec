# n/ Language Specification - 演化、提交與因果邊界 (Evolution & Causal Boundary)

本章節定義 `n/` 宇宙如何隨著時間演化，以及由 Commit 序列構成的**因果邊界 (Causal Boundary)** 內的狀態變遷規律。
因果邊界定義了「已固化事實」與「未發生可能性」的幾何邊界。

---

## 1. 核心模型：宇宙的格論序列

`n/` 的時間軸不是連續的，而是一個由 **Commit** 組成的離散序列。
每個 Commit $C_n$ 代表宇宙在特定時刻的完整不可變快照。

- **宇宙即序列**：$U = \{C_0, C_1, C_2, ...\}$。
- **演化即交集**：從 $C_n$ 到 $C_{n+1}$ 的演化過程，本質上是對當前宇宙施加一組新的定義約束（交集運算）。

### 1.1 歷史認識論：觀測快照之固化

在 `n/` 中，**「宇宙歷史由因果邊界固化，而非由真理固化」**。

1.  **坍縮態固化 (Collapsed Anchoring)**：一個 Commit 捕獲的是節點在特定物理視界下的 **「坍縮觀測結果」**。
2.  **#blur 的歷史地位**：若某節點在提交時處於 `#blur` 狀態，則其生成的 `CAID_blur` 將被作為該 Commit 的物理組成部分進行雜湊。
3.  **因果邊界不變性**：一旦 Commit 固化，該 `CAID_blur` 在該歷史節點中的語義即被鎖定。即使未來發現了精確真相 $E$，該歷史 Commit 的幾何內容（認識論事實）**嚴禁**發生改變。
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
- **成立條件 (Proof Obligation)**：精煉宣告必須滿足 **幾何單調性**。若宣告 $ID_{old} \rightarrow ID_{new}$，則在數學上必須滿足：
    $$ID_{new} \sqsubseteq ID_{old}$$
    這代表新物件提供的資訊量必須等於或大於舊物件，且兩者在邏輯上不可衝突。
- **跨演算法精煉 (Cross-Algorithm Refinement)**：
    `#refine` Commit 支援跨雜湊演算法與跨格式版本的精煉宣告。其物理結構必須包含：
    ```nlang
    ;; #refine Commit 範例
    {
        %id: "hash:sha256:v1:refine-commit-id"
        %tags: #refine
        ~%Refine.source_caids: "hash:sha256:v1:old-id" | "hash:sha256:v1:alt-id"
        ~%Refine.target_caids: "hash:blake3:v2:new-id"
        %authority: {
            signer: "hash:sha256:v1:architect-caid" ;; 建築師身份
            signature: b"..."                       ;; Ed25519 簽名數據
            timestamp: t"2026-04-02T12:00:00Z"
        }
    }
    ```
- **驗證義務與能階**：
    引擎對精煉宣告的驗證強度取決於其物理能力：
    1.  **完全驗證 (Total Verification)**：若引擎具備解析兩者內容的能力，則 **必須** 執行 $ID_{new} \sqcap ID_{old} = ID_{new}$ 判定。若判定失敗（即不滿足子集關係），引擎應將該精煉宣告視為無效，並回傳 `#refinement_conflict`。
    2.  **不透明驗證 (Opaque Trust)**：若引擎無法解析目標 CAID（如演算法不匹配），則將幾何一致性的保證權交由 `%authority` 簽署者。
    3.  **因果一致性義務**：引擎必須確保重定向後的物件在所有與舊物件相關的格論運算中，產生的結果與原意圖相容。
    4.  **權威簽署驗證**：`#refine` Commit 必須包含有效的 `%authority` 結構。
        - **簽署對象**：該 Commit 的 CAID（計算雜湊時排除 `%authority` 欄位本身）。
        - **權威判定**：`signer` 必須存在於當前紀元的 `~%Official.architects` 集合中。
        - **引導期特殊性**：引導期（Epoch < 0）之 Commit 預設不具備 `%authority`。其身分承襲由 **[ORDER_00](./ORDER_00_Interim_Constitution.md)** 定義之「創世精煉」清單硬編碼解決。

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
| **[SPEC_13](./SPEC_13_Discovery_and_Package.md)** | 定義了 `#refine` 如何驅動觀測視窗內的自動重定向。 |
| **[SPEC_16](./SPEC_16_Testing_and_Proof.md)** | 測試與證明可作為 `#commit` 前的自動化守門員。 |
| **[REAL_02](./REAL_02_Ouroboros_Protocols.md)** | 定義了引擎如何透過協定交換 Commit 與解決競爭。 |
| **[COSMOLOGY/08](./COSMOLOGY/08_PHYSICS_Thermodynamics.md)** | 演化的熱力學背景：Commit 鏈的增長與因果壓力。 |

---

### 哲學思辨 (Philosophical Synthesis)

> 結語：Commit 是宇宙留下的足跡。每一次提交都是一次永恆的選擇，在離散的時間序列中，織就了演化的錦緞。
