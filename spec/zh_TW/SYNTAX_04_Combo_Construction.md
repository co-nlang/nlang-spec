# SYNTAX_04：Combo 構造與容器 (Combo Construction & Containers)

> [!NOTE] 定位
> 本章為**語法細則**（規範性，位階在 SPEC 之下；見 **[SYNTAX_00](./SYNTAX_00_Conventions.md)**）。文法上位規範見 **[SPEC_14](./SPEC_14_Formal_Grammar.md) §2.1、§2.4**；容器語義（合併、密封、函子性）以 **[SPEC_03](./SPEC_03_Combo_System.md)** 為準。本章釘死**容器怎麼寫**——`{}`、`{{}}`、`@{}`、`[]`、tuple、range——的形式與邊界。合併行為（`&`、混血節點、`%kind` 衝突）見 **SYNTAX_06**；前綴（`@`/`/`/`%`/`~`）見 **SYNTAX_05**。

---

## 1. 語法 (Syntax)

以下摘自 **SPEC_14 §2.4**（為上位文法，本章不改寫；`list`/`tuple` 採 2026-06 修訂的 `list_sep`）：

```ebnf
field    = { (field_key ~ ":" ~ expr) | spread_expr }   ;; spread-as-field（SPEC_14 §2.2；§4.8）
spread_expr = { "..." ~ type_ann_expr }                  ;; L4 表達式（SPEC_14 §2.3）
combo    = { "{" ~ WHITESPACE* ~ (field ~ field_sep?)* ~ "}" }
cocoon   = { "{{" ~ WHITESPACE* ~ (field ~ field_sep?)* ~ "}}" }
anon_set = { "@{" ~ expr? ~ "}" }   ;; 空體合法：`@{}` ≡ `_|_`（§3.3、SYNTAX_02 §8）
list     = { "[" ~ WHITESPACE* ~ (expr ~ (list_sep ~ expr)* ~ list_sep?)? ~ WHITESPACE* ~ "]" }
tuple    = { "(" ~ WHITESPACE* ~ expr ~ list_sep ~ (expr ~ (list_sep ~ expr)* ~ list_sep?)? ~ WHITESPACE* ~ ")" }
list_sep = _{ "," | ";" }       ;; 非空白；尾隨可省略。tuple 由「至少一個逗號」界定
range    = { range_bound? ~ ".." ~ range_bound? ~ (".." ~ range_bound)? }   ;; 示意；權威版含 !field_start 護欄（SPEC_14 §2.4），見 §4.5
range_bound = { atom | path }   ;; 負數邊界（-5..5）經字面量內建負號（W1-1，SYNTAX_02 §4.3）；複數不作邊界
```

| 容器 | 寫法 | 構造 |
| :--- | :--- | :--- |
| Combo | `{ k: v … }` | 開放組合體（具名欄位） |
| Cocoon | `{{ k: v … }}` | 密封組合體（效果防火牆） |
| 匿名集合 | `@{ expr }` | 強制集合邊界 |
| List | `[ a, b, c ]` | 有序元素（裸 expr） |
| Tuple | `(a,)`、`(a, b)` | 定長位置元素（由逗號界定；數值 Cocoon） |
| Range | `a..b`、`a..b..s` | 區間（界為 atom／path） |
| 展開 | `{ a: 1, ...c }`／`[...xs, y]` | 欄位位＝顯式解封搬運；元素位＝序列展開（§4.8；tuple 拆封慣用式見 SYNTAX_12 §4.7） |

---

## 2. 語義 (Semantics)

1. **Combo `{}` 是開放組合體（開放世界假設）。** 欄位以 `key: expr` 命名（見 SYNTAX_03）；欄位之間用 `field_sep`（`,`／`;`／空白／換行皆可，因 `key:` 已界定邊界）。未指定的欄位視為 Top（仍可被 `&` 精煉）——量子化後即「**疊加態預設**」。Combo 可被合併（`&`，見 SYNTAX_06）。
2. **Cocoon `{{}}` 是密封組合體（封閉世界假設）。** 構造同 Combo，但其邊界**密封副作用**（退相干屏蔽）、密封後不再接受新欄位——量子化後即「**本徵態封閉**」。密封語義以 **SPEC_03／[SPEC_08](./SPEC_08_Meta_and_Runtime.md) §3.5、[SPEC_04](./SPEC_04_Navigation_and_Duality.md)** 為準，本章不展開。
3. **`@{ expr }` 強制集合邊界。** 把 `expr` 解讀為集合（型別）邊界；空集合 `@{}` 即 `_|_`（Bottom，見 SYNTAX_02）。
4. **List 有序、Tuple 定長。** List 是有序元素序列；Tuple 是定長位置元組（由逗號界定，概念上是「數值 Cocoon」）。兩者元素皆為**裸 expr**，故須以 `list_sep` 分隔（見 §4）。
5. **Tuple : List ≈ Cocoon : Combo。** Tuple 之於 List，正如 Cocoon 之於 Combo——同一容器的「密封／定長」對偶（撇開 `%state: #total_ordered` 不看）。**類比只及定長那一半（2026-07-06 裁決）**：tuple 的密封是**定長密封**（不收新欄位），**不含效應屏蔽**——tuple 的 `%effect` 為元素之 max，效應屏蔽（退相干屏蔽）是 Cocoon 專屬的語義裝置（SPEC_08 §3.5）。tuple 只是「對位傳多值」的包裹，不是效應邊界。依**同構原理（SPEC_03 §4）**，這些容器都可互轉為 Combo 格式；故即使某種字面量缺乏直接語法，其*物件*仍經由同構存在（這也是採 (B) 給 `(x,)` 直接語法的理由——物件本就存在，只是給它能說出口的寫法）。語義以 **SPEC_03 §4、§5.2/§5.3** 為準。
6. **容器內元素的觀測／升寫（`%fmap` 函子性）以 SPEC 為準**（見 SPEC_07 §4.4），本章只定構造。

---

## 3. 範例 (Examples)

```nlang
;; Combo（換行慣用，見 SYNTAX_01）
user: {
    name: "Alice"
    age: 30
}

;; List（git 友善多行；尾隨逗號可省略）
nums: [
    1,
    2,
    3,
]

xs: [1, 2, 3]          ;; 單行
pair: (1, 2)           ;; Tuple
r: 1..10               ;; Range
sealed: {{ effect: #io }}   ;; Cocoon
```

---

## 4. 邊界情況 (Edge Cases)

> 逐條釘死容器層曾經模糊的寫法。

1. **`()` / `(x)` / `(x,)` / `(x, y)` 四方區分——「逗號界定 tuple」。** `()` 是 **Unit 原子**（SYNTAX_02）；`(x)`（無逗號）是**分組括號**，`(1) == 1`；`(x,)`（一個逗號）是 **1-tuple**；`(x, y)` 是 **2-tuple**。判準單一：**有逗號才是 tuple，沒逗號是分組**。對照尾隨逗號：`[1,] == [1]`（list 的尾隨逗號*可*省略），但 `(1,)` 的逗號**不可**省略——它正是把分組升格為 tuple 的標記。故 `(1)`（分組，`==1`）、`[1]`（1-list）、`(1,)`（1-tuple）依同構為三個不同物件（見 §2.5）。
2. **List／Tuple 必須用非空白分隔符。** 元素是裸 expr，**必須**以 `,` 或 `;` 分隔；**whitespace-alone 不足**（`[1 2 3]` **非法**）。原因：元素內可含空白顯著的運算子，例如
   ```nlang
   [1 |> /double, 2 |> /double, 3 |> /double]   ;; == [2, 4, 6]
   ```
   若無逗號，`2 |> /double` 會被併入前一個表達式。分隔符前後**可**有任意空白（含換行），**尾隨分隔符可省略**（見上方多行 List 範例）。
3. **`{}` vs `@{}` vs `()`。** `{}` 開放空 Combo（非原子，可被合併出資訊）；`@{}` 即 `_|_`（空集合 Bottom）；`()` 是 Unit 原子。三者語義互異（詳見 SYNTAX_02 邊界 #1）。
4. **Combo vs Cocoon 的分隔規則一致，密封性不同。** `{}` 與 `{{}}` 的欄位分隔規則相同（`field_sep`）；差別只在 `{{}}` **密封效果**。`{{` 與 `}}` **必須相鄰**成對；`{ {`（中間有空白）**不**構成 Cocoon——`{` 會被當作一般 Combo 起始，其後須緊接合法欄位（`key: expr`），否則解析失敗。（巢狀 Combo 須作為某欄位的值，如 `x: { … }`。）
5. **Range ＝ 閉區間集合，不是迴圈。**（2026-07-10 裁決，解 SPEC_01 §2.6 vs 本節舊措辭之衝突）`a..b` 為**閉閉區間 [a, b]**——數學集合列舉，兩端屬於集合（`150 & 0..150` → `150`；`@u8` 幾何＝`0..255`，SPEC_09 同款）。**特別提醒：range 不是 `for`**——工程師熟悉的半開迭代（`[start, end)`）是態射 API 的事，物化用 `~%List./range`（維持閉開）；字面量 `a..b` 是格論值（數值集合邊界，SPEC_02 §3），支援成員判定與交集（`5 & 1..10` → `5`、`1..10 & 5..20` → `5..10`）、宣告後精煉。省略形式 `..b`／`a..`／`..` 皆合法，**缺界預設為序位錨點 `#_|_`／`#_`**（SPEC_02 §3、SPEC_01 §2.6——序極值，*非*資訊格的 `_`）；界 `range_bound` 為 atom 或 path（**變數界合法**：`0..y`，依惰性語義於觀測期解析）。帶步長 `a..b..s` ＝ 等差集合（含端點若落在步進上）。在欄位值位使用 range 時，文法以 `!field_start` 護欄避免吃進下一欄位（SPEC_14 §2.4）。
6. **巢狀容器 = 點路徑。** `{a: {b: 1}}` 與點路徑 `a.b: 1` 等價（見 SYNTAX_03）；可自由混寫。
7. **`@{}` 與型別構造。** `@{ expr }` 是把表達式*強制*為集合邊界的語法；一般型別約束多用前綴 `@`（見 SYNTAX_05），`@{}` 用於需要顯式集合邊界的場合。**求值語義（2026-07-10 裁決）：透明**——`@{ e } ≡ e`（集合強制是 parse 層意圖標記；Union 本就是集合，`@{ 5 }` ＝ `5`——單元素集即原子，一字一義）；`@{}` ≡ `_|_`（§3.3）。**有意留白**：`%kind` 型別邊界標記（`@{e}` 是否應標 `#type`）——首次真實需要型別邊界語義時重開，在此之前透明。
8. **容器內的展開 `...`。** Combo／Cocoon 體內可用**展開欄位** `{ a: 1, ...~c }`（`...` 作為 field 的替代形式——顯式解封，搬運定義、丟棄外殼；語義見 **SPEC_03 §3.1**，含 Spread Isolation 安全邊界）。List／Tuple 內的 `...xs` 則是**元素位置的展開表達式**（spread 本就是 L4 表達式）。兩者拼法同、所在層不同。

---

## 5. 對應 (See Also)

- 上位文法：**[SPEC_14](./SPEC_14_Formal_Grammar.md) §2.1（分隔符原則）、§2.4（容器規則、`list_sep`）**。
- 容器語義：**[SPEC_03](./SPEC_03_Combo_System.md)**（Combo／Cocoon 本體）、**[SPEC_08](./SPEC_08_Meta_and_Runtime.md) §3.5**（Cocoon 密封）、**[SPEC_07](./SPEC_07_Logic_and_Pipe.md) §4.4**（`%fmap` 升寫）。
- 鄰章：**[SYNTAX_02](./SYNTAX_02_Literals_and_Atoms.md)**（`()`／`{}`／`@{}` 原子區分）、**[SYNTAX_03](./SYNTAX_03_Paths_and_Assignment.md)**（巢狀路徑）、**[SYNTAX_05](./SYNTAX_05_Prefix_Ontology.md)**（前綴）、**[SYNTAX_06](./SYNTAX_06_Comparison_and_Subtyping.md)**（合併 `&`、混血節點、`%kind` 衝突）、**[SYNTAX_09](./SYNTAX_09_Morphism_Application.md)**（Tuple 作為多參數）。
