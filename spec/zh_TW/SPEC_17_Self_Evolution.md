# n/ Language Specification - 自我演化 (Self-Evolution)
本章節將 `n/` 的幾何哲學套回語言本身，描述規格如何迭代、如何面對分歧、以及如何在 CAID 系統中保持一致性。

---

## 1. 核心命題：規格即不可變 Combo

`n/` 的語言規格本身，就是宇宙中的一個幾何物件。

```nlang
;; 語言規格的幾何實體
@n_spec: {
    %id:        "hash:sha256:spec-v1-id..."
    version:    "1.0"
    @syntax:    { ... }
    @semantics: { ... }
}
```

語言的每一次迭代，不是「修改」舊規格，而是 **發現（Discover）** 一個新的、滿足更高約束的規格 Combo。

### 1.1 規格自省與版本聲明

規格書不僅描述語言，它本身也受 `n/` 的幾何規則管理。
*   **版本義務**：每一份正式發佈的規格 Commit **必須** 更新 **[SPEC_00](./SPEC_00_Introduction.md)** 中的版本映射表。
*   **相容性宣告 (`%compat`)**：規格節點應包含 `%compat` 欄位，明示其所依賴的底層 `fmt_version` 與 Ouroboros 引擎版本。
*   **精煉演化**：當規格發生重大語義變更（如 Layer 1 變更）時，必須發布對應的 `#refine` 演化 Commit，協助舊宇宙節點平滑遷移。

### 1.2 自指問題 (Self-Reference Problem)

由於 `n/` 用自己的格論描述自己的演化，產生了一個自指問題：

**問題**：如果 SPEC_v2 修改了 CAID 計算規則，那麼 SPEC_v2 本身的 CAID 應該用 v1 還是 v2 規則計算？

**解答**：採用「層級跳躍 (Level Hopping)」策略：

1.  **元規則不變性**：CAID 計算規則本身屬於**元層級 (Meta-Level)**，不隨規格版本變更。
2.  **演算法升級與 `#legacy` 池**：若未來 `n/` 需要升級基礎雜湊演算法（如由 SHA256 升級至 BLAKE3）或規範化規則：
    - 新版規格產生的 CAID 採用新演算法與新版本號（如 `v2`）。
    - 舊有規格的 CAID 不會被廢棄，而是自動歸入 **`#legacy` 池**。
    - **動態反映視圖**：
        ```nlang
        ;; 等價映射表是歷史 #refine Commit 的動態合成視圖
        ~%Engine.equivalence_map: {
            ;; 此映射表由引擎掃描歷史中所有 #refine Commit 後合成
            ;; 每個條目的來源是一個 #refine Commit，其 CAID 可被驗證
            "hash:sha256:v1:old-id": "hash:blake3:v2:new-id"
        }
        ```
    - **跨演算法透明度**：舊版引擎將新版雜湊（如 BLAKE3）視為不透明字面量。當映射關係成立時，舊引擎執行「身分轉交」，將觀測流量導向新 CAID 所標識的幾何本體。

### 1.2.1 等價映射表的合成機制

等價映射表 (`~%Engine.equivalence_map`) 不是一個獨立的規格節點，而是引擎對歷史中所有 **`#refine` Commit** 進行掃描與彙整後產生的**動態視圖**。

**合成演算法**：
1.  **掃描歷史**：引擎從 HEAD 向後遍歷所有 Commit。
2.  **識別 #refine**：篩選出標籤為 `#refine` 的 Commit。
3.  **提取映射**：從每個 `#refine` Commit 中提取：
    - `~%Refine.source_caids`: 舊 CAID 集合（聯集）。
    - `~%Refine.target_caids`: 新 CAID 集合（聯集）。
4.  **合成視圖**：將所有映射合併為單一映射表。

**驗證機制**：
*   **舊引擎義務**：舊引擎（v1）只需驗證 `#refine` Commit 自身的 CAID（使用 v1 規範化 + SHA256）。
*   **目標不透明性**：對於映射目標 CAID（如 v2 BLAKE3），舊引擎將其視為**不透明字串**，無需驗證其計算正確性。
*   **信任來源**：`#refine` Commit 必須由當前 Epoch 的**規格治理權威**（見 **[ORDER_01](./ORDER_01_Evolution_and_Governance.md)**）簽署。在引導期（Pre-genesis），該權威由 **[ORDER_00](./ORDER_00_Interim_Constitution.md)** 代理。

3.  **核心不變性**：雖然演算法可能升級，但「萬物皆 Combo、收斂為合併」的數學公理（Layer 0）是永久凍結的。這保證了跨版本的結構始終具備同構的可能性。

### 1.3 版本自舉與 N-1 原則
新規格版本的 CAID 計算與解析必須遵循 **「穩定先行 (Stable First)」** 原則：

#### 1.3.1 語義奇點 (Semantic Singularity)
對於 **Epoch 0** 的正式啟動，其官方 CAID 體系遵循以下**語義自舉演算法 (Semantic Bootstrapping)**：
1.  **創世包 (Genesis Bundle)**：定義為規格書內建的標準庫原始碼集合（`~%List`, `~%Math`, `~%Engine` 等）。
2.  **規範化**：使用屆時硬編碼於 v1.0.0 引擎內的規範化邏輯對創世包進行格式化。
3.  **雜湊**：對結果進行 SHA256 運算，產生 Epoch 0 的「語義創世 CAID」。
4.  **因果錨定**：此 CAID 被視為語義治理的起點，用於精煉引導期（Pre-genesis）的所有實驗性 Commit。

#### 1.3.2 跨世代退化封套 (The Degenerate Envelope)
為了確保舊版引擎（ $v_{N-1}$ ）能成功計算新規格（ $v_N$ ）的 CAID，任何規格跳躍的頂層結構必須遵循以下**退化佈局 (Degenerate Layout)**：

1.  **Layer 0 隔離**：新規格的核心定義內容（可能包含舊引擎不認識的語法）必須封裝在舊引擎視為**原子字面量**（如 `b"..."` 位元組陣列或 `""` 長字串）的欄位中。
2.  **元資訊公開**：封套外部僅保留舊引擎可識別的元資訊（如 `%id`, `%compat`, `%migration`）。
3.  **語義隔離範例**：
    ```nlang
    ;; 在 v1 引擎眼中，這是一個合法的 v1 Combo
    @spec_v2: {
        %id: "hash:v1:..."
        %version: "v2.0"
        ;; v2 的新語法內容被當作 v1 的黑盒數據處理
        ~%internal_ast: b"base64_encoded_v2_syntax..." 
        
        ;; 遷移態射必須是用 v1 語法撰寫的
        %migration: (v1_data -> /v1_to_v2_logic v1_data)
    }
    ```

#### 1.3.3 語義虛擬化掛載 (Semantic Virtualization)
「雙引擎」並非指同時運行兩套完整的二進制文件，而是指引擎核心必須具備**語義版本切換 (Semantic Mode Switching)** 的能力。

*   **物理要求**：引擎在執行 `%migration` 態射或解析具有歷史 CAID 的節點時，必須將統一化（Unification）算法的「公設集」切換至對應版本的狀態。
*   **執行路徑 (The Bridge)**：
    1.  **環境凍結**：暫停當前 $v_N$ 的新特性（如新的前綴或合併規則）。
    2.  **遺留執行**：在 $v_{N-1}$ 的語義約束下運行遷移態射。
    3.  **幾何映射**：將運算後的結果（通常是純數據或基礎 Combo）重新注入 $v_N$ 的觀測空間。
*   **WASM 建議 (Reference Recommendation)**：對於架構跨度極大的版本，建議實作者將舊版核心收斂邏輯編譯為獨立的 WASM 模組進行動態掛載，實現物理級別的語義隔離。

### 1.4 相容性宣告 (%compat)
規格版本透過 `%compat` 宣告其相容的舊版本 CAID 集合：
```nlang
@n_spec: {
    %id: "hash:sha256:spec-v2-id..."
    %compat: "hash:sha256:spec-v1-id" | "hash:sha256:spec-v1-1-id"
}
```

這個設計借鑑了型別論（Type Theory）中的 Universe 層級概念：
- Layer 0: 數學基礎（永久凍結）
- Layer 1: 語言系統（5 年凍結）
- Layer 2+: 可演化層級

自指只發生在 Layer 2+，不影響底層基礎。

---

## 2. 格論版本模型 (Lattice-based Versioning)

### 2.1 演化即細化 (Evolution as Refinement)
新版本在語義上應該是舊版本的收斂或擴展。
- **向後相容**：若版本 $v_2$ 是 $v_1$ 的子集（ $v_2 \subseteq v_1$ ），則所有在 $v_1$ 下合法的程式在 $v_2$ 下必然具備一致的坍縮。
- **衝突可視化**：當新舊語義互斥時，格論自動產生 `_|_`。

### 2.2 多版本共存
每個套件或程式可以宣告其相容的規格 CAID 集合。
*   **語法彈性**：由於 `Data | Type` 的三位一體同構，`%compat` 同時支援 **聯集型別語法** 與 **列表數據語法**，兩者在集合論語義上完全等價。
*   **建議實踐**：
    *   **聯集語法 (推薦)**：`%compat: "hash:A" | "hash:B"`（強調格論中的「集合邊界」）。
    *   **列表語法**：`%compat: ["hash:A", "hash:B"]`（便於從外部 JSON 自動合成）。
*   **禁止操作**：由於 CAID 無序位關係，嚴禁使用 `..` 範圍運算。

引擎在收斂時若偵測到環境規格不在該集合內，則回傳 `#compat_conflict`。

---

## 3. 分歧與合併 (Bifurcation & Merging)

### 3.1 方言即幾何分支 (Dialect as Branch)
社群對語言設計的分歧在 `n/` 中表現為一個**聯集狀態 (Union)**：
```nlang
;; 對 pipe 語義的兩種提案分支
@n_spec.@semantics.pipe: @proposal_A | @proposal_B
```
方言使用者可以選擇坍縮至特定分支，而主線規格則保持聯集，直到獲得足夠的資訊（觀測）來收斂。

### 3.2 永恆合併與遷移
任何方言分支永遠可以嘗試與主線進行 `#merge`。
- **合併語義**：即是計算兩者規格 Combo 的交集。
- **遷移態射 (%migration)**：語言規格可以包含「遷移邏輯」，這是一個將舊 CAID 結構轉化為新 CAID 結構的態射。
    - **語法範例**：
        ```nlang
        ;; 在新規格中定義遷移
        %migration: old_node -> {
            ;; 將 v1 的舊欄位映射至 v2 新結構
            new_field: old_node.legacy_key
            ...old_node \ { legacy_key: _ }
        }
        ```
    - **調用機制**：當引擎觀測到跨版本的內容引用時，若目標規格定義了針對來源規格的 `%migration`，則自動透明地應用該變換。

---

## 4. 銜尾蛇體系：演化與永恆 (The Ouroboros System)

銜尾蛇不只是循環，它是 **「遞迴觀測 (Recursive Observation)」**。
- **自體消化**：`n/` 用自己的格論描述自己的演化，用自己的 CAID 系統標識自己的版本，用自己的 Discovery 機制發現自己的下一個狀態。
- **螺旋上升**：每一圈演化都回到哲學起點，但 CAID 攜帶了更多的資訊量，讓宇宙在收斂中不斷前行。

### 4.1 宇宙的最終形態

在理論的極致處，當語言規格完整描述了自己，且沒有外部觀測者注入新的定義時，宇宙進入靜止狀態：

```nlang
;; 宇宙的最終形態：自省的靜止
_: _ & <_>    ;; Top 觀測自己的幾何結構態，結果仍然是 Top
              ;; 資訊量不增加，宇宙保持永恆的靜止
```

這不是終點，而是一個等待坍縮的潛能狀態。當下一個觀測者到來，這份靜止將被打破。

---

## 5. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_01](./SPEC_01_Foundation_and_Lattice.md)** | 格論收斂是版本演化的數學基礎。 |
| **[SPEC_09](./SPEC_09_Standard_Library.md)** | 版本演化的合法性與穩定性，由代數公設（如 Monoid 結合律）提供數學保證。 |
| **[SPEC_10](./SPEC_10_Evolution_and_Commit.md)** | Commit 模型紀錄了語言規格本身的演化歷史。 |
| **[SPEC_13](./SPEC_13_Discovery_and_Package.md)** | 語言版本透過 CAID 進行發現與驗證。 |
