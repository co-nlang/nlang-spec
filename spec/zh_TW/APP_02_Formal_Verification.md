# APP_02：量子化形式驗證戰略藍圖 (Quantum Formal Verification)

## 0. 兩軌原則：驗證撤入特徵二影子，執行留在複數投影（2026-07-11 修訂）

本章初稿寫於 Paper VI（量子化）視角。論文系列 VII–XXII 完成後，我們知道得更多：
可證明的不變量內容（Maslov／$\beta$、rank-parity、$\omega/q$-Gram、模數）**全數下降到
特徵二的 symplectic 影子** $V=\mathbb{F}_2^{2n}$（SPEC_13 §1.3：symplectic 指紋是 CAID
的數學本體，複數譜只是物理封套）；而連續量（cross-ratio 類）在 $\mathbb{F}_2$ 上退化
（item 21 prior-art 勘定）——**沒有任何安全承載的內容只活在 $\mathbb{C}$ 側**。

由此立兩軌，全章依此重寫：

| 軌 | 域 | 承載 | 性質 |
| :--- | :--- | :--- | :--- |
| **驗證軌（proof-bearing）** | $\mathbb{F}_2$ 位元代數 | ZK 證明、$\omega/q$ 指紋知識證明（§6）、型別/效果/收斂證書 | 精確、無定點數誤差、無 $O(n^3)$ 譜分解；約束皆為 GF(2) 線性代數＋二次式——**ZK-STARK 原生友善** |
| **執行軌（navigation-only）** | $\mathbb{C}$ 幾何投影 | 引力路由、smell search、`phase_diff` 連續距離、**持有聲明**、質量 | 啟發式、允許近似；**永不承載證明義務** |

> **本表 2026-07-28 更正**:驗證軌原列「**身分/反女巫**」。二者皆誤——§6.2 之電路公開
> 輸入不提證明者,故所證為**持有**不是「是誰」;而反女巫按
> **[ORDER_00](./ORDER_00_Prime_Directive.md)** §1.1 之論證無法由框架內部補齊。**持有**
> 因此隨質量一同移入執行軌;留在驗證軌的是那個電路本身,以其**見證**命名。判別表見
> **[REAL_01](./REAL_01_Ouroboros_Engineering.md)** §7.6。

**工程推論**：電路內不再出現複數算術化、128-bit 定點數編碼、特徵值分解（舊 §6 的三大
成本與誤差來源全數退場）。連續幾何的品質問題（數值精度、逼近誤差）自此屬執行軌 QoS，
不屬證明義務。

**命名規則(2026-07-28 新設,規範性)**:兩軌之分若只落在條款而不落在**名字**上,遷移
之後名字會繼續替舊軌背書。故:

> **凡屬執行軌者,不得以「證明 / proof」命名。**

本次修訂對**質量**已正確施行(退位並更名 `mass_hint`),但未及於**持有**——因為持有當時
被稱作「身分幾何」,而「身分」聽起來配得上「證明」。**一個借來的名字使一條已存在的
規則被跳過**,三個月後在 REAL_02 §7 顯影為兩個義務共用一個詞。判別表見
**[REAL_01](./REAL_01_Ouroboros_Engineering.md)** §7.6;完整經過見討論 026。

*誠實標記*：「不變量內容下降到特徵二」對阻礙階梯是定理級（rank-parity、$\beta$、
$N_{\text{anti}}$ 系列；item 21 為 **reduction 非已封閉定理**，與 ORDER_00 §1.1 同樣標注）；
「驗證軌足以承載全部工程證書」是以此為據的**架構裁決**，非定理。

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
- 證明所有 EML 表達式在複數域 $\mathbb{C}$ 上良好定義（除奇異點外）——Layer 0 元數學，
  屬 Lean 證明對象，與 ZK 電路無涉
- 數值精度傳播的誤差上界——**執行軌 QoS**（§0），不再是證明義務
- 驗證 EML 樹至 CAID 的規範化映射之決定論（bn_serial 位元流＝驗證軌對象）

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

ZK-STARK 整合**全數落在驗證軌（§0）**：證明對象是 $\mathbb{F}_2$ 側資料
（$\omega/q$-Gram、bn_serial 位元流、CAID 摘要鏈），不是複數投影。
*   **隱私保護驗證**：證明「我擁有一個滿足型別 $T$ 的值」而不透露值——型別約束
    在位元流上判定，電路為位元代數。
*   **計算壓縮**：將 Lattice 收斂過程壓縮為簡潔證明；輕客戶端驗 CAID＋證明即可，
    無需重放收斂。
*   **跨鏈語義橋**：CAID 宇宙與其他分散式系統的語義互操作。
*   **ω/q 指紋知識證明**（§6）：symplectic 指紋一致性證明——這是驗證軌的旗艦電路。
    **它不是身分證明,亦非反女巫機制**（2026-07-28 更正）：其陳述不提證明者，故所證為
    **持有**而非「是誰」；而女巫層按 **[ORDER_00](./ORDER_00_Prime_Directive.md)** §1.1
    無法由框架內部補齊。見 REAL_01 §7.6 判別表。

---

## 6. ω/q 指紋知識證明電路 (GPP STARK 電路)

> **更名(2026-07-28,§0 命名規則)**:本節電路以其**見證**命名。舊稱「GPP / 幾何機率
> 證明」保留為本電路的歷史縮寫,**但退出協定層**——REAL_02 與 APP_05 不再以 GPP 指稱
> 節點所出示之物(那是**持有聲明**,執行軌)。三個名字三個問題:`node_id`=是誰、
> 簽章=是不是他、本電路=**他能不能拿出承諾所指的幾何資料**。見 REAL_01 §7.6。

**本電路**曾被列為防禦 **[SPEC_15](./SPEC_15_Anti_Patterns.md)** §7 譜女巫攻擊的核心機制。
**該定位已於 2026-07-28 更正**:電路的陳述(§6.1)不提證明者,故一份有效證明**可被任何
持有它的人出示**;而女巫層按 **[ORDER_00](./ORDER_00_Prime_Directive.md)** §1.1 之論證
(框架內部不存在 genuine $H^4$ 障礙)**無法由內部機制補齊**。本電路所證為**持有**,
其協定地位見 REAL_02 §7。
本節電路自 **2026-07-11 起全面改為 $\mathbb{F}_2$ 辛影子電路**（§0 兩軌原則）：證明
對象從「複數投影算子的譜」改為「CAID 的數學本體＝$\omega/q$-Gram」（SPEC_13 §1.3）。
舊版複數電路（定點數雙軌編碼、特徵值分解見證）全數退場，存檔於 git 歷史。

### 6.1 證明目標

證明者聲稱：「我持有子空間資料 $W\subseteq\mathbb{F}_2^{2n}$（基底 $x_1\ldots x_k$）
與 quadratic refinement $q$，其 **$\omega/q$-Gram 與公開承諾的 symplectic 指紋一致**」。

驗證者只需驗 STARK 證明即可確認：
1.  見證是合法的 $\mathbb{F}_2$ 向量資料（booleanity）。
2.  $\text{Gram}_\omega[i][j] = \omega(x_i, x_j)$ 逐項正確（交換性資料）。
3.  $q$ 滿足 quadratic refinement 定律 $q(x\oplus y)=q(x)+q(y)+\omega(x,y)$（抽樣驗證）。
4.  指紋承諾 $= \text{Hash}(\text{Gram}_\omega \,\|\, q)$。

**質量退位**：舊版的 $m=\text{Tr}(P)$ 譜質量證明**退出證明範圍**——質量/引力自此為
執行軌路由啟發值（§6.6），不承載安全性。女巫防禦改由 (a) 本節指紋一致性證明 ＋
(b) 外部物理錨點（ORDER_00 §1.1；框架內部不存在 genuine $H^4$ 障礙——item 21
reduction，誠實標記同彼處）承擔。

### 6.2 算術化電路（$\mathbb{F}_2$ 位元代數）

```
Circuit GPP_Verify_F2 {
    ;; 公開輸入 (Public Inputs)
    pub fingerprint_commitment: Digest,   ;; Hash(Gram_ω ‖ q)
    pub n: usize, k: usize,               ;; 環境維度 2n、子空間秩 k

    ;; 私有見證 (Private Witness)
    wit X: Bit[k][2n],                    ;; 基底向量（每列一個 x_i）
    wit Q: Bit[k],                        ;; q(x_i) 值
    wit G: Bit[k][k],                     ;; 宣稱的 Gram_ω

    ;; 約束 1: booleanity（大素域嵌入時才需要；二元域原生免費）
    constraint boolean: forall b in X∪Q∪G: b·(b−1) == 0

    ;; 約束 2: ω 正確——標準 symplectic 形式
    ;;   ω(x,y) = Σ_{t<n} ( x[2t]·y[2t+1] + x[2t+1]·y[2t] )   (mod 2)
    constraint gram_omega: forall i≤j: G[i][j] == ω(X[i], X[j]) ∧ G[i][j] == G[j][i]
    ;; char 2 之下 ω 對稱＝反對稱；對角恆 0（alternating）
    constraint alternating: forall i: G[i][i] == 0

    ;; 約束 3: quadratic refinement 定律（Fiat–Shamir 抽樣 r 輪）
    ;;   對隨機 S ⊆ {1..k}: q(⊕_{i∈S} x_i) == Σ_{i∈S} Q[i] + Σ_{i<j∈S} G[i][j]
    constraint q_law: sampled r rounds

    ;; 約束 4: 承諾正確
    constraint commitment: Hash(G ‖ Q) == fingerprint_commitment
}
```

全部約束為 GF(2) 上**次數 ≤ 2** 的多項式——沒有定點數、沒有特徵值、沒有譜列表的
Merkle 化。`q_law` 抽樣輪數 $r$ 由 soundness 目標決定（每輪逃逸機率 $\le 1/2$）。

### 6.3 域的選擇（取代舊「複數算術化」節）

| 方案 | 說明 | 適用 |
| :--- | :--- | :--- |
| **binary-tower STARK**（建議） | 位元原生（$\mathbb{F}_{2^k}$ 塔式域）：XOR＝加法、booleanity 免費 | 首選；約束次數最低 |
| 大素域位元嵌入 | Goldilocks 等；每位元付 $b(b-1)=0$ 約束 | 過渡方案（工具鏈成熟度考量） |

兩案皆無精度議題：$\mathbb{F}_2$ 資料在任何域中都精確表示。舊版的 128-bit 定點數
雙軌編碼**廢止**——其唯一用途是逼近 $\mathbb{C}$，而 $\mathbb{C}$ 已退出證明範圍（§0）。

### 6.4 STARK 參數（$\mathbb{F}_2$ 電路）

| 參數 | 建議值 | 對照舊版（複數電路） |
| :--- | :--- | :--- |
| 見證規模 | $k\cdot 2n + k + k^2$ bits（$n\approx 3$–$8$、$k\le 2n$ ⇒ **數百 bit 級**） | $D{=}256$ 複矩陣 ＝ $2\times256^2$ 個 128-bit 定點數（~16 MB 級） |
| 約束次數 | $\le 2$（GF(2) 二次式） | 矩陣冪等性＝高次 |
| Security Level | 128 bits | 同 |
| Proof Size | ~10–50 KB | ~50–100 KB |
| Verification Time | ~1–10 ms | ~10–50 ms |

*（數量級估計；binary-field STARK 工具鏈選定後校準。）*

### 6.5 證明生成流程

```
Prover (節點):
    1. 取子空間基底 X ⊆ F₂^{2n} 與 q 值（直接來自 stabilizer 資料——無須分解任何東西）
    2. 計算 Gram_ω（O(k²·n) 位元運算）與承諾 Hash(G ‖ Q)
    3. 建構 witness、執行 STARK 證明生成
    4. 輸出: (proof, fingerprint_commitment)

Verifier (查詢節點):
    1. 驗 STARK（毫秒級）
    2. 通過 ⇒ 接受該節點**持有**與承諾一致的幾何資料〔2026-07-28：原作「接受該節點的『身分幾何』」——電路不提證明者，證不到「是誰」〕；質量聲稱另按 §6.6 處理（不入證明）
```

### 6.6 與執行軌的介面（含 REAL_02 協作）

*   **[REAL_02](./REAL_02_Ouroboros_Protocols.md)** §7 的 GPP 驗證傳輸層義務，其 Level 2
    驗證即本節 $\mathbb{F}_2$ STARK。
*   **引力/質量（執行軌）**：路由所需的質量聲稱**不再附譜證明**——它是執行軌啟發值。
    節點可謊報質量，但謊報只影響路由優先序（smell search 的連續重力），**不影響身分
    與內容真實性**（由指紋證明＋CAID 內容定址＋外部錨點把守）。惡意路由誘導的防禦
    維持 SPEC_15 反模式機制（黑名單、tiebreaker、hop 預算——引擎已實作）。
*   **封套一致性**：CAID 物理封套暫為複數譜（REAL_03），數學本體為 $\omega/q$
    （SPEC_13 §1.3）；兩者的綁定見 §6.7 問題 1。
*   資源受限設備仍可由幾何預言機代產證明（**[APP_05](./APP_05_LADD_Global_Logic_Lattice.md)** §6）
    ——$\mathbb{F}_2$ 電路的見證僅數百 bit，此需求已大幅下降。

### 6.7 開放問題（兩軌撤退後重排）

1.  **封套 ↔ 本體綁定**：複數譜封套（REAL_03 §3.2）與 $\omega/q$ 指紋是同一物的兩層
    （SPEC_13 §1.3），但物理格式尚未攜帶 $\omega/q$ 摘要——「封套沒有說謊」目前缺
    電路。**方向**：fmt v3 時將 symplectic 指紋納入 CAID 物理封套（雙承諾），或提供
    封套→本體的推導電路。此即 CAID v2 symplectic fingerprint 工程（linter Tier 2 的
    同一前提，SPEC_13 §1.3）的規格接口。
2.  **聚合證明**：遞迴 STARK 將多個 GPP 聚成單證明（證明樹／批次承諾）。$\mathbb{F}_2$
    電路使葉證明縮小，聚合壓力較舊版已低。
3.  **質量退位的經濟面**：質量不再可證後，女巫成本模型從「偽造譜」變為「偽造身分
    幾何＋外部錨點」；SPEC_15 側需重新量化攻擊成本（規格 TODO，非電路問題）。

*（舊問題 1「高效特徵值分解」**隨兩軌撤退整題消滅**——$\mathbb{F}_2$ 電路無譜分解；
舊問題 2「動態維度」降級為參數選擇——$k$、$n$ 是小整數，分箱不再必要。）*

---

## 7. 實施路線圖：四階段漸進式驗證

為了避免「驗證癱瘓 (Verification Paralysis)」，我們採取漸進式策略：

| 階段 | 目標 | 工具 | 預估時間 |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Layer 0 核心公設 | Lean 4 | 6 個月 |
| **Phase 2** | 投影層正確性 | Isabelle/HOL | 12 個月 |
| **Phase 3** | 運行時狀態機 | TLA+ | 6 個月 |
| **Phase 4** | 整合與 ZK 化（$\mathbb{F}_2$ 電路，§6） | binary-field STARK | 12 個月 → **預期下修**（兩軌撤退消滅了複數算術化與譜分解兩大工程，§6.4 對照表） |

*註：時間預估為單一全職研究團隊的概略估計，實際進度可能因發現新的理論挑戰而調整。*

---

## 8. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_01](./SPEC_01_Foundation_and_Lattice.md)** | 正交模格是驗證的基礎，定義了 Layer 0 的公設。 |
| **[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** | 譜單調性是不動點計算與發散偵測的理論基礎。 |
| **[SPEC_13](./SPEC_13_Ouroboros_Discovery_Protocol.md)** §1.3 | **驗證軌的錨**：CAID 數學本體＝$\omega/q$-Gram（char-2 影子）；§6 電路的證明對象。 |
| **[SPEC_15](./SPEC_15_Anti_Patterns.md)** | GPP 證明是防禦 OODP 安全反模式的核心機制；質量退位後的攻擊成本重估＝該章 TODO。 |
| **[REAL_02](./REAL_02_Ouroboros_Protocols.md)** | GPP 驗證的傳輸層義務與信任分級。 |
| **[REAL_03](./REAL_03_CAID_Protocol.md)** | CAID 複數譜**封套**的物理編碼（執行軌）；封套↔本體綁定見 §6.7。 |
| **[APP_04](./APP_04_Mathematical_Foundations.md)** | Solèr 定理與 Bohrification 的詳細數學背景。 |
| **[APP_07](./APP_07_The_Obstruction_Ladder.md)** §4 | $H^4$／女巫層：內部無 genuine 障礙 ⟹ 外部錨點必要性（§6.1 質量退位的階梯依據）。 |
| **[APP_05](./APP_05_LADD_Global_Logic_Lattice.md)** | GPP 證明的應用場景與幾何預言機協作。 |
| **[GUIDE_02](./GUIDE_02_Engine_Optimization.md)** | 啟發式發散偵測的實作指南與效能優化。
