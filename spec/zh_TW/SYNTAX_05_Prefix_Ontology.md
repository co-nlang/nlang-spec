# SYNTAX_05：前綴本體論 (Prefix Ontology)

> [!NOTE] 定位
> 本章為**語法細則**（規範性，位階在 SPEC 之下；見 **[SYNTAX_00](./SYNTAX_00_Conventions.md)**）。文法上位規範見 **[SPEC_14](./SPEC_14_Formal_Grammar.md) §2.2**；三位一體（Data／Type／Logic 同構）語義以 **[SPEC_05](./SPEC_05_The_Trinity_Isomorphism.md)** 為準；`%` 語義見 **[SPEC_08](./SPEC_08_Meta_and_Runtime.md) §1**；序列化／CAID 正規序見 **[REAL_03](./REAL_03_CAID_Protocol.md)**。本章釘死**前綴如何選定座標的本體論維度**。

---

## 1. 語法 (Syntax)

前綴接在識別碼之前，選定座標的**本體論分流**。摘自 **SPEC_14 §2.2**（2026-06 收緊後的結構化文法）：

```ebnf
prefix = @{ prefix_system | prefix_meta | (prefix_local ~ (prefix_type | prefix_logic)?) | prefix_type | prefix_logic }
prefix_type = "@"   prefix_logic = "/"   prefix_meta = "%"   prefix_system = "~%"(atomic)   prefix_local = "~"
```

合法前綴**僅以下八種**（含無前綴）；其餘組合（如 `%@`、`~%/`、`@/`）**非法**：

| 前綴 | 維度 | 意義 |
| :--- | :--- | :--- |
| （無）`a` | **Data** | 座標的存在與狀態 |
| `@a` | **Type** | 幾何約束（邊界） |
| `/a` | **Logic** | 變換分派（態射） |
| `~a` | Data（隱藏） | 局部私有的資料面向 |
| `~@a` | Type（隱藏） | 局部私有的型別面向 |
| `~/a` | Logic（隱藏） | 局部私有的邏輯面向 |
| `%a` | **Meta** | 元資訊（僅 Combo/Data，無子面向） |
| `~%a` | **System** | 系統／標準庫（atomic，僅 Combo/Data） |

---

## 2. 語義 (Semantics)

1. **三位一體（Data／Type／Logic）。** `a`／`@a`／`/a` 是**同一個 CAID 的三個面向**——資料（存在）、型別（邊界）、邏輯（變換）。前綴選維度、不改名字。同構語義以 **SPEC_05** 為準。
2. **`~` 是隱藏／封裝修飾，可疊在三位一體上。** `~`／`~@`／`~/` 給出三面向的「隱藏」版本。但**格論／CAID 本質上沒有可真正「隱藏」之物**；`~` 因此保留給類物件導向的**封裝性**，目前在 `n/` 只影響**路徑可達性**（見 **[SPEC_04](./SPEC_04_Navigation_and_Duality.md) §3.1**），不改變內容或 CAID。
3. **`%` 是元資訊維度——只有 Data/Combo，沒有 Type/Logic。** 故只有 `%a`，**沒有** `%@a`／`%/a`（雖三者同構，`%` 本身是一個 Combo 面向）。`%` 是執行期與 `oo` 引擎交換資訊最直觀的通道：多數欄位**可寫**（不限唯讀）。除規格釘死者（如 `%id`、`%cause`）外，引擎**可**自訂自己的 `%` 欄位——這是規格保留給實作的彈性（見 **SPEC_08 §1**，寫入一致性見 SYNTAX_08）。
4. **`~%` 是系統維度——atomic，同樣只有 Combo/Data。** 故只有 `~%a`，**沒有** `~%@a`／`~%/a`。概念上「（每個）local ＋（都具有的）meta ＝ system」也說得通，但語法上 `~%` 是單一前綴，**不**拆成 `~`＋`%`。
5. **正規前綴序（CAID 決定性）。** 序列化時欄位按前綴正規序排序；8 種前綴的完整順序以 **[REAL_03](./REAL_03_CAID_Protocol.md)（序列化前排序表）為唯一權威**（本章不重列，避免漂移）。書寫順序無關（SYNTAX_03），序列化採此正規序。

---

## 3. 範例 (Examples)

### 直覺對照：前綴 ≈ 副檔名＋隱藏檔

| n/ | 檔案系統 | 說明 |
| :--- | :--- | :--- |
| `a` / `@a` / `/a` | `a.txt` / `a.jpg` / `a.m4a` | 不同「副檔名」＝同名不同面向；可用他者工具開啟（這正是同構） |
| `~a`（`~@a`／`~/a`） | `.a`（隱藏檔，如 `.git`） | n/ 把 unix 點開頭隱藏檔符號化為前綴 `~`；可疊在三面向上 |
| 把 `~%Lib` 交集進路徑欄位 | `import` 一個函式庫 | `n/` **無 import 關鍵字**——交集即匯入 |

```nlang
a: 1            ;; Data
@a: @int        ;; Type（同名）
/a: /increment  ;; Logic（同名）
~tmp: "scratch" ;; Local（隱藏資料）
%kind: #data    ;; Meta

;; 「import」= 把標準庫交集進來（無 import 關鍵字，見 SPEC_09）
_: ~%Cond
total: ~%Math./sum xs
```

---

## 4. 邊界情況 (Edge Cases)

> 逐條釘死前綴層的寫法。

1. **同名異前綴共存。** `a`、`@a`、`/a`（及其 `~` 隱藏版）可在同一容器中**並存**——同一座標的不同面向，索引不同表，**不**互相覆寫。這與「同名同前綴重複賦值＝交集」（SYNTAX_03 邊界 #2）不同。
2. **前綴組合是結構化的，不是自由疊加。** 合法組合**僅** §1 的八種：三位一體 `{Data, @, /}` 可加隱藏修飾 `~`（→ `~`／`~@`／`~/`）；`%` 與 `~%` 是獨立維度，**不**與三位一體組合。故 `%@a`、`~%/a`、`@/a`、`@%a` 等**皆非法**（2026-06 收緊，SPEC_14 §2.2）。
3. **`~%` vs `~`：最長匹配。** `~%` 是**單一 atomic 前綴**（系統），文法**必須**先於 `~` 匹配：`~%Math` 是系統命名空間，`~x` 才是隱藏／局部。（與 `;;`／`;` 同理，SYNTAX_01 邊界 #2。）**所有權**：`~%` 唯引擎鑄造——使用者 LHS 寫入任何 `~%` 座標違法（root＝evolve 邊界報錯、combo 鍵＝⊥ `#system_reserved`；`~%Config` 規範家豁免）；拼法合法、違法在語義層。見 **SPEC_09** 所有權條款（2026-07-16）。
4. **`/a` 邏輯鍵 vs `/f` 態射應用。** 鍵位 `/a:`（邏輯面向，本章）與表達式中 `/f arg`（態射應用，SYNTAX_09）由**位置**區分。
5. **`@a` 型別前綴 vs `@{ }` 匿名集合。** `@` 接識別碼是型別前綴；`@` 接 `{` 是匿名集合（SYNTAX_04）。
6. **沒有 import 關鍵字。** 匯入即「把 `~%` 標準庫物件**交集**進一個路徑欄位」（範例見 **SPEC_09** §5.2）。`n/` **嚴禁**期待 `import`／`use`／`require` 等關鍵字。

---

## 5. 對應 (See Also)

- 上位文法：**[SPEC_14](./SPEC_14_Formal_Grammar.md) §2.2**（結構化前綴）。
- 語義：**[SPEC_05](./SPEC_05_The_Trinity_Isomorphism.md)**（三位一體同構）、**[SPEC_08](./SPEC_08_Meta_and_Runtime.md) §1**（`%` 元資訊）、**[SPEC_04](./SPEC_04_Navigation_and_Duality.md) §3.1**（`~` 路徑可達性）、**[REAL_03](./REAL_03_CAID_Protocol.md)**（正規前綴序）。
- 鄰章：**[SYNTAX_03](./SYNTAX_03_Paths_and_Assignment.md)**、**[SYNTAX_04](./SYNTAX_04_Combo_Construction.md)**（`@{}`）、**[SYNTAX_08](./SYNTAX_08_Metadata.md)**（`%` 細則）、**[SYNTAX_09](./SYNTAX_09_Morphism_Application.md)**（`/f`）。
- 系統庫與「交集即匯入」：**[SPEC_09](./SPEC_09_Standard_Library.md)**。範式：**[APP_03](./APP_03_Paradigm_Comparison.md)**。
