# APP_02：量子化形式驗證戰略藍圖 (Quantum Formal Verification)

## 1. 驗證架構：量子可信計算基 (Quantum TCB)

我們將 `n/` 的形式化驗證分為三個維度，對應量子化架構。這種分層策略避免了複雜度爆炸，同時確保了從數學基礎到運行時實作的全鏈條可信度。

### 1.1 量子本體層 (Layer 0) - Solèr 證明

*   **工具**：**Lean 4**。
*   **對象**：**[SPEC_01](./SPEC_01_Foundation_and_Lattice.md)** (正交模格格論公設), **[SPEC_09](./SPEC_09_Standard_Library.md)** (量子化代數憲法)。
*   **目標**：建立子空間格的「數學黃金參考」——一個不可變的、機器可驗證的數學基礎。
    *   證明**對合否定 `!`** 的正交性質（對合性、互斥收斂、窮舉全域、反單調性）。
    *   證明 **EML 算子** 的函數覆蓋完備性——即所有初等函數皆可由 `eml(x, y) = exp(x) - ln(y)` 與常數 `1` 組合生成。
    *   證明正交模格（而非分配格）滿足 Solèr 定理所需的無窮維條件。

**為何選擇 Lean 4**：其依賴型別系統（Dependent Type Theory）與 `n/` 的格論語義高度同構，可直接將 Combo 結構映射為 Lean 的歸納型別（Inductive Types）。Lean 4 的元編程能力也允許我們自動生成部分證明義務，減少手動證明的負擔。

**工程實踐**：
- 建立 `nlang-lean` 倉庫，包含正交模格公設的形式化定義。
- 定義與 SPEC 文件對應的「規格跟蹤矩陣 (Spec Traceability Matrix)」，確保每個 SPEC 公設都有對應的 Lean 定理。
- 使用 Lean 的 `simp` 與 `aesop` 自動化策略處理常見的格論等價變換。

### 1.2 觀測投影層 (Layer 1) - Bohrification 驗證

*   **工具**：**Isabelle/HOL**。
*   **對象**：**[SPEC_06](./SPEC_06_Unification_Logic.md)** (統一化邏輯), **[SPEC_07](./SPEC_07_Logic_and_Pipe.md)** (態射與管道)。
*   **目標**：驗證投影正確性與觀測語義。
    *   **匯流性 (Confluence)**：證明在特定視角（Perspective）下，無論投影順序如何，最終 CAID 一致。這對應於 Bohrification 中「不同交換子代數的投影結果相容」的性質。
    *   **進展性 (Progress)**：證明只要燃料充足，子空間正交分解總能繼續——即觀測過程不會無故停滯。
    *   **KS 定理合規性**：驗證引擎的實作不允許構造出違反 Kochen-Specker 定理的「隱藏變數」觀測。

**為何選擇 Isabelle/HOL**：其高階邏輯（HOL）適合建模 Bohrification 的拓撲結構，且具備豐富的數學庫（Archive of Formal Proofs）支援。Isabelle 的 `sledgehammer` 工具能自動調用外部 SMT 求解器，適合處理管道語義中的複雜約束。

**工程實踐**：
- 使用 Isabelle 的 Locale 機制定義「觀測視角 (Observation Perspective)」的模組化規範。
- 建立「反例搜尋 (Counterexample Search)」流程：對於每個「不應發生」的性質（如 KS 違規），使用 Nitpick 尋找潛在的實作漏洞。
- 與 Ouroboros 引擎的實作進行「證明提取 (Proof Extraction)」對接，確保形式化模型與實際程式碼的語義一致性。

### 1.3 運行時與狀態層 (Layer 2/3) - 守恆定律

*   **工具**：**TLA+**。
*   **對象**：**[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** (計算視界與 KS 定理), **[SPEC_10](./SPEC_10_Evolution_and_Commit.md)** (演化、提交與時間), **[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** (遞迴與譜驗證)。
*   **目標**：驗證狀態變遷與不變性。
    *   **Invariant 檢查**：將 **[SPEC_00](./SPEC_00_Introduction.md)** 的五大不變性建模為 TLA+ 的 `INVARIANT`：
        - 內容定址不變性 (Content Addressability)
        - 資訊單調性 (Information Monotonicity)
        - 格論封包 (Lattice Closure)
        - 視界決定論 (Horizon Determinism)
        - 自我演化完整性 (Evolution Integrity)
    *   **併發安全**：證明平行 Commit 在不同合併策略下的安全性，特別是在量子化語境下的「譜同步」問題。
    *   **活性 (Liveness)**：證明在公平調度下，任何提交的演化請求最終都會被處理（或明確失敗）。

**為何選擇 TLA+**：其狀態機模型與 `n/` 的「觀測即狀態坍縮」語義天然契合。TLA+ 的「精煉 (Refinement)」概念與 `n/` 的 `#refine` 操作形成直接對應，允許我們從高層抽象逐步精煉至實作細節。

**工程實踐**：
- 使用 PlusCal 演算法語言編寫引擎核心狀態機的偽代碼，再轉譯為 TLA+ 規範。
- 建立「模型檢驗 CI (Model Checking CI)」：每次 SPEC 變更自動執行 TLC 模型檢驗器，驗證不變性在有限狀態空間下是否保持。
- 定義「災難場景 (Disaster Scenarios)」：如網路分區、惡意節點、燃料耗盡等，驗證系統在極端條件下的 graceful degradation。

## 2. 關鍵挑戰：從「停機」到「有界投影」

傳統程序驗證聚焦於「停機問題 (Halting Problem)」，但在 `n/` 的量子語義中，**「停機」是一個過於絕對的概念**。由於量子邏輯的不確定性與計算視界的存在，我們證明的是 **「有界投影性 (Bounded Projection)」**：在給定燃料下，投影行為必在有限步內坍縮。

### 2.1 有界收斂證明策略

為了在形式化驗證中處理這種「資源受限的收斂」，我們採用以下策略：

1.  **燃料單調性 (Fuel Monotonicity)**：
    證明對於任何給定的 `%fuel` $F$，觀測過程涉及的遞迴深度與節點展開數量具有上界 $B(F)$。這使得我們能將「發散」轉化為一個可判定的資源耗盡事件。

2.  **譜測度遞減 (Spectral Measure Decreasing)**：
    將每次合併或態射應用視為對子空間的「精煉」。證明每次精煉都嚴格減少某個良基測度 (Well-founded Measure)，例如：
    *   未解析的 `%blur` 節點數量
    *   待匹配的模式節點總數
    *   跨 Commit 的引用深度

3.  **跡循環偵測 (Trace Cycle Detection)**：
    對於可能包含循環引用的遞迴結構（如透過 CAID 的延遲加載），引擎必須在展開時維護一個「跡 (Trail)」。形式化驗證需證明：當同一 CAID 在單一路徑上被觀測到第二次時，引擎將標記 `#divergent` 並中止。

### 2.2 EML 結構歸納法 (Structural Induction on EML)

由於所有數學表達式 $S \to 1 \mid eml(S, S)$，形式化驗證只需針對以下公設進行建模：

**基礎公設 (Layer 0)**：
1.  $eml(x, 1) = \exp(x)$
2.  $eml(0, y) = 1 - \ln(y)$
3.  $eml(x, y) = \exp(x) - \ln(y)$（一般形式）

**結構歸納規則**：
對於任意性質 $P$ 關於 EML 表達式 $E$：
- **基底情況**：$P(1)$ 成立（常數 1 滿足性質）
- **歸納步驟**：若 $P(E_1)$ 與 $P(E_2)$ 成立，則 $P(eml(E_1, E_2))$ 成立

**應用範例**：
- 證明所有 EML 表達式在複數域 $\mathbb{C}$ 上良好定義（除奇異點外）
- 證明數值精度傳播的誤差上界
- 驗證 EML 樹至 CAID 的規範化映射之決定論

**證明工具**：
- **Lean 4**：利用其歸納型別系統直接建模 EML 文法
- **Coq**：使用 `Inductive` 定義 EML 表達式，配合 `fixpoint` 進行歸納證明

---

## 3. 譜發散偵測與啟發式演算法

在實際引擎實作中，我們無法等待無限時間來「證明」發散。因此，規格書定義了一套**可在多項式時間內執行的發散偵測啟發式演算法**，並將其作為引擎合規性驗證的一部分。

### 3.1 跡指紋快取與熵閾值判定

為了在 $O(1)$ 時間內偵測潛在發散：

1.  **快取結構**：
    鍵為 `(Operator_CAID, Input_Spectral_Signature)`，值為 `(Fuel_Consumed, Result_Entropy, Timestamp)`。

2.  **熵檢查**：
    若對同一輸入的後續觀測發現 `Result_Entropy` 未遞減（即未收斂至更精確的狀態），且燃料持續消耗，則判定為「量子發散 (Quantum Divergence)」並標記為 `#divergent`。

3.  **全域逃逸 (Global Escape Hatch)**：
    即使發散偵測演算法本身陷入循環（如快取無限增長），`%timeout` 參數作為最後防線確保觀測必將終止。

### 3.2 階躍式驗證 (Leaping Verification)

對於涉及複雜遞迴的形態（如 Y-Combinator 或遞迴類型定義），我們採用**階躍式驗證**：

*   **基底躍遷 (Base Leap)**：驗證器嘗試在不展開遞迴的情況下，驗證最外層的型別約束。
*   **歸納躍遷 (Inductive Leap)**：假設遞迴體在第 $k$ 層滿足性質 $P$，驗證第 $k+1$ 層是否保持 $P$。
*   **錯誤隔離**：若階躍失敗，驗證器將標記最小的「不信任邊界 (Distrust Boundary)」，讓開發者知道從哪一層開始需要人工審查。

---

## 4. 自我演化的自指保護 (SPEC_17)

形式化驗證面臨一個根本性的自指問題：**「我們如何用被驗證的規格來驗證規格本身？」**

### 4.1 層級宇宙 (Universe Levels) 與 Tarski 斷層

為了解決這個循環，我們採用與 Lean 4 類似的**層級理論 (Universe Levels)**：

*   **驗證器 (Verifier)** 位於 Layer $N$。
*   **被驗證的規格 (Specification)** 位於 Layer $N-1$。
*   **絕對起點**：Layer 0 是數學核心，它基於 Solèr 定理的元數學證明，無需自我驗證。

這創造了一個**塔斯基斷層 (Tarski Gap)**：規格書無法完全描述其自身的驗證過程，但我們可以建立一個「足夠接近」的相對一致性證明。

### 4.2 核心凍結 (Core Freezing) 與社會共識

Layer 0 數學核心（正交模格公設、EML 算子定義）被視為**永久凍結 (Permafrost)**：

*   **語義不變性**：一旦發布，Layer 0 的定義不允許任何破壞向後相容性的修改。
*   **社會驗證**：Layer 0 的正確性不僅依賴機器證明，也依賴數學社群對 Solèr 定理與 Bohrification 的同行評審共識。
*   **分層信任**：使用者可以選擇信任到 Layer $N$ 的不同深度。對於高風險應用（如金融合約），可能要求驗證到 Layer 1；對於一般腳本，信任 Layer 2/3 的 TLA+ 模型檢驗就足夠。

---

## 5. 終極目標：幾何完整性證明 (CIP) 與 ZK 整合

`n/` 形式化驗證的終極目標是建立 **幾何完整性證明 (Geometric Integrity Proofs, GIP)**：

### 5.1 CAID-連結證明 (CAID-linked Proofs)

每一個 CAID（內容定址標識符）都將伴隨一個不可變的幾何證明物件，包含：
*   **類型證書**：證明該 CAID 的內容滿足其宣稱的型別約束。
*   **效果證書**：證明該 CAID 的副作用標籤 (`%effect`) 正確無誤。
*   **收斂證書**：證明該 CAID 在給定視界參數下必定收斂（或標記為 `#divergent`）。

### 5.2 零知識語義驗證 (ZK-Semantic Verification)

未來，我們計劃整合 **ZK-STARK** 技術：
*   **隱私保護驗證**：允許證明者證明「我擁有一個滿足型別 $T$ 的值」，而無需透露該值的具體內容。
*   **計算壓縮**：將長時間的 Lattice 收斂過程壓縮為簡潔的證明，讓輕量級客戶端只需驗證 CAID 與其附帶的 ZK 證明，無需重新執行整個收斂過程。
*   **跨鏈語義橋**：使 `n/` 的內容定址宇宙能與其他區塊鏈或分散式系統進行語義互操作，同時保持 CAID 的完整性。

---

## 6. GPP STARK 電路設計 (Geometric Probability Proofs)

**GPP (Geometric Probability Proof)** 是防禦 **[SPEC_15](./SPEC_15_Anti_Patterns.md)** §7 定義的譜女巫攻擊的核心機制。本節定義 GPP 的具體 STARK 算術化電路設計。

### 6.1 證明目標

證明者聲稱：「我持有一個子空間投影算子 $P$，其譜特徵為 $S$，且質量 $m = \text{Tr}(P)$」。

驗證者無需下載完整投影算子，只需驗證一個簡潔的 STARK 證明即可確認：
1.  $P$ 是合法的投影算子（$P^2 = P$，$P^\dagger = P$）。
2.  $P$ 的跡確實等於聲稱的 $m$。
3.  $P$ 的譜特徵確實匹配承諾的 $S$。

### 6.2 算術化電路 (Arithmetic Circuit)

將投影算子的驗證轉化為有限域 $\mathbb{F}_p$ 上的多項式約束：

```
Circuit GPP_Verify {
    ;; 公開輸入 (Public Inputs)
    pub spectrum_commitment: Field[N],  ;; 譜特徵的 Merkle 根
    pub claimed_mass:        Field,      ;; 聲稱的質量 m
    
    ;; 私有見證 (Private Witness)
    wit projection_matrix:   Field[D][D], ;; 投影算子 P (D×D 矩陣)
    wit eigenvalues:         Field[D],    ;; 特徵值列表 (0 或 1)
    wit eigenvectors:        Field[D][D], ;; 特徵向量基底
    
    ;; 約束 1: P^2 = P (冪等性)
    constraint idempotent: {
        forall i, j in 0..D-1:
            sum_k(P[i][k] * P[k][j]) == P[i][j]
    }
    
    ;; 約束 2: P 對稱 (自伴性，實數域上等價於厄米性)
    constraint hermitian: {
        forall i, j in 0..D-1:
            P[i][j] == P[j][i]
    }
    
    ;; 約束 3: 特徵值為 0 或 1
    constraint binary_eigenvalues: {
        forall i in 0..D-1:
            eigenvalues[i] * (eigenvalues[i] - 1) == 0
    }
    
    ;; 約束 4: 跡的計算正確
    constraint trace_correct: {
        sum_i(P[i][i]) == claimed_mass
    }
    
    ;; 約束 5: 譜特徵承諾正確 (Merkle 驗證)
    constraint spectrum_commitment_valid: {
        merkle_root(eigenvalues) == spectrum_commitment
    }
}
```

### 6.2.1 複數運算的算術化 (Complex Arithmetic Arithmetization)

STARK 電路運作在有限域 $\mathbb{F}_p$（如 Goldilocks 素數 $p = 2^{64} - 2^{32} + 1$）上，然而投影算子 $P$ 及其特徵值是**複數 (Complex Numbers)** $\mathbb{C}$。

為了解決這個語義裂隙，GPP 採用**實部/虛部雙軌定點數表示 (Dual-Track Fixed-Point Representation)**：

#### 複數編碼

| 數學物件 | 編碼方式 | $\mathbb{F}_p$ 表示 |
| :--- | :--- | :--- |
| 複數 $z = a + bi$ | 分解為 $(a, b)$ | `(Field(a_real), Field(b_imag))` |
| 矩陣元素 $P_{ij}$ | $P_{ij} = \alpha_{ij} + \beta_{ij} i$ | 獨立儲存實部與虛部 |

#### 電路約束擴展

將複數運算轉換為實部/虛部運算：

1. **冪等性** ($P^2 = P$)：
   - 實部約束: $(P_{real}^2 - P_{imag}^2) = P_{real}$
   - 虛部約束: $(2 \cdot P_{real} \cdot P_{imag}) = P_{imag}$

2. **自伴性** ($P^\dagger = P$，即共軛轉置等於自身)：
   - 實部對稱: $P_{ij}^{real} = P_{ji}^{real}$
   - 虛部反對稱: $P_{ij}^{imag} = -P_{ji}^{imag}$

3. **特徵值** (0 或 1)：
   - 複數特徵值實際上僅有 0 或 1（投影算子特徵值必須實數）
   - 虛部約束: $\forall i, eigenvalues[i]_{imag} = 0$
   - 實部約束: $\lambda_{real} \cdot (\lambda_{real} - 1) = 0$

4. **跡的計算**：
   - 僅需實部求和: $m = \sum_{i} P_{ii}^{real}$
   - 虛部跡必須為 0

#### 定點數精度建議

採用 **128-bit 定點數表示**（見 **[REAL_03](./REAL_03_CAID_Protocol.md)** §3.1 的精度規範）：
- 高 64-bit: 整數部分
- 低 64-bit: 小數部分（精度 $2^{-64}$）
- 範圍: $[-2^{63}, 2^{63} - 2^{-64}]$

此設計確保了在有限域上對連續幾何語義的精確逼近。

---

### 6.3 STARK 參數建議

| 參數 | 建議值 | 說明 |
| :--- | :--- | :--- |
| **Field** | $\mathbb{F}_p$, $p = 2^{64} - 2^{32} + 1$ | Goldilocks 素數，64-bit 架構友好 |
| **D (維度)** | 256 | 投影算子矩陣維度（對應 8-bit 譜解析度） |
| **Security Level** | 128 bits | 抗碰撞與偽造強度 |
| **Proof Size** | ~50-100 KB | 壓縮後的證明大小 |
| **Verification Time** | ~10-50 ms | 客戶端驗證時間 |

### 6.4 證明生成流程

```
Prover (節點):
    1. 載入本地投影算子 P
    2. 計算 P 的特徵值分解 (eigenvalues, eigenvectors)
    3. 計算譜承諾: commitment = MerkleRoot(eigenvalues)
    4. 建構 GPP_Verify 電路的 witness
    5. 執行 STARK 證明生成算法
    6. 輸出: (proof, commitment, mass)

Verifier (查詢節點):
    1. 接收 (proof, commitment, mass)
    2. 執行 STARK 驗證算法
    3. 若驗證通過，將 mass 納入引力路由計算
```

### 6.5 與 REAL_02 的協作

*   **[REAL_02](./REAL_02_Ouroboros_Protocols.md)** §7 定義的 GPP 驗證傳輸層義務，其 Level 2 驗證即為本節定義的 STARK 驗證。
*   為了相容資源受限設備，證明生成可由「幾何預言機 (Geometric Oracle)」代為執行（見 **[APP_05](./APP_05_LADD_Global_Logic_Lattice.md)** §6）。

### 6.6 開放問題

以下問題需要進一步研究才能進入 Phase 4 實作。為每個問題附上初步的潛在解決方向：

1.  **高效特徵值分解**：如何在保持零知識的前提下，高效證明投影算子的特徵值分解正確？
    *   **潛在方向：非決定性見證 (Nondeterministic Witness)**
        由證明者在電路外算好特徵值 $(\lambda_i, \mathbf{v}_i)$，電路內只需驗證 $P\mathbf{v}_i = \lambda_i \mathbf{v}_i$。這將複雜度從 $O(n^3)$ 的分解降至 $O(n^2)$ 的矩陣-向量乘法。
    *   **驗證隨機抽樣**：驗證者挑選 $k$ 個隨機座標驗證約束，確保證明者沒有偽造整個特徵值集合。

2.  **動態維度**：如何處理不同維度的投影算子（固定 D=256 可能不適用所有場景）？
    *   **潛在方向：分箱策略 (Binning)**
        定義梯級化的固定維度（16, 64, 256, 1024...）。較小的子空間用零填充至最近的梯級，較大的拆解為多個區塊。
    *   **電路組合技術**：使用遞迴或聚合 STARK，將不同維度的證明組合成單一證明。

3.  **聚合證明**：能否使用遞迴 STARK 將多個 GPP 證明聚合為單一證明，降低驗證開銷？
    *   **潛在方向：遞迴證明樹**
        每個 CAID 的 GPP 是葉節點。中間節點的證明驗證其所有子節點的證明。根節點的證明代表整個子空間樹。
    *   **批次驗證**：當節點一次廣告多個服務時，使用 KZG-based 多項式承諾進行批次驗證，而非逐個檢查。

---

## 7. 實施路線圖：四階段漸進式驗證

為了避免「驗證癱瘓 (Verification Paralysis)」，我們採取漸進式策略：

| 階段 | 目標 | 工具 | 預估時間 |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Layer 0 核心公設 | Lean 4 | 6 個月 |
| **Phase 2** | 投影層正確性 | Isabelle/HOL | 12 個月 |
| **Phase 3** | 運行時狀態機 | TLA+ | 6 個月 |
| **Phase 4** | 整合與 ZK 化 | 自定義 | 12 個月 |

*註：時間預估為單一全職研究團隊的概略估計，實際進度可能因發現新的理論挑戰而調整。*

---

## 8. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_01](./SPEC_01_Foundation_and_Lattice.md)** | 正交模格是驗證的基礎，定義了 Layer 0 的公設。 |
| **[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** | 譜單調性是不動點計算與發散偵測的理論基礎。 |
| **[SPEC_15](./SPEC_15_Anti_Patterns.md)** | GPP 證明是防禦 OODP 安全反模式的核心機制。 |
| **[REAL_02](./REAL_02_Ouroboros_Protocols.md)** | GPP 驗證的傳輸層義務與信任分級。 |
| **[REAL_03](./REAL_03_CAID_Protocol.md)** | 討論 CAID 譜指紋的物理編碼與可驗證性。 |
| **[APP_04](./APP_04_Mathematical_Foundations.md)** | Solèr 定理與 Bohrification 的詳細數學背景。 |
| **[APP_05](./APP_05_LADD_Global_Logic_Lattice.md)** | GPP 證明的應用場景與幾何預言機協作。 |
| **[GUIDE_02](./GUIDE_02_Engine_Optimization.md)** | 啟發式發散偵測的實作指南與效能優化。
