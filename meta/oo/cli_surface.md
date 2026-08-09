# cli_surface — 指令面該長什麼樣(W22 設計稿)

> **不是規格,也還不是工單。** 這是 2026-08-09 一次設計討論的落檔,
> 目的是讓 **W10(savepoint)** 定形時有一份現成的需求可以對。
> 用戶原話與驗收方的補充都保留,推翻之處明寫。

---

## 0. 為什麼現在寫,卻不現在做

〔量 2026-08-09〕**`savepoint` 在引擎全樹出現 0 次。**

下面整份命令面**是 savepoint 模型的投影**——「預設建 savepoint」「`--dry-run` 不建」
「commit 失敗退回 savepoint」三句話都預設了一個**可定址、可替換的物件**。
今天最接近的是 `staged`,而它**不是** savepoint:一塊可變的暫存區,
沒有位址、不能替換、一次只有一份。

⟹ **設計現在定是對的**(它反過來約束 W10 該長什麼樣),**實作排在 W10 之後**。
否則 `--dry-run` 沒有東西可以「不建」。

**依賴**:**W6**(名字,見 §2)、**W10**(savepoint)。**本稿不排進弧序,由 W22 承接。**

---

## 1. 起點:規格記載了兩個不存在的旗標

```
REAL_01 §1.1:  oo run --observe <path> [--commit] [--format json|n] [--load <file>]
實際:          --observe --format --privileged --grant
```

`--commit` 與 `--load` **都不存在**。
⟹ 「重新規劃指令」不是在改一個穩定的介面,**是在補一份從未被兌現的記載**。

〔量〕另一項使目前的面貌不自洽:

| 指令 | 看得見這個倉嗎 |
| :-- | :-- |
| `oo evolve` | ✓(寫進 staged) |
| `oo status`／`oo commit`／`oo log` | ✓ |
| **`oo run`／`oo eval`** | **✗——連已提交的資料都看不見** |

實測:提交 `y: 5` 之後,`oo eval 'y'`、`oo eval '_.y'`、`oo run` 觀測 `_.y`
**三者皆回 `_`**;同一份檔案自帶 `y: 5` 時回 `5`。
**這是 W4‴ (b′) 的待裁項:一次性求值器該不該看見倉。**

---

## 2. 第一條軸:與倉有關 / 無關

用戶:「區分與倉無關／有關,無關的話概念類似一個臨時的獨立宇宙,
有關則是操作當前 `.oo/`(宇宙)。」

**名字**:規格稱 `.oo/` 為「工作區儲存結構」,承載它的東西是
**宇宙節點 (Universe Node)**(REAL_01 §1.2)。故 `--universe <path>` 是對的詞。

**但它把 W6 從「清潔」升級成「前置」**:`dot_oo` §1.1 量到**有兩個 `.oo`**
——HOME 側裝身分金鑰、工作區側才是宇宙。**只要兩邊都叫 `.oo`,這個旗標就是有歧義的。**

**`--universe null` 建議換掉**(驗收方,用戶同意):`null` 不是 n/ 的詞
(n/ 有 `_`、`_|_`、`#none`),而且臨時宇宙不是「空」而是「匿名」。
**沒有倉的目錄本來就是臨時宇宙**;只在「人在倉裡但要隔離」時才需要旗標,
`--ephemeral` 說的是「這次不要碰倉」,比 `--universe null` 誠實。

---

## 3. 第二條軸:觀測 / 執行 / 讀檔

用戶的草案:

```
oo observe <path> [--commit|--dry-run] [--universe <path>]
oo commit  [--universe <path>]
oo eval    <code> [--commit|--dry-run] [--universe <path>]
oo load    <file> [<file>...] [--commit] [--universe <path>]
```

驗收方的三點修改(用戶同意):

1. **`eval` 與 `observe` 的差別不是 LHS,是「觀測誰」。**
   `oo eval '1+1'` 沒有座標可觀測——**運算式本身就是被觀測的東西**;
   `observe <path>` 是「在宇宙裡指一個座標」。這是真的兩件事,兩個動詞留著。
2. **`load` 併進 `observe --from`。** 「讀檔然後與 universe 交集」**就是 evolve**;
   多一個動詞會讓「什麼時候用 load、什麼時候用 evolve」變成要記的事。
3. **`oo commit` 而不是 `oo node commit`。** `node` 那個命名空間治的是**節點**
   (身分、服務、發現),commit 治的是**宇宙**。既然 `--universe` 已是選擇器,
   `oo commit --universe <p>` 自洽;放進 `node` 會重演 `dot_oo` §1.1
   「一個名字兩個尺度」的錯。

**收斂後的草案:**

```
oo observe <path> [--from <file>...] [--commit|--dry-run] [--universe <p>|--ephemeral]
oo eval    <code>                    [--commit|--dry-run] [--universe <p>|--ephemeral]
oo commit                                                 [--universe <p>]
```

---

## 4. 留給 W10 決定的一題

用戶:「`--commit` 是先建 savepoint 並直接嘗試 commit(但不符合 commit 條件會報錯,
退回 savepoint?)」

**這一問正好是 savepoint 模型的賣點**:有了 savepoint,「退回」是免費的(指標移回去);
沒有它,今天 `commit` 失敗時 `staged` 是什麼狀態要逐案想。
**不用現在答——它會被 W10 的形狀決定,而這一題正是驗收 W10 的第一個問題。**

---

## 5. 與既有動詞的關係(尚未處理)

`evolve` 在收斂後的草案裡沒有出現,因為它的工作被 `observe --from` 涵蓋。
**但 `evolve` 是規格與引擎現行的詞**(SPEC_10 §2.2「`~%Engine./evolve`」是**語義**態射),
CLI 動詞若改名,要說清楚**語義態射的名字不動、只有 CLI 投影改**——
否則會製造第三個「一個概念兩種拼法」。**本稿不裁,列為 W22 的第一項待議。**
