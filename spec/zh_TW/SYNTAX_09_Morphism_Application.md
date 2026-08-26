# SYNTAX_09：態射應用與中綴運算 (Morphism Application & Infix Operators)

> [!NOTE] 定位
> 本章為**語法細則**（規範性，位階在 SPEC 之下；見 **[SYNTAX_00](./SYNTAX_00_Conventions.md)**）。文法上位規範見 **[SPEC_14](./SPEC_14_Formal_Grammar.md) §2.3**（`apply_expr`／`logic_infix` 優先權）；應用與柯里化語義以 **[SPEC_07](./SPEC_07_Logic_and_Pipe.md) §3** 為準；分派演算法見 **[SPEC_07](./SPEC_07_Logic_and_Pipe.md) §1.1**、**[SPEC_06](./SPEC_06_Unification_Logic.md) §1.5**。本章釘死**態射如何被呼叫——juxtaposition／infix 兩種形式、多引數的兩種傳遞慣例、空格規範——以及算術中綴運算子（`* / %`＝L8、`+ -`＝L9；此前無 SYNTAX 之家，2026-07-05 W1-4 併入本章）**。
>
> **範圍**：本章只管**應用（Application）**——已存在的態射如何被呼叫。態射**定義**（`->`、匿名態射、Combo-as-Union 分派定義）是獨立且份量不小的主題，**不在本章**；目前尚未排入 SYNTAX 系列（見文末）。

---

## 1. 語法 (Syntax)

態射應用有兩種形式，摘自 **SPEC_14 §2.3**：

```ebnf
apply_expr    = { unary_expr ~ (!field_start ~ !add_op ~ !mul_op ~ !cmp_op ~ !logic_infix ~ unary_expr)* } ;; Level 6：juxtaposition（護欄見 §4 #9；!logic_infix 2026-07-05 引擎同步補齊）
infix_expr    = { apply_expr ~ (!field_start ~ logic_infix ~ apply_expr)* } ;; Level 7：infix 糖衣
logic_infix   = @{ "/" ~ ident }                                            ;; atomic：/ 與 ident 間不得有空白
mul_expr      = { infix_expr ~ (!field_start ~ mul_op ~ infix_expr)* }      ;; Level 8：* / %
mul_op        = @{ "*" | ("/" ~ !ident) | ("%" ~ !ident) }
add_expr      = { mul_expr ~ (!field_start ~ add_op ~ mul_expr)* }          ;; Level 9：+ -
add_op        = { "+" | "-" }
```

| 寫法 | 形式 | 說明 |
| :--- | :--- | :--- |
| `/f arg` | **Prefix（juxtaposition）** | 態射與參數以空白相接，Level 6，**左結合**（`f a b` = `(f a) b`，見 **SPEC_02** 優先權表）。 |
| `arg /f arg2` | **Infix** | `/`+ident 作中綴糖衣，Level 7（比 Level 6 鬆一階，比 `*`／`/`／`%`〔Level 8〕緊）。 |
| `a * b`、`a / b`、`a % b` | **算術中綴（L8）** | 乘、除、取餘；`/`／`%` 帶 `!ident` 護欄（見 §4 #7/#8）。 |
| `a + b`、`a - b` | **算術中綴（L9）** | 加、減；`-` 的空白規則見 **SYNTAX_02 §4.3**。 |

---

## 2. 語義 (Semantics)

1. **兩種傳遞慣例（SPEC_07 §3）**，引數本身用既有語法（不新增文法）：
   | 慣例 | 寫法 | 引數個數 | 綁定方式 |
   | :--- | :--- | :--- | :--- |
   | **Curry（連續 juxtaposition）** | `/f a b` | 逐次單引數 | 逐層應用，`(/f a) b` |
   | **一個 Combo 引數** | `/f {k₁: a, k₂: b}` | 一個 Combo | 依**態射自己宣告的鍵**綁定 |

   **`/f (a, b)` 是第二種的糖**，鍵恰為 `0`、`1`（**SYNTAX_04**）——它不是第三種慣例。
   **萬物皆 Combo**：`(a, b)` 與 `{0: a, 1: b}` 是同一個值，`/f` 分不出它們，
   〔量 v0.36.0〕書寫順序亦不構成差別（`{1: b, 0: a}` 同義）。

   **態射必須宣告它綁定哪些鍵（MUST）。** 宣告**必須是一件規格事實，不得只是一件實作事實**
   ——即：本規格定義該宣告的形狀與內容，任何符合本規格的實作都據此回答「這個態射收哪些鍵」。
   **住處由實作選擇**（**2026-08-26 O78 ② 鬆綁**）：使用者定義的態射把它放在自身的值裡
   （`%rules` 的模式鍵與 `%params`）；引擎投影的態射**得**放在其內建登記表中，
   **不必**因此改變該態射的值——後者會移動標準根的 digest 而牽動每一個根的身分（O58），
   而那是一次紀元，不該由本款觸發。〔例，v0.36.0 實測〕
   `((x, y) -> …)` 的值逐字含 `%params: {{ 0: "x"  1: "y" }}` ⟹ **位置式只是「鍵剛好叫 `0`、`1`」**。
   應用側**必須**配對被宣告的鍵；未被宣告的形**不得**被靜默接受。

   參考引擎把內建的宣告放在**登記表**（不進值）。問「這個內建收哪些鍵」不必執行它。
   具名鍵能不能抵達內建已於 2026-07-25 修好（`unified_arg` 抬非 `%` 具名欄位）；
   [SPEC_08](./SPEC_08_Meta_and_Runtime.md) §3.5 的
   `~%Engine./project_down { target: @Combo, masa: @caid }` 由 conformance **L2-104** 釘住。
   補向量 **L2-120**／**L2-121** 釘宣告的形答對、未宣告的形不靜默答。
2. **每次應用都觸發分派。** 態射被套用於輸入時，引擎執行分派演算法（極小元素規則）以選出最特定分支；語義以 **SPEC_07 §1.1**、**SPEC_06 §1.5** 為準，本章不重述。
3. **Infix 是 Prefix 的語法糖。** `a /f b` 與 `/f a b` 語義相同（`logic_infix` 只是把第一個引數挪到 `/f` 前面書寫），供二元態射（如 `2 /add 4`）取得中綴可讀性。

---

## 3. 範例 (Examples)

兩種傳遞慣例（SPEC_07 §3）：

```nlang
/add 2 4              ;; Curry：6
2 /add 4               ;; Infix 糖衣，同上：6
/add (2, 4)             ;; 一個 Combo 引數，鍵為 0、1：6
/add { 0: 2, 1: 4 }    ;; 同上，鍵寫出來（同一個值）
```

空引數與空格規範：

```nlang
/func ()      ;; 建議寫法：態射與參數之間保持空格
/func()       ;; 不建議（見 §4 #1）
```

---

## 4. 邊界情況 (Edge Cases)

> 逐條釘死應用層的寫法。

1. **態射與參數之間應保持空格（SHOULD）。** 建議寫法 `/func ()`；省略空格 `/func()` **不**觸發實際的文法錯誤（whitespace 在 `apply_expr` 中並非強制分隔符），但引入了「看起來像 C 風格呼叫語法」的視覺陷阱——`n/` 的應用是**空白即運算子**的 juxtaposition 模型，不是括號界定的呼叫清單。故 `n/` 規範**建議**（非強制）不省略空格，以維持模型的一致心像。
2. **Curry 與「一個 Combo 引數」不是同義詞——引數個數不同。** `/func () ()` 是**兩次**獨立的單引數應用（`(/func ()) ()`，逐層柯里化）；`/func ((), ())` 是**一次**單引數應用，引數恰好是鍵為 `0`、`1` 的 Combo（兩個 Unit）。兩者能否互通取決於 `/func` 的模式定義**宣告了哪些形**——語法層**不**假定兩者等價。〔量 2026-08-26，v0.36.0〕`((x, y) -> …)` 施於 `7 17` 為 `⊥ #conflict`、`(x y -> …)` 施於 `(7, 17)` 為部分施用的繭 ⟹ 使用者態射今日已守此款；**未守的是內建**（見 §2 #1 的未兌現宣告）。
3. **應用優先於合併，合併結果需要括號。** `apply_expr`（Level 6）比 `&`（Level 10）緊：
   ```nlang
   /func a & b     ;; 等價於 (/func a) & b
   /func (a & b)   ;; 明確：對合併結果應用態射，需要括號
   ```
   （**SPEC_14 §2.3.3 範例 C**；細節不重述。）
4. **`!field_start` 邊界保護會截斷連續應用鏈。** 在 Combo 欄位值中連續書寫應用鏈時，一旦解析器偵測到下一個 `key:` 匹配 `field_start`，當前應用鏈立即終止——不需要逗號或括號來分隔欄位（**SPEC_14 §2.3.3 範例 D**；**SPEC_07 §3**）。
5. **高階傳遞（把態射當資料）用結構態引用。** 把態射本身（而非其應用結果）傳給另一個態射時，應以 `<<...>>` 包住整個態射路徑（如 `<</f>>`），確保接收端拿到的是完整 Combo 本體，而非可能被提前坍縮的收斂值（坍縮／結構對偶原則見 **SYNTAX_07**；範例見 **SPEC_07 §5.1**）。
7. **`/` 的三態（空白與 ident 判定）。** `/f a` 是**前綴應用**；`a /f b`（`/` 緊接識別碼）是**中綴態射**（`logic_infix` 為 atomic——`/` 與 `f` 之間**不得**有空白）；`a / b`（`/` 後有空白或非識別碼，如 `a / (b)`）是**除法**。三者由字元層即可判定，無歧義。
8. **`%` 的雙態。** `a % b`（`%` 後空白）是**取餘**；`a %len`（`%` 緊接識別碼）**不是**取餘——`%len` 讀作元鍵，整式成為 juxtaposition 應用（合法但罕見；讀元資訊請用 postfix `a.%len`，見 SYNTAX_08，或加括號自明）。
9. **apply 護欄與負數引數。** `apply_expr` 帶 `!add_op !mul_op !cmp_op` 護欄：**運算元之後的中綴符號一律讓位給中綴層**——`f -1` 是「f 減 1」，不是「f 應用於 -1」；負數引數**必須**括號：`f (-1)`（SYNTAX_02 §4.3、SYNTAX_01 §4.8）`!logic_infix` 同理（2026-07-05 補齊）：`a /f b` 上浮至 L7 中綴層，juxtaposition 不得吞 `/f` 為運算元——以態射為 apply 引數須括號：`f (/g)`。
10. **態射*定義*不在本章範圍。** `->`（Level 15）、匿名態射 `(x -> body)`、`{}`-as-Union 分派定義等屬於**定義**語法，語義已見於 **SPEC_07 §1、§5.2**，但尚未有對應的 SYNTAX 章節釘死其書寫細則（柯里化參數 `x y -> ...` 的空格規範、`->` 鏈的右結合換行慣例等）。目前**不得**假定本章的應用規則反向約束定義語法。

---

## 5. 對應 (See Also)

- 上位文法：**[SPEC_14](./SPEC_14_Formal_Grammar.md) §2.3**（`apply_expr`／`logic_infix`／優先權範例 C、D）。
- 語義：**[SPEC_07](./SPEC_07_Logic_and_Pipe.md) §1.1**（分派演算法）、**§3**（應用與柯里化）、**§5.1**（高階傳遞）；**[SPEC_06](./SPEC_06_Unification_Logic.md) §1.5**（極小元素規則）；**[SPEC_02](./SPEC_02_Lexical_Structure.md)**（優先權總表、結合律）。
- 鄰章：**[SYNTAX_04](./SYNTAX_04_Combo_Construction.md)**（tuple／Combo 字面量）、**[SYNTAX_07](./SYNTAX_07_Observation_Duality.md)**（`<<x>>` 結構態）、**[SYNTAX_06](./SYNTAX_06_Comparison_and_Subtyping.md)**（`&` 合併優先權）。
