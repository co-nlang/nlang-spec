# APP_04：數學基礎 (Mathematical Foundations)

本附錄總結了 `n/` 語言背後的量子化數學架構，詳細說明正交模格論（Orthomodular Lattice Theory）、Hilbert 空間與 Bohrification 如何交織構成宇宙的幾何公設。

---

## 導言：從經典極限到量子實相

`n/` 的核心哲學是將動態的計算行為轉換為靜態的幾何收斂。在重構後的體系中，我們確認：經典的格論只是量子語義在特定觀測條件下的「經典極限」。真正的語義空間是一個由投影算子構成的非交換幾何。

---

## 1. 本體論：Solèr 定理與 Hilbert 空間

`n/` 的 Data 與 Type 本質上是 Hilbert 空間 $\mathcal{H}$ 中的子空間。這一設定並非隨意，而是由 **Solèr 定理** 證明的必然結果。

### 1.1 Solèr 定理的啟示
**定理概要**：若一個正交模格 $\mathcal{L}$ 包含一個無限的正交序列，則 $\mathcal{L}$ 必然同構於某個實數、複數或四元數域上的 Hilbert 空間的子空間格。

*   **複數域的優越性**：為了滿足 EML 算子自舉出的初等函數運算，`n/` 選擇複數域 $\mathbb{C}$ 作為其標準數值基底。
*   **無限維度**：`n/` 的宇宙是無限可分的，這對應了無限維度的 Hilbert 空間 $\mathcal{H}$。

### 1.2 子空間即定義
在 `n/` 中，每一個 Combo 或節點 $A$ 對應一個封閉子空間 $\mathcal{S}_A \subseteq \mathcal{H}$。
*   **交集收斂 (Meet)**：$A \sqcap B$ 對應子空間的交集 $\mathcal{S}_A \cap \mathcal{S}_B$。
*   **疊加聯集 (Join)**：$A \sqcup B$ 對應子空間的併元 $\mathcal{S}_A \oplus \mathcal{S}_B$。

---

## 2. 認識論：Bohrification 與 Sheaf Topos

根據 **Kochen-Specker 定理**，不存在一個「上帝視角」能同時賦予所有量子觀測量確定的真值。因此，`n/` 的觀測模型採用了 **Bohrification** 框架。

### 2.1 交換視角偏序集
定義 $\mathcal{C}(\mathcal{A})$ 為非交換代數 $\mathcal{A}$ 的所有交換子代數構成的偏序集。
*   **觀測視角**：每一個節點 $C \in \mathcal{C}(\mathcal{A})$ 代表一個觀測者的「交換視角（Perspective）」。
*   **經典投影**：當觀測者位於視角 $C$ 時，量子本體被投影為一個經典的分配格。

### 2.2 Sheaf Topos 內的內在邏輯
`n/` 的邏輯實質上是建立在 $\mathcal{C}(\mathcal{A})$ 之上的 **Sheaf Topos** 的內在邏輯。
*   **Heyting 代數**：在 Sheaf Topos 中，排中律不必然成立。這完美解釋了為什麼 `#blur`（不完全觀測）是系統的本質屬性，而非暫時的工程狀態。
*   **局部截面 (Local Section)**：CAID 被定義為該 Sheaf 在局部覆蓋下的截面。

### 2.3 Čech 神經 (Čech Nerve)

Bohrification 的 $\mathcal{C}(\mathcal{A})$ 上可以建構 **Čech 神經 (Čech Nerve)**——一個記錄所有 MASA 交集結構的單純複形 (simplicial complex)：

$$N(\mathcal{U})_n = \{ (C_0, C_1, \dots, C_n) \mid C_0 \cap C_1 \cap \cdots \cap C_n \neq \varnothing \}$$

其中 $\mathcal{U}$ 是 $\mathcal{C}(\mathcal{A})$ 的一個開覆蓋，$C_i$ 是 MASA（交換視角）。

**維度與障礙的對應：**

| 神經維度 | MASA 重疊數 | 對應障礙 | 物理意義 |
|:---:|:---:|:---:|:---|
| 1-單形 (邊) | 2 個 MASA 交集 | $H^1$（幾何相位）| 兩個觀測視角的不一致 |
| 2-單形 (三角形) | 3 個 MASA 交集 | $H^2$（中央擴張）| 三個視角間的循環障礙 |
| 3-單形 (四面體) | 4 個 MASA 交集 | $H^3$（gerbe）| 全局時空拓撲 |
| 4-單形 | 5 個 MASA 交集 | $H^4$（身分拓撲）| 女巫抵抗 |

> **Note**：此表為充分條件而非必要條件。具體障礙維度由系統的實際拓撲決定。例如 Peres-Mermin 方塊的 $H^2$ 障礙來自 4-cycle（1-骨架上的環路），而非 2-單形——這是 $H^n$ 可在低於 $n$ 維的神經上出現的典型案例（詳見 Paper III）。

**統一化邏輯中的應用**（見 SPEC_06 §1.3.1）：引擎的 meet 操作在 Čech 神經上對應於沿交集複形的路徑選擇。$d_1$ 沿邊收斂，$d_2$ 在三角形面上分支，$d_3$ 擴張到四面體體積。

> Čech 神經的完整形式化及其在 L-S 收縮譜序列中的應用，見系列論文《The Cohomological Obstruction Ladder: From Bohrification to Spectral Flow》。

---

## 3. 定址論：投影算子與譜幾何

### 3.1 投影算子 ($P_A$)
每一個子空間 $\mathcal{S}_A$ 唯一對應一個正交投影算子 $P_A$。
*   **包含關係**：$A \sqsubseteq B \iff P_A P_B = P_A$。
*   **幾何指紋**：CAID 是投影算子 $P_A$ 的**譜摘要 (Spectral Summary)**。利用跡（Trace）與特徵譜（Spectrum）的不變性，我們可以在不讀取完整數據的情況下判定引力關係。

### 3.2 譜交錯與格距離
*   **格距離 $d_L(A, B)$**：定義為投影算子間的幾何測度，反映了資訊熵的差異。
*   **譜交錯 (Interlacing)**：提供了幾何包含關係的快速過濾依據。

---

## 4. 計算與加速：熱帶退相干 (Tropical Decoherence)

熱帶幾何在 `n/` 中扮演了「量子到經典」的退化橋樑。

*   **Maslov 去量子化**：透過將經典特徵值問題轉換為熱帶特徵值問題，引擎能以 $O(n \log n)$ 的成本模擬高維空間的引力過濾。
*   **經典極限**：熱帶半環是量子邏輯在失去相位資訊（退相干）後的統計投影，這保證了 `oo` 引擎在工程上的高效性與理論上的自洽性。

---

## 5. 術語對照表：直觀 ↔ 量子 ↔ 數學

本表建立 `n/` 語言的三層表達對應關係：

| **直觀用語**<br>(使用者視角) | **量子/格論術語**<br>(規格書用語) | **數學對應**<br>(嚴謹定義) |
| :--- | :--- | :--- |
| **萬有集合** `_` | Top 元素 | $\top \in \mathcal{L}$ |
| **矛盾/衝突** `_|_` | Bottom 元素 | $\bot \in \mathcal{L}$ (零維子空間) |
| **合併** `&` | Meet / 交集 | $A \sqcap B$ / $\mathcal{S}_A \cap \mathcal{S}_B$ |
| **選擇** `\|` | Join / 聯集 | $A \sqcup B$ / $\mathcal{S}_A \oplus \mathcal{S}_B$ |
| **否定** `!` | 正交補 | $!A = A^\perp$ / $P_{!A} = I - P_A$ |
| **觀測** | Projection | 從潛在到確定的態坍縮過程 |
| **清晰** `#exact` | 確定態 | 特徵值 $v$ 的特徵子空間 |
| **模糊** `#blur` | 不完全觀測 | 局部截面 / 模糊集合 |
| **疊加態** `A \| B` | 聯集態 | 子空間的直和 $\mathcal{S}_A \oplus \mathcal{S}_B$ |
| **內容定址** `%id` | 譜幾何指紋 | 投影算子的跡與特徵譜 |
| **視角** | 交換子代數 | $C \in \mathcal{C}(\mathcal{A})$ |
| **視界邊緣** | 觀測極限 | 燃料耗盡時的近似投影 |
| **收斂** | Convergence | 偏序集的極限運算 |
| **態射** `/func` | 么正變換 | $U: \mathcal{H} \to \mathcal{H}$, $U^*U = I$ |
| **效果** `#io` | 糾纏 | 與環境子空間的張量積 |

### 5.1 符號層級對應

| 符號 | 名稱 | 語義 |
| :--- | :--- | :--- |
| `_` | 萬有 | 所有可能性的總和 (Top) |
| `_\|_` | 虛無 | 邏輯衝突導致的空集 (Bottom) |
| `&` | 合併/相遇 | 同時滿足兩者的最大約束 |
| `\|` | 選擇/聯集 | A 或 B 的可能性疊加 |
| `\|>` | 管道/演化 | 態射的順序組合 |
| `!` | 否定/正交補 | 不包含在 A 中的所有可能 |
| `...` | 展開/解封 | 移除封閉邊界的操作 |
| `<...>` | 結構態 | 幾何本體的中立觀測 |

### 5.2 概念層級對應

**Data (存有)**
- 直觀：「這裡有個值」
- 量子：「子空間的態向量」
- 數學：$v \in \mathcal{S}_A \subseteq \mathcal{H}$

**Type (邊界)**
- 直觀：「只能是這些值」
- 量子：「正交投影算子」
- 數學：$P_A: \mathcal{H} \to \mathcal{S}_A$

**Logic (變換)**
- 直觀：「把 A 變成 B」
- 量子：「么正算子的應用」
- 數學：$U: \mathcal{S}_A \to \mathcal{S}_B$, $\psi \mapsto U\psi$

---

## 6. 與其他章節的關係

| 數學概念 | 規格章節 | 應用場景 |
| :--- | :--- | :--- |
| **正交模格 (Orthomodular)** | **[SPEC_01](./SPEC_01_Foundation_and_Lattice.md)** | 量子邏輯與對合否定 `!`。 |
| **Bohrification** | **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** | 計算視界與 `#blur` 狀態。 |
| **EML 算子** | **[SPEC_09](./SPEC_09_Standard_Library.md)** | 基於複數域 $\mathbb{C}$ 的初等函數自舉。 |
| **投影算子 (Projection)** | **[REAL_03](./REAL_03_CAID_Protocol.md)** | **CAID** 的譜幾何指紋。 |
| **熱帶幾何 (Tropical)** | **[GUIDE_02](./GUIDE_02_Engine_Optimization.md)** | 量子退相干極限下的搜尋加速。 |

---

## 7. 總結：Solèr 與 Bohrification 的銜尾蛇
*   **Solèr 提供了「本體」**：確保了幾何結構能映射至強大的 Hilbert 空間。
*   **Bohrification 提供了「觀測」**：確保了有限觀測者能在非交換宇宙中獲得一致的經典視角。

在 `n/` 的量子化體系下，程式碼不再是指令的集合，而是在 Hilbert 空間中劃分出的子空間，透過觀測者的視角投影，收斂成真理的切面。
