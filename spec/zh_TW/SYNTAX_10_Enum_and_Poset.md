# SYNTAX_10：Enum／Poset 字面量 (Enum & Poset Literals)

> [!NOTE] 定位
> 本章為**語法細則**（規範性，位階在 SPEC 之下；見 **[SYNTAX_00](./SYNTAX_00_Conventions.md)**）。Enum 語義（對標籤施加偏序的 Combo）以 **[SPEC_03](./SPEC_03_Combo_System.md) §5.1**、序位錨點以 **[SPEC_01](./SPEC_01_Foundation_and_Lattice.md) §2.6** 為準；設計決議源自 `discussion/008`。本章釘死 **`#{}` Poset 字面量、序位鏈、`<=>` 方向探測、與 `%rank` 的地位**。（2026-07-05 新寫；文法同步補入 SPEC_14 §2.4。）

---

## 1. 語法 (Syntax)

```ebnf
;; Poset 字面量：一等公民結構（與 {}／[]／@{} 平級）
poset_lit   = { "#{" ~ WHITESPACE* ~ (order_chain ~ field_sep?)* ~ "}" }
order_chain = { poset_node ~ (order_op ~ poset_node)+ }
order_op    = { "<=" | ">=" | "=" | "<" | ">" }      ;; 序位關係＝格論家族五符號（008 §2；2026-07-05 == 改 =）
poset_node  = { tag_start | tag_end | tag }

;; 方向探測運算子（表達式層，L11 cmp 槽；最長匹配先於 <=）
cmp_op      = { "<=>" | "<=" | ">=" | "==" | "!=" | "=" | "<" | ">" }
```

| 寫法 | 意義 |
| :--- | :--- |
| `#{ #a <= #b < #c }` | Poset 字面量：宣告標籤間的偏序鏈 |
| `#{ #a < #c, #b < #c }` | 多鏈（DAG：多對一／一對多皆可） |
| `#{ #a = #b }` | 同序位宣告（`=`＝格論相等；`==` 不得入鏈） |
| `x <=> y` | **方向探測**：回傳序位標籤（聯集態），非布林 |
| `#_|_`、`#_` | 序位錨點 Start／End（隱式封箱，見 §4 #7） |
| `Status.#draft` | 以路徑存取 Enum 成員（tag 路徑段） |

---

## 2. 語義 (Semantics)

1. **`#{}` 宣告的是關係，不是資料。** Poset 字面量只含**序位鏈**；資料維度分開宣告、以 `&` 合併（**維度分離**，008 §2）：
   ```nlang
   ~Status: #{ #draft <= #review < #publish }
   ~Status: { current: #draft }        ;; 兩欄自動合併：序位 & 資料
   ```
2. **序位是容器局部的。** `#tag` 是全域原子，但序位關係定義於容器內：`workflowA.#draft` 與 `workflowB.#draft` 的序位**互相獨立**；跨容器序位比較幾何上無意義（008 §1；見 §4 #3）。
3. **雙軌比較（008 §3）。** 軌道一：`<=` 等格論關係（SYNTAX_06）——回傳布林。軌道二：`<=>` 方向探測——回傳**序位標籤聯集**：純態 `#lt`／`#gt`／`#eq`／`#un`（不可比）；非嚴格關係以聯集表達（如 `#le` ≡ `#lt | #eq`）。
4. **`%rank` 是引擎內部衍生屬性（008 §4）。** 底層以累積聯集／稠密座標支援比較；使用者**應**使用 `<=`／`<=>` 而非直接讀寫 `%rank`。稠密座標保證中途插入新狀態不位移既有 `%rank`（CAID 穩定性）。
5. **Poset 合併＝關係聯集；矛盾坍縮。** 兩個 `#{}` 交集（`&`）取關係之聯集；出現矛盾（`#a < #b` 遇 `#a > #b`）坍縮為 `_|_`（`%cause: #order_conflict`，008 意見 #5）。

---

## 3. 範例 (Examples)

```nlang
~Status: #{ #draft <= #review < #publish }
~Status: { current: #draft }

ok:  ~Status.#draft <= ~Status.#publish    ;; #true（格論軌）
dir: ~Status.#draft <=> ~Status.#publish   ;; #lt（方向軌，純態）
le:  ~Status.#draft <=> ~Status.#review    ;; #lt | #eq（<= 宣告 ⟹ 非嚴格：聯集態）

;; 匿名 poset 當場傳遞（008 意見 #3）
prio: /sort_by #{ #high < #mid < #low } items
```

---

## 4. 邊界情況 (Edge Cases)

1. **`#{` 是獨立 token 序列，與 `@{}`／`{}`／`#tag` 不混淆。** `#` 後接 `{` 不構成標籤（`tag = "#" ~ ident`，`{` 非 ident 起首）；`#{}`（空 poset）宣告空關係集，**不是** `_|_`（`@{}` 才是 Bottom，SYNTAX_02 §4.1）。
2. **鏈中每對相鄰節點構成一條關係；方向可混寫。** `#a < #c > #b` 宣告 `#a < #c` 與 `#c > #b`（即 `#b < #c`）——DAG 的分叉／匯流以多鏈或混向鏈表達皆可。`order_chain` 至少一個 `order_op`（單一 tag 不成鏈——要宣告成員存在而無序位，放資料維度）。
3. **跨容器 `<=>` → `_|_`，同容器不可比 → `#un`。** 同一 poset 內無路徑相連的兩標籤，`<=>` 回傳 `#un`（合法觀測結果）；**跨容器**的序位比較是幾何錯誤，坍縮 `_|_`（008 §1）。
4. **`<=>` 回傳標籤（聯集態），永不回傳布林。** 勿把 `<=>` 的結果直接當條件；轉布林經 `~%Logic`／分派表（`{#lt: …, #eq: …}`）。`<=>` 於 cmp 槽（L11）**非鏈式**（`a <=> b <=> c` 非法，同 SYNTAX_06 §1 注意）。詞法最長匹配：`<=>` 先於 `<=`。
5. **同序位用 `=`（格論家族），不用 `==`。** poset 鏈中 `#a = #b` 宣告兩標籤同序位（別名／同格）。序位關係一律取**格論／集合家族**五符號 `< <= = >= >`（SYNTAX_06 §1）；`==`／`!=`（塌縮家族）**不得**入鏈。（2026-07-05 使用者裁決：008 起草時比較兩家族尚未分離、`==` 曾雙義；分離後 `=` 因賦值實為 `:` 而空缺，正好歸位——序位宣告本就是集合語義，不塌縮。）
6. **`%rank` 使用者不應寫入。** 屬引擎衍生屬性（SYNTAX_08 自省類的寫入協商適用）；宣告序位的唯一正典寫法是 `#{}` 鏈。
7. **錨點隱式封箱。** 每個 poset 隱含 `#_|_ <= 每個成員 <= #_`（008 意見 #2：全域歸一化）；鏈中可顯式使用錨點（如 `#_|_ < #init`），不改變隱式封箱語義。
8. **Enum 成員以 tag 路徑段存取。** `Status.#draft` 合法（路徑段接受 tag，2026-07-05 收編入 SPEC_14 §2.4 path）；List 投影**已有結論**（SPEC_03 §5.4）：Enum 於 `#total_ordered` 狀態下經 **`~%Enum./toList`** 顯式轉換為 List——走 library 顯式轉換，**無**語法級投影（`Status[0]` 不直接可用；先 `/toList` 再索引）。
9. **序位鏈只住在 `#{}`。** 一般 `{}`／`{{}}` 內**不得**書寫裸序位鏈（`{ #a < #b }` 非法）——關係維度一律經 `#{}` 宣告再合併（引擎現況的 in-combo `order_relation` 為過渡實作，將收斂至本規則）。

---

## 5. 對應 (See Also)

- 上位文法：**[SPEC_14](./SPEC_14_Formal_Grammar.md) §2.4**（`poset_lit`、`cmp_op` 含 `<=>`、path tag 段）。
- 語義：**[SPEC_03](./SPEC_03_Combo_System.md) §5.1**（Enum 本體）、**[SPEC_01](./SPEC_01_Foundation_and_Lattice.md) §2.6**（序位錨點）。
- 鄰章：**[SYNTAX_02](./SYNTAX_02_Literals_and_Atoms.md)**（`#tag`／錨點原子）、**[SYNTAX_06](./SYNTAX_06_Comparison_and_Subtyping.md)**（雙軌比較的布林軌）、**[SYNTAX_08](./SYNTAX_08_Metadata.md)**（`%rank` 寫入協商）。
- 設計紀錄：`discussion/008`（雙軌決議、稠密座標、DAG）。
