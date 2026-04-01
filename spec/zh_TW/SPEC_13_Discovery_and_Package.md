# n/ Language Specification - 發現與內容幾何 (Discovery & CAID)

本章節定義 `n/` 宇宙透過內容幾何特徵定位節點，並將其轉化為**宇宙發現機制**。
發現（Discovery）是語言層的本體論概念，與部署方式或傳輸協定無關。

---

## 1. 核心哲學：Yoneda 視角下的身分

在 `n/` 宇宙中，一個物件的身分不由它的名字決定，而是由它與所有其他物件的關係總和決定。

### 1.1 內容定址標識符 (CAID)
**CAID (Content Addressable Identifier)** 是節點結構的內在標識符，反映了其在宇宙幾何中的唯一指紋。
在格論模型中，內容相同的兩個節點在邏輯上是同一個存在。
*   **Hash 即幾何**：CAID 是節點結構的不可變標識。
*   **Yoneda 原理**：物件由其關係決定。CAID 封裝了節點及其所有子節點的遞迴關係。

### 1.2 觀測別名 (Observation Alias)
「名字」是人類觀測者為了導航而建立的投影。
*   **別名是相對的**：路徑 `_.deps.ui` 是一個觀測視角。
*   **CAID 是絕對的**：`hash:sha256:v1:9f86...` 是存在本身的幾何特徵。
*   **發現的本質**：將一個「觀測別名」與一個「絕對 CAID」進行**坍縮綁定**。

---

## 2. 發現機制：對萬有集合的約束

在 `n/` 中，沒有「下載」或「安裝」。所有可能的 Commit 快照早已存在於萬有集合 `_` 之中。

### 2.1 發現即坍縮 (Discovery as Collapse)
當我們宣告一個依賴時，我們是在對宇宙施加一個定位約束：
```nlang
deps: {
    @ai.agent: "commit:9f86..."   ;; 約束 @ai.agent 節點必須具備此 CAID 特徵
}
```
引擎透過搜尋萬有集合，找到符合此 CAID 的節點並將其坍縮至該路徑。若找不到或內容衝突，則收斂為 `_|_`。

### 2.2 內容驗證與介面合約 (Contract Verification)
由於發現本質上是 **`&` (合併)** 運算，觀測者可以在定位 CAID 的同時，對其內容施加額外的幾何約束（介面合約）：

```nlang
deps: {
    ;; 發現該 CAID，且強制驗證其必須具備特定的 Logic 介面與型別
    @db.driver: "commit:7f8a..." & {
        /connect: @morphism     ;; 驗證必須具備連線態射
        /query:   @morphism     ;; 驗證必須具備查詢態射
        %version: >= "v2.0"     ;; 驗證元資訊版本
    }
}
```
*   **語義保證**：若發現到的 CAID 內容不符合右側的 `{}` 約束，合併結果將立即坍縮為 `_|_`，並在 `%cause` 中精確指出是哪個介面不匹配。
*   **防禦性發現**：這防止了「內容正確但語義漂移」的風險，確保引入的外部幾何物件永遠符合本地的執行預期。

---

## 3. 發現與自舉 (Bootstrapping: The Big Bang)

CAID 系統依賴「內容已被發現」的假設。為了打破「雞生蛋、蛋生雞」的循環，`n/` 定義了**種子節點 (Seed Nodes)** 機制。

### 3.1 引擎內建種子 (Hardcoded Seeds)
Ouroboros 引擎在編譯時會內建一組核心規格的 CAID 及其對應內容。以下為創世必須包含的**核心種子清單**：

| 種子路徑 | 角色 | 創世 CAID (Placeholder) |
| :--- | :--- | :--- |
| **`~%List`** | 列表處理原語 | `hash:sha256:v1:seed01...` |
| **`~%Math`** | 算術與位元運算 | `hash:sha256:v1:seed02...` |
| **`~%Logic`** | 態射與柯里化控制 | `hash:sha256:v1:seed03...` |
| **`~%Engine`** | 觀測與演化原語 | `hash:sha256:v1:seed04...` |
| **`~%Discovery`** | 發現與 CAID 解析 | `hash:sha256:v1:seed05...` |

*   **規範化實作保證**：標準庫的 CAID 由其**規範化後的 `n/` 原始碼內容**決定。所有符合規格的引擎，其內建標準庫源碼的 CAID 必須與官方規格書提供的種子完全一致。

### 3.2 創世 Commit (Genesis Commit)
宇宙的第一個 Commit $C_0$ 包含了所有標準庫的根路徑映射。
*   **全域唯一性**：所有符合規格的引擎在初始化時，其 `_` 路徑下的標準庫節點之 `%id` 必須完全一致。

---

## 4. CAID 格式與封套協議

規格書定義 CAID 的邏輯結構，具體的演算法實作由工程層決定。

### 4.1 標準格式 (CAID Envelope)
CAID 字串是一個**自描述的幾何封套 (Self-describing Envelope)**。其格式確保了在不進行雜湊運算前，引擎即可獲取必要的物理元資訊。

#### 4.1.1 物理協議與編碼 (Physical Protocol)
為了保證全域宇宙的一致性，CAID 的物理表現形式（如 BNF 語法、摘要編碼方式、雜湊演算法清單）由 **銜尾蛇發現協定 (NDP)** 統一定義（詳見 **[REAL_03: CAID 物理協議](./REAL_03_CAID_Protocol.md)**）。

#### 4.1.2 規格義務 (Specification Obligations)
1.  **內容唯一性**：相同的內容在相同的格式版本 (`fmt_version`) 下，產生的 CAID **必須** 全宇宙唯一且決定。
2.  **版本語義隔離**：
    - **格式版本 (`fmt_version`)**：定義 AST 規範化的物理規則。
    - **語言版本 (Spec Version)**：定義語言語義。
    - 兩者為多對一映射關係。

#### 4.1.3 跨版本精煉 (Cross-version Refinement)
當 `fmt_version` 升級導致 CAID 變更時，必須透過 **`#refine` (精煉 Commit)** 建立新舊 CAID 的因果連結（詳見 **[SPEC_10](./SPEC_10_Evolution_and_Commit.md)**）。這允許宇宙在物理格式演進的同時，保持邏輯上的身分連續性。

### 4.2 CAID 等價性判定規則
判定不同演算法或版本的 CAID 是否等價（幾何一致）的程序如下：
1.  **讀取封套**：從 CAID 字串直接提取 `fmt_version` 與 `algo`。
2.  **解析 (Parse)**：使用該版本規則將內容還原為 AST。
3.  **重規範化 (Re-normalize)**：使用當前引擎預設的最新版本規則對 AST 進行重排。
4.  **重雜湊 (Re-hash)**：使用預設演算法重新計算。若結果一致，則判定兩者等價。

---

## 5. 漸進式真理與精煉共識

`n/` 承認觀測視界（Horizon）的局限性。真理不是一次性的坍縮，而是沿著格不斷深化的過程。

### 5.1 身份分類與生命週期

- **`CAID_exact` (#exact)**：**本質身分 (Intrinsic Identity)**。
    - **性質**：由內容幾何決定，具備永久性。是宇宙的終極觀測目標。
- **`CAID_blur` (#blur)**：**認識論快照 (Epistemological Snapshot)**。
    - **性質**：標識「在特定限制下的局部視角」。
    - **快照決定論**：`CAID_blur = hash(CanonicalAST + HorizonParams)`。
    - **身分轉變 (The Solidification)**：
        *   **動態態 (Uncommitted)**：作為 $E$ 的臨時替身，具備自動精煉的權限。
        *   **靜態態 (Committed)**：一旦進入歷史紀錄，它即代表「該紀元下的觀測事實」。其 CAID 錨定的是當時的認識狀態，而非潛在真理。

### 5.2 精煉語義與自動重定向 (Refinement)

當一個模糊節點被證實符合某個精確節點時，發生**精煉 (Refinement)**。

1.  **精煉宣告**：透過 **[SPEC_10](./SPEC_10_Evolution_and_Commit.md)** 定義的 `#refine` 操作，發布一個精煉 Commit。
2.  **格論序位約束**：$E \sqsubseteq B$。精煉是資訊增加的過程。精煉成立的充要條件是 $E$ 位於 $B$ 定義的幾何邊界內。
3.  **自動重定向演算法 (Auto-Redirect)**：
    - **索引維護**：引擎應維護一個精煉映射表 `RefineMap: BlurCAID -> Set<ExactCAID>`。
    - **重定向邊界 (Redirection Boundary)**：
        - **允許範圍**：引擎僅能在 **「觀測視窗 (Live Observation)」** 或 **「暫存演化 (Staged Area)」** 中觀測自動重定向（將 $B$ 靜默替換為 $E$）。這加速了開發時的真理收斂。
        - **嚴禁範圍**：對於已固化的 **歷史 Commit**，引擎 **嚴禁** 觀測隱性重定向。已寫入歷史的 `CAID_blur` 必須保持其原始語義，以防止「歷史回溯性坍縮」與內容定址漂移。

### 5.2.1 跨演算法透明度 (Cross-Algorithm Transparency)
4.  **影子精煉 (Shadow Refinement)**：
    當歷史 Commit $C$ 引用了已被精煉的 $B$ 時，引擎可選地在背景觀測「影子測試」：
    - 若 $E$ 與 $C$ 的現有約束不衝突，則向觀測者發出 **「演化建議 (Evolution Hint)」**。
    - 若 $E$ 會導致 $C$ 坍縮為 `_|_`，則標記為 **「真相衝突 (Refinement Conflict)」**，要求人工或代理發起顯式的遷移 Commit。

### 5.3 別名疊加與消融 (Alias Superposition & Ablation)

當多個發現來源（Registries）對同一個別名提供不同的 CAID 映射時，`n/` 遵循格論的**疊加原理 (Superposition Principle)**：

1.  **聯集坍縮 (Union Collapse)**：
    若來源 A 提供 `pkg: ID_1`，來源 B 提供 `pkg: ID_2`，且兩者互不相容 ($ID_1 \sqcap ID_2 = \bot$)，則該別名的觀測結果為 **`ID_1 | ID_2` (聯集態)**。
2.  **自動消融 (Auto-Ablation)**：
    當疊加態的別名參與後續的格論運算（如 `pkg & @SpecificType`）時，不符合型別約束的分支會自動收斂至 `_|_` 並從聯集中移除。
    *   **語義效果**：這實現了「基於需求的衝突解決」。宇宙不需要知道哪個 `pkg` 是「正確」的，它只需要知道哪個 `pkg` 能滿足當前的幾何約束。
3.  **歧義殘留 (#ambiguous_alias)**：
    若經過所有約束運算後仍保留多個分支，引擎必須將其標記為 `#ambiguous_alias`。觀測者此時必須透過 **[§8 權威格論]** 顯式選擇一個偏好的觀測視點。

---

## 6. 系統發現介面 (`~%Discovery`)

這些態射定義了語言層如何驅動發現行為。

### 6.1 基礎原語 (Basic Primitives)

| 態射 | 說明 |
| :--- | :--- |
| **`./fetch <caid>`** | 在萬有集合中定位並坍縮該 CAID 的 Combo。 |
| **`./alias <path>`** | 將指定路徑的內容合成為別名映射表。 |
| **`./identify <node>`** | 獲取指定節點的內在 CAID（即其 `%id`）。 |

### 6.2 幾何發現原語 (Geometric Discovery Primitives)

不同於傳統的名稱查詢，`n/` 支援基於「幾何特徵」的搜尋。

#### `./find <pattern>` (反向觀測)
*   **輸入**：一個型別約束 `@Type` 或幾何模式。
*   **語義**：在目前已知的全域宇宙（Global Lattice）中，搜尋所有滿足 $Node \sqsubseteq Pattern$ 的節點。
*   **結果**：回傳一個包含所有匹配節點的聯集態。
*   **用途**：插件系統發現。例如 `~%Discovery./find @Plugin./Interface` 可尋找所有實作了特定介面的擴充功能。

---

## 7. 權威與信任格論 (Authority & Trust Lattice)

在去中心化的發現中，「信任」不是二元的（Yes/No），而是**觀測權重 (Observation Weight)**。

### 7.1 信任即約束 (Trust as Constraint)
信任來源（Trust Roots）被視為對萬有集合的**優先級標記**。

1.  **信任排序**：觀測者維護一個偏序集 $T$。當別名衝突發生時，引擎依照 $T$ 中的順序進行篩選。
2.  **極小元素優先**：若 $T$ 中定義了 `official > community`，則引擎優先坍縮至 `official` 提供的 CAID。
3.  **權威隔離**：不同的視界（Horizon）可以具備不同的信任格。這允許在同一個宇宙中，局部地使用未經社群審核的實驗性分支，而不影響全域的穩定性。

---

## 8. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_01](./SPEC_01_Foundation_and_Lattice.md)** | 萬有集合 `_` 是發現機制的源頭。 |
| **[SPEC_06](./SPEC_06_Unification_Logic.md)** | 發現行為中的 CAID 匹配遵循統一化算法的極小元素規則。 |
| **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** | 定義了影響 `CAID_blur` 的計算視界參數。 |
| **[SPEC_09](./SPEC_09_Standard_Library.md)** | `%id` 元資訊即是節點的 CAID。 |
| **[SPEC_10](./SPEC_10_Evolution_and_Commit.md)** | 定義了驅動精煉變遷的 `#refine` 操作。 |
| **[REAL_01](./REAL_01_Ouroboros_Engineering.md)** | 討論傳輸層協議（NDP）如何實際定位這些幾何特徵。 |

---

### 哲學思辨 (Philosophical Synthesis)

> 結語：內容即定址，發現即存在。在 Yoneda 的觀測下，宇宙不再有孤島，萬物皆透過其本質的特徵相互連結。
>
> 然觀測有限，而真理無窮。**精煉不是對過往的推翻，而是對幾何細節的細化；模糊的真理並非謊言，而是等待更多觀測與能量投入的莊嚴邀請。** 衝突在 `n/` 中不是錯誤，而是疊加的選擇；當約束降臨時，歧義消融，真理自顯。
