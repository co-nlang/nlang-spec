# REAL_02：銜尾蛇協定 (Ouroboros Protocols)

> [!NOTE]: [Standard / 混合規範性]  
> [!NOTE]: 本規範定義 Ouroboros 引擎間進行發現（NDP）、內容交換與特權管理的工作協議。

> [!IMPORTANT]
> [!NOTE]：
> - **[Core Requirement]**：為了確保跨實作的 CAID 一致性與互操作性，實作者**必須**遵循的規範。其地位等同於法典之延伸。
> - **[Reference Recommendation]**：為了與官方工具鏈相容，**建議**實作者採用的最佳實踐。

本文件是 **[SPEC_13](./SPEC_13_Discovery_and_Package.md)** 的工程實作配套。

---

## 1. 本文定位

**[SPEC_13](./SPEC_13_Discovery_and_Package.md)** 定義了發現的語言語義：hash 格式、`&` 收斂、`~%Discovery` 態射介面。但物理層的傳輸、信任鏈與多節點協調由本指南定義。

---

## 2. 創世自舉流程 (Genesis Bootstrapping) **[Core Requirement]**

為了解決語言初期的「冷啟動 (Cold Start)」問題，並確保跨實作的全域 CAID 一致性，引擎必須實作嚴格的自舉流程。

1.  **初次啟動檢測**：當引擎（如 `oo`）啟動且本地不存在 `.oo/` 目錄時，觸發自舉。
2.  **種子解壓縮**：引擎將內建的官方標準庫（如 `~%List`, `~%Math`）的規範化原始碼寫入本地存儲。
3.  **創世 Commit 產生**：
    *   計算這些種子原始碼的 CAID。
    *   驗證計算出的 CAID 是否與引擎硬編碼的「官方官方種子 CAID」完全一致（以防實作者擅自修改標準庫語義）。
    *   產生並固化為宇宙的第一個 Commit $C_0$（創世 Commit）。
4.  **建立根宇宙 `_`**：將 `_` 指向 $C_0$，完成工作區初始化。

---

## 3. 傳輸層設計

`~%Discovery./fetch` 在語言層是一個抽象態射，實際的網路行為由 Ouroboros 引擎實作。
建議的優先順序：

```
1. 本地快取 (.oo/objects/)     ← 最快，無網路請求
2. 工作區已知節點              ← 團隊內部共享
3. 設定的 registry 節點        ← 類似 npm registry，但非強制中央
4. IPFS / Git HTTP             ← 公開後備來源
```

引擎按順序嘗試，第一個回應有效內容的來源獲勝。
來源不影響收斂結果——相同的 hash 無論從哪裡取得，內容必然相同。

### 3.1 效能優化建議
*   **本地優先**：本地快取（`.oo/objects/`）的優先級必須極高，以確保離線觀測的流暢。
*   **預取機制 (Prefetching)**：建議實作者針對 Staged 區或歷史鏈中的未知 CAID 實作非同步預取，避免在交互式觀測時因網路延遲造成卡頓。

### 3.2 n/ Discovery Protocol (NDP)

任何運行 `oo serve-discovery` 的節點都能成為發現節點。
這是一個選用功能，不是必要的基礎設施。

**Request 結構**（n/ Cocoon）：
```nlang
{{
    %op:   #discover
    %hash: "sha256:9f86d081..."
}}
```

**Response 結構**：
```nlang
{
    %status: #success | #not_found
    %result: _    ;; 發現到的 Combo（壓縮後）
    %source: @str ;; 回應節點的識別碼（供審計）
}
```

NDP 本身可以跑在任何傳輸層上：Unix socket、TCP、HTTPS、或作為 Git HTTP 的擴展。

---

## 4. 信任模型

### 4.1 Hash 保證完整性，不保證可信度

`hash:sha256:xxx` 只保證「你拿到的內容和發布者當初的內容一致」。
它**不保證**：
- 發布者的意圖是善意的
- 套件沒有安全漏洞
- 套件符合你的使用場景

這和所有基於內容雜湊的系統（Git、IPFS、Nix）面臨相同的問題。

### 4.2 幾何信任鏈 (Recursive Trust Geometry)

信任在 `n/` 中被轉化為對 **CAID 的偏好選擇**。建議實作者建立以下框架：

**1. 顯式別名優先 (Explicit Priority)**
若多個發現來源對同一個別名（如 `@ai.agent`）提供不同的 CAID，引擎應依據 `discovery.n` 中配置的來源順序進行收斂。使用者本地定義的別名映射具備最高優先權（極小元素）。

**2. 信任黑名單的自洽性**
黑名單本身也是具備 CAID 的 Combo。
*   **防污染機制**：引擎應允許設定一個「根信任清單 (Root of Trust)」。只有在此清單授權範圍內的黑名單更新才會被合併。
*   **遞迴判定**：若一個套件被任何已信任的黑名單標記，引擎在 `./fetch` 時應自動將其收斂結果設為 `_|_`，`%cause: #blocked_by_policy`。

**3. 簽章驗證 (建議實作)**
在 Commit 結構中加入 GPG 或 Ed25519 簽章欄位：
```nlang
;; 套件的 Commit 結構（建議包含）
{
    %content: { ... }    ;; 實際內容
    %sig:     b"..."     ;; 發布者簽章
    %pubkey:  b"..."     ;; 發布者公鑰
}
```
Ouroboros 引擎在 `./fetch` 時可選擇性驗證簽章，不影響格論收斂語義。

### 4.3 惡意套件的處理

惡意內容一旦存在於網路中，其 hash 是不可變的事實。
建議的工程機制：

- **本地黑名單**：`oo block <hash>` 將指定 hash 加入本地拒絕清單。
- **社群黑名單**：黑名單本身也是一個 n/ Combo，可以被發現和合併。
- **隔離執行**：Ouroboros 的沙箱機制（見 **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)**）限制套件的路徑存取權限。

重要：**黑名單是工程機制，不是語言規格。** 語言層只保證收斂的正確性，
不對套件的意圖做任何判斷。

---

## 5. 版本管理策略

### 5.1 Hash-based 版本控制的本質

在 n/ 中，「升級套件」= 把 `deps` 中的 hash 換成新的 hash，
然後觀測收斂結果是否有 `_|_`。

```bash
# 預覽升級是否產生衝突，不實際 commit
oo upgrade @ai.agent <new-hash> --dry-run

# 確認無衝突後執行
oo upgrade @ai.agent <new-hash>
```

### 5.2 語義版本的相容性

傳統的 semver（`^1.2.3`、`~2.0`）是對人類承諾的約定，不是數學保證。
n/ 的方式更誠實：**用 `&` 收斂的結果說話**，有衝突就是有衝突，沒有「應該相容」的灰色地帶。

套件作者若想表達版本意圖，可以在 Combo 中加入 `version` 欄位，
讓使用者透過內容驗證（見 **[SPEC_13](./SPEC_13_Discovery_and_Package.md)** §2.2）來約束。

---

## 6. 本地快取與效能

### 6.1 物件儲存結構

建議的 `.oo/` 內部結構（參考 Git 的 object store）：

```
.oo/
├── objects/
│   ├── 9f/
│   │   └── 86d081884c7d659a...   ← 以 hash 前兩碼分目錄
│   └── ...
├── refs/
│   ├── HEAD
│   └── deps/                     ← 已發現套件的 hash 記錄
└── discovery.n                   ← 發現節點設定
```

### 6.2 `discovery.n` 設定範例

```nlang
;; .oo/discovery.n
sources: {
    registry: u"https://registry.co-nlang.org"
    team:     u"https://internal.example.com/oo"
    fallback: u"ipfs://"
}

trust: {
    official: "commit:official-alias-hash..."
    team:     "commit:team-alias-hash..."
}
```

### 6.3 CAID 重定向快取 (Redirection Cache) **[Reference Recommendation]**

為了落實 `**[SPEC_13](./SPEC_13_Discovery_and_Package.md)** §6.3` 定義的「自動重定向」而不損害觀測效能，建議實作者採用以下快取策略：

1.  **重定向查表 (Redirection Lookup Table, RLT)**：
    引擎應維護一個高效的 Key-Value 映射表（如 HashMap 或 LSM-tree），記錄 `CAID_blur -> CAID_exact` 的映射關係。在解析任何路徑前，優先通過 RLT 進行 O(1) 的跳轉判定。
2.  **鏈式扁平化 (Chain Flattening)**：
    若存在多級精煉（`CAID_v1 -> CAID_v2 -> CAID_exact`），RLT 應在寫入時直接進行「路徑壓縮」，使所有中間節點直接指向最終的精確 CAID，避免連鎖跳轉產生的延遲。
3.  **路徑解析快取 (Path-to-CAID Memoization)**：
    對於頻繁存取的邏輯路徑（如 `/math/solver`），引擎應快取其解析後的最終 CAID。
    - **失效機制**：當新的「精煉 Commit」被導入宇宙時，引擎必須根據 DAG 依賴關係使受影響的路徑快取失效。
4.  **背景查驗**：
    對於標記為 `#blur` 的節點，引擎可啟動背景 Worker 向發現節點詢問是否存在更新的精確版本，並在背景更新 RLT，確保觀測者在下次存取時能獲得更精準的幾何視角。

---

## 7. `~%Discovery` 系統邏輯

根據 **[SPEC_13](./SPEC_13_Discovery_and_Package.md)**，核心發現介面定義如下：

| 態射 | 說明 |
| :--- | :--- |
| **`./fetch <caid>`** | 在萬有集合中定位並坍縮該 CAID 的 Combo。 |
| **`./alias <path>`** | 將指定路徑的內容合成為別名映射表。 |
| **`./identify <node>`** | 獲取指定節點的內在 CAID（即其 `%id`）。 |

### 7.1 工程實作展望
雖然核心規格僅定義上述三個態射，但 Ouroboros 工具鏈（`oo`）可在此之上實作更高階的功能：
*   **`oo search <pattern>`**：透過發現節點搜尋符合語義描述的 CAID。
*   **`oo upgrade`**：利用 `./fetch` 取得新版 CAID 並進行合併。
*   **`oo share`**：公開當前 Commit 的 CAID。

---

## 8. 雜湊演算法的未來相容性

### 8.1 帶前綴的 hash 格式是關鍵

n/ 的 hash 格式天然帶有演算法前綴：

```nlang
hash:sha256:9f86d081...
hash:blake3:1234abcd...   ;; 未來可直接支援，不需要遷移舊格式
```

這讓不同演算法的 hash 可以在同一個宇宙中共存，遷移時不需要一次性替換所有舊 hash。
這是 n/ 相較於 Git（SHA-1 深入每個角落，遷移代價極高）的天然優勢。

### 8.2 物件儲存結構 **[Core Requirement]**

本地物件儲存的目錄結構**必須**將演算法納入路徑，避免不同演算法的 hash 碰撞：

```
.oo/objects/
├── sha256/
│   └── 9f/
│       └── 86d081884c7d659a...
└── blake3/                        ;; 未來演算法直接新增目錄
    └── 12/
        └── 34abcd...
```

**演算法遷移建議 (Algorithm Migration)**：
為了最小化新舊演算法更替時的效能衝擊，建議引擎採取以下策略：
1.  **優先檢查**：優先尋找當前預設演算法目錄。
2.  **回溯讀取 (Legacy Fallback)**：若未找到，檢查 `legacy/` 目錄或舊演算法目錄。
3.  **漸進式重雜湊 (Incremental Re-hashing)**：在讀取舊物件時，於背景計算新雜湊並存入新目錄，逐步將宇宙狀態遷移至更高效的幾何表示。

### 8.3 Rust 實作的建議型別定義

Phase 1 先實作 SHA-256，但型別定義現在就要為未來預留空間：

```rust
/// 內容雜湊，帶演算法標識
/// 不直接使用 String，避免未來遷移成本
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct ContentHash {
    pub algorithm: HashAlgorithm,
    pub digest: Vec<u8>,
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum HashAlgorithm {
    Sha256,
    // Blake3,   // 未來加入時只需新增 variant
    // Sha3_256, // 不需要改動其他程式碼
}

impl ContentHash {
    /// 從帶前綴的字串解析，如 "hash:sha256:v1:9f86081..."
    pub fn parse(s: &str) -> Result<Self, HashParseError> {
        let parts: Vec<&str> = s.splitn(4, ':').collect();
        match parts.as_slice() {
            ["hash", "sha256", fmt_v, digest] => {
                let version = fmt_v.strip_prefix('v').ok_or(HashParseError::InvalidVersion)?;
                Ok(Self {
                    algorithm: HashAlgorithm::Sha256,
                    fmt_version: version.parse()?,
                    digest: hex::decode(digest)?,
                })
            },
            _ => Err(HashParseError::UnknownFormat),
        }
    }

    /// 轉回帶前綴的字串
    pub fn to_string(&self) -> String {
        let algo = match self.algorithm {
            HashAlgorithm::Sha256 => "sha256",
        };
        format!("hash:{}:v{}:{}", algo, self.fmt_version, hex::encode(&self.digest))
    }
}

    /// 物件儲存的目錄路徑
    /// 回傳 (演算法目錄, 前兩碼子目錄, 剩餘檔名)
    pub fn to_storage_path(&self) -> (String, String, String) {
        let algo = match self.algorithm {
            HashAlgorithm::Sha256 => "sha256",
        };
        let hex = hex::encode(&self.digest);
        (algo.to_string(), hex[..2].to_string(), hex[2..].to_string())
    }
}
```

這個設計的核心原則：**演算法是型別的一部分，不是字串的一部分**。
未來加入 Blake3 只需要新增一個 enum variant 和對應的解析分支，
所有使用 `ContentHash` 的程式碼不需要修改。

---

## 9. CAID 格式化版本相容性 **[Core Requirement]**

詳見 **[SPEC_13](./SPEC_13_Discovery_and_Package.md)** §4.2 關於 Legacy Lock 的語言層定義。本節為工程實作提供具體指引。

### 9.1 必須支援的處理策略

引擎實作必須選擇以下兩種策略之一：

**策略 A：多版本內建**
- 內建所有官方標記為 `#legacy` 的 `oo fmt` 格式化版本解析器
- 確保能讀取任何歷史 CAID（如 `v1`, `v2` 等）
- 推薦用於需要長期維護歷史 Commit 的企業級實作

**策略 B：嚴格拒絕**
- 遇到不支援的 `v<fmt_version>` 時，必須回傳 `#unsupported_fmt_version` 錯誤
- 嚴禁靜默忽略或產生未定義行為
- 適用於輕量級實作或嵌入式環境

### 9.2 版本偵測與錯誤處理

```rust
// 範例：Rust 實作的版本檢查邏輯
fn parse_caid(caid_str: &str) -> Result<CAID, CAIDError> {
    // 解析 hash:sha256:v2:9f86... 格式
    let parts: Vec<&str> = caid_str.split(':').collect();
    let fmt_version = parts.get(2).unwrap_or(&"v1"); // 預設 v1
    
    match fmt_version {
        "v1" | "v2" => Ok(parse_supported(caid_str)?),
        unsupported => Err(CAIDError::UnsupportedFmtVersion {
            version: unsupported.to_string(),
            cause: "#unsupported_fmt_version".to_string(),
        }),
    }
}
```

### 9.3 與 **[SPEC_13](./SPEC_13_Discovery_and_Package.md)** 的對應

| 本指南 | **[SPEC_13](./SPEC_13_Discovery_and_Package.md)** 對應 |
| :--- | :--- |
| 策略 A（多版本） | §4.2「多版本支援」選項 |
| 策略 B（嚴格拒絕） | §4.2「嚴格拒絕」選項，回傳 `_\|_` 與 `%cause` |
| `#unsupported_fmt_version` | **[SPEC_13](./SPEC_13_Discovery_and_Package.md)** 定義的錯誤標籤 |

---

## 10. 幾何因果鏈協議 (Causal Chain Protocol) **[Core Requirement]**

當觀測結果收斂至 `_|_` (Bottom) 時，為了確保跨實作與工具鏈（如 IDE）具備一致的診斷能力，`%cause` 欄位的內部結構必須遵循本協議定義的 Schema。

### 10.1 核心因果結構 (Core Schema)

`%cause` 必須是一個 Combo，且包含以下欄位：

| 欄位 | 型別 | 說明 |
| :--- | :--- | :--- |
| **`%type`** | `@tag` | 衝突型別。如 `#conflict`, `#type_mismatch`, `#missing_key`, `#divergent`, `#fuel_exhausted`。 |
| **`%path`** | `p"..."` | 發生衝突的絕對宇宙路徑。 |
| **`%involved`** | `[@caid]` | (選用) 參與衝突的節點 CAID 列表。 |
| **`%expected`** | `_` | (選用) 預期的格論約束（如型別定義）。 |
| **`%found`** | `_` | (選用) 實際觀測到的不相容原子或結構。 |
| **`%trace`** | `[@cause]` | (選用) 遞迴因果鏈。若衝突是由下游傳導而來，應包含子層級的因果 Combo。 |

### 10.2 診斷一致性義務

1.  **結構完整性**：實作者**嚴禁**使用純字串替代結構化的 `%cause` Combo。
2.  **標籤標準化**：必須優先使用 **[ERROR_CODES.md](./ERROR_CODES.md)** 定義的標準標籤。
3.  **惰性保證 (Reference Recommendation)**：
    *   引擎應僅在 `%cause` 被顯式觀測時才生成完整的 `%trace` 鏈，以降低一般收斂過程中的記憶體壓力。
    *   對於深層遞迴產生的因果鏈，建議引擎實作「鏈式扁平化」或限制最大追蹤深度（預設建議為 32 層）。

---

## 11. 與規格書的對應

| 本指南章節 | 對應規格 |
| :--- | :--- |
| 傳輸層 / NDP | **[SPEC_13](./SPEC_13_Discovery_and_Package.md)** §5（系統發現介面） |
| 信任模型 | **[SPEC_13](./SPEC_13_Discovery_and_Package.md)** §4.2（遞迴信任幾何） |
| 惡意套件 | **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)**（沙箱機制） |
| 版本管理 | **[SPEC_13](./SPEC_13_Discovery_and_Package.md)** §2.2（內容驗證） |
| 本地快取 | **[SPEC_11](./SPEC_11_Reflection_and_Synthesis.md)**（合成機制） |
| 雜湊演算法 | **[SPEC_13](./SPEC_13_Discovery_and_Package.md)** §3（CAID 格式定義） |