# n/ Language Specification - 錯誤代碼與診斷指南 (Error Codes & Diagnostics)

## 1. 錯誤標籤索引

以下是根據 `%cause.%val` 分類的標準標籤及其對應的修復方向。

### 1.1 格論衝突 (Lattice Conflicts)

| 標籤 | 說明 | 修復建議 |
| :--- | :--- | :--- |
| **`#conflict`** | 靜態邏輯不相容 | 檢查合併的兩個值或型別是否互斥（如 `1 & 2`）。建議使用更寬鬆的型別約束，或使用聯集（`\|`）而非交集（`&`）。 |
| **`#arithmetic_on_anchor`** | 錨點算術非法 | 對序位錨點（如 `#_\|_` 或 `#_`）觀測了非法算術運算。錨點代表序位的極值，其算術行為受格論約束。 |
| **`#numerical_error`** | 數值運算異常 | 發生除以零、溢出或無效浮點數運算。請檢查態射輸入域或增加邊界檢查。 |
| **`#divergent`** | 動態非終止（無限遞迴） | 檢測到循環定義。請檢查是否存在終止條件，或增加基底案例以確保收斂到不動點。 |
| **`#incomplete`** | 視界內無法完全收斂 | 在目前的計算視界內結果仍具有歧義。建議增加 `%fuel` 配置，或優化邏輯以減少不確定性。 |
| **`#partial_geometry`** | 幾何內容缺失 | 因網路斷線或資料未發現導致的局部不完全觀測。對應 LADD 協議中的幾何冗餘保護。 |
| **`#recursive_lazy`** | 結構遞迴標籤 | 表示該節點具備合法的無限結構遞迴定義，僅在顯式觀測路徑抵達時展開。 |
| **`#tropical_approximation_failed`** | 熱帶近似失敗 | 使用熱帶幾何進行優化加速時發生異常（見 **[APP_01](./APP_01_Tropical_Geometry.md)**）。建議回歸精確格論觀測。 |
| **`#order_conflict`** | 序位矛盾 | Poset 合併時關係聯集出現矛盾（如 `#a < #b` 遇 `#a > #b`），坍縮為 `_\|_`（**[SYNTAX_10](./SYNTAX_10_Enum_and_Poset.md)** §4.5）。請檢查兩個序位宣告的方向一致性。 |
| **`#log_singularity`** | 對數奇異點 | `ln(0)` 等對數奇異點。預設策略下回傳 `#blur` 並以本標籤標記 `%cause`（**[SPEC_09](./SPEC_09_Standard_Library.md)**）。可沿 `%branch` 選擇 Riemann 面分支，或檢查輸入域。 |
| **`#eml_singularity`** | EML 奇異點 | `eml(x, 0)` 之 `ln(0)` 分量奇異。行為同上（**[SPEC_09](./SPEC_09_Standard_Library.md)**）。 |
| **`#branching`** | 多值分支 | 遞迴/譜驗證中產生合法多值分支（非錯誤，**[SPEC_12](./SPEC_12_Logic_Validation_and_Recursion.md)** §4.1.1）；與 `#divergent`（非終止）區分。如需單值，顯式選擇分支或加約束收窄。 |
| **`#cancellation_risk`** | 災難性消去風險 | EML 執行策略偵測到浮點災難性消去（**[GUIDE_04](./GUIDE_04_EML_Execution_Strategy.md)**）。屬執行軌數值 QoS（**[APP_02](./APP_02_Formal_Verification.md)** §0），非證明義務；建議改寫算式或提高精度策略。 |
| **`#fractional_bitwise`** | 分數位元運算違規 | 對非整數複數執行位元運算（如 `/bitAnd 3.5 1`）。位元運算僅在數值**投影**至整數子空間 `@int` 時定義。請先將值投影至整數域再執行位元操作。 |

### 1.2 視界與資源邊界 (Horizon Boundaries)

| 標籤 | 說明 | 修復建議 |
| :--- | :--- | :--- |
| **`#fuel_exhausted`** | 觀測燃料耗盡 | 運算步數超過限制。請在環境中增加 `%fuel` 配額，或簡化計算邏輯。 |
| **`#timeout`** | 運算時間超標 | 運算耗時超過 `%timeout`。請優化性能、減少嵌套，或放寬時間限制。 |
| **`#max_nodes_exceeded`** | 模式匹配節點數超標 | 模式過於複雜。建議簡化模式匹配邏輯，或增加 `%max_pattern_nodes` 上限。 |
| **`#max_depth_exceeded`** | 統一化深度超標 | 結構嵌套過深。請嘗試扁平化數據結構，或增加 `%max_unification_depth`。 |
| **`#max_lifting_exceeded`** | 態射升寫深度超標 | 管道 `|>` 遞迴升寫層數過深。建議手動展開部分結構，或增加 `%max_lifting_depth`。 |
| **`#max_branches_exceeded`** | 聯集分支數超標 | 聯集產生的可能性過多。建議減少不確定的聯集路徑，或增加 `%max_branches`。 |
| **`#no_matching_branch`** | 模式匹配無匹配分支 | 在態射分派或條件收斂中，輸入值不符合任何定義的分支條件。請檢查 `@Type` 約束或增加 `_` 預設分支。 |
| **`#out_of_horizon`** | 視界過度穿透 | 路徑導航符號 `^` 超出了實際的嵌套層級。請檢查 `details.requested_depth` 與 `details.actual_depth` 以對齊結構。 |

### 1.3 發現與內容驗證 (Discovery & Verification)

| 標籤 | 說明 | 修復建議 |
| :--- | :--- | :--- |
| **`#not_found`** | 發現失敗 | 找不到指定的 CAID 或資源。請確保資源已發佈到宇宙中，並檢查路徑或雜湊值是否正確。 |
| **`#caid_mismatch`** | 內容與 CAID 不符 | 取得的內容雜湊與請求的不一致。請檢查傳輸過程是否損壞，或內容是否已被篡改。 |
| **`#compat_conflict`** | 版本相容性失敗 | `%compat` 宣告與當前環境不符。請更新版本宣告，或更換相容的庫版本。 |
| **`#unsupported_ca_algo`** | 雜湊演算法不支援 | 引擎無法解析該 CAID 使用的雜湊演算法。請升級引擎或使用相容的雜湊標準。 |
| **`#unsupported_fmt_version`** | 規格版本不支援 | CAID 所使用的 `v<fmt_version>` 超出當前引擎的解析能力。請升級 Ouroboros 引擎或將該內容遷移至新版本格式。 |
| **`#ambiguous_refinement`** | 精煉歧義 | 發現多個相互衝突的精確 Commit 試圖精煉同一個模糊節點（`#blur`）。請顯式指定首選的 Commit CAID。 |
| **`#refine_authority_missing`** | 精煉授權缺失 | `#refine` 操作缺少有效的治理權威簽署。請確保該 Commit 來自受信任的架構師。 |
| **`#refine_authority_invalid`** | 精煉簽署無效 | `#refine` Commit 的數位簽署驗證失敗（金鑰不匹配或已撤銷）。 |
| **`#refine_signer_unknown`** | 未知簽署者 | 簽署者不在委員會名單中。請檢查 `%authority.signer` 欄位。 |
| **`#refine_source_unverifiable`** | 精煉來源不可驗證 | 引擎無法驗證 `#refine` 定義中的原始 CAID（通常因演算法版本過舊）。 |
| **`#refinement_cycle`** | 精煉重定向循環 | 偵測到 `#refine` 宣告形成了因果循環（如 A->B->A）。受影響的路徑自動失效。 |
| **`#semantic_isolation`** | 語義隔離警告 | 檢測到不同信任路徑下的觀測結果存在幾何不連續性，疑似遭受語義日蝕攻擊。 |
| **`#verification_failed`** | 證明/測試驗證失敗 | 邏輯節點不滿足指定的 `%termination_proof` 或 `%contract` 約束。請修正邏輯或更新證明。 |

### 1.4 幾何與存取違規 (Geometric & Access Violations)

| 標籤 | 說明 | 修復建議 |
| :--- | :--- | :--- |
| **`#private_access_violation`** | 跨邊界私有存取 | 嘗試從外部存取以 `~` 標記的私有欄位。請改為存取公開欄位，或在合法的封裝邊界內存取。 |
| **`#cocoon_isolation_violation`** | Cocoon 隔離違規 | 試圖透過管道 `|>` 將態射升寫穿透至雙大括號 `{{}}` 隔離的封閉結構內部。 |
| **`#blocking`** | 合規性阻擋 | 套件內容違反了當前環境的強制性合規性規範。 |
| **`#missing_key`** | 本徵態封閉合併違規 | 向 **Cocoon `{{}}`** 進行合併時，對方帶有 Cocoon 未宣告的額外欄位。請檢查合併對象的完整性，或將 Cocoon 轉換為**疊加態預設**的 Combo `{}`。 |
| **`#lifting_failed`** | 態射升寫失敗 | 在管道 (`|>`) 演化過程中，容器內的元素不符合態射的型別約束。請檢查容器內容或態射輸入域。 |
| **`#effect_violation`** | 純粹性違規 | 在 `#pure` 環境中執行了副作用操作（如 `#io`）。請移除副作用操作，或將環境標記為相應的效應標籤。 |
| **`#type_mismatch`** | 型別不匹配 | 值不符合其型別約束。請確保輸入數據符合 `@Type` 定義，或更新型別約束以適應數據。 |
| **`#projection_conflict`** | 型別投影衝突 | 合併兩個型別約束時發生投影衝突（如 `{ x: @int } & { x: @float }`）。整數與浮點數在譜幾何中屬於不同的子空間投影，無法同時滿足。請統一型別約束或使用 `@num` 萬有型。 |
| **`#no_context`** | 無上下文觀測 | 自由 `$` 在無綁定的觀測下被求值（**[SPEC_07](./SPEC_07_Logic_and_Pipe.md)** §1.2、**[SYNTAX_12](./SYNTAX_12_Pipe_Ternary_and_Context.md)**）。`$` 由最近包圍演化（pipe／dispatch）動態綁定；請將表達式置於管道右側，或改用具名路徑。 |

### 1.5 系統與特權操作 (System & Privileged Operations)

| 標籤 | 說明 | 修復建議 |
| :--- | :--- | :--- |
| **`#invalid_target`** | 無效的作業目標 | 系統操作（如 `rollback`）指向了不存在的目標。請檢查 Commit ID 或路徑是否正確。 |
| **`#already_exists`** | 目標已存在 | 試圖建立重複命名的資源。請更換名稱或刪除舊資源。 |
| **`#nothing_to_undo`** | 無可撤銷的操作 | `~%repl./undo` 被呼叫，但當前工作階段沒有可回退的演化歷史。 |
| **`#privileged_required`** | 需要特權模式 | 進行了受限操作（如 `#pin`）。請在啟動引擎時開啟特權模式或提供有效的 Token。 |
| **`#blocked_by_policy`** | 被策略黑名單阻擋 | 套件或來源被當前環境的信任鏈策略阻擋。請檢查 **[REAL_01](./REAL_01_Ouroboros_Engineering.md)** 中的信任配置。 |
| **`#ffi_panic`** | 外部函數崩潰 | 外部函數執行過程中發生崩潰 (Panic)。請檢查 FFI 實作的穩定性。 |
| **`#ffi_malformed`** | 外部回傳格式錯誤 | FFI 回傳的數據結構不符合 `n/` 的物理規範。請確保外部映射邏輯正確。 |

---

## 2. 診斷流程建議

當觀測到 `%cause` 時，建議遵循以下步驟進行偵錯：

1.  **檢查 `%val`**：確定衝突的本體論分類。
2.  **觀測 `path`**：定位衝突發生的精確幾何位置。
3.  **分析 `parent`**：追蹤因果鏈，判斷是直接衝突還是由底層合併引發的連鎖反應。
4.  **利用 `details`**：獲取標籤特定的診斷數據（如 `#conflict` 的左/右運算元）。

---

> [!NOTE]:
> - **[SPEC_08: 計算視界與運行時](./SPEC_08_Meta_and_Runtime.md)**
> - **[REAL_04: 因果結構](./REAL_04_Causal_Chain_Protocol.md)**
