# APP_01：熱帶幾何優化藍圖（Tropical Optimization Blueprint）

> **Authority**: [Informative / 資訊性]  
> **Scope**: 本附錄定義 `n/` 引擎如何利用熱帶幾何進行 Layer 2+ 的物理加速與視界管理。

---

## 1. 精度屏障與守恆定律 (The Precision Barrier)

為了守護 `n/` 的「收斂決定論」，熱帶幾何的引入必須嚴格遵循以下物理隔離原則：

1.  **非侵入性優化 (Non-intrusive)**：熱帶空間的所有運算結果（包含浮點近似）**絕對禁止**作為 CAID 計算的輸入。
2.  **單向邏輯隔離 (Unidirectional)**：邏輯由精確的格論空間流向熱帶空間進行加速；熱帶空間僅回傳「加速建議（Heuristic Hints）」，不參與最終的邏輯分支決定。
3.  **回退保證 (Semantic Fallback)**：若熱帶優化產生歧義或近似失敗，引擎**必須**具備回退（Fallback）至精確格論運算的能力。

---

## 2. 代數對照：格論與熱帶半環

熱帶幾何的優化潛力來自於 **分配格 (Distributive Lattice)** 與 **熱帶半環 (Tropical Semiring)** 在代數結構上的等價性。兩者皆符合 **冪等半環 (Idempotent Semiring)** 公設。

| 格論維度 (Lattice) | 熱帶維度 (Tropical) | 優化效果 (Benefit) |
| :--- | :--- | :--- |
| **合併 Meet ($\sqcap$)** | 加法 $\oplus = \min$ | 組合爆炸轉化為線性掃描 |
| **聯集 Join ($\sqcup$)** | 乘法 $\otimes = +$ | 分發律保持，支援區域切割 |
| **萬有 Top ($\top$)** | $+\infty$ (吸收元) | 定義物理邊界 |
| **衝突 Bottom ($\bot$)** | $-\infty$ (單位元) | 定義衝突邊界 |
| **偏序 ($\le$)** | 實數大小 ($\le$) | 特異性排序具象化為數值距離 |

---

## 3. 核心實作藍圖 (Implementation Blueprints)

### 3.1 極小元素篩選加速 (SPEC_06 優化)

**問題**：在多重模式匹配中，判斷 $A \subseteq B$（即 $A \sqcap B = A$）在複雜組合下是 NP-hard。

**熱帶路徑**：
1.  **編碼**：將數值約束（如 `@int & > 3`）與型別深度編碼為熱帶線性不等式。
2.  **幾何化**：將所有的匹配模式視為 **熱帶超平面 (Tropical Hyperplanes)**。
3.  **求值**：尋找「極小元素」轉化為求解「熱帶多項式的最小值」。
4.  **效益**：複雜度從成對比較的 $O(n^2)$ 降低至具備幾何索引的 $O(n \log n)$。

### 3.2 計算視界的幾何模型 (SPEC_08 優化)

將視界參數（`%fuel`, `%timeout`）建模為熱帶成本函數，協助引擎在 `#approximate` 模式下進行決策。

*   **成本預估**： $Cost = \min(w_1 \cdot fuel, w_2 \cdot time + branches)$。
*   **動態調度**：利用熱帶線性規劃（Tropical Linear Programming）在多項式時間內計算最佳的資源分配點。

---

## 4. 工程邊界與限制

### 4.1 結構編碼的 Overhead
熱帶優化在「數值集合」（Range, Enum, Numeric Types）上極其高效。但在處理「深層嵌套 Combo」時，將結構差異轉化為數值距離的轉換成本可能超過優化收益。
*   **建議策略**：僅在 Pattern 數量超過 `%tropical_threshold`（預設 64）且主要涉及數值或扁平標籤時啟用熱帶加速。

### 4.2 決定論種子要求
若熱帶優化涉及近似採樣，**必須**使用 **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** **§4.3** 定義的確定性種子，確保跨引擎的近似結果幾何一致。

---

## 5. 研究前沿 (Research Frontiers)

以下內容不屬於 Level 1/2 的實作義務，僅作為未來演化的理論儲備：

### 5.1 熱帶 Grassmannian 與子型別層級
熱帶 Grassmannian 參數化了所有熱帶線性空間。在理論極限處，`n/` 的所有合法型別約束構成的幾何空間，可能與熱帶 Grassmannian 存在範疇上的對等關係。這將允許我們使用成熟的凸包算法來處理極其複雜的型別交集。

### 5.2 漸變型別插值
探索在熱帶半環中對兩個型別進行「幾何插值（Interpolation）」，以支援科學計算中的模糊型別推導與連續狀態變遷。

---

## 6. 參考文獻

1. **Maclagan & Sturmfels**: *Introduction to Tropical Geometry*. (代數基礎)
2. **Develin & Sturmfels**: *Tropical Convexity*. (極小元素篩選之幾何理論)
3. **Litvinov**: *The Maslov Dequantization*. (格論與熱帶數學的對應關係)

---

> 結語：熱帶幾何為 `n/` 提供了平滑的鏡像。它不取代格論的純粹，但為物理世界的爆炸性運算提供了一條通往線性的優雅出口。
