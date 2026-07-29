# n/ 合規語料庫 (Conformance Corpus)

> **Authority**: [Normative / 規範性] — 本目錄是 **REAL_05 §3 合規矩陣的可執行形式**。
> 索引與出處見 `spec/zh_TW/REAL_05_Compliance_and_MVP.md`;版號閘門見 `meta/VERSIONING.md` §3
> (引擎裸核版號 = 通過 Level 2 全數向量)。

## 檔案約定

- `L1/`、`L2/` 依合規等級分目錄;每向量一對檔案:
  - `NN-slug.n` — 輸入程式。**被觀測欄位一律名為 `out`**。
  - `NN-slug.expect` — 期望輸出。
- 向量 ID = `L<級>-<NN>`(如 `L1-05`),與 REAL_05 §3 索引一一對應。

## Runner 契約

1. 對每個 `.n` 檔執行等價於 `oo run FILE --observe out` 的觀測。
2. **值期望**:stdout(去除首尾空白)必須與 `.expect` 首段**逐字元相等**
   (canonical print;多行 combo 含縮排)。
3. **⊥ 期望**:`.expect` 首行為 `_|_`。下列任一即為通過:
   - stdout 以 `_|_` 開頭;
   - 演化衝突報錯(非零退出 + Conflict 類錯誤)。
4. **`%cause` 行**(`.expect` 第二行,如 `%cause: #divergent`):規範性標註。
   - Level 1/2 合規:**SHOULD**(不比對強制;引擎目前以人話註解印因果,
     統一印出 `%cause` 標籤屬引擎待辦);
   - Level 3 起:**MUST**(REAL_04 因果鏈義務)。
5. 逐向量報告 pass/fail;任一 fail = 該等級不合規(§4 通過標準:100%)。

參考 runner:`scripts/run-conformance.py --engine <oo 路徑>`(唯讀,不改語料)。

## 紀律

- 語料是**法典的一部分**:新增/修改向量 = 規格變更,走 changelog
  (破壞性/增量/編輯性)與(v0.5.0 後)RFC 流程。
- 向量必須引用裁決出處(REAL_05 §3 索引之「出處」欄);孤兒向量不收。
- 引擎已知未通過的向量**照收不刪**——矩陣記錄規格真值,不遷就實作
  (現況見 REAL_05 §3.5)。
