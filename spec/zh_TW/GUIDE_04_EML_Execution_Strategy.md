# GUIDE_04：EML 執行策略與優化指南

> **Authority**: [Reference Recommendation / 參考建議]  
> **Scope**: 本指南提供 EML 算子在實際引擎中的執行策略選擇、數值穩定性分析與硬體優化建議。

---

## 1. 執行策略選擇指南

`n/` 引擎支援三種 EML 執行策略，依使用場景選擇：

| 策略 | 適用場景 | 數值穩定性 | 效能 | CAID 影響 |
| :--- | :--- | :--- | :--- | :--- |
| **`#eml_native`** | 形式化驗證、CAID 測試、小規模精確計算 | ⭐⭐⭐⭐⭐ | ⭐⭐ | 不變 |
| **`#expanded_opt`** | 生產環境、大規模數值模擬 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 不變 |
| **`#adaptive`** (預設) | 一般用途、混合工作負載 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 不變 |

### 1.1 #eml_native：嚴格 EML 語義

完全遵循 EML 樹結構進行計算，不進行任何展開優化。

```nlang
~%Math: {
    %execution_strategy: #eml_native
}

;; 計算範例
/ln(2.0)  ;; 實際執行：eml(1, eml(eml(1, 2.0), 1))
```

**適用時機**：
- 形式化驗證需要嚴格對應 EML 公設
- CAID 測試套件驗證
- 教育或除錯用途，理解 EML 語義

**注意事項**：
- 深層嵌套（>4 層）會導致浮點誤差迅速累積
- 建議僅用於淺層計算或驗證場景

### 1.2 #expanded_opt：展開優化執行

將 EML 樹展開為直接硬體指令，最大化執行效能。

```nlang
~%Math: {
    %execution_strategy: #expanded_opt
}

;; 計算範例
/ln(2.0)  ;; 實際執行：x86 `fldln2` / ARM `vlog` 等硬體指令
```

**適用時機**：
- 生產環境數值模擬
- 即時系統（Real-time）
- 大規模科學計算

**注意事項**：
- 引擎**應**標記 `%effect: #approximate`
- 結果與 `#eml_native` 可能有微小差異（IEEE 754 容差範圍內）
- CAID 保持不變，僅數值結果變化

### 1.3 #adaptive：自適應策略（預設）

自動選擇執行策略：淺層使用 EML 原生，深層自動展開。

```nlang
~%Math: {
    %execution_strategy: #adaptive
    %adaptive_threshold: 4  ;; 嵌套深度閾值
}

;; 淺層（<= 4 層）：使用 EML 原生
/eml(1, 2)                    ;; EML 原生

;; 深層（> 4 層）：自動展開
/ln(/ln(/ln(2.0)))            ;; 自動展開為硬體指令
```

**切換邏輯**：
1. 計算 EML 樹的嵌套深度
2. 深度 <= 閾值：使用 `#eml_native`
3. 深度 > 閾值：使用 `#expanded_opt`
4. 標記 `%effect: #approximate`（若發生展開）

---

## 2. 數值誤差分析

### 2.1 EML 誤差傳播模型

EML 核心算子 `eml(x, y) = exp(x) - ln(y)` 的誤差分析：

| 運算 | IEEE 754 誤差界 | 誤差累積特性 |
| :--- | :--- | :--- |
| `exp(x)` | 0.5 ulp | 指數放大輸入誤差 |
| `ln(y)` | 0.5 ulp | 對數壓縮輸入誤差 |
| 減法 | 0.5 ulp | 相消誤差（Cancellation）風險 |

**深層嵌套誤差估計**：

```
誤差(1層 EML) ≈ 1.5 ulp
誤差(n層 EML) ≈ 1.5^n ulp（最壞情況）
```

**實務建議**：
- 4 層以下：誤差可控（< 10 ulp）
- 4-6 層：需評估應用容忍度
- 6 層以上：強制使用 `#expanded_opt`

### 2.2 相消誤差風險區域

當 `exp(x) ≈ ln(y)` 時，減法產生相消誤差：

```nlang
;; 高風險：eml(1, e) = e - 1 ≈ 1.718...
;; exp(1) ≈ 2.718, ln(e) = 1, 差異小
/eml(1, 2.718281828459045)   ;; 可能損失精度

;; 低風險：eml(10, 1) = e^10 - 0 ≈ 22026...
;; 差異大，無相消問題
/eml(10, 1)                  ;; 精度良好
```

**偵測機制**：
引擎可實作相消警告：
```nlang
eml(x, y) {
    %warn_if: |exp(x) - ln(y)| < 1e-6 * max(|exp(x)|, |ln(y)|)
    %cause: #cancellation_risk
}
```

### 2.3 誤差預算追蹤

引入 `%numerical_error_budget` 元欄位進行累積誤差追蹤：

```nlang
complex_calc: /eml(/eml(a, b), /eml(c, d)) {
    %numerical_error_budget: 1e-10  ;; 最大容許誤差
}

;; 若估計誤差超過預算，引擎回傳 #blur
```

---

## 3. 硬體優化對照表

### 3.1 x86-64 架構

| EML 運算 | 展開指令 | 延遲 (cycles) | 吞吐量 |
| :--- | :--- | :--- | :--- |
| `exp(x)` | `fldl2e` + `fscale` / AVX `vexp` | 10-20 | 1/cycle |
| `ln(x)` | `fldln2` + `fyl2x` / AVX `vlog` | 15-25 | 1/2 cycles |
| `eml(x,y)` | `vexp` + `vlog` + `vsub` | 30-50 | 1/2 cycles |

**AVX-512 建議**：
- 使用 `vexp` / `vlog` 進行向量化批次計算
- 適合大規模矩陣運算

### 3.2 ARM64 架構

| EML 運算 | 展開指令 | 延遲 (cycles) | 備註 |
| :--- | :--- | :--- | :--- |
| `exp(x)` | NEON `vexp` / SVE `sveexp` | 8-15 | 功耗優化 |
| `ln(x)` | NEON `vlog` / SVE `svelog` | 12-20 | 功耗優化 |

**Apple Silicon 特化**：
- 利用 AMX 加速器進行矩陣 EML 運算
- 適合深度學習場景

### 3.3 GPU (CUDA/Metal)

| 運算 | CUDA 指令 | 記憶體頻寬限制 |
| :--- | :--- | :--- |
| `exp(x)` | `expf` / `__expf` (快速) | 計算密集 |
| `ln(x)` | `logf` / `__logf` (快速) | 計算密集 |
| EML 批次 | 自定義 kernel | 記憶體頻寬 |

**GPU 最佳實踐**：
- 使用共享記憶體快取中間結果
- 批次處理減少 kernel 啟動開銷
- 考慮使用 Tensor Core（若支援）

---

## 4. 精度與效能權衡決策樹

```
開始
  │
  ▼
應用場景是形式化驗證？
  │
  ├── 是 → 使用 #eml_native
  │
  └── 否 → 需要數值重現性（Reproducibility）？
            │
            ├── 是 → 使用 #eml_native（或固定隨機種子）
            │
            └── 否 → EML 嵌套深度 > 4？
                      │
                      ├── 是 → 使用 #expanded_opt
                      │
                      └── 否 → 效能敏感？
                                │
                                ├── 是 → 使用 #adaptive
                                │
                                └── 否 → 使用 #eml_native
```

---

## 5. 監控與除錯

### 5.1 執行統計

引擎應透過 `~%Engine./profile` 提供 EML 執行統計：

```nlang
~%Engine./profile.eml: {
    native_calls: @int
    expanded_calls: @int
    total_error_budget_consumed: @float
    cancellation_warnings: @int
}
```

### 5.2 除錯建議

**數值不一致調查**：
1. 檢查 `%execution_strategy` 設定
2. 比較 `#eml_native` 與 `#expanded_opt` 結果差異
3. 確認是否在 IEEE 754 容差範圍內
4. 若超出容差，可能是實作錯誤，回報至引擎開發者

**效能瓶頸分析**：
1. 使用 `~%Engine./profile` 識別熱點 EML 運算
2. 評估是否可改寫為淺層 EML 或直接使用原生態射
3. 考慮批次處理或向量化

---

## 6. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_09](./SPEC_09_Standard_Library.md)** | EML 語義層定義、派生函數 |
| **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** | `#approximate` 效果標記、執行差異與 CAID 穩定性 |
| **[REAL_01](./REAL_01_Ouroboros_Engineering.md)** | FFI 浮點精度、硬體指令對應 |
| **[APP_02](./APP_02_Formal_Verification.md)** | EML 結構歸納法、形式化驗證 |

---

> **結語**：EML 的極簡數學結構與工程執行效率之間存在本質張力。本指南提供的策略選擇框架，旨在讓開發者依據應用需求，在語義純粹性與數值效能之間找到最佳平衡點。
