# REAL_01：銜尾蛇工程 (Ouroboros Engineering）

> [!NOTE]: [Standard / 混合規範性]  
> [!NOTE]: 本規範定義 Ouroboros 引擎在物理世界的實作標準、工作區結構與 CLI 行為。

> [!IMPORTANT]
> [!NOTE]：
> - **[Core Requirement]**：為了確保全域邏輯格論的統一與網路連通性，實作者**必須**遵循的規範。其地位等同於法典之延伸。
> - **[Reference Recommendation]**：為了與官方工具鏈相容，**建議**實作者採用的最佳實踐。

本文件是 **[SPEC_10](./SPEC_10_Evolution_and_Commit.md)** 與 **[SPEC_11](./SPEC_11_Reflection_and_Synthesis.md)** 的工程實作配套。

---

## 1. Ouroboros 運行模式與 CLI (oo)

`oo` 是 Ouroboros 引擎的官方參考 CLI 實作。

### 1.1 One-shot 模式 (`oo run`)
```bash
# 基本語法
oo run --observe <path> [--commit] [--format json|n] [--load <file>]
```
- **實作建議**：引擎應在記憶體中建立臨時宇宙，完成收斂後立即釋放。若帶有 `--commit`，則需更新本地 `.oo/` 狀態。

### 1.2 REPL 模式 (`oo repl`)
```bash
# 基本語法
oo repl [--privileged] [--load <file>] [--empty]
```
- **特權模式**：需檢查啟動環境是否具備權限。
- **Auto-commit**：建議預設開啟，以提升互動體驗。

### 1.3 Service 模式 (`oo service`)
```bash
# 基本語法
oo service [--socket <path>] [--host <h>] [--port <p>] [--privileged-token <t>]
```
- **宇宙節點 (Universe Node)**：在此模式下，Ouroboros 不僅是工具，而是一個**語義運算節點**。它承載了一個特定視界內的宇宙狀態，並透過標準協議向全球邏輯格論暴露其「觀測與演化」能力。

---

## 2. Ouroboros Protocol (JSON-RPC 封裝)

雖然規格書定義 Request/Response 為 n/ Combo，但實際傳輸時建議使用 JSON 序列化。RPC 的 `%op` 欄位應直接對應到 **[SPEC_10](./SPEC_10_Evolution_and_Commit.md)** 中定義的系統態射路徑。

### 2.1 Request 序列化範例 (JSON)
```json
{
  "jsonrpc": "2.0",
  "method": "oo.request",
  "params": {
    "%op": "~%Engine./observe",
    "%path": "_.user.profile",
    "%session": "session-id-123"
  },
  "id": 1
}
```

### 2.2 Response 序列化範例 (JSON)
```json
{
  "jsonrpc": "2.0",
  "result": {
    "%status": "#success",
    "%result": { "name": "Alice", "age": 30 },
    "%commit": "sha256:7f8a9b2c..."
  },
  "id": 1
}
```

### 2.3 型別對映表與 IO 狀態處理
為了避免與使用者定義的欄位衝突，特殊的格論極值建議使用特殊的 `$kind` 標籤。

> [!WARNING] **有損傳輸預警**
> JSON 僅作為 `n/` 宇宙在特定時刻的 **物理傳輸快照 (Transport Snapshot)**。
> 由於 JSON 缺乏表達「疊加態 (Union)」與「格論約束 (Constraint)」的能力，當宇宙尚未完全坍縮時，態射至 JSON 的行為將是 **有損的 (Lossy)**。建議僅在節點已收斂為原子或純 Cocoon 時才進行 JSON 導出。

#### 非原子態映射規則：
*   **Pending (待定)**：代表觀測已發起但尚未返回結果（如非同步 IO）。在傳輸層，應映射為 `{"$kind": "pending", "request_id": "..."}`。這與 `_` (Top) 不同，`_` 代表「所有可能性」，而 `pending` 代表「正在確定中的單一可能性」。
*   **Union (聯集)**：映射為 `{"$kind": "union", "branches": [...]}`。

| n/ 型別 | JSON 序列化表示 |
| :--- | :--- |
| `_` (Top) | `{"$kind": "top"}` |
| `_\|_` (Bottom) | `{"$kind": "bottom", "cause": "..."}` |
| `#tag` | `{"$kind": "tag", "name": "tag"}` |
| `p"..."` (Path) | `{"$kind": "path", "value": "..."}` |
| Combo `{}` | JSON Object |
| List `[]` | JSON Array |

---

## 3. 工作區儲存結構 (.oo/)

本節定義 Ouroboros 工作區的儲存規範。實作者應區分「核心必要結構」與「參考佈局」。

### 3.1 核心必要結構 **[Core Requirement]**
為了確保跨實作的內容互操作性，任何符合 `n/` 規範的儲存引擎**必須**實作以下邏輯：
*   **內容定址儲存 (Content-Addressable Storage)**：物件必須以 CAID 為標識存儲於 `objects/` 目錄中。目錄深度與演算法前綴必須對齊 **[REAL_01](./REAL_01_Ouroboros_Engineering.md)**。

### 3.2 參考實作佈局 **[Reference Recommendation]**
為了與 `oo` 官方工具鏈保持 100% 相容，建議實作者採用以下佈局：

```
.oo/
├── objects/        ← [核心] 內容定址存儲
├── refs/
│   ├── heads/      ← 分支指標 (如 main -> hash)
│   └── HEAD        ← 當前活躍指標
├── staged          ← 暫存的演化定義 (n/ 格式)
├── sessions/       ← Service 模式下的工作階段快取
├── config.n        ← 局部環境配置
└── repl_history    ← 交互式命令歷史
```

### 3.3 增量依賴追蹤 (Incremental Dependency Tracking) **[Reference Recommendation]**
為了支援高效的增量收斂，引擎應在記憶體中維護一張依賴圖（Dependency DAG）：

1.  **動態建構**：在「視界優先解析」過程中，每當一個節點引用另一個節點時，建立一條從下游到上游的有向邊。
2.  **循環處理**：若偵測到強連通分量（SCC），且路徑中無態射變換，則依據 **[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** 判定為靜止循環（結果為 `_`）。
3.  **無效化策略**：當一個 Commit 被切換或演化時，僅對 DAG 中受影響的節點標註為「髒 (Dirty)」，在下次觀測時重新收斂。
4.  **存儲建議**：依賴圖屬於運行時狀態，**不建議持久化**。引擎啟動後可從不可變的 Commit 中隨時重建。

---

## 4. 指令對應表 (CLI to System Morphisms)

| CLI 指令 | 對應系統態射 | 說明 |
| :--- | :--- | :--- |
| `oo add` | `~%Engine./evolve` | 將檔案內容注入暫存區。 |
| `oo commit` | `~%repl./commit` | 將暫存區固化為新 Commit。 |
| `oo run --observe` | `~%Engine./observe` | 收斂並輸出目標路徑。 |
| `oo rollback` | `~%repl./rollback` | 移動 HEAD 指標。 |
| `oo branch` | `~%repl./branch` | 建立演化分支。 |

---

## 5. 漸進式採用與嵌入模式 (Incremental Adoption)

`n/` 並非必須全盤取代現有系統。透過 **Ouroboros Service (oo service)**，現有程式碼可以將 `n/` 作為一個**語義插件 (Semantic Plugin)** 來逐步嵌入。

### 5.1 作為 DSL 嵌入現有語言
現有的 C/Rust/Python 程式可以透過標準的 JSON-RPC 呼叫 `oo service`：
1.  **發起觀測 (Observe Request)**：將 `n/` 腳本（定義或規則）發送給引擎。
2.  **接收坍縮結果 (Collapsed Response)**：引擎進行格論收斂，並將結果以 JSON 形式回傳。
3.  **語法對齊**：利用 JSON 的 `{"$kind": "..."}` 標記來處理 `n/` 的特殊極端值（如 Top/Bottom）。

### 5.2 外部函數介面 (FFI) 的實作 **[Core Requirement]**

對於需要極高性能或底層系統調用的場景，實作者可以實作 **[SPEC_09](./SPEC_09_Standard_Library.md)** 定義的 `%external` 態射。

#### 5.2.1 FFI 沙箱與純粹性義務
為了守護 **Invariant 1 (決定論)**，若 FFI 態射被標記為 **`#pure`**，引擎實作者 **必須** 提供具備下列特性的沙箱環境：

1.  **環境隔離 (Env Isolation)**：嚴禁外部程式存取宿主機之環境欄位、硬體識別碼或物理路徑。
2.  **時鐘凍結 (Clock Freezing)**：嚴禁讀取系統物理時間。所有對時間的請求必須回傳固定值（Epoch 0 創世時刻）。
3.  **無狀態保證 (Statelessness)**：外部程式在兩次呼叫之間嚴禁保留任何物理層面的可變狀態。
4.  **確定性熵源 (Deterministic Entropy)**：若外部程式需使用隨機性，引擎必須透過當前路徑的 CAID 衍生出確定性種子（Deterministic Seed）進行注入。

> [!CAUTION] **規格合規警告**
> 若引擎實作環境無法提供上述硬性隔離（例如受限於作業系統權限），則該引擎 **必須** 將所有 FFI 調用強制標記為 **`#io`**。嚴禁在不具備隔離能力的情況下將 FFI 偽裝為 `#pure`，這將導致 CAID 在不同節點間產生分歧，視為嚴重違反規格。

*   **動態載入**：引擎可透過動態連結庫（`.so`, `.dll`）或 WebAssembly（Wasm）加載外部函數實作。
*   **型別安全檢查**：在進入外部程式前，引擎**必須**驗證輸入參數是否滿足態射的型別約束。
*   **隔離與安全**：建議將外部函數運行於獨立的沙箱或線程中，防止其崩潰影響 `n/` 引擎的穩定性。


### 5.3 FFI 型別映射參考
為了保證跨語言呼叫的一致性，建議實作者遵循以下映射標準：

| n/ 型別 | Rust (建議) | C (ABI) | JavaScript |
| :--- | :--- | :--- | :--- |
| **`@int`** | `i64` / `num_bigint` | `int64_t` | `BigInt` |
| **`@float`** | `f64` | `double` | `Number` |
| **`@str`** | `String` / `&str` | `const char*` | `String` |
| **`@list`** | `Vec<Value>` | `Value**` | `Array` |
| **`@combo`** | `IndexMap<String, Value>` | `struct Map*` | `Object` |
| **`_\|_` (Bottom)** | `Err(Cause)` | `NULL` | `undefined` / `Error` |
| **`_` (Top)** | `Value::Top` | `void*` | `null` |


---

## 6. IO 實戰模式 (IO Practice Patterns)

為了讓開發者能編寫實際的應用，建議採用以下「純粹化」模式來包裝外部 IO：

### 6.1 外部 API 抽象化模式
不直接在業務邏輯中呼叫 `~%IO`，而是定義一個「能力 Combo」：

```nlang
;; 1. 定義能力型別 (Boundary)
@UserAPI: {{
    get_user: (id: @str) -> @User | #error
}}

;; 2. 實作外部綁定 (FFI Bridge)
~my_service: @UserAPI & {
    get_user: (id -> ~%IO./http_get "https://api.example.com/user/${id}")
}

;; 3. 業務邏輯保持純粹 (Pure Logic)
/process: (api: @UserAPI, id) ->
    api.get_user(id) |> { ... }
```

### 6.2 快取與固化策略
利用 **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** 定義的 `#cached` 標籤，引擎應自動對冪等的 GET 請求進行 CAID 快取。
*   **工程建議**：在分散式系統中，`oo service` 應維護一個「CAID 到 IO 回應」的映射表，讓重複的外部觀測能在不觸發實際網路請求的情況下直接收斂。

---

## 7. 格式化工具 (oo fmt) 的建議算法 **[Reference Recommendation]**

1. **AST 解析**：將 `.n` 檔案解析為抽象語法樹。
2. **語義縮排**：根據 Combo 嵌套層級增加縮排（建議 4 空格）。
3. **Key 排序**：
   - 優先排列前綴：`%`, `~%`, `~`, `@`, `/`.
   - 最後排列 **Data 欄位 (無前綴)**。
   - 相同類別內依字母排序。
4. **換行規則**：
   - 欄位定義後強制換行。
   - `{` 前保留一個空格，若內部欄位超過 3 個則解開折疊（Unfold）。

> [!TIP]
> [!NOTE]：引擎在進行 `#commit` 前，應自動對 Staged 內容進行 `fmt` 轉換，再進行內容雜湊計算。這對於維護全域 CAID 的唯一性至關重要。

---

## 8. 特權與權限管理 (Privilege & Token Management)

特權操作（如 `~%Engine./pin`）在 Service 模式下必須受到嚴格的安全驗證。

### 8.1 Token 生命週期與格式管理
建議 `oo` 引擎透過工作區配置實作以下權限原語：

*   **Token 格式 (建議)**：採用 `CAID:PrivilegeSet:Signature` 結構。
    - `CAID`: 該 Token 自身的內容識別。
    - `PrivilegeSet`: 權限標籤聯集（如 `#pin | #squash`）。
    - `Signature`: 基於發放者私鑰的加密簽章。
*   **Token 產生**：`oo token generate --expires 15m`
    *   建議預設有效期為 15 分鐘，以降低洩露風險。
*   **Token 撤銷**：`oo token revoke <token-id>`
    *   建立黑名單機制，立即作廢尚未過期的特權憑證。
*   **持久化**：Token 紀錄應存儲於 `.oo/config.n` 的私有區域（Local Home），不應進入宇宙的 Commit 歷史。

### 8.2 安全建議
*   **隔離觀測**：特權工作階段應具備獨立的視界快取，防止特權收斂結果意外污染一般觀測者的快取。
*   **審計日誌 (Audit Log Schema)**：所有特權操作必須記錄於 `.oo/audit.log`，其欄位應包含：
    - `timestamp`: ISO 8601 時間戳。
    - `actor_id`: 進行操作的 Token CAID。
    - `op`: 進行的特權操作型別。
    - `path`: 受影響的宇宙路徑。
    - `status`: #success 或錯誤標籤。


---

## 9. IDE 與符號觀測 (IDE & Symbolic Observation)

為了提升開發者的觀測體驗，建議 `oo-lsp` (Language Server Protocol) 與 IDE 插件實作下列「符號美化 (Symbolic Ligatures)」與「視覺觀測透鏡」功能。

### 9.1 幾何符號坍縮 (Symbolic Collapsing)

當開發者在 IDE 中執行程式碼時，插件可動態將文字符號渲染為其格論的數學原形。這只是顯示層的變換，檔案內容保持不變。IDE 的 Symbolic Ligatures（如把 `_` 渲染成 $\top$）是顯示層變換，不影響 CAID 計算。

| 原始文字 | 建議渲染符號 | 語義 |
| :--- | :---: | :--- |
| `_` | **$\top$** (Top) | 萬有集合 / 所有的可能性 |
| `_\|_` | **$\bot$** (Bottom) | 空集合 / 邏輯衝突 |
| `#_` | **#$\top$** (End) | 序位終點 |
| `#_\|_` | **#$\bot$** (Start) | 序位起點 |
| `->` | **$\to$** | 態射定義 |
| `\|>` | **$\rhd$** | 演化管道 |

### 9.2 視界邊界與語義著色 (Highlighting)

*   **三位一體著色**：根據 **[SPEC_05](./SPEC_05_The_Trinity_Isomorphism.md)**，LSP 應為不同前綴分配具備本體論區隔的顏色。
    *   **`/` (Logic)**：建議使用動態感強烈的顏色（如紫色或藍色）。
    *   **`@` (Type)**：建議使用具備定界感、穩定的顏色（如綠色或青色）。
    *   **`%` (Meta)**：建議使用具備權威感的特殊顏色（如金色或橙色）。
*   **視界隔離預覽**：根據 **[SPEC_14](./SPEC_14_Formal_Grammar.md)** 的 `!field_start` 斷言，動態淡化（Dim）下一個欄位的 Key，以視覺化地呈現表達式的「收斂邊界」。

### 9.3 實時收斂內插 (Inlay Hints)

利用 Ouroboros 的 `~%Engine./observe` 原語，IDE 可在編輯時於行尾顯示該節點的當前坍縮結果。
*   **範例**：`x: /add 1 2` 旁邊顯示 `→ 3`。
*   **型別推導**：若尚未坍縮至原子，則顯示當前收斂到的最窄型別（如 `→ @int`）。

### 9.4 虛空觀測 (Hover Tips)

對於宇宙中尚未約束的「虛空」節點，LSP 應提供深度的哲學與狀態提示：
*   **`_` 懸停**：顯示「此路徑尚未收斂，當前處於萬有集合（Top）狀態，具備無限可能性。」
*   **`_|_` 懸停**：顯示「此處發生邏輯衝突，已坍縮至空集合（Bottom）。」並聯動顯示 `%cause` 診斷資訊。

### 9.5 測試與覆蓋率展望 (oo test)
*   **自動取樣**：`oo test` 可根據態射的輸入型別（如 `@u8`）自動產生邊界測試案例（0, 255, 256）。
*   **空間覆蓋報告**：不僅報告測試通過與否，還應視覺化地展示態射輸入域的「覆蓋地圖」，標示哪些子空間尚未經過觀測驗證。

### 9.6 啟發式型別推導與靜態分析 (Type Inference)
由於 `n/` 的型別亦是動態收斂的 Combo，LSP 應採用啟發式算法（Heuristics）來提供即時回饋：

1.  **局部局部收斂 (Partial Convergence)**：IDE 不應等待全域收斂，而應在有限的 `%fuel` 限制下對當前視界進行「嘗試性坍縮」。
2.  **結構化提示**：若型別尚未坍縮為原子標籤，IDE 應展示其具備的結構特徵（如 `→ { name: @str, ... }`）。
3.  **型別錯誤報告規範**：當偵測到預期收斂為 `_|_` 時，建議以「幾何不相交」的邏輯展示錯誤：
    *   `Expected: @int`
    *   `Found: "string" @str`
    *   `Conflict: @int & @str == _|_`
4.  **邊界判定**：明確區分「語法錯誤」（Layer 1）與「收斂失敗」（Layer 2/3）。

### 9.7 互動式衝突解決流程 (Conflict Resolution UI)
當平行提交觸發 `#conflict` (特別是在 `~%repl.merge_strategy: #strict` 時)，工具鏈（如 `oo` CLI 或 IDE）應提供互動式的衝突解決流程：

1.  **Three-way Diff 視圖**：展示 `Staged` (目前的工作階段)、`Incoming` (晚到的遠端或平行 HEAD) 以及 `Base` (兩者共同的祖先 Commit)。
2.  **語義層級衝突**：與傳統基於純文字的 git merge 不同，`oo` 的衝突解決應基於 AST。若衝突點在於 `a: 1` 與 `a: 2`，工具不應提示行數衝突，而應提示「路徑 `$.a` 在原子層級不相容」。
3.  **解決策略選項**：允許開發者在互動介面中選擇保留本機 (`#favor_staged`)、接受外部 (`#favor_incoming`) 或手動編寫一個新的 Combo 結構來替代衝突節點。

### 9.8 除錯與溯源建議 (Debugging)
為了應對非嚴格錯誤處理帶來的定位難度，建議實作者提供以下工具：
*   **`oo debug --trace <path>`**：當路徑收斂至 `_|_` 時，深度遍歷其 `%cause` 鏈，並以時間軸或邏輯樹的形式展示衝突發生的完整過程。
*   **視覺化衝突點**：在 IDE 中，對於局部收斂至 `_|_` 的節點，建議使用特殊的視覺提示（如紅色波浪線或警告圖示），點擊後可直接跳轉至導致該衝突的原始定義位置。
*   **漸進式收斂提示 (Optimization Hints)**：當觀測觸發 `#incomplete` 或 `%fuel` 消耗超過閾值（如 80%）時，引擎應在診斷資訊中包含優化建議。例如：
    *   *「偵測到深層聯集合併，建議將 ${path} 改為 Cocoon 以縮小搜索空間。」*
    *   *「此路徑觸發了非全序模式匹配，建議重構為更具體的型別約束以啟用熱帶優化。」*

---

## 10. 規範化計費模型 (Standardized Billing Model) **[Core Requirement]**

為了確保跨引擎實作在觸及計算視界邊緣時能產生一致的 `#blur` CAID，所有符合 Ouroboros 規範的引擎**必須**遵循下列最小計費單位（Minimum Billing Units, MBU）。

### 10.1 核心操作計費表

| 操作型別 | 單位消耗 (MBU) | 說明 |
| :--- | :---: | :--- |
| **節點展開 (Node Expansion)** | 1 | 透過路徑訪問並讀取一個 Combo 欄位或原子。 |
| **態射應用 (Morphism App)** | 10 | 執行一次 `/` 態射呼叫（包含參數綁定）。 |
| **格論合併 (Lattice Merge)** | 5 | 執行一次兩個非原子節點的 `&` 或 `\|` 合併運算。 |
| **模式匹配 (Pattern Match)** | 2 | 匹配一個 AST 節點（按匹配路徑深度計費）。 |
| **外部調用 (FFI Call)** | 50+ | 基本消耗 50，其餘依實作提供的複雜度宣告計費。 |

### 10.2 計費不變性
*   **與效能無關**：MBU 描述的是「邏輯步數」而非「物理 CPU 週期」。一個優化良好的引擎可以用 1ms 跑完 1000 MBU，而慢速引擎需要 10ms，但兩者**必須**在消耗相同數額時停止觀測。
*   **遞迴計費**：所有嵌套的操作必須累加計費。
*   **CAID 參與義務**：當產生 `#blur` 狀態時，剩餘的 `%fuel` 數值**不得**納入 CAID 計算（因為它受觀測者起始燃料影響），但所採用的計費模型版本號**必須**納入雜湊。

---

## 11. 物件生存週期與視界清理 (Object Lifecycle & Pruning) **[Reference Recommendation]**

在 `n/` 的內容定址架構中，物理儲存空間的管理基於「可達性 (Reachability)」模型。實作者應提供機制來清理不再具備觀測價值的物理物件。

### 11.1 根集合 (Root Set)

引擎在進行清理操作前，必須識別當前的根集合。任何從根集合可達的 CAID 物件**嚴禁**被刪除。根集合包括：
*   **活躍指標**：`.oo/refs/HEAD` 及其指向的所有 Commit 節點。
*   **命名參照**：所有位於 `.oo/refs/heads/` 與 `.oo/refs/tags/` 的指標。
*   **演化區 (Staged Area)**：目前尚未 commit 但已注入工作區的節點定義。
*   **釘選集合 (Pin Set)**：使用者透過 `oo pin <caid>` 顯式標記為永久保留的物件。

### 11.2 視界清理策略 (Pruning Strategies)

建議引擎實作下列清理等級：

1.  **Session Cleanup**：清理所有已失效的會話（Session）快取與臨時 `#blur` 結果。
2.  **Loose Object Pruning**：清理所有不再被任何 Commit 指向的孤立物件。
3.  **History Truncation (進階)**：
    *   允許使用者將 Commit 歷史截斷至特定深度。
    *   截斷後的舊 Commit 內容被物理刪除，僅保留其 CAID 指紋以維持因果鏈的完整性。若未來需要存取這些內容，引擎應透過 `~%Discovery` 向外尋找（詳見 **[REAL_02](./REAL_02_Ouroboros_Protocols.md)**）。

### 11.3 精煉重定向與空間回收

當一個模糊節點（`#blur`）被精確節點（`Exact`）自動重定向後：
*   引擎應將原本指向 `BlurCAID` 的依賴更新為 `ExactCAID`。
*   若 `BlurCAID` 對應的實體物件已無其他邏輯引用，則其佔用的空間應被標記為可回收。

---

