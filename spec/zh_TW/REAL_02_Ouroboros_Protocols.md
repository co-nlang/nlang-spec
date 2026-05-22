# REAL_02：銜尾蛇發現協定 - 傳輸層與基礎發現 (OODP L1-L3)

> [!NOTE]: [Standard / 混合規範性]  
> 本規範定義 **OODP (Ouroboros Discovery Protocol)** 的 **L1-L3 層**實作：物理傳輸、節點定址與基礎收斂協議。

> [!IMPORTANT]
> - **[Core Requirement]**：為了確保跨實作的互操作性，實作者**必須**遵循的規範。
> - **[Reference Recommendation]**：**建議**實作者採用的最佳實踐。

本文件是 **[SPEC_13: 銜尾蛇發現協定](./SPEC_13_Ouroboros_Discovery_Protocol.md)** 的 **L1-L3 層**工程實作配套。

關於 OODP 五層架構的完整定義，請參閱 SPEC_13 §0。

---

## 本文定位

| OODP 層級 | 名稱 | 對應文件 | 職責 |
| :--- | :--- | :--- | :--- |
| **L1 物理層** | 傳輸載體 | **本文 §3** | TCP/UDP、libp2p、QUIC 封包傳輸 |
| **L2 定址層** | 節點定位 | **REAL_03** | CAID 格式、Kademlia XOR 路由、節點發現 |
| **L3 收斂層** | 基礎收斂 | **本文 §7** | 分散式 `&` 運算、衝突判定、基礎路由 |
| L4-L5 優化 | 譜幾何 | **APP_05** | LADD 引力路由、熱帶剪枝、視角管理 |

**關鍵區分**：
- 本文 (REAL_02) 處理「傳統」分散式系統問題：封包怎麼傳、節點怎麼找、基礎合併如何判定
- APP_05 (LADD) 處理「譜幾何」優化：如何用譜特徵加速路由、如何用引力場優化選擇

---

## 1. 創世自舉流程 (Genesis Bootstrapping) **[Core Requirement]**

為了解決語言初期的「冷啟動」問題，引擎必須實作嚴格的自舉流程。

1.  **初次啟動檢測**：當引擎啟動且本地不存在 `.oo/` 目錄時，觸發自舉。
2.  **種子解壓縮**：引擎將內建的官方標準庫（如 `~%List`, `~%Math`）寫入本地存儲。
3.  **創世 Commit 產生**：
    *   計算種子原始碼的 CAID。
    *   驗證 CAID 是否與引擎硬編碼的「官方種子 CAID」一致。
    *   產生宇宙的第一個 Commit $C_0$（創世 Commit）。
4.  **建立根宇宙 `_`**：將 `_` 指向 $C_0$，完成工作區初始化。

---

## 2. OODP 協定棧總覽

```
┌──────────────────────────────────────────────┐
│  L5 應用層: ~%Discovery./find (SPEC_13 §6)    │
│  L4 視角層: 權威格論、譜消融 (APP_05)          │
├──────────────────────────────────────────────┤
│  L3 收斂層: 分散式 & 運算、衝突判定 (本文 §7) │
├──────────────────────────────────────────────┤
│  L2 定址層: CAID、Kademlia (REAL_03)          │
├──────────────────────────────────────────────┤
│  L1 物理層: TCP/UDP/libp2p (本文 §3)          │
└──────────────────────────────────────────────┘
```

**本文涵蓋**：L1 傳輸、L3 基礎收斂，以及 L2-L3 的協定介面。

---

## 3. L1 物理層：傳輸載體 (The Carrier Layer)

`~%Discovery./fetch` 在語言層是抽象態射，實際的網路行為由引擎實作。

### 3.1 傳輸優先順序

```
1. 本地快取 (.oo/objects/)     ← 最快，無網路請求
2. 工作區已知節點              ← 團隊內部共享
3. 設定的 registry 節點        ← 類似 npm registry，但非強制中央
4. IPFS / Git HTTP             ← 公開後備來源
```

引擎按順序嘗試，第一個回應有效內容的來源獲勝。
來源不影響收斂結果——相同的 hash 無論從哪裡取得，內容必然相同。

### 3.2 OODP 基礎封包格式

任何運行 `oo serve-discovery` 的節點都能成為發現節點。

**Request 結構**（n/ Cocoon）：
```nlang
{{
    %op:   #discover | #fetch | #advertise
    %hash: "hash:sha256:v1:9f86d081..."  ;; 目標 CAID
    %from: @caid                          ;; 請求節點 ID
}}
```

**Response 結構**：
```nlang
{
    %status: #success | #not_found | #conflict
    %result: _         ;; 發現到的 Combo（壓縮後）或衝突資訊
    %source: @str      ;; 回應節點的識別碼
    %hops:   @int       ;; 路由跳數（用於統計）
}
```

**傳輸協定**：OODP 封包可跑在任何傳輸層上：Unix socket、TCP、HTTPS、或作為 libp2p 的擴展。

### 3.3 效能優化建議 [Reference Recommendation]

*   **本地優先**：本地快取（`.oo/objects/`）的優先級必須極高，以確保離線觀測的流暢。
*   **預取機制 (Prefetching)**：針對 Staged 區或歷史鏈中的未知 CAID 實作非同步預取。

---

## 4. L2-L3 介面：節點發現與路由

### 4.1 Kademlia DHT 基礎路由 **[Core Requirement]**

L2 使用 **Kademlia XOR 路由**尋找物理節點。這是工程妥協——純粹的譜路由在離散 DHT 中難以實作。

**路由表結構**：
- 節點 ID = CAID 的內容指紋（content_digest）前 160 bit
- 距離度量 = XOR(node_id_a, node_id_b)
- 桶分區 = 標準 Kademlia 二叉樹

**與譜幾何的分層**：
- **L2 (Kademlia)**：解決「這台機器在哪裡」
- **L3+ (譜感知)**：解決「這個子空間由誰服務」

### 4.2 服務廣告基礎格式

節點向網路宣告其承載的服務（L3 基礎版）：

```nlang
@ServiceAdvertisement: {{
    node_id:    @caid      ;; 節點 CAID
    services:   [@caid]    ;; 該節點可服務的子空間 CAID 列表
    capacity:   @int       ;; 當前負載容量（相對值）
    signature:  b""        ;; 節點簽名
    ttl:        @int & < 16
}}
```

**與 LADD 的區分**：
- 本文 (L3 基礎)：簡單的服務列表廣告
- APP_05 (L4 優化)：譜幾何廣告 (GBB)，包含質量、譜指紋、引力場

---

## 5. 本地儲存結構

### 5.1 建議的 `.oo/` 內部結構

```
.oo/
├── objects/                    ;; L2: 內容定址儲存
│   ├── sha256/
│   │   └── 9f/
│   │       └── 86d081884c7d659a...
│   └── blake3/
├── refs/                       ;; L3: 別名與重定向
│   ├── HEAD
│   ├── deps/                   ;; 已發現套件的 hash 記錄
│   └── redirects/              ;; CAID_blur -> CAID_exact 映射
├── routing/                    ;; L2: Kademlia 路由表
│   └── buckets.dat
└── discovery.n                 ;; 發現節點與信任設定
```

### 5.2 物件儲存結構 **[Core Requirement]**

本地物件儲存必須將演算法納入路徑：

```
.oo/objects/
├── sha256/
│   └── 9f/
│       └── 86d081884c7d659a...
└── blake3/
    └── 12/
        └── 34abcd...
```

### 5.3 CAID 重定向快取 [Reference Recommendation]

為了落實 SPEC_13 §5.2 的「自動重定向」，建議實作以下策略：

1.  **重定向查表 (RLT)**：記錄 `CAID_blur -> CAID_exact` 的 O(1) 跳轉。
2.  **鏈式扁平化**：多級精煉自動壓縮為直接指向最終 CAID。
3.  **背景查驗**：對 `#blur` 節點啟動 Worker 詢問是否有更新的精確版本。

---

## 6. 信任模型與安全

### 6.1 Hash 保證完整性，不保證可信度

`hash:sha256:xxx` 只保證「你拿到的內容和發布者當初的內容一致」。
它**不保證**：發布者善意、套件無漏洞、符合使用場景。

### 6.2 幾何信任鏈 (Recursive Trust Geometry)

信任在 `n/` 中被轉化為對 **CAID 的偏好選擇**。

**1. 顯式別名優先**
若多個來源對同一個別名提供不同 CAID，引擎依據 `discovery.n` 中的來源順序進行收斂。

**2. 根信任清單 (Root of Trust)**
引擎應允許設定「根信任清單」。只有在此清單授權範圍內的黑名單更新才會被合併。

**3. 簽章驗證 (建議實作)**
```nlang
{
    %content: { ... }
    %sig:     b"..."     ;; Ed25519 簽章
    %pubkey:  b"..."     ;; 發布者公鑰
}
```

### 6.3 惡意套件處理

- **本地黑名單**：`oo block <hash>` 加入本地拒絕清單。
- **社群黑名單**：黑名單本身也是 n/ Combo，可被發現和合併。
- **隔離執行**：沙箱機制限制套件的路徑存取權限（見 SPEC_08）。

**重要**：黑名單是工程機制，不是語言規格。

---

## 7. 幾何機率證明驗證 (GPP Verification) **[Core Requirement]**

為了防禦 **[SPEC_15](./SPEC_15_Anti_Patterns.md)** §7 定義的譜女巫攻擊與其他 LADD 層攻擊，節點必須在傳輸層實作 GPP (Geometric Probability Proof) 的基礎驗證。

### 7.1 GPP 封包擴展

當節點廣告其幾何質量 (Geometric Mass) 時，必須附帶可驗證的證明：

```nlang
@ServiceAdvertisement: {{
    node_id:    @caid
    services:   [@caid]
    capacity:   @int

    ;; GPP 證明結構（參見 APP_05 §5）
    gpp_proof: {{
        spectrum_commitment: @hash  ;; 譜特徵的雜湊承諾
        boundary_proof:      b""   ;; STARK 證明數據（壓縮後）
        mass_evidence:       @float ;; 聲稱的幾何質量證據
        timestamp:           @int    ;; Unix 時間戳，防止重放攻擊
    }}

    signature:  b""        ;; 對上述結構的 Ed25519 簽名
    ttl:        @int & < 16
}}
```

### 7.2 基礎驗證義務

引擎收到 `ServiceAdvertisement` 時必須執行以下驗證：

1.  **簽名驗證**：驗證 `signature` 與 `node_id` 對應的公鑰匹配。
2.  **時間驗證**：`timestamp` 與本地時間差異不得超過 **60 秒**。
3.  **質量承諾驗證**：`mass_evidence` 必須與 `gpp_proof.spectrum_commitment` 數學一致（即 $m = \text{Tr}(P)$ 的聲稱必須與譜承諾對應）。
4.  **STARK 驗證**（若引擎支援）：驗證 `boundary_proof` 證明節點確實持有對應子空間的投影算子。

### 7.3 信任分級

| 驗證層級 | 要求 | 信任權重 |
| :--- | :--- | :--- |
| **Level 0** | 僅簽名驗證 | 0.1 |
| **Level 1** | 簽名 + 時間 + 質量承諾 | 0.5 |
| **Level 2** | 完整 STARK 驗證 | 1.0 |

*   **預設行為**：引擎在資源受限時可退至 Level 1，但必須明確記錄降級事件。
*   **高安全模式**：對關鍵路徑（如 `@Auth` 或 `@StandardLibrary` 查詢），引擎**必須**要求 Level 2 驗證。

### 7.4 與 LADD 的協作

GPP 驗證是 LADD L3+ 層優化的**基礎依賴**：

*   **[APP_05](./APP_05_LADD_Global_Logic_Lattice.md)** §4.1 的引力路由算法使用 `node.gbb.mass` 計算轉發權重。
*   **安全約束**：若節點的 GPP 驗證失敗，其 `mass` 必須被視為 **0**，該節點不得被納入測地線路由計算。
*   **快取策略**：驗證通過的 GPP 結果可快取 **TTL 建議值：300 秒**，避免重複驗證開銷。

---

## 8. L3 收斂層：基礎分散式收斂

### 8.1 基礎 `&` 運算協議 **[Core Requirement]**

當節點收到遠端的合併請求時，執行基礎格論運算：

1.  **接收請求**：`{ %op: #unify, %target: CAID_A, %with: CAID_B }`
2.  **本地計算**：嘗試計算 `CAID_A & CAID_B` 的結果
3.  **回傳結果**：
    - 成功：回傳合併後的 CAID 與內容
    - 衝突：回傳 `_|_` 與 `%cause` 結構（見 REAL_04）

### 8.2 與 LADD 優化的介接

基礎 L3 收斂（本文）：
- 直接對 CAID 進行合併運算
- 無額外路由優化
- 適用於小規模或區域網路

LADD 優化收斂（APP_05）：
- 利用譜引力預測合併可能性
- 熱帶剪枝避免無意義的衝突
- 測地線路由選擇最優節點進行合併

**兩者關係**：LADD 是 L3 的**優化擴充**，基礎收斂必須先正確實作，才能導入 LADD 優化。

---

## 9. 版本管理與遷移

### 9.1 Hash-based 版本控制

在 n/ 中，「升級套件」= 把 `deps` 中的 hash 換成新的 hash，然後觀測收斂結果是否有 `_|_`。

```bash
# 預覽升級是否產生衝突
oo upgrade @ai.agent <new-hash> --dry-run

# 確認無衝突後執行
oo upgrade @ai.agent <new-hash>
```

### 9.2 雜湊演算法未來相容性 **[Core Requirement]**

n/ 的 hash 格式天然帶有演算法前綴：

```nlang
hash:sha256:v1:9f86d081...
hash:blake3:v2:1234abcd...
```

本地儲存必須將演算法納入路徑（見 §5.2）。

---

## 10. 與規格書的對應

| 本文章節 | OODP 層級 | 對應規格 |
| :--- | :--- | :--- |
| §3 物理層 | L1 | **[SPEC_13](./SPEC_13_Ouroboros_Discovery_Protocol.md)** §6（系統發現介面） |
| §4 節點路由 | L2-L3 | **[REAL_03](./REAL_03_CAID_Protocol.md)** (L2 定址) |
| §5 本地儲存 | L2-L3 | **[SPEC_13](./SPEC_13_Ouroboros_Discovery_Protocol.md)** §4 (CAID 格式) |
| §6 信任模型 | L4 | **[SPEC_13](./SPEC_13_Ouroboros_Discovery_Protocol.md)** §7 (信任格論) |
| §7 GPP 驗證 | L3+ | **[SPEC_15](./SPEC_15_Anti_Patterns.md)** §7 (安全反模式)、**[APP_05](./APP_05_LADD_Global_Logic_Lattice.md)** §5 (GPP) |
| §8 收斂層 | L3 | **[SPEC_13](./SPEC_13_Ouroboros_Discovery_Protocol.md)** §6.3 (LADD 介接) |
| §9 版本管理 | L2 | **[SPEC_13](./SPEC_13_Ouroboros_Discovery_Protocol.md)** §5 (精煉) |

**與 LADD 的關係**：
- 本文：OODP L1-L3 **基礎實作**（必須實作）
- APP_05：OODP L3-L5 **譜幾何優化**（選擇性實作）

符合規格的引擎**必須**實作本文定義的基礎傳輸與收斂，可選地實作 APP_05 的 LADD 優化。
