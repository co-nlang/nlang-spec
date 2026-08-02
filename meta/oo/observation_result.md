# observation_result — 一次觀測回來的東西是什麼形狀

> **這是原料,不是規格。** 精煉成條文之前的討論稿。
> 開稿 2026-08-02。標記 **〔量〕** 者為實測,**〔讀〕** 者為讀原始碼/條文得出。

**為什麼不叫 `blur.md`:** 本文的論旨正是「blur 不是格上的一個位置」。
用它命名,會把要治的那個混淆再犯一次。

---

## 0. 這份文件回答什麼

**觀測收斂之後回來的那個東西,它的值域是什麼?** 以及:今天那個值域為什麼讓人
問不出「blur 到底是聯集態、bottom 還是 top」這種問題的答案。

---

## 1. 承重結論:那裡有三條軸,而其中兩條被塞進一個槽

> **更正(2026-08-03):** 初稿寫「兩條軸」。**漏了 `%effect`**(見 §9),
> 它是獨立的第三條。這裡先列三條,§1 其餘部分談的是 Q1/Q2 的混用。

| 軸 | 問題 | 值域 |
| :-- | :-- | :-- |
| **Q1 位置** | 結果落在格的哪裡? | top / atom / union / combo / range / bottom |
| **Q2 為什麼停** | 算完了,還是視界到了? | (完成) / `#incomplete` / `#blur` |
| **Q3 能不能再算** | **值由內容決定嗎?** | `#pure` / `#io` `#nondet` `#state` |

三條互相獨立:一個 `#io` 值可以是 atom、可以是 blur、可以是 bottom。

**`Blur` 回答的是 Q2,卻被實作成 Q1 的一格。**

證據就在它自己的欄位裡〔讀 `value.rs:1549`〕:

```rust
pub struct BlurDetail {
    pub cause: BlurCause,            // 為什麼停 —— Q2
    pub horizon: HorizonParams,      // fuel_remaining, strategy, salt
    pub partial: Option<Box<Value>>, // 走到哪裡 —— Q1,被降級成一個欄位
    pub effect: EffectTag,
}
```

如果已經收窄到一個聯集態才燒完燃料,得到的是 `Blur { partial: Some(Union[...]) }`
——**格上的位置被包進了「停下來的理由」裡。**

⟹ 「blur 究竟是聯集態、bottom 還是 top」問不出答案,**不是因為概念不清,是因為它
根本不在那條軸上。**

> 用戶原本的設計(口述):觀測/收斂的結果只有**聯集態 / 原子態 / `_|_`** 三種,
> 為了區分 bottom 才設計了 `%cause`;後來覺得有些東西該是 **top(帶 %cause)**。
> 本文認為那個「後來」是對的,而且**它已經發生過,只是沒有被寫成規則**(§3)。

---

## 2. 實際值域〔讀 `value.rs:216`〕

```
Top   TopCaused{cause,members}   Atom   Combo   Union
Code   Thunk   Ref   Bottom(BottomDetail)   Blur(BlurDetail)   Range
```

**11 個變體。** 其中 `Thunk` / `Code` / `Ref` 是「還沒收斂 / 非結果」,
其餘 8 個才是觀測結果。原設計說 3 種。

**`Blur` 既不是聯集態、也不是 bottom、也不是 top —— 它是自己一格**,而且是唯一帶著
**視界參數**與**部分結果**的那一個。

---

## 3. 「不知道 → top,矛盾 → bottom」已經被套用兩次,規則從沒寫下來

`TopCaused` 的註解把 cause 鎖死〔讀 `value.rs:218`〕:

```rust
/// `cause`: `"static_cycle"` | `"no_coordinate"` (ERROR_CODES tags).
/// lattice-identical to bare Top (solution set = everything) with
/// observation-only provenance.
```

**只有這兩個。** 也就是說「有些東西不該算 bottom 而該算 top」這件事已經做過兩次,
每次都是個案。

**候選規則(格論強制,不是偏好):**

> **「我還不知道」是 top。「我知道它矛盾」是 bottom。**

按這條,`#fuel_exhausted` 在 strict 下變成 bottom 是**錯的**——算不完不是矛盾,
是沒有前進。正確的 strict 語義應是「回 top(帶 cause)並拒絕固化」,
而不是宣稱一個比實情強得多的東西。

---

## 4. `#fuel_exhausted` 的歸屬:是策略決定的,不是它本身的性質

〔讀 `crates/interpreter/src/observation.rs:56` `handle_resource_exhausted`〕
——**三個分支寫在同一個函式裡:**

| `ObservationStrategy` | 產出 | 部分結果去哪 |
| :-- | :-- | :-- |
| `Strict` | `Bottom { cause: FuelExhausted }` | 塞進 `found` 欄位 |
| `Blur` | `Blur { cause, horizon, partial }` | `partial`,正位 |
| `Approximate` | `Atom(Tag("approximate"))` | **被丟掉** |

⟹ **「`#fuel_exhausted` 在 blur 底下」是對的**;`#strict` 才是把它變成 bottom 的那個,
而那正是 strict 的意思(「別給我半成品」)。

> 記帳:本文作者曾據 `BottomCause` enum 單獨斷言「燃料用盡是一個 `_|_`」,
> 該斷言不完整——**讀 enum 不等於量行為**。

**但第三行是真缺陷:** `Approximate` 回一個**原子**,沒有 cause、沒有視界、沒有
partial。原子的意思是「收斂完成的確定值」,而這個東西不是。**它對自己的種類說謊。**

---

## 5. 兩條軸的詞彙已經存在於 SPEC_08 §3.2.1,只是別處不用它

> **更正(2026-08-02):** 本節初稿寫「`#incomplete` 與 `#fuel_exhausted` 是兩個碼在說
> 同一件事」。**那是錯的**,而且錯在把「原因」和「狀態」當成同一類東西比較。
> 由另一個持早期規格的 agent 的答覆間接引出,查證後改寫。

SPEC_08 §3.2.1「語義邊界:暫態與快照」:

| | 是什麼 | 可否內容定址 |
| :-- | :-- | :-- |
| **`#incomplete`** | 觀測精度的「**掛起**」——「計算請求的**餘額**」 | **不可**(結果隨燃料變動) |
| **`#blur`** | 觀測精度的「**凍結**」——(視界參數 + 局部收斂結果)的內容雜湊 | **可**,且 CAID **必須**含視界參數 |

同節註腳(§172):

> 若引擎根據 `%strategy: #blur` 決定將中斷點轉化為可傳遞狀態,則該節點從
> `#incomplete` **提升(Lift)為 `#blur`**。

**那就是 §4 量到的 `handle_resource_exhausted` 三分支,規格裡的名字叫 Lift。**

⟹ 正確的分層是:

* **「為什麼停」(原因)**:`#fuel_exhausted` / `#timeout` / `#stack_overflow` /
  `#log_singularity`
* **「你現在手上握著什麼」(狀態)**:`#incomplete`(暫態,不可定址) /
  `#blur`(快照,可定址) / `_|_`(strict 下)

**§1 的兩條軸不但存在,SPEC_08 §3.2.1 已經把它畫對了。**

### 5.1 真正的病:別的文件不用這套詞彙

* **ERROR_CODES** 把 `#incomplete`(狀態)與 `#fuel_exhausted`(原因)並列在同一張表
  的同一欄裡,兩者的「建議修法」都寫「增加 `%fuel`」,讀起來像同義詞。
* **SPEC_04 §162** 直接跳過中間狀態:「全量觀測掛 fuel 視界,自指結構於視界**誠實
  截斷為 `_|_ #fuel_exhausted`**」——沒有提 `#incomplete`,沒有提 Lift,
  也沒有說那只是 strict 下的結果。

**與 SPEC_13 §0 / APP_05 §2.1 那張重複的五層譜模型表同一種病:對的東西寫在一個
地方,別處不知道它存在。**

### 5.2 §3.2.1 順帶答掉的另一件事

「`#incomplete` **不具備內容定址的合法性**」給了 §1 那條軸一個**硬理由**,不是美學:
它的值會隨燃料改變,所以它不能有 CAID;而 `#blur` 之所以可以,正是因為它的 CAID
**必須**包含視界參數——把「在什麼條件下停的」烘進身分裡,它才重新變成一個穩定的東西。

⟹ **這也是「格是穩定狀態」在觀測未完成時的正確拼法。**

---

## 6. 相關:這條軸也解釋了別處的混用

* `BottomCause` 裡同時住著 `Conflict`(過度約束)與 `FuelExhausted` / `Timeout`
  (沒算完)——**格上相反的兩端共用一個拼法**。
* `Blur` 有 `MathSingularity`,而 ERROR_CODES `#log_singularity` 寫「預設策略下回傳
  `#blur` 並以本標籤標記 `%cause`」——這一格是自洽的,可作為正確用法的樣本。

---

## 7. 開放問題

0. **(§5 之後升為首位)把 SPEC_08 §3.2.1 的「原因 / 狀態」二分推廣到 ERROR_CODES
   與 SPEC_04。** 這一件不需要任何裁定——詞彙已經存在且已經是規範性的,只是別處
   沒有用它。成本最低、影響最大。
1. **兩條軸要不要拆開?**(位置 × 停下來的理由)
   若拆,`Blur` 會從一個 `Value` 變體變成一個**標註**,而 `partial` 就直接是那個值本身。
   這是大改,但它一次解掉「這些觀念全部混著用」。
   (注意:§5.2 給了 `#blur` 保持獨立型別的**理由**——CAID 必須含視界參數。
   所以這一題不是「Blur 不該存在」,是「Blur 是不是該只在**要定址它**的時候才出現」。)
2. **「不知道 → top,矛盾 → bottom」要不要升成規則?**
   寫下來之後 `#fuel_exhausted` 在 strict 下的歸屬就自動有答案,不必逐案裁定。
   (SPEC_08 §3.2.1 對 `#incomplete` 已經給了第三個選項:**權限校驗**,
   而不是二選一。)
3. **`TopCaused` 的 cause 要不要開放?** 今天鎖死在兩個字串。
4. **`Approximate` 回原子:修,還是廢掉這個策略?**
5. **`#incomplete` 與 `#fuel_exhausted` 合併,還是講清楚分工?**
6. **`%cause` 到底掛在誰身上?** 今天 `Bottom`、`Blur`、`TopCaused` 各有一套自己的
   cause 型別(`BottomCause` / `BlurCause` / `String`),三者不共用詞彙表。

---

## 9. 第三條軸:`%effect`

(2026-08-03。用戶在收尾時想到「`%effect` 一直沒討論到」,查證後確認它不是多慮。)

**〔讀〕它是什麼,SPEC_08 §4.1 註解直接說了:**

> 同屬「**值不由內容決定、依賴外部子空間**」這**同一個**障礙,差別僅在出處。

**〔讀〕它住在值上,不是住在 commit 上。** `EffectTag(u8)` 是位元場
(`Pure=0` / `IO=0b0001` / `NonDet=0b0010` / `State=0b0100`),而
`Value` 的 `Atom` / `Thunk` / `Blur` / `Combo` **每一個都帶一個**。
SPEC_08 §4.2.1 結構傳染:任一欄位有效果 ⟹ 容器有效果(join)。

### 9.1 它填的是 `commit.md` §1.8 漏掉的一格

`commit.md` §1.8 把「自我認證 / 可重算 / 斷言」寫成一條軸上的三點。
**實際上那是兩個獨立的布林**,而 `%effect` 住在沒被寫出來的那一格:

| | 能驗證它是它宣稱的嗎? | 能再產生一次嗎? |
| :-- | :-- | :-- |
| `#pure` 值 · `DERIVED` 邊 | ✓ | ✓ |
| **`#io` / `#nondet` / `#state` 值** | **✓(雜湊它)** | **✗** |
| `DECLARED` 邊 · pin 日誌 · 廣告 | ✗(只能信簽章) | ✗ |
| —— | ✗ | ✓(空) |

⟹ **`%effect ≠ #pure` 就是「這個值可被定址,但不可被重現」的標記。**

### 9.2 兩件本來像特例的事,因此不再是特例

* **為什麼 `#io` 值可以合法地被提交。** SPEC_10 §1.1:「宇宙歷史由**因果邊界**
  固化,而非由真理固化」——因為它**可驗證**(你確實得到了這個),
  只是**不可重現**(別人重跑不會得到同一個)。那不是通融,是那一格的定義。
* **傳染不是一條規定,是那一格的封閉性。** 從不可重現的值算出來的東西必然
  不可重現。而 **Cocoon 屏蔽是在邊界上斷言純度**——一句你從外面驗不了的話,
  所以 Cocoon 的純度宣告落在第三列(斷言),不是第一列。

### 9.3 待確認

* Q3 與 Q1/Q2 的正交性只在**值域**上檢查過,**沒有實測**是否每個組合都可達
  (例:`#io` 的 `#blur`)。
* `%effect` 與 `%cause` 的關係:`BottomCause::EffectViolation` 存在
  (宣告 `#pure` 卻被傳染),那是 Q3 的違反落到 Q1 的 bottom 上——
  **三條軸之間唯一已知的耦合點**,值得單獨看。
* disc 023 記著「`%effect` = 觀測障礙」。本節從「可重現性」進來,
  與那條路線是否同一件事,未對照。

---

## 8. 素材出處

* `crates/interpreter/src/value.rs` — `Value`(§216)、`BlurDetail`(§1549)、
  `BlurCause`(§1515)、`BottomDetail`(§1119)、`BottomCause`(§1349)。
* `crates/interpreter/src/observation.rs:56` — `handle_resource_exhausted`。
* `spec/zh_TW/ERROR_CODES.md` — `#incomplete`、`#fuel_exhausted`、`#log_singularity`。
* `spec/zh_TW/SPEC_04` §162 — force = 觀測原語,fuel 只在 force 點消耗。
* `spec/zh_TW/SPEC_00` §5 — 五條語義不變性(邊界一致性那條沒有內容)。
