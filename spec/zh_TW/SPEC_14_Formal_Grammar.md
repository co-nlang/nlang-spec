# n/ Language Specification - 正式語法 (Formal Grammar)

本章節提供 `n/` 語言的規範語法定義 (Canonical Grammar)，並詳細說明解析器中的「欄位邊界保護」機制。本規格基於 PEG (Parsing Expression Grammar) 範式描述。

---

## 1. 欄位邊界保護 (Field Boundary Protection)

在 `n/` 中，空白（Whitespace）是態射應用的運算子。為了在沒有強制分隔符（如逗號）的情況下，精確區分「運算式的延續」與「新欄位的啟動」，`n/` 引入了**邊界保護斷言 (`!field_start`)**。

### 1.1 `field_start` 斷言
任何在語法上構成「欄位定義起點」的模式，都稱為 `field_start`。
*   **定義**：`field_start = { field_key ~ ":" }`
*   **作用範疇**：
    *   **層級局部性 (Local Scoping)**：斷言僅針對**當前作用域層級**。嵌套在括號（`()`）、列表（`[]`）或內部 Combo（`{}`）中的 `:` 不會觸發當前層級表達式的終止。
    *   **跨行斷言與單行鍵限制 (Single-line Key Constraint)**：
        - **規則**：為了確保解析的決定論並防止回溯爆炸，**`field_key` 及其對應的 `:` 必須位於同一詞法行內**。
        - **行為**：斷言的觸發可以跨越換行符（探測下一行是否為新欄位），但在匹配單個 `field_start` 的過程中，若在 `:` 出現前遇到換行，則該斷言立即失效。
        - **非法案例 (Parsing Failure)**：
            ```nlang
            long_field_name    ;; 換行發生在冒號前
                : /add 1 2     ;; 解析器將 long_field_name 視為一個標籤原子，而非 Key
            ```
        - **正確案例**：
            ```nlang
            long_field_name:   ;; 冒號與 Key 同行
                /add 1 2       ;; 值可以位於下一行（透過縮排）
            ```

*   **邊界案例**：
    ```nlang
    val: /f { sub_key: 1 }  ;; 內部的 : 不觸發終止，因為它在 {} 作用域內
    next: 2                 ;; 觸發終止，因為它與 val 處於同一層級
    ```

### 1.2 邊界保護範例
```nlang
result: /add 10 20    ;; /add 的參數解析
next_val: 30          ;; 探測到 field_start，/add 解析終止
```
這確保了 `n/` 既具備 JSON 的結構清晰度，又具備態射式語言的流暢感。

---

## 2. 規範語法定義 (The Canonical Rules)

### 2.1 基礎符號與空白
```ebnf
WHITESPACE = _{ " " | "\t" | "\n" | "\r\n" | "\r" }
COMMENT    = _{ ";;" ~ (!("\n" | "\r\n" | "\r") ~ ANY)* }
program    = { SOI ~ WHITESPACE* ~ (field ~ field_sep?)* ~ EOI }
field_sep  = _{ "," | ";" | WHITESPACE+ }
```

#### Compact 格式支援

`field_sep` 中的 `,` 與 `;` 提供**可選的視覺分隔**，語義等價於空白：

```nlang
;; 以下三種寫法等價
{a: 1, b: 2, c: 3}     ;; compact（JSON-like）
{a: 1; b: 2; c: 3}     ;; 分號分隔
{a: 1 b: 2 c: 3}       ;; 純空白分隔（n/ 慣用）
```

**設計原則**：
- **欄位層級**：`,` `;` `␣` `\n` 在 Combo/Cocoon 欄位之間完全等價（`key:` 已界定元素邊界，故空白即可分隔）
- **集合元素層級**：`list [ ]`／`tuple ( )` 的元素是**裸 expr**，**必須**以非空白分隔符 `,`／`;`（`list_sep`）分隔——whitespace-alone 不足以界定裸 expr 的邊界（例：`[1 |> /double, 2 |> /double]` 若無逗號會被解讀為單一表達式）。分隔符前後可有任意空白（含換行），**尾隨分隔符可省略**
- **表達式層級**：不支援 `,` 作為運算式分隔（如 `/add a, /sub b` 非法）；`,`／`;` 只作為**集合元素**分隔，不作為子運算式分隔
- **JSON 互操作**：緊湊輸出時可選擇保留 `,` 以提升外部可讀性

### 2.2 識別碼與前綴
```ebnf
;; 識別碼：支援全 Unicode 字符，以字母或底線開頭
ident      = @{ (XID_START | "_") ~ (XID_CONTINUE | "_" | "-")* }
numeric    = @{ ASCII_DIGIT+ }
```
*註：`n/` 採用 `XID_START` 與 `XID_CONTINUE` 標準，確保中文、日文、韓文等非拉丁字元皆可作為合法的座標名稱。*

```ebnf
;; 前綴本體論（2026-06 收緊）：三位一體 {Data, @Type, /Logic} 可加隱藏修飾 ~（→ ~a, ~@a, ~/a）；
;; %（元資訊）與 ~%（系統）為獨立維度，僅 Combo/Data，無 Type/Logic 子面向。
;; 有序選擇：prefix_system 先於 prefix_local（~% 最長匹配）。
prefix         = @{ prefix_system | prefix_meta | (prefix_local ~ (prefix_type | prefix_logic)?) | prefix_type | prefix_logic }
prefix_type    = { "@" }
prefix_logic   = { "/" }
prefix_meta    = { "%" }
prefix_system  = { "~%" }   ;; atomic
prefix_local   = { "~" }

;; 命名鍵：包含可組合前綴的識別碼，或純數字鍵
numeric_key = @{ numeric }
named_key = @{
    (prefix? ~ ident)
    | numeric_key
}

;; 引用鍵：包含空格或運算子的鍵
quoted_key = @{ "\"" ~ (!"\"" ~ ANY)* ~ "\"" }
;; 多行鍵：名字含 `"` 者的唯一寫法（SYNTAX_03 §5 #12，2026-08-20）
multiline_key = @{ multiline_str }

;; 欄位鍵：解析優先序為 匿名集合 > 路徑 > 命名鍵；tag 鍵用於分派表（2026-07-05 自引擎現況收編）
field_key = { anon_set | path | named_key | quoted_key | multiline_key | tag }
;; spread-as-field：{ a: 1, ...~c } 的展開欄位（語義見 SPEC_03 §3.1；2026-07-05 補上位文法）
field     = { (field_key ~ ":" ~ expr) | spread_expr }
```

### 2.3 表達式優先權 (遞歸下降)
運算子優先權由文法的嵌套層次決定（由低至高 / 由鬆至緊）：

```ebnf
expr          = { morphism_expr }
;; 註：解析器實作（AST Builder）必須將 `->` 迭代層級手動摺疊為右結合樹 (Right-to-Left)
morphism_expr = { ternary_expr ~ (!field_start ~ "->" ~ ternary_expr)* } ;; Level 15: Morphism
ternary_expr  = { pipe_expr ~ (!field_start ~ "?" ~ pipe_expr ~ ":" ~ pipe_expr)? } ;; Level 14: Ternary
pipe_expr     = { join_expr ~ (!field_start ~ "|>" ~ join_expr)* } ;; Level 13: Pipe
join_expr     = { cmp_expr ~ (!field_start ~ join_op ~ cmp_expr)* } ;; Level 12: Union / Diff
join_op       = { "|" | "\\" }
cmp_expr      = { meet_expr ~ (!field_start ~ cmp_op ~ meet_expr)? } ;; Level 11: Comparison
;; 兩個家族：格論/集合關係 < <= = >= >（不塌縮，適用疊加態）；原子比較 == !=（須塌縮）
cmp_op        = { "<=>" | "<=" | ">=" | "==" | "!=" | "=" | "<" | ">" }   ;; "<=>" 方向探測（序位，回傳標籤聯集；SYNTAX_10）——最長匹配在前
meet_expr     = { add_expr ~ (!field_start ~ "&" ~ add_expr)* } ;; Level 10: Merge（& 比 cmp 緊；與 C 相反）
add_expr      = { mul_expr ~ (!field_start ~ add_op ~ mul_expr)* } ;; Level 9: Additive
add_op        = { "+" | "-" }
mul_expr      = { infix_expr ~ (!field_start ~ mul_op ~ infix_expr)* } ;; Level 8: Multiplicative
mul_op        = @{ "*" | ("/" ~ !ident) | ("%" ~ !ident) }   ;; !ident：`a /f`／`a %len` 非除法／取餘（2026-07-05 對齊引擎）
infix_expr    = { apply_expr ~ (!field_start ~ logic_infix ~ apply_expr)* } ;; Level 7: Infix Logic
logic_infix   = @{ "/" ~ ident }   ;; atomic：`a /f b` 中綴態射（/ 與 ident 間不得有空白）；`a / b`（有空白）是除法
apply_expr    = { unary_expr ~ (!field_start ~ !add_op ~ !mul_op ~ !cmp_op ~ !logic_infix ~ unary_expr)* } ;; Level 6: Morphism Apply（護欄：運算元後的 -/*… 讓位給中綴層——`a -1` 是減法非應用，SYNTAX_02 §4.3；2026-07-05 補齊。!logic_infix：`a /f b` 須上浮至 L7 中綴層，juxtaposition 不得吞 `/f` 為運算元——2026-07-05 引擎同步時發現原護欄不足，補齊；代價：以態射為 apply 運算元須括號 `f (/g)`）
unary_expr    = { (unary_op ~ unary_expr) | spread_expr } ;; Level 5: Unary
unary_op      = { "!" }   ;; 2026-07-05 W1-1：負號自 unary 移除——負數屬字面量（int_lit/float_lit/complex_lit 內建 "-"，見 SYNTAX_02 §4.3）；識別碼取負非原語（寫 0 - x 或 stdlib）
spread_expr   = { ("..." ~ type_ann_expr) | type_ann_expr } ;; Level 4: Spread

type_ann_expr = { postfix_expr ~ (!field_start ~ "@" ~ postfix_expr)* } ;; Level 3: Type Annotation
postfix_expr  = { primary ~ postfix_op* } ;; Level 2: Access / Navigation
postfix_op    = { ("." ~ named_key) | ("[" ~ expr ~ "]") }

field_start   = _{ field_key ~ ":" }
```

### 2.4 導航與原子 (Navigation & Atoms)

```ebnf
primary = { range | complex_lit | context | structural | tuple | "(" ~ expr ~ ")" | combo | cocoon | anon_set | poset_lit | list | interp_str | atom | path }

;; tuple 由「至少一個逗號」界定：(x) 是分組，(x,) 是 1-tuple，(x, y) 是 2-tuple
tuple = { "(" ~ WHITESPACE* ~ expr ~ list_sep ~ (expr ~ (list_sep ~ expr)* ~ list_sep?)? ~ WHITESPACE* ~ ")" }

atom = {
    bottom
    | tag_start
    | tag_end
    | top
    | unit
    | float_lit
    | int_lit
    | regex_lit
    | path_lit
    | bytes_lit
    | uri_lit
    | time_lit
    | multiline_str
    | str_lit
    | tag
}

;; 區間 (Range)
range = {
    (range_start ~ ".." ~ (!field_start ~ range_end)? ~ (".." ~ !field_start ~ range_step)?)
    | (".." ~ (!field_start ~ range_end)? ~ (".." ~ !field_start ~ range_step)?)
}
range_start = { range_bound }
range_end = { range_bound }
range_step = { range_bound }
range_bound = { atom | path }

;; 上下文符號 (Context)
context = @{ "$" }

;; 水晶括號 (Structural)：雙角括號（與 cocoon {{}} 同為「雙括號＝特殊視角」慣例）；
;; 不與比較 < > 衝突（最長匹配：<< 先於 <）
structural = { "<<" ~ expr ~ ">>" }

;; Combo
combo = { "{" ~ WHITESPACE* ~ (field ~ field_sep?)* ~ "}" }

;; Cocoon
cocoon = { "{{" ~ WHITESPACE* ~ (field ~ field_sep?)* ~ "}}" }

;; 匿名集合（空體合法：`@{}` ≡ `_|_`，SYNTAX_02 §4.2/§8；2026-07-10 文法行同步 prose 既有裁決）
anon_set = { "@{" ~ expr? ~ "}" }

;; Poset 字面量（Enum 序位；SYNTAX_10，2026-07-05 自 discussion/008 定案）
poset_lit   = { "#{" ~ WHITESPACE* ~ (order_chain ~ field_sep?)* ~ "}" }
order_chain = { poset_node ~ (order_op ~ poset_node)+ }
order_op    = { "<=" | ">=" | "=" | "<" | ">" }   ;; 格論家族五符號（同序位用 =，非 ==；2026-07-05 裁決）
poset_node  = { tag_start | tag_end | tag }

;; List
list     = { "[" ~ WHITESPACE* ~ (expr ~ (list_sep ~ expr)* ~ list_sep?)? ~ WHITESPACE* ~ "]" }
;; 集合元素分隔符：非空白（裸 expr 邊界需明確）；尾隨分隔可省略
list_sep = _{ "," | ";" }

;; 內插字串
interp_str = ${ "`" ~ interp_part* ~ "`" }
interp_part = { interp_expr | interp_literal }
interp_expr = { "${" ~ expr ~ "}" }
interp_literal = @{ (!("`" | "${") ~ ANY)+ }

;; 路徑（段可為 tag：Enum 成員存取 Status.#draft——2026-07-05 收編）
path = { (root_path | parent_path | bare_path) ~ ("." ~ (named_key | tag) | "[" ~ expr ~ "]")* }
root_path = @{ "_." }
parent_path = @{ "^"+ ~ "." }
bare_path = @{ named_key }

;; 原子定義
bottom = @{ "_|_" }
tag_start = @{ "#_|_" }
tag_end = @{ "#_" }
top = @{ "_" }
unit = @{ "(" ~ ")" }
float_lit = @{ "-"? ~ numeric ~ "." ~ numeric ~ (("e" | "E") ~ ("+" | "-")? ~ numeric)? }
int_lit = @{ "-"? ~ numeric }

;; 複數字面量（SPEC_02 §2.2 正典；atomic 無空白——`2+3i` 是單一複數，`2 + 3i`（帶空白）是加法）
;; 置於 primary（range 之後、context 之前）而非 atom：區間邊界／序關係不取複數。
;; 尾端 !(XID_CONTINUE | "-") 護欄（2026-07-06 補齊）：`io`／`it`／`i-1` 是識別碼，
;; 不得被拆成「複數 i ＋ apply」；裸 `i`／`-i` 仍為虛數單位。含 `-` 與 kebab 識別碼規則一致。
complex_lit = @{
    ( "-"? ~ numeric ~ ("." ~ numeric)? ~ (("e" | "E") ~ ("+" | "-")? ~ numeric)? )
      ~ ("+" | "-") ~ numeric ~ ("." ~ numeric)? ~ (("e" | "E") ~ ("+" | "-")? ~ numeric)? ~ "i" ~ !(XID_CONTINUE | "-")
    | "-"? ~ numeric ~ ("." ~ numeric)? ~ (("e" | "E") ~ ("+" | "-")? ~ numeric)? ~ "i" ~ !(XID_CONTINUE | "-")
    | "-"? ~ "i" ~ !(XID_CONTINUE | "-")
}
tag = @{ "#" ~ ident }

regex_lit  = @{ "r\"" ~ (!"\"" ~ ANY)* ~ "\"" }
path_lit   = @{ "p\"" ~ (!"\"" ~ ANY)* ~ "\"" }
bytes_lit  = @{ "b\"" ~ (!"\"" ~ ANY)* ~ "\"" }
uri_lit    = @{ "u\"" ~ (!"\"" ~ ANY)* ~ "\"" }
time_lit   = @{ "t\"" ~ (!"\"" ~ ANY)* ~ "\"" }
str_lit    = @{ "\"" ~ (!"\"" ~ ANY)* ~ "\"" }
multiline_str = @{ "\"\"\"" ~ ( ("\\" ~ "\"\"\"") | (!"\"\"\"" ~ ANY) )* ~ "\"\"\"" }
```

---

## 3. 字串內插與特殊字面量

*   **內插字串 (interp_str)**：`` `...` `` 內部可包含 `${expr}`。
*   **匿名集合 (anon_set)**：`@{ expr }` 強制將表達式解析為集合邊界；空體 `@{}` 即 `_|_`（SYNTAX_02 §8）。
*   **水晶括號 (structural)**：`<<expr>>` 觀測結構態（雙角括號，不與比較 `<`／`>` 衝突）。

---

## 4. 複雜運算子解析範例

為了強化規格書的嚴謹性，以下列舉幾種運算子組合的解析路徑：

### 範例 A：Pipe 與集合運算的互動
```nlang
result: 1 | 2 |> /check
```
*   **解析順序**：`|` (Level 12) 的優先權高於 `|>` (Level 13)。
*   **結果**：聯集會先形成，再整體進入管道。等價於 `(1 | 2) |> /check`。
*   **風格指南 (Style Guide)**：雖然語言定義了嚴格的優先級，但當聯集（或合併）與管道混合使用時，為了避免閱讀者的認知負擔與歧義，**官方強烈建議顯式使用括號進行視覺分組**：
    ```nlang
    ;; 推薦寫法
    result: (1 | 2) |> /check    ;; 若意圖為聯集優先
    result: 1 | (2 |> /check)    ;; 若意圖為管道優先
    ```
### 範例 B：Pipe 與型別約束的結合
```nlang
val: 123 @int |> /process
```
*   **解析層級**：`@` (Level 3) > `|>` (Level 13)。
*   **結果**：型別邊界會先坍縮，產生的原子或子集再進入管道。

### 範例 C：態射應用與合併的優先級
```nlang
result: /func a & b
```
*   **解析層級**：`apply_expr` (Level 6) > `&` (Level 11)。
*   **等價於**：`(/func a) & b`。
*   **說明**：態射應用會優先於合併發生。若需對合併結果應用態射，**必須使用括號**：`/func (a & b)`。


### 範例 D：邊界保護斷言 (!field_start)
```nlang
/f: data |> /transform
next_key: 100
```
*   **解析**：遇到 `next_key:` 匹配 `field_start` 模式。
*   **結果**：`/transform` 後方的解析強制終止。這確保了在大規模 Combo 中不需要逗號也能精確區分欄位。

---

## 5. 解析器保證 (Parser Guarantees)

任何符合 `n/` 規格的解析器實作必須保證：
1.  **冪等格式化**：解析後再經由規範化表示態射（`oo fmt`）輸出，內容雜湊（CAID）必須不變。
2.  **欄位邊界隔離**：嚴格執行 `!field_start` 斷言，確保長鏈表達式不會越過欄位邊界。
    *   *實作建議*：為了優化效能，建議實作者採用「兩階段解析」或「明確的狀態機」來處理邊界探測，而非單純依賴 PEG 的遞迴先行斷言。
3.  **UTF-8 支援**：所有字串與標籤必須完整支援萬國碼。

---

## 6. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_02](./SPEC_02_Lexical_Structure.md)** | 詞法原子是文法解析的終點幾何。 |
| **[SPEC_04](./SPEC_04_Navigation_and_Duality.md)** | 導航與作用域解析規則決定了 `path` 的解析邏輯。 |
| **[SPEC_11](./SPEC_11_Reflection_and_Synthesis.md)** | `oo fmt` 的實作基礎即是本章定義的規範文法。 |
| **[REAL_02](./REAL_02_Ouroboros_Protocols.md)** | 討論具體解析器如何處理語法錯誤與恢復。 |

---

### 哲學思辨 (Philosophical Synthesis)

> 結語：語法是宇宙的邊界，定義了存在的合法性。在精確的斷言中，語言完成了從混沌到秩序的第一次躍遷。
