# REAL_04：因果鏈協議 (OODP Causal Chain Protocol)

> [!NOTE]: [Standard / 規範性標準]  
> 本協議統一定義 **OODP (Ouroboros Discovery Protocol)** 中 `%cause` 元欄位的物理結構與所有標準化的因果標籤（Cause Tags）。

基於 **觀測對偶性 (Observation Duality)**，`%cause` 既是一個可直接比較的標籤，也是一個包含豐富診斷資訊的封閉結構。

**本文定位**：
- **層級**：OODP 跨層級基礎設施（用於 L3-L5 的錯誤傳播與診斷）
- **上游**：SPEC_13 (發現語義)、SPEC_08 (視界管理)
- **下游**：REAL_02 L3 (收斂層衝突處理)

> 關於 OODP 五層架構的完整定義，請參閱 **[SPEC_13: 銜尾蛇發現協定](./SPEC_13_Ouroboros_Discovery_Protocol.md)** §0。

---

## 1. 標準結構 (Standard Structure) — 調和裁定 2026-07-19

`%cause` 是一個 **Cocoon**(封閉結構)。**正典核**:

```nlang
%cause: {{
    ;; 核心對偶欄位 (Duality Core) —— 唯一必備欄
    %val:       #Tag    ;; 因果標籤 (如 #conflict)。直接觀測 %cause 時
                        ;; 依值語境律 (SYNTAX_06 §4 #6) 坍縮返回此值;
                        ;; <<path>> 結構視圖保全整繭。

    ;; 診斷欄位 (Diagnostics) —— 全部可選、%-前綴 (meta 軸),
    ;; 依 ERROR_CODES 類別容許變形 (不同因果類鑄不同欄集)
    %message:   @str    ;; 人類可讀描述
    %expected:  @any    ;; 期望值/形 (衝突類)
    %found:     @any    ;; 實際值/形 (衝突類)
    %involved:  [@str]  ;; 參與節點 CAID (重現用)
    %path:      @str    ;; 觸發座標路徑 (座標缺失類,如 #missing_key)
    %members:   [@str]  ;; 環成員 (來歷類,如 #static_cycle)
}}
```

**三條調和法**(2026-07-19 裁定,A 案):

1. **欄位走 meta 軸**:診斷欄一律 `%`-前綴。因果是 meta,裸名欄
   會把診斷資料放進封閉繭的資料軸。
2. **`%type` 廢止**(設計考古:`%type` 是舊代節點模型殘欄——
   型別內容曾放 `%type` 欄,後由同構原理 SPEC_03 §4 的
   `%kind` + `%super`〔+ `%name`;`%predicate` 退場→R2〕取代;
   cause 繭的 `%type` 與
   `%val` 恆同值,是化石雙帳)。`%val` 為唯一對偶核;`.%type`
   讀法一併退役——⊥ 上的 `.%type` 依 ⊥ 合成性原樣傳出,
   `#blur` 上依座標吸收律吸收(SPEC_08 §3.2.2 同步)。
3. **鷹架不可見**:引擎為防剝殼等目的所需之內部墊欄(如
   `_: _`)是實作細節,**不得出現在任何用戶可見投影**(結構視圖
   `<<x>>` 含);用戶自定欄(含名為 `_` 之欄)不受影響。

> **非規範性附註(未來診斷擴充)**:定位欄(path/source/line/
> column)、語境欄(operation/operands)、鏈結欄(parent/trace)、
> 擴展欄(details)曾列於舊版本節——引擎從未鑄造,現降級為
> 未來擴充候選;引擎開始追蹤時再立法,屆時亦走 `%`-前綴。

---

## 2. 因果標籤分類 (Cause Tag Taxonomy)

> **正典登記簿 = [ERROR_CODES](./ERROR_CODES.md)**(2026-07-17 裁定):標籤
> 清單的**唯一維護點**。本節只立**類別法**,不再重複列表——雙帳必漂移,
> 本節舊表曾落後法典多輪(缺 `#missing_key`/`#private_access_violation`/
> `#no_context`/`#system_reserved`/`#static_cycle` 等)即為病例。

所有標籤分為**六大類別**:

| 類別 | 定義 | 例(詳見 ERROR_CODES) |
| :--- | :--- | :--- |
| **格論衝突** | 靜態邏輯不相容、動態非終止 | `#conflict`、`#numerical_error`、`#divergent`、`#order_conflict` |
| **視界與資源邊界** | 觀測預算耗盡;`#blur` 快照之 `%cause` 同拼此類(視界傳播律=本體地位不可互鑄、runaway 誠實 `#fuel_exhausted`,SPEC_08 §3.2.2) | `#fuel_exhausted`、`#timeout`、`#out_of_horizon` |
| **存取與所有權違規** | 幾何邊界/所有權侵犯 | `#private_access_violation`、`#system_reserved`、`#missing_key`、`#no_context` |
| **來歷類(非錯誤)** | 觀測性來歷標籤,值本身合法 | `#static_cycle`(Top)、BlurCause 家族 |
| **引擎作業錯誤** | 不鑄 `_|_`,走 Err 通道/CLI exit | `#invalid_target`、`#privileged_required`、`#ffi_panic` |
| **登記在案未鑄** | 法典保留,引擎現以他標籤覆蓋或未實作 | `#incomplete`、`#max_*` 家族(現以 `#fuel_exhausted` 覆蓋,G3 之 R3 法理)、`#effect_violation` |

> 註:`#invalid_path` 為未立法之引擎誤鑄,2026-07-14 廢止(座標缺失=開放
> `_`;`^` 溢出=`#out_of_horizon`;聯集全 `_|_`=§4 主因果);存量宇宙解碼
> 保留讀取。`#not_found` 屬**發現與內容驗證類**(ERROR_CODES §1.3,LADD
> 語境)——不屬值收斂因果,故自 §4 主因果優先級移出(非除籍)。

---

## 3. 標籤特定詳細結構 (Tag-Specific Details)

> **非規範性(2026-07-19 調和註)**:本節 `details` 結構屬舊版理想形,
> 引擎從未鑄造(同 §1 附註之未來擴充候選);現行診斷欄=§1 正典核。
> 保留作未來擴充藍圖;立法時走 `%`-前綴。

### 3.1 `#conflict` 詳細結構
```nlang
details: {{
    left:       @any        ;; 左運算元值
    right:      @any        ;; 右運算元值
    left_type:  @any        ;; 左運算元型別約束
    right_type: @any        ;; 右運算元型別約束
    merge_path: @str        ;; 衝突發生的相對路徑
}}
```

### 3.2 `#out_of_horizon` 詳細結構
```nlang
details: {{
    requested_depth: @int    ;; 請求的穿透深度 (如 ^^^^ 為 4)
    actual_depth:    @int    ;; 當前環境中可供穿透的最大深度
}}
```

---

## 4. 因果鏈組合規則 (Causal Chain Composition)

當收斂過程中多個衝突同時發生時,引擎必須選出一個作為「主因果標籤」返回。優先級(2026-07-17 重立法,對齊實作五階;舊列 `#effect_violation` 屬登記未鑄類、`#not_found` 屬發現類非值收斂因果,俱移出):

1. `#divergent` > 2. 存取與所有權違規(`#private_access_violation`/`#system_reserved`)> 3. 格論衝突族(`#conflict`/`#numerical_error`/…)> 4. 視界資源族(`#fuel_exhausted`/`#timeout`/`#out_of_horizon`)> 5. 座標缺失(`#missing_key`)。

> **工程補充(2026-07-17,G4 惰性 ⊥ 收帳)**:聯集全 ⊥ 支坍縮時,結果為**主因果位階最高成員的 `_|_` 原樣傳出**(訊息/座標/涉入項保全;同位階取相遇序最左)——不得改鑄僅存標籤的新 `_|_`(blur 吸收原樣先例 + 誠實訊息方向,cause 正典審計 T3 同族)。

> **`#blur` 之投影(2026-08-10 增,O46)**:一個 `#blur` 可攜帶**多筆視界記錄**
> (合併兩個 `#blur` ＝ 記錄集合取聯集,見 REAL_03 §7.3)。`.%cause` 觀測仍**回單一標籤**,
> 依本節優先級自該集合投影而得。
> **同位階時,`#blur` 取記錄集合的正準序最前者,不取相遇序**——相遇序是運算元的書寫位置,
> 而 `%cause` 進入 CHS ⟹ 進入身分,於是 `x & y` 與 `y & x` 會得到不同的地址,
> 合併不再交換。**本款只治 `#blur`;上一款對 `_|_` 的「相遇序最左」不變**
> (⊥ 的訊息/座標本就不進 CAID 之外的判定,不受此害)。

---

## 5. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_03](./SPEC_03_Combo_System.md)** | Cocoon 結構定義 `%cause` 的封閉性。 |
| **[SPEC_05](./SPEC_05_The_Trinity_Isomorphism.md)** | `%val` 如何驅動觀測對偶性。 |
| **[SPEC_08](./SPEC_08_Meta_and_Runtime.md)** | 運行時如何生成本標準定義的報告。 |
