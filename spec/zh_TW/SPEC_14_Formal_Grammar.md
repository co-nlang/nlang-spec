# n/ Language Specification - 正式語法 (Formal Grammar)
本章節提供 `n/` 語言的規範語法定義 (Canonical Grammar)，並詳細說明解析器中的「視界邊界保護」機制。本規格基於 PEG (Parsing Expression Grammar) 範式描述。

---

## 1. 視界邊界保護 (Horizon Boundary Protection)

在 `n/` 中，空白（Whitespace）是態射應用的運算子。為了在沒有強制分隔符（如逗號）的情況下，精確區分「運算式的延續」與「新視界的啟動」，`n/` 引入了**邊界保護斷言 (`!field_start`)**。

### 1.1 `field_start` 斷言
任何在語法上構成「欄位定義起點」的模式，都稱為 `field_start`。
*   **定義**：`field_start = { field_key ~ ":" }`
*   **作用範疇**：
    *   **層級局部性 (Local Scoping)**：斷言僅針對**當前視界層級**。嵌套在括號（`()`）、列表（`[]`）或內部 Combo（`{}`）中的 `:` 不會觸發當前層級表達式的終止。
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
    val: /f { sub_key: 1 }  ;; 內部的 : 不觸發終止，因為它在 {} 視界內
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

### 2.2 識別碼與前綴
```ebnf
;; 識別碼：支援全 Unicode 字符，以字母或底線開頭
ident      = @{ (XID_START | "_") ~ (XID_CONTINUE | "_" | "-")* }
numeric    = @{ ASCII_DIGIT+ }
```
*註：`n/` 採用 `XID_START` 與 `XID_CONTINUE` 標準，確保中文、日文、韓文等非拉丁字元皆可作為合法的座標名稱。*

```ebnf
prefix_type    = @{ "@" }
prefix_logic   = @{ "/" }
prefix_meta    = @{ "%" }
prefix_system  = @{ "~%" }
prefix_local   = @{ "~" }

;; 命名鍵：包含前綴的識別碼，或純數字鍵（用於 List 同構）
numeric_key = @{ numeric }
named_key = @{
    (prefix_system ~ ident)
    | (prefix_local ~ ident)
    | (prefix_meta ~ ident)
    | (prefix_type ~ ident)
    | (prefix_logic ~ ident)
    | ident
    | numeric_key
}

;; 引用鍵：包含空格或運算子的鍵
quoted_key = @{ "\"" ~ (!"\"" ~ ANY)* ~ "\"" }

;; 欄位鍵：解析優先序為 匿名集合 > 路徑 > 命名鍵
field_key = { anon_set | path | named_key | quoted_key }
field     = { field_key ~ ":" ~ expr }
```

### 2.3 表達式優先權 (遞歸下降)
運算子優先權由文法的嵌套層次決定（由低至高 / 由鬆至緊）：

```ebnf
expr          = { morphism_expr }
;; 註：解析器實作（AST Builder）必須將 `->` 迭代層級手動摺疊為右結合樹 (Right-to-Left)
morphism_expr = { ternary_expr ~ (!field_start ~ "->" ~ ternary_expr)* } ;; Level 15: Morphism
ternary_expr  = { pipe_expr ~ (!field_start ~ "?" ~ pipe_expr ~ ":" ~ pipe_expr)? } ;; Level 14: Ternary
pipe_expr     = { join_expr ~ (!field_start ~ "|>" ~ join_expr)* } ;; Level 13: Pipe
join_expr     = { meet_expr ~ (!field_start ~ join_op ~ meet_expr)* } ;; Level 12: Union / Diff
join_op       = { "|" | "\\" }
meet_expr     = { cmp_expr ~ (!field_start ~ "&" ~ cmp_expr)* } ;; Level 11: Merge
cmp_expr      = { add_expr ~ (!field_start ~ cmp_op ~ add_expr)? } ;; Level 10: Comparison
cmp_op        = { "<=" | ">=" | "==" | "!=" | "<" | ">" }
add_expr      = { mul_expr ~ (!field_start ~ add_op ~ mul_expr)* } ;; Level 9: Additive
add_op        = { "+" | "-" }
mul_expr      = { infix_expr ~ (!field_start ~ mul_op ~ infix_expr)* } ;; Level 8: Multiplicative
mul_op        = { "*" | "/" | "%" }
infix_expr    = { apply_expr ~ (!field_start ~ logic_infix ~ apply_expr)* } ;; Level 7: Infix Logic
logic_infix   = @{ "/" ~ ident }
apply_expr    = { unary_expr ~ (!field_start ~ unary_expr)* } ;; Level 6: Morphism Apply
unary_expr    = { (unary_op ~ unary_expr) | spread_expr } ;; Level 5: Unary
unary_op      = { "!" | "-" }
spread_expr   = { ("..." ~ type_ann_expr) | type_ann_expr } ;; Level 4: Spread

type_ann_expr = { postfix_expr ~ (!field_start ~ "@" ~ postfix_expr)* } ;; Level 3: Type Annotation
postfix_expr  = { primary ~ postfix_op* } ;; Level 2: Access / Navigation
postfix_op    = { ("." ~ named_key) | ("[" ~ expr ~ "]") }

field_start   = _{ field_key ~ ":" }
```

### 2.4 導航與原子 (Navigation & Atoms)

```ebnf
primary = { range | context | structural | tuple | "(" ~ expr ~ ")" | combo | cocoon | anon_set | list | interp_str | atom | path }

tuple = { "(" ~ expr ~ ("," ~ expr)+ ~ ")" }

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

;; 水晶括號 (Structural)
structural = { "<" ~ expr ~ ">" }

;; Combo
combo = { "{" ~ WHITESPACE* ~ (field ~ field_sep?)* ~ "}" }

;; Cocoon
cocoon = { "{{" ~ WHITESPACE* ~ (field ~ field_sep?)* ~ "}}" }

;; 匿名集合
anon_set = { "@{" ~ expr ~ "}" }

;; List
list = { "[" ~ WHITESPACE* ~ (expr ~ ("," ~ expr)*)? ~ "]" }

;; 內插字串
interp_str = ${ "`" ~ interp_part* ~ "`" }
interp_part = { interp_expr | interp_literal }
interp_expr = { "${" ~ expr ~ "}" }
interp_literal = @{ (!("`" | "${") ~ ANY)+ }

;; 路徑
path = { (root_path | parent_path | bare_path) ~ ("." ~ named_key | "[" ~ expr ~ "]")* }
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
*   **匿名集合 (anon_set)**：`@{ expr }` 強制將表達式解析為集合邊界。
*   **水晶括號 (structural)**：`<expr>` 觀測結構態。

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
2.  **視界隔離**：嚴格執行 `!field_start` 斷言，確保長鏈表達式不會越過欄位邊界。
    *   *實作建議*：為了優化效能，建議實作者採用「兩階段解析」或「明確的狀態機」來處理邊界探測，而非單純依賴 PEG 的遞迴先行斷言。
3.  **UTF-8 支援**：所有字串與標籤必須完整支援萬國碼。

---

## 6. 與其他章節的關係

| 章節 | 關聯 |
| :--- | :--- |
| **[SPEC_02](./SPEC_02_Lexical_Structure.md)** | 詞法原子是文法解析的終點幾何。 |
| **[SPEC_04](./SPEC_04_Navigation_and_Duality.md)** | 導航與視界解析規則決定了 `path` 的解析邏輯。 |
| **[SPEC_11](./SPEC_11_Reflection_and_Synthesis.md)** | `oo fmt` 的實作基礎即是本章定義的規範文法。 |
| **[REAL_02](./REAL_02_Ouroboros_Protocols.md)** | 討論具體解析器如何處理語法錯誤與恢復。 |

---

### 哲學思辨 (Philosophical Synthesis)

> 結語：語法是宇宙的邊界，定義了存在的合法性。在精確的斷言中，語言完成了從混沌到秩序的第一次躍遷。
