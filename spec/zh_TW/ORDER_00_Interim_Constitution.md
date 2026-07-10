# ORDER_00：臨時治理憲法 (Interim Constitution)

> **Authority**: [Experimental / 臨時治理標準]
> **Epoch**: Pre-Genesis (引導期)
> **Operation Mode**: GitHub-Centric (以 GitHub 為物理實體)

## 1. 創世定義 (Genesis Definitions)

### 1.1 物理創世 (Physical Genesis, $C_0$)
- **日期**：**2026-04-01** (v0.1.0)。
- **點火機制**：由創始人執行官方創世腳本（詳見 `@co-nlang/nlang-tools` 之說明文件）產生首個極簡雜湊。
- **物理載體**：
    1.  **`GENESIS_CAID`**：產生的 CAID 字串將寫入 `@co-nlang/nlang-spec` 根目錄之此檔案中。
    2.  **Git 錨點**：此檔案的創建作為 Initial Commit，將「物理事實」與「文件記錄」於時空奇點合一。
    3.  **引擎驗證義務**：任何符合規格的 `oo` 引擎原型在自舉時，**必須**讀取此檔案並驗證本地計算結果與之相符，作為驗證宇宙物理法則的唯一原點。

> **必要性（為何外部錨點不可省）**：物理創世錨點並非僅為工程便利。身分層對應上同調障礙階梯的 $H^4$／女巫攻擊層；item 21 的 reduction 指出，框架*內部*（symplectic／Pauli 雙線性資料）**不存在** genuine 的 arity-5／$H^4$ 障礙類（ambient degree-4 環 $=\langle q^2\rangle$ 可分解 = family B，無 exotic 不變量）。因此底層真實性無法純由內部格論補齊，**必須**由外部物理錨點（本節 $C_0$）強制。詳見 **[APP_07](./APP_07_The_Obstruction_Ladder.md)** §4（$H^4$ 列）。*(誠實標記：item 21 為 reduction，非已封閉之定理。)*

### 1.2 組織架構 (Repository Ecosystem)
引導期治理分佈於以下 **GitHub 組織 (@co-nlang)** 儲存庫：
*   **`@co-nlang/nlang-spec`**：法典本體（SPEC, REAL, ORDER, GUIDE）。
*   **`@co-nlang/nlang-tools`**：核心工具鏈與 `oo` 引擎實作。
*   **`@co-nlang/rfcs`**：存放正式提案與 **引導演練紀錄 (`drills/`)**。
*   **`@co-nlang/nlang-docs`**：非規格文檔（手冊、教學），由邏輯守護者確保語義一致性。

---

## 2. 核心權威：四人委員會 (The Council of Four)

委員會在引導期作為 **@co-nlang 組織** 的核心維護者（Maintainers）。

### 2.1 席次分配 (Seats)
1.  **邏輯守護者 (SPEC Guardians) x2**：負責 `@co-nlang/nlang-spec` 與 `@co-nlang/nlang-docs` 的內容審核。
2.  **幾何工程師 (REAL Engineers) x2**：負責 `@co-nlang/nlang-tools` 的實作與技術合規性。

### 2.2 創始人角色 (The Founder)
- **物理中樞**：創始人持有 GitHub 組織與儲存庫的最終管理權。
- **守護者否決權 (The Guardian's Veto)**：若提案違反 **[SPEC_00](./SPEC_00_Introduction.md)** 之不變性，創始人有權關閉 PR。行使時需提供邏輯證明，受影響之提案進入 7 天冷卻修正期。

---

## 3. 演化程序 (Evolutionary Process)

### 3.1 物理實施：GitHub PR
- **合併即注入**：在引導期，PR 的合併即代表該語義被注入宇宙。
- **決策優先級**：
    1.  **否決優先**：創始人基於不變性的否決效力最高，不可被任何多數決覆蓋。
    2.  **核心規格變更**：必須獲得 2 位邏輯守護者全體 `Approve`，否則直接否決，無需進行多數決。。
    2.  **一般提案/工程變更**：3/5 委員 `Approve`。

### 3.2 委員會晉升與產生 (v0.5.0+)
- **維護者 (Maintainer) 定義**：
    1.  **實質貢獻者**：累積 3 個以上 Merged PR 者。
    2.  **保薦維護者**：創始人與每位現任委員每屆具備 **1 個保薦名額**，被保薦者不論 PR 數量直接獲取維護者資格與候選人身分。
- **兩階段選舉制度**：
    1.  **初選 (Snapshot)**：若在轉型期一次性重選全體席次且候選人超過 6 位，進行 3 天初選，由得票前 4 名進入決賽。
    2.  **決賽 (Run-off)**：進行 4 天複選，採相對多數決選出新任委員。
    3.  **法定人數防衛**：投票率需達維護者總數之 1/3。若不足則延長 7 天；二次延長後仍不足，則由現任委員會直接裁定。

---

## 4. 治理演練機制 (Simulation Drills)

引導期的核心任務是透過模擬操作來驗證 `oo` 引擎的規格實現度。

### 4.1 演練類別 (Drill Categories)
*   **`#drill_refine`**：測試跨演算法的精煉宣告與自動重定向語義。
*   **`#drill_sign`**：測試治理 Commit 的 Ed25519 簽署與 `%authority` 驗證。
    - **效力聲明**：在引導期（Epoch < 0），`#drill_sign` 產生的簽署僅用於**技術驗證**，不具備法典層級的終效約束力。
*   **`#drill_conflict`**：故意製造語義衝突，測試 `%cause` 結構的精確度。
*   **`#drill_horizon`**：測試計算視界邊界觸發與 `#blur` 狀態的決定論。

### 4.2 演練紀錄
每次演練的執行過程、引擎輸出與 CAID 對齊結果應記錄於 `@co-nlang/rfcs/drills/` 中。演練記錄由委員會多數決確認為『成功』後，方計入條件 3 的達成計數。

---

## 5. 邁向 Epoch 0 (Semantic Genesis)

當以下條件達成時，委員會應啟動 Epoch 0 儀式，發布 **v1.0.0** 並移交權力：

### 5.1 達成條件 (Activation Conditions)
1.  **引擎達標**：核心引擎 `oo` 通過 100% 的 **[REAL_05](./REAL_05_Compliance_and_MVP.md)** **Level 3** 測試與分散式一致性驗證。
2.  **標準庫完備**： **[SPEC_09](./SPEC_09_Standard_Library.md)** 定義的核心代數結構與 `~%System` 態射在社群達成共識。
3.  **演練達標**：成功完成至少 **3 次** 覆蓋所有類別的「全流程治理演練」。
4.  **語義穩定**：Layer 1 規格連續 90 天無破壞性變更 RFC。

### 5.2 啟動程序 (Launch Procedure)
1.  **物理公告**：由委員會共同簽署 Epoch 0 啟動宣告。
2.  **歷史精煉 (The Final Pruning)**：
    - 委員會產出一份 **「創世精煉清單 (Genesis Refinement List)」**，將引導期產生之重要 CAID 映射至 Epoch 0 之創世身分。
    - 此清單將 **硬編碼** 於 `oo v1.0.0` 引擎內，作為所有後續 `%authority` 驗證的幾何原點（即不需驗證其舊簽名）。
3.  **正式治理啟用**：正式將權限移交予 **[ORDER_01](./ORDER_01_Evolution_and_Governance.md)**。

---

## 6. 緊急狀態 (Emergency Procedures)

- **行政授權政策**：委員會成員在引導期應被授予組織管理權限。
- **創始人失能保障**：若創始人連續 **90 天** 未在 GitHub 活躍且無法聯繫，此憲法自動授權委員會依據共識接管組織。
