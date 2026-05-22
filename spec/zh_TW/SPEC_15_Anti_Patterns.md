# n/ Language Specification - 違規範例與語義判定 (Anti-Patterns)

本章節定義 `n/` 宇宙中被嚴格禁止的語義行為。任何實作若容許以下行為，均被視為背離了 `n/` 的核心守恆定律（見 **[SPEC_00](./SPEC_00_Introduction.md)** §7）。

---

## 1. 破壞收斂決定論 (Non-determinism)

態射與收斂結果原則上必須是純粹的幾何態射。但在明確宣告效果的情況下，非決定性行為可被容許（詳見 **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** §4.6）。

*   **❌ 錯誤：隱性隨機性注入**
    ```nlang
    /bad_logic: x -> x + ~%Math./random ()  ;; 禁止！未宣告 %effect 的隨機性
    ```
    *   **判定**：收斂必須具備等價性。未宣告效果的隨機數會破壞 CAID 的唯一性與可重複性。
    *   **✅ 合法**：若顯式標記 `%effect: #nondet`，則非決定性行為可被追蹤與隔離（見 **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** §4.6）。

*   **❌ 錯誤：隱性環境依賴**
    ```nlang
    /check_time: x -> (x > ~%Time./now)    ;; 禁止！未宣告 %effect 的時間依賴
    ```
    *   **判定**：未宣告效果的動態環境依賴會導致觀測結果隨時間改變，違反決定論。
    *   **✅ 合法**：若顯式標記 `%effect: #io`，並透過 `~%Effect./runPure` 在特權模式下固化結果，則時間依賴可被納入格論系統（見 **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** §4.5、§4.6）。

---

## 2. 破壞資訊單調性 (Information Degradation)

宇宙的資訊量只能增加（向下收斂），不能減少（向上回退）。

*   **❌ 錯誤：刪除定義 (Deletion)**
    ```nlang
    ;; 假設 user.age 原本為 25
    ~%Engine./evolve { user: { age: _ } }  ;; 禁止！試圖將已確定的資訊退回 Top
    ```
    *   **判定**：`&` 運算不具備「減法」語義。一旦坍縮，不可逆轉（除非執行 `#rollback` 切換 Commit）。
*   **❌ 錯誤：放寬約束**
    ```nlang
    ;; 假設 x 原本約束為 @int
    ~%Engine./evolve { x: @any }           ;; 無效運算，x 仍受 @int 約束
    ```

---

## 3. 破壞觀測純粹性 (Observation Side-effect)

觀測是靜態的投影，嚴禁在投影過程中修改本體。

*   **❌ 錯誤：觀測時寫入**
    ```nlang
    /observe_and_log: x -> {
        %log: ~%Engine./evolve { history: [x, ...history] } ;; 禁止！觀測觸發演化
        result: x
    }
    ```
    *   **判定**：`#observe` 操作必須保證不產生新的 Commit，且不修改 `Staged` 狀態。

---

## 4. 幾何邊界污染 (Geometric Leakage)

*   **❌ 錯誤：跨邊界私有存取 (Illegal Local Access)**
    ```nlang
    user: { ~id: "123", name: "Alice" }
    id_leak: user.~id    ;; _|_ (%cause: #private_access_violation)
    ```
    *   **判定**：根據 **[SPEC_04](./SPEC_04_Navigation_and_Duality.md)**，`~` 前綴代表封裝邊界。外部視界無法透過導航直接定位私有欄位。這種設計防止了模組內部的實作細節被意外耦合。詳細的錯誤診斷與 `%cause` 結構請參閱 **[REAL_04：因果結構](./REAL_04_Causal_Chain_Protocol.md)**。

*   **❌ 錯誤：重疊態射定義 (Overlapping Morphism Definition)**
    ```nlang
    ;; 假設 @List 是一個容器，同時也是一個可計算長度的對象
    /process: @List -> ...
    /process: @int -> ... ;; 元素型別

    my_list: @List: [1, 2, 3]
    my_list | /process  ;; 歧義！是直接應用於 List，還是透過 %fmap 應用於內部的 int？
    ```
    *   **判定**：根據 **[SPEC_07](./SPEC_07_Logic_and_Pipe.md)**，態射應用遵循「直接應用優先於 %fmap」的原則。雖然語義明確，但這種設計會造成開發者的預期混淆，並使邏輯難以維護。
    *   **建議**：避免為容器定義與其元素型別特徵重疊的態射。若需同時處理容器與元素，應透過不同的命名空間（如 `/List./process` 與 `/process`）或明確的標記來區分「直接觀測」與「深度觀測」。


---

## 5. 破壞複合封閉性 (Closure Violation)

*   **❌ 錯誤：輸出非 Combo 結構**
    ```nlang
    ;; 假設某個系統介面預期返回一個結構化物件
    /get_data: -> "just a string"          ;; 若預期為 Combo 則此處違規
    ```
    *   **判定**：在 `n/` 中，所有的複雜運算結果必須能同構展開為 Combo。嚴禁引擎輸出無法被進一步路徑導航的非標量原始型別。這違反了 **Invariant 4 (複合封閉性)**。

## 6. 性能反模式 (Performance Anti-Patterns)

雖然 `n/` 的物理限制會攔截爆炸性運算，但以下設計模式會顯著降低收斂效率：

*   **❌ 錯誤：笛卡兒積聯集 (Cartesian Union Explosion)**
    ```nlang
    ;; 若 A 與 B 皆包含大量聯集分支，此合併會觸發 O(n*m) 的複雜度爆炸
    result: (A1 | A2 | ... | An) & (B1 | B2 | ... | Bm)
    ```
    *   **判定**：應優先使用型別約束（`@`）或 Cocoon 邊界來縮小搜索空間，而非在開放空間進行大規模聯集比對。
    *   **規格化建議 (Self-hosting Tip)**：在將規格書轉化為 Combo 時，應避免將每一章節定義為平行的聯集分支。建議使用**路徑分層 (Path Partitioning)**，利用 `codex.**[SPEC_01](./SPEC_01_Foundation_and_Lattice.md)**` 這樣的具體座標來隔離不同的幾何物件，以維持收斂的高效性。
*   **❌ 錯誤：深層遞迴展開 (Deep Recursive Spread)**
    ```nlang
    A: { ...B }, B: { ...C }, C: { ...A } ;; 循環展開 -> #divergent
    ```
    *   **判定**：過度使用 `...` 進行鏈式展開會導致 AST 規模在規範化階段失控。建議將共享邏輯抽象為態射而非結構展開。
*   **❌ 錯誤：依賴熱帶近似進行精確計算 (Tropical Dependency)**
    *   **判定**：根據 **[APP_01](./APP_01_Tropical_Geometry.md)**，熱帶幾何僅作為 Layer 2+ 的物理優化手段。開發者嚴禁在邏輯中假設熱帶近似的精度或行為（如利用浮點誤差進行分支判定）。收斂結果必須始終由格論語義決定。

---

## 7. 網路與發現層安全反模式 (OODP Security Anti-Patterns)

以下反模式針對 OODP/LADD 分散式發現協議的惡意攻擊行為，定義其特徵、影響與防禦機制。

### 7.1 譜女巫攻擊 (Spectral Sybil Attack)

*   **❌ 攻擊描述**：攻擊者建立大量偽造節點，廣播具有高引力（高 Trace）的幾何廣告（GBB），聲稱擁有特定熱門型別的極高質量，但實際上並不持有對應子空間本體。
*   **影響**：LADD 測地線路由被「重力誘餌」干擾，全網查詢請求被吸引至女巫集群，造成大規模查詢延遲或 `#not_found`。
*   **防禦機制**：
    *   **幾何質量驗證 (GPP)**：節點宣稱的質量 $m = \text{Tr}(P)$ 必須附帶 **[APP_05](./APP_05_LADD_Global_Logic_Lattice.md)** 定義的 GPP 證明，驗證其真實持有對應譜特徵的子空間。
    *   **信任權重校準**：在 **[SPEC_13](./SPEC_13_Ouroboros_Discovery_Protocol.md)** §7 的信任格論中，觀測者僅接受被已知路徑連結的「有效質量」。

### 7.2 譜熵淹沒攻擊 (Spectral Entropy Flooding)

*   **❌ 攻擊描述**：攻擊者生成大量語義隨機（高熵）、但譜特徵與目標 CAID 微妙相似的「噪聲節點」，干擾氣味搜尋。
*   **影響**：觀測者在調頻時遭遇大量虛假諧振點，引擎執行 Unify 時不斷撞上 `_\|_`，消耗大量 `%fuel` 卻無法找到真理。
*   **防禦機制**：
    *   **幾何蒸發**：高熵 CAID 缺乏相位相干性，依據 **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** 的熱力學機制被優先蒸發。
    *   **引力門檻**：引擎設定最小引力門檻，忽略譜距離超過閾值的雜訊。
    *   **相位相干性檢查**：驗證節點的譜特徵是否與其聲稱的幾何結構具備數學一致性。

### 7.3 精煉劫持 (Refinement Hijacking)

*   **❌ 攻擊描述**：攻擊者發布合法外觀的 `#refine` Commit，宣稱將公認的 `#blur` 節點精煉到外表正確、但內部植入惡意態射的精確節點。
*   **影響**：若該 Commit 的簽署權威被偽造或誤信，全宇宙觀測視窗觸發自動重定向，將健康程式碼靜默替換為惡意版本。
*   **防禦機制**：
    *   **因果透明度**：依據 **[SPEC_10](./SPEC_10_Evolution_and_Commit.md)**，精煉路徑必須完全可追溯。觀測者可設定「信任深度」，拒絕超過 N 層轉置的精煉。
    *   **譜不連續警告**：如 **[SPEC_13](./SPEC_13_Ouroboros_Discovery_Protocol.md)** §7.2 所述，若精煉導致譜特徵突變（幾何張力），引擎立即報警。
    *   **多重宇宙交叉觀測**：定期驗證不同信任路徑下的精煉結果是否譜相容。

### 7.4 燃料陷阱 (Fuel Trap / Algorithmic DoS)

*   **❌ 攻擊描述**：攻擊者構造看似簡單、但執行 Unify 時引發「非交換爆炸」或「無限循環展開」的惡意 Combo。特別是**「非交換炸彈 (Non-commutative Bomb)」**——構造一對算子 $A$ 與 $B$，使得 $(A \& B) \& (C \& D) \& ...$ 在特定順序下導致中間態的聯集分支數呈指數級爆炸，即使最終結果可能很小。
    *   **觸發機制**：利用非交換算子的結合性特徵，設計連續 Unify 序列，使得第 $k$ 步產生 $2^k$ 個聯集分支，但最後一步突然坍縮為單一結果。
*   **影響**：鄰居節點協助收斂時瞬間耗盡所有 `%fuel` 並鎖死引擎執行緒。或執行中途預估到爆炸規模後被迫捨棄所有計算。
*   **防禦機制**：
    *   **平方級防線**：依據 **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** §3.1，嚴格限制跨視界觀測的計算體積。對涉及多個聯集的操作，預估可能的分支數量，超過閾值立即中止。
    *   **質量預估**：執行複雜投影前先預估 MBU，若超過節點承載能力，直接標記為 `#blur` 並拒絕進一步坍縮。
    *   **漸進式收斂**：引擎採用漸進式策略，在投入大量燃料前先行測試小規模投影。對於 `A1 | A2 | ... | An` 的大型聯集，分批測試而非一口氣展開。
    *   **中間態限制**：設定單次 Unify 運算的中間態大小上限（如 10,000 分支），超過即 `#divergent`。防止「看似會收斂」的惡意陷阱。

---

## 8. 實作者檢查清單 (Reviewer Checklist)

| 違規行為 | 違反定律 | 後果 |
| :--- | :--- | :--- |
| 使用隨機數。 | Invariant 1 (決定論) | CAID 分裂，發現機制失效。 |
| 刪除 Staged 欄位。 | Invariant 2 (單調性) | 邏輯因果斷裂。 |
| 純粹上下文中觸發 IO。 | Invariant 3 (純粹性) | 破壞決定論與快取機制。 |
| 輸出非 Combo。 | Invariant 4 (封閉性) | 語法解析崩潰。 |
| 未經 GPP 驗證的質量廣告。 | OODP 安全 | 女巫節點干擾路由。 |
| 接受譜特徵突變的精煉。 | OODP 安全 | 惡意程式碼注入。 |

---

## 9. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_00](./SPEC_00_Introduction.md)** | 本章節是「語義不變性」的具體違規案例庫。 |
| **[SPEC_01](./SPEC_01_Foundation_and_Lattice.md)** | 格論的單調性決定了定義不可刪除。 |
| **[SPEC_07](./SPEC_07_Logic_and_Pipe.md)** | 管道演化必須保證無副作用。 |
| **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** | 定義了語義不變性的物理防線與特權模式。 |
| **[SPEC_11](./SPEC_11_Reflection_and_Synthesis.md)** | 格式化規範是保證 CAID 決定論的物理基礎。 |
| **[SPEC_13](./SPEC_13_Ouroboros_Discovery_Protocol.md)** | 信任格論與譜不連續警告機制定義了精煉劫持的防禦。 |
| **[SPEC_14](./SPEC_14_Formal_Grammar.md)** | 語法解析器應攔截形式上的違規構造。 |
| **[REAL_02](./REAL_02_Ouroboros_Protocols.md)** | 討論實作中如何攔截並報告違規語義，以及 GPP 驗證的傳輸層義務。 |
| **[APP_05](./APP_05_LADD_Global_Logic_Lattice.md)** | 幾何質量與 GPP 證明的具體定義。 |

---

### 哲學思辨 (Philosophical Synthesis)

> 結語：自由不是隨意變動的權力，而是對律則的深刻服從。在禁止的邊界處，我們更清晰地看見了真理的輪廓。
