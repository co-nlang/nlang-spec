# REAL_01：銜尾蛇工程 (Ouroboros Engineering）

> [!NOTE]: [Standard / 混合規範性]  
> [!NOTE]: 本規範定義 Ouroboros 引擎在物理世界的實作標準、工作區結構與 CLI 行為。

本文件將工程實作與 **[APP_04](./APP_04_Mathematical_Foundations.md)** 定義的量子化數學模型對齊，確立物理引擎如何在有限資源下執行子空間投影。

---

## 1. Ouroboros 運行模式與 CLI (oo)

`oo` 是 Ouroboros 引擎的官方參考 CLI 實作。

### 1.1 One-shot 模式 (`oo run`)
```bash
oo run --observe <path> [--commit] [--format json|n] [--load <file>]
```

### 1.2 Service 模式 (`oo service`)
*   **宇宙節點 (Universe Node)**：承載特定視角內的子空間狀態，並透過標準協議暴露「投影與演化」能力。
```bash
oo service [--socket <path>] [--host <h>] [--port <p>] [--privileged-token <t>]
```

---

## 2. Ouroboros Protocol (JSON-RPC 封裝)

`oo service` 啟動的 Service 節點透過 **JSON-RPC 2.0** 協議暴露 API。JSON 僅作為 `n/` 宇宙在特定時刻的 **物理投影快照 (Transport Snapshot)**，而非語義本體。

### 2.1 協議基礎

**傳輸層**：
*   **Unix Domain Socket** (預設): `~/.oo/service.sock`
*   **TCP**: 監聽 `localhost` 或網路介面
*   **WebSocket**: 用於瀏覽器客戶端連接
*   **標準輸入輸出 (stdio)**: 用於 Language Server Protocol (LSP)

**訊息格式**：
```json
{
    "jsonrpc": "2.0",
    "id": 1,                    // 請求 ID，通知可為 null
    "method": "nlang/observe",  // 方法名
    "params": { ... }           // 參數對象
}
```

### 2.2 核心 API 端點

#### `nlang/observe` - 觀測子空間

請求觀測特定路徑的收斂結果。

**Request**:
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "nlang/observe",
    "params": {
        "path": "_.config.port",
        "fuel": 10000,
        "timeout": 5000,
        "strategy": "blur",
        "format": "json"        // "json" | "n" | "canonical"
    }
}
```

**Response**:
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "caid": "hash:sha256:v1:abc123...",
        "value": {"$kind": "data", "val": 8080},
        "fuel_consumed": 150,
        "effect": "#pure",
        "strategy_applied": "blur"
    }
}
```

**Error Response**:
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "error": {
        "code": -32001,
        "message": "Fuel exhausted",
        "data": {
            "cause": "#fuel_exhausted",
            "fuel_requested": 100,
            "fuel_consumed": 100,
            "partial_result": { ... }
        }
    }
}
```

#### `nlang/commit` - 提交演化

將 Staged 區的變更固化為新的 Commit。

**Request**:
```json
{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "nlang/commit",
    "params": {
        "message": "更新端口配置",
        "author": "developer@example.com",
        "parents": ["hash:sha256:v1:parent..."],
        "sign": true,             // 使用 GPG/SSH 簽名
        "allow_conflict": false   // 是否允許提交含有 _|_ 的內容
    }
}
```

**Response**:
```json
{
    "jsonrpc": "2.0",
    "id": 2,
    "result": {
        "commit_caid": "hash:sha256:v1:commit123...",
        "root_caid": "hash:sha256:v1:root456...",
        "timestamp": 1704067200,
        "affected_paths": ["_.config.port", "_.config.host"]
    }
}
```

#### `nlang/query` - 內容查詢

透過 CAID 查詢節點內容（需節點已於本地存在或可從遠端獲取）。

**Request**:
```json
{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "nlang/query",
    "params": {
        "caid": "hash:sha256:v1:abc123...",
        "depth": 3,               // 解析深度，0 僅返回元資訊
        "include_meta": true      // 是否包含 % 欄位
    }
}
```

#### `nlang/morph` - 態射應用

應用特定態射於輸入節點。

**Request**:
```json
{
    "jsonrpc": "2.0",
    "id": 4,
    "method": "nlang/morph",
    "params": {
        "input_caid": "hash:sha256:v1:target...",
        "morphism_caid": "hash:sha256:v1:morph...",
        "args": [
            {"$kind": "number", "val": 42}
        ],
        "fuel": 5000
    }
}
```

#### `nlang/subscribe` / `nlang/unsubscribe` - 訂閱變更

訂閱特定路徑的觀測結果變更（基於 DAG 的響應式更新）。

**Request**:
```json
{
    "jsonrpc": "2.0",
    "id": 5,
    "method": "nlang/subscribe",
    "params": {
        "path": "_.ui.components.*",
        "event_types": ["converged", "conflict", "refined"]
    }
}
```

**Notification** (當路徑變更時推送):
```json
{
    "jsonrpc": "2.0",
    "method": "nlang/notify",
    "params": {
        "subscription_id": "sub123",
        "event": {
            "type": "converged",
            "path": "_.ui.components.header",
            "old_caid": "hash:sha256:v1:old...",
            "new_caid": "hash:sha256:v1:new...",
            "fuel_consumed": 230
        }
    }
}
```

#### `nlang/discover` - LADD 發現

執行格論感知的分散式發現。

**Request**:
```json
{
    "jsonrpc": "2.0",
    "id": 6,
    "method": "nlang/discover",
    "params": {
        "pattern": {
            "$kind": "type_constraint",
            "type": "@Database./Connection"
        },
        "horizon": {
            "max_hops": 3,
            "min_trust": 0.5
        }
    }
}
```

### 2.3 批次與管線請求

**批次請求 (Batch Request)**：
```json
[
    {"jsonrpc": "2.0", "id": 1, "method": "nlang/observe", "params": {...}},
    {"jsonrpc": "2.0", "id": 2, "method": "nlang/observe", "params": {...}},
    {"jsonrpc": "2.0", "id": 3, "method": "nlang/commit", "params": {...}}
]
```

引擎**不保證**批次內請求的執行順序，除非使用 `depends_on` 顯式聲明依賴：

```json
{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "nlang/commit",
    "params": { ... },
    "depends_on": [1, 2]    // 等待 id 1 和 2 完成後才執行
}
```

**管線請求 (Pipeline Request)**：
類似 GraphQL 的連續投影：
```json
{
    "jsonrpc": "2.0",
    "id": 7,
    "method": "nlang/pipeline",
    "params": {
        "steps": [
            {"op": "observe", "path": "_.data.users"},
            {"op": "morph", "morphism": "~%List./filter", "args": [{"age": "> 18"}]},
            {"op": "morph", "morphism": "~%List./map", "args": [{"select": ["name", "email"]}]}
        ],
        "global_fuel": 10000
    }
}
```

### 2.4 錯誤碼規範 **[Core Requirement]**

| 錯誼碼 | 名稱 | 說明 |
| :--- | :--- | :--- |
| `-32700` | `Parse error` | JSON 解析失敗 |
| `-32600` | `Invalid Request` | 非法的 JSON-RPC 請求結構 |
| `-32601` | `Method not found` | 不存在的方法 |
| `-32602` | `Invalid params` | 參數型別或數量錯誤 |
| `-32603` | `Internal error` | 引擎內部錯誤 |
| `-32001` | `Fuel exhausted` | 燃料耗盡 |
| `-32002` | `Timeout` | 觀測超時 |
| `-32003` | `Orthogonal conflict` | 正交衝突 `_\|_` |
| `-32004` | `CAID not found` | 請求的 CAID 不存在且無法冷凝 |
| `-32005` | `Privilege required` | 需要特權令牌 |
| `-32006` | `Invalid token` | 特權令牌無效或過期 |
| `-32007` | `Cycle detected` | 發現循環引用 |
| `-32008` | `Divergent` | 遞迴發散 |

### 2.5 型別對映與有損處理

由於 JSON 缺乏表達「疊加態」與「正交約束」的能力，投影至 JSON 的行為是 **有損的**。建議僅在穩定特徵值時進行導出。

| n/ 型別 | JSON 序列化表示 | 還原說明 |
| :--- | :--- | :--- |
| `_` (Top) | `{"$kind": "top"}` | 萬有子空間，無具體值 |
| `_\|_` (Bottom) | `{"$kind": "bottom", "cause": "...", "caid": "..."}` | 包含衝突原因與因果鏈 CAID |
| `A \| B` (Union) | `{"$kind": "union", "branches": [{...}, {...}]}` | 聯集態的所有分支 |
| `#tag` | `{"$kind": "tag", "name": "tag"}` | 標籤型別 |
| `@Type` | `{"$kind": "type", "name": "Type", "caid": "..."}` | 型別引用 |
| Combo `{}` | JSON Object | 標準 JSON 對象，欄位名可能包含 `%` 前綴 |
| `@list` | `{"$kind": "list", "items": [...]}` | 列表容器 |
| `@num` | `{"$kind": "number", "val": 3.14, "complex": false}` | 數值，複數時 complex 為 true |
| `@str` | `"string value"` | 純字串 |
| `#blur` | `{"$kind": "blur", "caid": "...", "partial": {...}}` | 模糊狀態的已知部分 |
| `#incomplete` | `{"$kind": "incomplete", "reason": "..."}` | 不完全狀態，無 CAID |

**有損注意事項**：
*   **效果標籤遺失**：JSON 無法表達 `%effect` 的傳染性，需顯式檢查 `metadata.effect` 欄位。
*   **CAID 指紋保留**：所有 JSON 對象的 `$caid` 欄位可用於驗證內容一致性。
*   **環狀引用**：JSON 不支持引用循環，引擎使用 `$ref: "caid://..."` 表示循環引用。

### 2.6 認證與安全 **[Core Requirement]**

**Unix Socket 認證 (預設)**：
*   透過 Unix socket 的 `getpeername` 驗證 UID/GID。
*   僅允許同一使用者的進程連接，或配置的白名單群組。

**Token 認證 (TCP/WebSocket)**：
```json
{
    "jsonrpc": "2.0",
    "id": 0,
    "method": "nlang/auth",
    "params": {
        "token": "hash:sha256:v1:privileged...",
        "session_timeout": 3600
    }
}
```

**TLS 加密 (TCP)**：
*   建議使用 mTLS，客戶端需提供客戶端證書。
*   證書的 CN 欄位映射至 `n/` 的觀測身份。

---

## 3. 運行時實作細節 (Runtime Implementation) **[Reference Recommendation]**

### 3.1 核心執行緒模型

Ouroboros 引擎採用 **M:N 執行緒模型**，與異步 Rust 的 `tokio` 或 `async-std` 類似：

*   **工作者執行緒池 (Worker Threads)**：數量通常等於 CPU 核心數，用於執行 CPU 密集型的投影計算。
*   **I/O 執行緒 (I/O Threads)**：用於處理 FFI 調用、網路請求等阻塞操作。
*   **調度器 (Scheduler)**：採用工作竊取 (Work-Stealing) 算法，確保負載均衡。

### 3.2 觀測請求的生命週期

```rust
// 虛擬碼：觀測請求處理流程
enum ObservationRequest {
    Converge { path: Path, fuel: MBU, timeout: Duration },
    Query { caid: CAID, depth: usize },
    Morph { source: Node, morphism: CAID, args: Vec<Node> },
}

async fn handle_request(req: ObservationRequest) -> ObservationResult {
    // 1. 檢查快取 (Cache Lookup)
    if let Some(cached) = cache.get(&req.key()) {
        return Ok(cached);
    }
    
    // 2. 燃料配額檢查
    if !fuel_manager.reserve(req.fuel) {
        return Err(ObservationError::FuelExhausted);
    }
    
    // 3. 執行投影
    let result = match req {
        Converge { path, fuel } => converge_path(path, fuel).await,
        Query { caid, depth } => query_node(caid, depth).await,
        Morph { source, morphism, args } => apply_morphism(source, morphism, args).await,
    };
    
    // 4. 結果快取與計費
    if let Ok(ref node) = result {
        cache.insert(req.key(), node.clone());
        fuel_manager.consume(req.fuel - node.remaining_fuel());
    }
    
    result
}
```

### 3.3 協程與綠色執行緒

對於 `#divergent` 偵測和長時間運算，引擎使用協程 (Coroutine) 實現協作式多工：

*   **協作點 (Yield Points)**：在每次遞迴合併、態射應用、CAID 計算時插入檢查點。
*   **搶佔 (Preemption)**：雖然 `n/` 語義上不支持搶佔（保證原子性），但引擎可以在協作點檢查 `%timeout` 並拋出 `#timeout` 異常。
*   **上下文切換成本**：協程切換成本約 100-200ns，遠低於 OS 執行緒切換。

### 3.4 錯誤恢復與熱重載

*   **分段觀測 (Segmented Observation)**：將大型 Combo 的觀測分解為多個小片段，每個片段獨立計費與快取。
*   **檢查點 (Checkpoint)**：每隔一定 MBU 消費自動建立檢查點，允許從檢查點恢復而非重新開始。
*   **熱重載 (Hot Reload)**：在開發模式下，引擎監聽源碼變更，僅使受影響的 DAG 節點失效，而非重啟整個會話。

---

## 4. 工作區儲存結構 (.oo/)

### 4.1 核心必要結構 **[Core Requirement]**
*   **內容定址儲存 (CAS)**：物件必須以 **CAID** (譜幾何指紋) 為標識存儲於 `objects/` 目錄中。

### 4.2 參考佈局 **[Reference Recommendation]**
```
.oo/
├── objects/        ← [核心] 內容定址儲存 (CAS)
│   ├── objects.idx      ← 物件索引 (CAID → 文件位置)
│   ├── refs.idx         ← 反向引用索引
│   ├── pack/            ← 打包壓縮的物件
│   └── 00/              ← 按前兩碼分散儲存
│       ├── 0001abc...   ← 實際物件文件
│       └── ...
├── refs/           ← 分支指標 (heads/HEAD)
│   ├── heads/main
│   └── HEAD
├── staged          ← 暫存的投影定義
├── config.n        ← 局部環境配置
├── audit.log       ← 特權操作審計日誌
└── wal/            ← 寫前日誌 (Write-Ahead Log)
```

### 4.3 內容定址儲存 (CAS) 格式 **[Core Requirement]**

每個存儲於 `objects/` 的對象必須遵循以下物理格式：

```
┌─────────────────────────────────────────────────────────┐
│  Object Header (32 bytes)                               │
│  - Magic: "NLAG" (4 bytes)                              │
│  - Version: 1 (4 bytes)                                 │
│  - CAID Algorithm: enum (4 bytes)                       │
│  - Payload Size: u64 (8 bytes)                          │
│  - Reserved: 12 bytes                                   │
├─────────────────────────────────────────────────────────┤
│  CAID (variable, depends on algorithm)                  │
├─────────────────────────────────────────────────────────┤
│  Payload (compressed, see below)                        │
├─────────────────────────────────────────────────────────┤
│  Checksum (Blake3, 32 bytes)                            │
└─────────────────────────────────────────────────────────┘
```

**檔案命名**：物件檔案以完整 CAID 命名，但按前兩個位元組分散儲存於子目錄（如 `objects/00/0001abc...`），避免單一目錄檔案過多。

### 4.4 壓縮策略 **[Reference Recommendation]**

為了節省存儲空間，Payload 可選擇壓縮：

| 壓縮算法 | 適用場景 | 壓縮率 | CPU 開銷 | 建議閾值 |
| :--- | :--- | :--- | :--- | :--- |
| **None** | 小型 Combo | 100% | 無 | < 1KB |
| **LZ4** | 中型 Combo，快速解壓優先 | 60-70% | 低 | 1KB - 100KB |
| **Zstd** | 大型 Combo，存儲優先 | 40-50% | 中 | > 100KB |
| **Dictionary Zstd** | 重複模式多的結構化數據 | 30-40% | 中高 | 大量相似物件 |

**自動選擇**：引擎根據 Payload 大小自動選擇壓縮算法。

### 4.5 索引與查找 **[Core Requirement]**

**物件索引 (`objects.idx`)**：
*   格式：`CAID → (file_id, offset, size, compression_algo)`
*   存儲於記憶體中的 HashMap，啟動時從磁碟加載。
*   寫入新對象時同步更新。
*   定期檢查點（Checkpoint）至磁碟，避免啟動時全量掃描。

**反向引用索引 (`refs.idx`)**：
*   格式：`CAID → Vec<Referrer_CAID>`
*   用於碎片整理時識別孤兒對象。
*   僅在 `oo gc` 時重建，避免寫放大。

**索引快取策略**：
*   啟動時載入全部索引（假設 < 100MB）。
*   寫操作先寫 WAL，再更新記憶體索引，最後異步刷盤。

### 4.6 事務與崩潰恢復 **[Core Requirement]**

**寫前日誌 (Write-Ahead Log, WAL)**：
*   寫入新對象前，先寫入 WAL。
*   WAL 條目包含：操作類型、CAID、暫存文件路徑。
*   確認寫入成功後才更新主索引，最後刪除 WAL 條目。

**原子提交**：
*   `oo commit` 操作必須是原子的——要麼完全成功，要麼完全不寫入。
*   使用兩階段提交（2PC）：先寫入所有新對象，再原子性更新 `refs/HEAD`。

**啟動檢查**：
*   引擎啟動時檢查 WAL 目錄。
*   若有未完成的事務，根據策略回滾（刪除暫存文件）或重做（完成寫入）。

**校驗和驗證**：
*   讀取對象時驗證 Blake3 校驗和。
*   若不匹配則標記為 `#corrupted` 並嘗試從遠端節點恢復（若配置）。

### 4.7 打包與垃圾回收 **[Reference Recommendation]**

**物件打包 (Packing)**：
*   類似 Git 的 packfile，將大量小物件打包為連續存儲。
*   使用差分壓縮（delta compression）儲存相似物件的差異。
*   `oo gc --aggressive` 觸發重新打包。

**垃圾回收 (GC)**：
*   `oo gc` 掃描所有 Commit，識別被引用的對象。
*   刪除未被任何 Commit 引用的「孤兒對象」。
*   `--dry-run` 選項僅預覽將被刪除的對象。

---

## 5. 外部函數介面 (FFI) 的實作 **[Core Requirement]**

### 5.1 FFI 沙箱：量子退相干屏蔽 **[Core Requirement]**

若 FFI 態射標記為 **`#pure`**，引擎 **必須** 隔離環境相位噪聲，確保觀測結果的決定論：

1. **時鐘凍結 (Clock Freezing)**：
   *   沙箱內的時間函數（如 `gettimeofday`）必須回傳固定值（Epoch 0 或請求開始時間）。
   *   確保多次調用同一純粹 FFI 函數產生完全相同的結果。

2. **確定性熵源 (Deterministic Entropy)**：
   *   沙箱內的隨機數生成器必須由當前路徑的 **CAID** 衍生隨機種子。
   *   這確保了「相同輸入產生相同輸出」的純粹性。

3. **環境變數隔離**：
   *   沙箱內無法讀取或修改主進程的環境變數。
   *   僅允許透過顯式參數傳遞配置。

4. **檔案系統虛擬化**：
   *   純粹 FFI 函數無法存取真實檔案系統，僅能操作記憶體中的虛擬檔案描述符。
   *   若需讀取檔案，必須在 FFI 調用前由引擎預先載入並作為參數傳入。

### 5.2 FFI 型別映射參考 **[Core Requirement]**

`n/` 的型別與外部語言（C、Rust、WASM）的映射必須遵循以下規範，確保跨語言調用的語義一致性：

#### 基礎型別映射表

| n/ 型別 | C 對應型別 | Rust 對應型別 | 位元組對齊 | 備註 |
| :--- | :--- | :--- | :---: | :--- |
| `@bool` | `bool` (C99+) | `bool` / `u8` | 1 | `0` = false, `1` = true |
| `@int` | `int64_t` | `i64` | 8 | LEB128 編碼後傳輸 |
| `@float` | `double` | `f64` | 8 | IEEE 754 標準雙精度 |
| `@complex` | `n_complex_t` (見下方) | `(f64, f64)` | 16 | 實部 + 虛部各 8 bytes |
| `@str` | `const char*` | `*const u8` + `usize` | 8/16 | UTF-8 編碼，含長度前綴 |
| `@bytes` | `const uint8_t*` | `&[u8]` | 8/16 | 原始位元組，含長度前綴 |
| `@caid` | `const char*` | `String` / `&str` | 8 | CAID 字串，UTF-8 編碼 |

#### 複數型別結構 (n_complex_t)

量子化後的 `n/` 支援複數運算，FFI 層必須明確定義其記憶體佈局：

```c
// C 標頭檔定義
#ifndef NLANG_COMPLEX_H
#define NLANG_COMPLEX_H

typedef struct {
    double real;      // 實部
    double imag;      // 虛部
} n_complex_t;

// 輔助巨集
define NLANG_COMPLEX_REAL(c) ((c).real)
#define NLANG_COMPLEX_IMAG(c) ((c).imag)
#define NLANG_COMPLEX_MAKE(r, i) ((n_complex_t){.real = (r), .imag = (i)})

#endif // NLANG_COMPLEX_H
```

```rust
// Rust FFI 定義
#[repr(C)]
pub struct NComplex {
    pub real: f64,
    pub imag: f64,
}

impl NComplex {
    pub fn new(real: f64, imag: f64) -> Self {
        Self { real, imag }
    }
    
    pub fn from_complex128(c: Complex<f64>) -> Self {
        Self { real: c.re, imag: c.im }
    }
}
```

#### 定點數型別 (Fixed-Point)

為確保跨平台數值一致性，`n/` 的內部定點數表示（見 **[REAL_03](./REAL_03_CAID_Protocol.md)** §4.1）在 FFI 邊界的轉換規則：

| n/ 內部表示 | FFI 傳輸格式 | 轉換公式 |
| :--- | :--- | :--- |
| 128-bit 定點數 (64+64) | `n_fixed128_t` 結構 | `value = integer + fraction / 2^64` |
| 譜座標 (複數定點) | `n_spectral_coord_t` | 實部/虛部各為 128-bit 定點 |

```c
typedef struct {
    int64_t integer;
    uint64_t fraction;
} n_fixed128_t;

typedef struct {
    n_fixed128_t real;
    n_fixed128_t imag;
} n_spectral_coord_t;
```

#### Combo 結構傳遞

Combo 結構在 FFI 邊界以 **JSON 序列化字串** 形式傳遞，或透過記憶體共享介面（零拷貝）：

**選項 A：JSON 字串（預設）**
- 優點：語言無關，易於除錯
- 缺點：序列化開銷

**選項 B：共享記憶體（零拷貝）**
- 適用場景：高頻數值計算（如矩陣運算）
- 要求：呼叫方與被呼叫方協定固定的記憶體佈局

```c
// 共享記憶體介面範例：投影算子矩陣
typedef struct {
    uint32_t dim;           // 矩陣維度 D
    n_complex_t* data;      // D×D 複數矩陣，行優先存儲
    uint32_t flags;         // 標記：1=唯讀, 2=需釋放
} n_projection_matrix_t;
```

#### 型別驗證義務

引擎在 FFI 調用前**必須**執行以下驗證：

1. **NULL 檢查**：指針型別參數不得為 NULL（除非標記為可選）。
2. **對齊檢查**：結構體指標必須符合對齊要求（通常為 8-byte 對齊）。
3. **範圍檢查**：數值型別在轉換前檢查溢位風險。
4. **編碼驗證**：字串型別必須為有效的 UTF-8。

若驗證失敗，引擎必須回傳 `#ffi_malformed` 並附帶詳細的型別不符資訊。

---

### 5.3 FFI 調用協議 **[Core Requirement]**

FFI 函數必須遵循以下調用協議，以確保與 `n/` 的 Combo 結構正確互轉：

**輸入序列化**：
```c
// C ABI 介面範例
typedef struct {
    const char* caid;          // 輸入節點的 CAID 字串
    const char* json_payload;  // Combo 的 JSON 序列化表示
    size_t payload_len;
} nlang_input_t;
```

**輸出反序列化**：
```c
typedef struct {
    char* caid;                // 輸出節點的 CAID（若為新節點）
    char* json_payload;        // 輸出 Combo 的 JSON
    size_t payload_len;
    char* error_message;       // 若為 _|_，錯誤原因
} nlang_output_t;
```

**記憶體所有權**：
*   輸入記憶體由引擎分配，FFI 函數**嚴禁釋放**。
*   輸出記憶體由 FFI 函數分配（使用 `malloc`），引擎讀取後負責釋放。
*   若 FFI 函數使用自訂分配器，必須提供對應的 `free` 回調。

### 5.4 FFI 效果傳播 **[Core Requirement]**

FFI 函數的效果標籤（`%effect`）必須正確傳播至調用者：

*   **聲明義務**：FFI 函數必須在註冊時明確聲明其效果（`#pure`, `#io`, `#nondet`, `#state`）。
*   **執行時驗證**：引擎在 FFI 調用前後檢查效果標籤的一致性。若聲明為 `#pure` 但實際執行時檢測到 I/O 操作，引擎將拋出 `#ffi_impurity_violation`。
*   **效果升級**：若 FFI 函數內部調用了另一個效果更強的 FFI 函數，效果會自動升級（如 `#pure` → `#io`）。

### 5.5 常見 FFI 實作模式 **[Reference Recommendation]**

**模式 A：C ABI 直接綁定**
*   適用場景：效能敏感的數值計算（如線性代數庫）。
*   工具：使用 `bindgen` 從 C 標頭檔自動生成 `n/` 綁定。

**模式 B：WASM 沙箱**
*   適用場景：來源不可信的外掛（如社群貢獻的態射）。
*   工具：將 FFI 函數編譯為 WASM，引擎透過 WASI 介面執行。提供額外的安全隔離。

**模式 C：子進程 RPC**
*   適用場景：需要完整運行時環境的語言（如 Python、Node.js）。
*   工具：FFI 函數運行於獨立子進程，與引擎透過管道或 gRPC 通信。
*   缺點：效能開銷較大，適合 I/O 密集型而非計算密集型任務。

---

## 6. 記憶體管理與垃圾回收 (Memory Management) **[Reference Recommendation]**

### 6.1 子空間引用語義

`n/` 中的「節點」本質上是 **不可變的結構共享 (Immutable Structural Sharing)**：

*   **引用計數 (RC)**：每個 Combo 節點維護一個引用計數。當節點被其他節點引用（如作為欄位值）時，計數遞增。
*   **不可變性保證**：節點一旦創建，其內容不可修改。這消除了「修改後影響其他引用者」的風險。
*   **寫時複製 (CoW)**：當看似需要「修改」節點時（如合併操作），實際上創建新節點並共享未變更的部分。

### 6.2 世代垃圾回收

對於長時間運行的 Service 模式，引擎採用 **世代 GC (Generational GC)**：

*   **新生代 (Young Generation)**：剛創建的節點。採用複製算法（Copying GC），快速回收短期存活的臨時對象。
*   **老年代 (Old Generation)**：經過多輪 GC 仍存活的節點。採用標記-清除算法（Mark-Sweep），減少長期對象的複製開銷。
*   **永久代 (Permanent)**：CAID 已被寫入 Commit 的節點。僅在 `#squash` 操作後才可能被回收。

### 6.3 觀測視界與 GC 的協作

*   **視界內節點 (In-Horizon)**：正在被觀測或等待觀測的節點被標記為「根 (Roots)」，GC 絕不回收。
*   **視界外節點 (Out-of-Horizon)**：未被任何觀測路徑引用的節點可被回收。即使其 CAID 存在於 `objects/` 目錄，記憶體中的副本仍可被清除。
*   **惰性加載 (Lazy Loading)**：當觀測需要一個已被 GC 回收的節點時，引擎從 `objects/` 重新讀取並反序列化。

### 6.4 記憶體碎片整理

長時間運行後，`.oo/objects/` 目錄可能積累大量「孤兒對象」（未被任何 Commit 引用的舊版本）：

*   **碎片整理 (Compaction)**：`oo gc` 命令掃描所有 Commit，識別被引用的對象，刪除未被引用的對象。
*   **增量整理**：在 Service 模式下，碎片整理在背景執行，避免阻塞主線程。
*   **硬連結共享**：若多個工作區引用相同 CAID，引擎使用硬連結 (Hard Link) 共享物理存儲。

---

## 7. 特權與權限管理 (Privilege & Token Management) **[Core Requirement]**

特權模式提供繞過格論約束的能力。為了守護宇宙完整性，其安全管理被視為**核心規格義務 (Core Requirement)**。

### 7.0 兩個面，兩種機制 **[Core Requirement，2026-07-27 新增]**

特權可經**兩個**面被請求，而二者需要的機制不同。混同二者曾使本章描述了一個未實作且較弱的機制，同時完全沒有描述已實作且較強的那個。

| 面 | 請求者 | 機制 |
| :--- | :--- | :--- |
| **本機面**（§1.1 One-shot／CLI） | **操作者本人**，於工作區之擁有者身分下逐次呼叫引擎 | **每次呼叫出示的能力授予**（§7.0.1）；**[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** §6.1.4 能力格 |
| **服務面**（§1.2 Service／§2 JSON-RPC） | **遠端方**，其身分不等同於工作區擁有者 | **令牌**（§7.1／§7.2）＋§2.6 連線認證 |

#### 7.0.1 本機面：逐次呼叫之能力授予 **[Core Requirement]**

*   **機制（MUST）**：本機面的特權**必須**由操作者於**每一次引擎呼叫**時明示授予，且該授予**必須**來自語言層無法產生的通道（如命令列參數）。以 `oo` 為例即 `--grant <能力>`／`--privileged`。
*   **為何這已滿足 P1**：**[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** §6.1.2 裁定 P1 禁止的是**由程式自內部自授**。命令列參數對 `n/` 程式而言是帶外的——程式無從設定它——故此通道即 P1 所要求之可信通道。
*   **為何逐次出示強於長期令牌**：不留存者不會外洩。§7.2 建議之最長 24 小時有效期意味著一份**可被複製的持有者憑證**在磁碟或環境中存在 24 小時；逐次出示的參數在行程結束時即不復存在。故本機面**不得**以長期令牌取代逐次出示。
*   **本機面之界限（誠實聲明）**：工作區之擁有者能改寫 `.oo/`、能替換引擎二進位。依 **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** §6.3.3，該類對手**不在**任何本機機制的保護範圍內。本機面之特權閘所防守者為**程式**（含取自對等點者），非防守操作者本人；任何宣稱能約束操作者的本機機制皆為虛飾。

#### 7.0.2 服務面：§7.1／§7.2 之適用條件 **[Core Requirement]**

§7.1 之令牌格式與 §7.2 之生命週期、撤銷清單，**適用於服務面**。在實作提供服務面之前，其**不適用**，且實作**不得**為滿足形式而於本機面引入令牌——那將以較弱者取代較強者（§7.0.1）。

**[Reference Recommendation]** 引入服務面時，宜先讀 §2.6（連線認證）與 §7.3（審計與隔離）：三者是同一套機制的三個面，分開實作會留下 §7.0 所述之同一類縫。

### 7.1 特權令牌格式 **[Core Requirement]**

**Token 結構**：採用 `CAID:PrivilegeSet:Signature` 的三段式結構。

```
hash:sha256:v1:abc123...:PIN|SQUASH:ed25519:signature...
│                    │  │          │           │
│                    │  │          │           └─ Ed25519 簽名
│                    │  │          └─ 簽名算法
│                    │  └─ 權限集合（位元標記）
│                    └─ 分隔符
└─ 授權者的 CAID
```

**權限集合 (Privilege Set)**：
| 位元 | 權限 | 說明 |
| :--- | :--- | :--- |
| 0 | `PIN` | 允許直接覆蓋節點值 (#pin)。 |
| 1 | `COMMIT` | 允許提交含有 `_\|_` 的內容。 |
| 2 | `SQUASH` | 允許執行歷史壓縮 (#squash)。 |
| 3 | `ROLLBACK` | 允許回滾至任意歷史提交。 |
| 4 | `EFFECT` | 允許強制標記效果 (#effect_override)。 |
| 5 | `MIGRATE` | 允許執行跨版本結構遷移。 |

### 7.2 令牌生命週期 **[Core Requirement]**

**發放 (Issuance)**：
*   由具備 `ADMIN` 權限的令牌或硬體安全模組 (HSM) 簽名發放。
*   必須包含有效期（建議最長 24 小時）。
*   可選擇綁定至特定 IP、PID 或工作區路徑。

**驗證 (Validation)**：
1.  引擎啟動時載入公鑰白名單（`~/.oo/authorized_keys`）。
2.  每次特權操作前驗證 Token 簽名與有效期。
3.  檢查操作類型是否包含於 Token 的權限集合。

**撤銷 (Revocation)**：
*   記錄撤銷清單 (CRL) 於 `~/.oo/revoked_tokens`。
*   即使 Token 尚未過期，也可透過管理介面立即撤銷。
*   引擎每 5 分鐘重載 CRL。

### 7.3 隔離觀測與審計 **[Core Requirement]**

特權工作階段應具備獨立的投影快取：

*   **快取隔離**：特權操作產生的中間結果必須與普通快取物理隔離，避免污染非特權會話。
*   **審計日誌**：所有特權操作必須記錄至 `.oo/audit.log`：
    ```
    [2024-01-15T09:23:45Z] PRIVILEGED: #pin
    Token: hash:sha256:v1:abc123...
    Path: _.config.debug
    Old: {...}
    New: {...}
    CAID: hash:sha256:v1:new456...
    ```
*   **不可否認性**：審計日誌必須寫入防篡改存儲（如 Append-only 文件系統或簽名鏈）。

> **`.oo/audit.log` 之適用條件【2026-07-27 補】**：本節之獨立審計日誌與 §7.1／§7.2 同屬**服務面**（§7.0.2）。於本機面，特權操作之審計面是 **Commit**（**[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** §6.2：審計標記不得入值，其歸屬為 Commit），而非工作區內的一個檔案——後者位於斷言層，無從驗證，且對能寫入它的對手不提供任何保證（§6.3.3）。**不得**以 `.oo/audit.log` 取代 §6.2 之 Commit 標記；二者一為服務面之連線紀錄，一為歷史本身之干預紀錄。

### 7.4 最小權限原則 **[Reference Recommendation]**

建議實作採用以下策略：

*   **臨時提升 (Temporary Elevation)**：類似於 `sudo`，特權令牌不應長期持有。
*   **操作確認**：危險操作（如 `#squash`）需二次確認。
*   **影響預覽**：執行前顯示將受影響的節點數量與 Commit 範圍。
*   **自動降級**：閒置 5 分鐘後自動清除特權狀態。

### 7.5 操作者身分與私鑰保管 (Operator Identity) **[Core Requirement，2026-07-27 新增]**

§7.1–7.2 規定了**公鑰**白名單（誰有權），**[SPEC_10](./SPEC_10_Evolution_and_Commit.md)** §93 規定了 `#refine` 的簽署者必須在 `~%Official.architects` 之中。二者皆假定存在一個**穩定的簽署身分**，而規格此前從未規定該身分的私鑰住在哪裡、由誰產生、何時產生。本節補上。

#### 7.5.1 身分屬於操作者，不屬於工作區 **[Core Requirement]**

*   **歸屬（MUST）**：簽署身分是**操作者**的，非工作區的、非行程的。**[ORDER_01](./ORDER_01_Evolution_and_Governance.md)** §7.1 定義的 `~%Governance.@Voter` 帶 `weight` 與人類可讀之 `alias`——那是**人**。
*   **位置（MUST NOT）**：私鑰**不得**置於工作區儲存（`.oo/`）之內。理由是結構性的而非慣例：`.oo/objects` 正是**設計來被對等點取用、被連同倉庫複製**的成品。秘密不得住在為了被複製而存在的東西裡；依賴「服務路徑剛好不讀那個檔案」是實作巧合，不是保證。
*   **預設位置（SHOULD）**：`~/.oo/identity`，與 §7.2 之公鑰白名單同處操作者家目錄。
*   **覆寫（MAY / MUST）**：實作**得**提供環境變數或配置以覆寫該路徑（供區隔不同身分之用）；若提供，該路徑**必須**為絕對路徑，相對路徑**必須**被拒絕而非以任意基準解析。
*   **鑄造用,不得服務用（MUST NOT，2026-07-30 新增）**：凡以此金鑰簽出、而後由某台機器**持續出示**之物（如 **[REAL_02](./REAL_02_Ouroboros_Protocols.md)** §4.2.8 之歸屬聲明），其設計**必須**使該機器在出示時**不需要**此金鑰——一次鑄成、其後只讀公開產物。否則「操作者金鑰不屬於工作區」在紙上成立而在部署上落空:一台需要它才能服務的機器,就是一台握有操作者簽署能力的機器。**判定法**:移除金鑰檔後,該機器仍應能出示既有產物,且**不得**因此重新鑄造一把(重鑄即違 §7.5.2 惰性,且會靜默換掉操作者的身分)。

#### 7.5.2 引擎得造名字,不得造宣告 **[Core Requirement]**

*   **金鑰是名字（MAY）**：引擎**得**於首次需要簽章時自行產生金鑰對並持久化。金鑰對本身只是一個**名字**，而 `n/` 的名字本即自鑄——CAID 也不需要任何人批准。
*   **權威來自宣告（MUST NOT）**：引擎**不得**將自產金鑰寫入任何權威名單。權威來自**帶外宣告**（§7.2、SPEC_10 §93），而宣告永遠在引擎之外。**[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** §6.1.2 裁定 P1 之同形，低一層。
*   **惰性（MUST NOT）**：引擎**不得**於啟動或一般操作（求值、演化、提交、觀測歷史）時產生身分。僅當**確實需要簽章**時方得產生。未曾簽署過任何東西的操作者不應在磁碟上憑空擁有一把金鑰。
*   **可宣告性（MUST）**：實作**必須**提供一個介面，使操作者能取得自身公鑰以進行帶外宣告。**該介面回報的公鑰,必須是實際簽署所使用者**——回報 X 而以 Y 簽署，會使操作者宣告一把永不簽署的鑰匙，而失敗要到很久以後才以「簽署者不在名單中」浮現，且指向錯誤的原因。

#### 7.5.3 保管 **[Core Requirement]**

*   **形式（MUST）**：磁碟上**只**存私鑰（PKCS#8）。公鑰**必須**於載入時導出，**不得**另存——分別儲存的一對可以自相矛盾。
*   **權限（MUST / MUST NOT）**：金鑰檔**必須**自建立當下即為擁有者專屬（Unix：`0600`），**不得**先以較寬鬆之模式建立再收緊。若引擎**建立**了容納目錄，該目錄**必須**為 `0700`；若目錄**已存在**，引擎**不得**變更其權限——操作者的目錄由操作者決定，且該目錄亦為 §7.2 白名單與撤銷清單之所在。
*   **不得靜默取代（MUST）**：既存但無法解析之身分檔**必須**導致明確失敗（訊息中須指明該檔案路徑），且該檔案位元組**必須**維持不變。靜默改鑄會使「我的簽章突然驗不過了」成為無從追查之謎，且原金鑰不可復原。
*   **併發產生（MUST）**：多個行程同時首次產生身分時，**必須**恰有一個結果被持久化，且**每個行程回報與使用的公鑰必須即為被持久化者**。以「先寫暫存檔再改名取代」實作者將使每個競爭者各自成功而各持己鑰——回到 §7.5.2 最後一條所禁止之情形。建議以「原子性地宣告該路徑（存在即失敗）」實作，敗者改讀勝者之檔案。
*   **語言層不可觸及（MUST）**：私鑰檔**必須**在 SPEC_08 §6.3 之語言層路徑邊界之內，且該保護**不得**依賴其路徑恰好含有儲存目錄名之元件。
*   **不得進入宇宙（MUST NOT）**：身分**不得**成為任何值、CAID 或宇宙根之一部分（**[SPEC_13](./SPEC_13_Ouroboros_Discovery_Protocol.md)** §4.1.2 義務 #3）。

#### 7.5.4 節點身分是另一把鑰匙 **[Core Requirement,2026-07-27 新增]**

本節所定義者為**操作者**身分。另有一把 **[REAL_02](./REAL_02_Ouroboros_Protocols.md)** §4.1.1 所定義的**節點**身分,二者**不得**混為一談,亦**不得**共用同一把金鑰:

| | 回答的問題 | 歸屬 | 用途 |
| :--- | :--- | :--- | :--- |
| **操作者身分**(本節) | **誰授權** | **人**(ORDER_01 §7.1 的 Voter 帶 weight/alias) | 簽署 `#refine` 等治理行為 |
| **節點身分**(REAL_02 §4.1.1) | **哪一台在服務** | **工作區**(`.oo/` 一個,節點一個) | OODP `%from`/`%source`、DHT `node_id`、服務廣告簽章 |

**歸屬相反是刻意的**:§7.5.1 明確否決「每工作區」作為**操作者**金鑰之歸屬,而節點金鑰**正是**每工作區——因為節點**就是**工作區。以一把金鑰兼任二者,將使複製工作區等同複製操作者的簽署能力。§7.5.3 之保管條款對兩者同等適用。

**讀取時機(2026-07-29 新增,規範性)**:節點金鑰**得**於開啟工作區時即被讀取,而不必等到首次需要簽章。

*   **理由**:REAL_02 §5.1.2 的耐久對等目錄必須在載入時判斷「這份檔案是不是**我**寫的」,而該判斷需要本節點的 `node_id`,亦即需要公鑰,亦即需要讀取金鑰檔——**不存在只讀公鑰的路徑**,PKCS#8 兩半同檔。
*   **界線(MUST)**:「得讀取」**不等於**「得鑄造」。§7.5.2 與節點身分弧之 P5 不變——**一般工作不得產生金鑰**。開啟時的讀取**必須**以「檔案已存在」為條件;不存在時**必須**維持缺席,由第一個真正需要簽章者依原路徑產生。
*   實作**應**明示此時機,因為它改變的是**一個秘密何時進入行程記憶體**。此性質正是 §7.5.5 所言、內容定址與格論框架**無話可說**的那一個,故它只能靠條文而非結構來守。

#### 7.5.5 設計理由

**[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** §6.3.1 把引擎儲存劈為**物件層**（要驗證，不要權限）與**斷言層**（要認證，無從驗證）。私鑰**兩者皆非**：它要的既非驗證亦非認證，而是**隱蔽**——而隱蔽恰是內容定址與格論框架**完全無話可說**的那個性質。因此問題從來不是「放在 `.oo/` 的哪個子目錄」，而是「它根本不該在那棵樹裡」。

**[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** §6.3.4 的度數分離在此再現一次：0 階（身分層）毫不留情，≥1 階（語義層）分歧是內容。金鑰是 0 階的東西——它是誰的名字這件事沒有模糊空間，所以它的保管條款是全篇最像傳統安全工程的一節。這不是對誠實原則的妥協，而是其代價：**正因為 0 階從不容讓，≥1 階才付得起那份寬容。**

### 7.6 六個問題:身分族詞彙的判別表 **[Core Requirement,2026-07-28 新設;2026-07-30 增第 6 列]**

本規格前後出現「身分、認證、授權、憑證、許可、委任、背書、歸屬」等詞。它們**不是**同一件事的不同說法,而是**六個不同的問題**,各由不同機制回答。任何一個詞跨兩個問題,規格就會在幾個月後自相矛盾——這已發生過一次(見 §7.6.2 末),而本表第一次**事前**擋下一次(見 §7.6.3)。

| # | 問題 | 標準術語 | 由何回答 | 出處 |
| :-- | :--- | :--- | :--- | :--- |
| 1 | **你是誰** | identification | 節點:公鑰之 CAID / 操作者:公鑰 | REAL_02 §4.1.1、本章 §7.5 |
| 2 | **你真的是他嗎** | authentication | **簽章**(對已知公鑰驗證) | REAL_02 §4.2.2、SPEC_10 §93 |
| 3 | **你可以做什麼** | authorization | **能力格**(逐次出示,不留存) | 本章 §7.0、SPEC_08 §6.1.4 |
| 4 | **你真的有那份東西嗎** | — | **持有聲明**(執行軌;無證明義務) | REAL_02 §4.2.4、APP_05 §5 |
| 5 | **你是不是一千個分身之一** | Sybil resistance | **外部物理錨點**(內部格論供不出來) | ORDER_00 §1.1 |
| 6 | **誰為你作保** | affiliation | **歸屬聲明**(操作者簽署;收方須自行判斷) | REAL_02 §4.2.8 |

**判別方式:問「若這件事是假的,誰付出代價、付出什麼」。** #2 假 ⟹ 有人被冒名,代價是不可否認性;#3 假 ⟹ 有人做了不該做的事,代價是特權;#4 假 ⟹ 你白跑一趟取物,代價是**延遲**;#5 假 ⟹ 路由被整群佔據,代價是全網可用性;#6 假 ⟹ 有人把某操作者的信譽延伸給一個該操作者並未擔保的節點,代價是**錯置的偏好**,且**只由選擇信任該操作者的人承擔**。**#4 的代價與其他四者不同量級,這正是它屬於執行軌的判準。**

**#6 不是 #5。** 二者最容易被混為一談,而它們的差別是可判定的:歸屬聲明只約束**選擇加入**的一方——攻擊者不簽就是了——故它使誠實操作者的分身**可辨識**,不使任何人的分身**變少**。凡讀到「歸屬聲明抵抗女巫攻擊」者,讀錯了一列。

#### 7.6.1 「聲明」是一個承擔責任的詞 **[Core Requirement]**

第 4 列刻意**不叫證明,叫聲明**。這不是措辭保守,是把判斷的責任明確交還給**接收方**:收到證明可以被動接受,收到聲明**必須主動判斷**。

本規格早已在多處實行這條紀律而未給它名字——REAL_02 §3.2「對等點的 `%status` 是**主張**,不是驗證」、同節「`%from` 是**主張**,不是認證」、§4.2.4「`services` 是**主張**」。三處都在說同一件事:**弱化的詞把驗證的義務留在讀者身上**,而強化的詞會把它悄悄拿走。

#### 7.6.2 命名規則:執行軌之物不得以「證明」命名 **[Core Requirement]**

**[APP_02](./APP_02_Formal_Verification.md)** §0 立兩軌:驗證軌承載證明義務,執行軌**永不**承載。由此得一條可機械檢查的命名規則:

> **凡屬執行軌者,不得以「證明 / proof」命名。**

2026-07-11 兩軌重寫已對**質量**正確施行此規則(退位並更名 `mass_hint`),卻未及於**持有**——因為持有當時被稱作「身分幾何」,而「身分」聽起來配得上「證明」。**一個借來的名字使一條已存在的規則被跳過。** 該次改名的完整經過與其三個月後的碰撞,見討論 026。

#### 7.6.3 本表第一次事前擋下一次碰撞 **[說明,2026-07-30]**

第 6 列所命名之機制,設計時的兩個順手名字**都已被本規格用掉**,且各自用在**別的問題**上:

| 想用的詞 | 已被誰用掉 | 它在那裡回答哪個問題 |
| :-- | :--- | :--- |
| **委任** | ORDER_01 §7.4 | 核心層下放子路徑之行政權給 `@Voter`——第 **3** 列(授權) |
| **背書** | SPEC_13 §179 | `#refine` 之簽署權威擔保 `CAID_target` **正確**——關於**值**,不在本表 |

二者皆非「某節點屬於某操作者」。若沿用任一,本表所預言的自相矛盾會如期而至;既然它已被寫下,代價就只是改一個名字。定名 **歸屬聲明**——`聲明` 依 §7.6.1 把判斷的義務留在收方,`歸屬` 說的是 N 屬於 O 而非誰能做什麼。

**這是本表第一次在事前而非事後生效。** §7.6.2 記的是它被跳過的那次;此節記的是它被用上的那次。兩者同樣值得留下:一條只在事後被引用的規則,無從分辨自己是規則還是講法。

---

## 8. IDE 與符號觀測 (IDE & Symbolic Observation) **[Reference Recommendation]**

`n/` 語言設計時充分考慮 IDE 支援。Ouroboros 引擎提供 **語言伺服器協議 (LSP)** 實作，實現「語義感知的開發體驗」。

### 8.1 幾何符號渲染 (Symbolic Ligatures)

為了提升可讀性，建議 IDE 或終端使用具備 Ligature 支援的字型（如 Fira Code、JetBrains Mono），將特定字元序列渲染為數學符號：

| 原始文字 | 建議渲染符號 | 語義 |
| :--- | :---: | :--- |
| `_` | **$\top$** | 萬有子空間 |
| `_\|_` | **$\bot$** | 零維空間 |
| `\|>` | **$\rhd$** | 算子應用管道 |
| `<...>` | **$\diamond$** | 正交投影算子 |
| `&` | **$\sqcap$** | 格論相遇（Meet） |
| `\|` | **$\sqcup$** | 格論聯集（Join） |
| `!<` | **$\lnot$** | 對合否定 |
| `->` | **$\rightarrow$** | 態射映射 |
| `=>` | **$\Rightarrow$** | 邏輯蘊含 |

### 8.2 三位一體語義著色

建議語法高亮將三種核心符號以不同顏色區分，強化開發者的模式識別：

*   **`/` (Logic)**：建議使用動態感強烈的紫色 (#8B5CF6)。代表計算與轉換。
*   **`@` (Type)**：建議使用穩定的青色 (#06B6D4)。代表定義與結構。
*   **`%` (Meta)**：建議使用權威感的金色 (#F59E0B)。代表自省與元資訊。

**效果標籤著色**：
*   `#pure`：綠色（安全）
*   `#io`：黃色（注意）
*   `#nondet`：橙色（警告）
*   `#state`：紅色（危險）
*   `#cached`：藍色（已固化）

### 8.3 語言伺服器協議 (LSP) 擴展 **[Reference Recommendation]**

Ouroboros LSP (`oo-lsp`) 提供標準 LSP 功能與 `n/` 特有的「幾何感知」功能：

**標準功能**：
*   **自動完成 (Completion)**：基於當前宇宙的已觀測節點提供欄位建議。
*   **跳轉定義 (Go to Definition)**：解析 CAID 引用，跳轊至定義源碼（若可用）。
*   **符號重命名 (Rename)**：重命名別名並更新所有引用（注意：不影響 CAID）。
*   **懸停提示 (Hover)**：顯示節點的 `%id`、型別、`%effect` 等元資訊。

**n/ 特有功能**：
*   **譜系視圖 (Lineage View)**：顯示節點的合併歷史與 `#refine` 鏈。
*   **視界模擬 (Horizon Simulation)**：允許 IDE 臨時修改 `%fuel` 或 `%timeout`，預覽不同精度下的觀測結果。
*   **衝突視覺化 (Conflict Visualization)**：當合併產生 `_|_` 時，並排顯示衝突雙方的結構差異。
*   **燃料儀表板 (Fuel Dashboard)**：即時顯示當前文件的 MBU 消耗分布。

### 8.4 LSP 通訊協議 **[Reference Recommendation]**

```typescript
// n/ 特有的 LSP 擴展介面
interface NLangServer {
    // 請求特定路徑的觀測結果（可能觸發引擎計算）
    "nlang/observe": (params: {
        path: string;
        fuel?: number;
        strategy?: "blur" | "strict" | "approximate";
    }) => ObservationResult;
    
    // 獲取節點的譜系（精煉鏈）
    "nlang/getLineage": (params: {
        caid: string;
    }) => LineageInfo;
    
    // 模擬合併結果（不寫入實際狀態）
    "nlang/simulateMerge": (params: {
        base: string;
        left: string;
        right: string;
    }) => MergeResult;
    
    // 訂閱特定路徑的變更（增量更新）
    "nlang/subscribe": (params: {
        path: string;
    }) => void;
    
    // 通知：路徑觀測結果變更
    "nlang/onObserved": Notification<{
        path: string;
        oldCAID: string;
        newCAID: string;
        fuelConsumed: number;
    }>;
}
```

### 8.5 除錯支援 **[Reference Recommendation]**

`oo` CLI 提供除錯協議適配器 (`oo-debugger`)，支援 VS Code 等 IDE：

*   **斷點 (Breakpoints)**：支援在管道 (`|>`)、合併 (`&`)、態射應用處設置斷點。
*   **逐步執行 (Stepping)**：
    *   *Step Over*：跳過當前態射的內部實作。
    *   *Step Into*：進入態射的定義（若為純 `n/` 定義）。
    *   *Step Out*：跳出當前合併層級。
*   **變數檢視 (Variables)**：顯示當前作用域內的所有綁定及其 CAID。
*   **譜回溯 (Spectral Traceback)**：當觀測到 `_|_` 時，顯示導致衝突的完整因果鏈。

---

## 9. 規範化計費模型 (Standardized Billing Model) **[Core Requirement]**

為了確保在視界邊緣產生一致的 **#blur CAID**，引擎必須遵循 MBU 能階計費。

### 9.1 核心操作計費表

| 操作型別 | 單位消耗 (MBU) | 說明 |
| :--- | :---: | :--- |
| **投影展開 (Subspace Expansion)** | 1 | 透過路徑訪問子空間基底。 |
| **算子應用 (Operator App)** | 10 | 執行一次么正變換（包含參數糾纏）。 |
| **譜校準 (Spectral Calibration)** | 25 | 提取正交投影譜摘要（參與 CAID）。 |
| **正交合併 (Orthogonal Merge)** | 5 | 執行一次子空間的交集或併元運算。 |
| **算子升寫 (Lifting)** | 5 + $E_{inner}$ | 管道穿透張量容器的管理能耗。 |
| **FFI 調用 (External Interaction)** | 50+ | 與外部環境進行干涉。 |

### 9.2 遞迴累計原則
*   **管道鏈計費**：能量消耗隨邏輯流傳導累加。
*   **短路權益**：若投影因正交衝突提前終止，僅扣除至衝突點為止的能耗。

---

## 10. 物件生存週期與幾何蒸發 (Object Lifecycle & Geometric Evaporation) **[Reference Recommendation]**

`n/` 宇宙的物件（以 CAID 標識的內容）經歷完整的生命週期，從誕生到最終的「蒸發」。

### 10.1 生命週期狀態機

```
┌─────────┐    ┌──────────┐    ┌─────────┐    ┌──────────┐
│ Staged  │───▶│ Observed │───▶│ Commit  │───▶│ Persist  │
│ (暫存)   │    │ (已觀測)  │    │ (已提交) │    │ (已持久化)│
└─────────┘    └──────────┘    └────┬────┘    └────┬─────┘
                                    │              │
                                    ▼              ▼
                              ┌──────────┐    ┌──────────┐
                              │ Refine   │    │ Evaporate│
                              │ (被精煉)  │    │ (被蒸發)  │
                              └──────────┘    └──────────┘
```

**各狀態說明**：

1. **Staged (暫存)**：
   *   位於工作記憶體，尚未被完整觀測。
   *   可能處於 `#incomplete` 或編輯中狀態。
   *   若進程崩潰，Staged 內容丟失。

2. **Observed (已觀測)**：
   *   已完成收斂，具備穩定 CAID。
   *   位於記憶體快取，尚未寫入磁碟。
   *   可被 `#blur` 或 `#exact`。

3. **Committed (已提交)**：
   *   已寫入 `.oo/objects/` 目錄。
   *   記錄於當前分支的提交歷史中。
   *   除非執行 `gc`，否則永久保留。

4. **Persisted (已持久化)**：
   *   已推送至遠端節點或備份存儲。
   *   具備多重冗餘，可從本地災難恢復。

5. **Refined (被精煉)**：
   *   存在 `#refine` Commit 指向更精確的版本。
   *   舊版本仍可被歷史 Commit 引用，因此不能刪除。

6. **Evaporated (被蒸發)**：
   *   長期未被引用，從本地存儲移除。
   *   但 CAID 仍可能存在於遠端或備份中。

### 10.2 幾何蒸發 (Evaporation) **[Reference Recommendation]**

**觸發條件**：
*   **時間條件**：物件超過 30 天未被任何觀測路徑引用。
*   **空間條件**：磁碟空間低於閾值（預設 10%）。
*   **熱度條件**：物件的「觀測熱度 (Observation Heat)」排名處於末位。

**熱度計算公式**：
```
Heat(O) = Σ (1 / (current_time - access_time_i)) * importance_factor
```

其中 `importance_factor` 考慮：
*   是否被標準庫引用（高重要性）
*   是否被當前 HEAD 引用（中高重要性）
*   是否被多個分支引用（中重要性）
*   僅被歷史 Commit 引用（低重要性）

**蒸發過程**：
1.  將物件標記為 `EVAPORATED`，從 `objects.idx` 移除。
2.  實際刪除物理文件（可配置為移至冷存儲而非直接刪除）。
3.  記錄蒸發日誌，便於審計與恢復。

### 10.3 幾何冷凝 (Condensation) **[Reference Recommendation]**

當觀測需要一個已被蒸發的物件時，引擎嘗試「冷凝 (Condensation)」：

1. **本地冷存儲檢查**：若配置為移至冷存儲（如 S3 Glacier），先嘗試從冷存儲恢復（可能需要數小時）。

2. **LADD 協議請求**：透過 **[APP_05](./APP_05_LADD_Global_Logic_Lattice.md)** 的發現機制，向鄰居節點請求該 CAID。
   ```nlang
   ;; 虛擬碼：冷凝請求
   ~%Discovery./fetch <caid> {
       %strategy: #strict
       %timeout: 3600  ;; 給予較長的超時
   }
   ```

3. **種子節點回退**：若 LADD 發現失敗，嘗試從創世種子節點（官方鏡像）獲取。

4. **冷凝失敗**：若所有嘗試失敗，返回 `_|_` (%cause: `#evaporated_permanently`)。

### 10.4 生命週期策略配置 **[Reference Recommendation]**

使用者可透過 `config.n` 配置生命週期策略：

```nlang
~%Engine: {
    lifecycle: {
        ;; 蒸發策略
        evaporation: {
            enabled: #true
            threshold_days: 30
            min_disk_free_percent: 10
            cold_storage_path: "/mnt/cold-storage/oo"
        }
        
        ;; 冷凝策略
        condensation: {
            enabled: #true
            ladd_timeout_seconds: 300
            seed_fallback: #true
            max_concurrent_requests: 10
        }
        
        ;; GC 策略
        gc: {
            auto_schedule: #true
            interval_hours: 24
            aggressive_mode: #false  ;; 若為 #true，也刪除被歷史引用但非當前 HEAD 的物件
        }
    }
}
```

### 10.5 與內容定址的兼容性 **[Core Requirement]**

蒸發機制**絕不違反**內容定址的不變性：

*   **CAID 不變**：即使物件被蒸發，其 CAID 仍指向相同的邏輯內容。
*   **冷凝一致性**：從任何來源（本地、遠端、冷存儲）冷凝的物件必須通過 CAID 驗證，否則視為 `#corrupted`。
*   **歷史不可變**：蒸發**不影響**已存在的 Commit 歷史，僅影響本地存儲的物理可用性。

---

## 11. 與其他規格的關係

| 本文件章節 | 對應規格文件 | 說明 |
| :--- | :--- | :--- |
| FFI 沙箱 | **[SPEC_08](./SPEC_08_Meta_and_Runtime.md) §5** | `#pure` 的嚴格定義與效果傳播。 |
| 計費模型 | **[SPEC_08](./SPEC_08_Meta_and_Runtime.md) §3** | `%fuel` 與視界參數的詳細語義。 |
| 特權管理 | **[SPEC_08](./SPEC_08_Meta_and_Runtime.md) §6** | `#pin`, `#commit` 等操作的定義。 |
| LSP 協議 | **[SPEC_11](./SPEC_11_Reflection_and_Synthesis.md)** | 反映與合成機制。 |
| 蒸發與冷凝 | **[SPEC_13](./SPEC_13_Ouroboros_Discovery_Protocol.md)** | OODP 發現協議。 |
| 增量收斂 | **[GUIDE_03](./GUIDE_03_Incremental_Convergence.md)** | DAG 與快取的實作指南。 |

---

## 工程實作總結

Ouroboros 引擎的實作是量子化語義與物理現實的橋樑。本文件定義了從 CLI 到儲存、從 FFI 到 IDE、從權限到生命週期的完整工程規範。實作者應遵循 **[Core Requirement]** 標記的義務，並參考 **[Reference Recommendation]** 的最佳實踐，以確保不同實作間的互操作性。

> **結語**：銜尾蛇不斷吞噬自己的尾巴，象徵著無限的循環與自我參照。Ouroboros 引擎即是這樣一個系統——它透過內容定址實現自我描述，透過格論合併實現自我演化，透過形式驗證追求自我完善。
