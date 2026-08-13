# meta/ — 專案後設文件 (Project Meta-Documents)

放置「關於規格書」而非「屬於規格書」的工作文件：spec ↔ 論文系列的映射與審計、
路線圖、歷史素材。這些文件是活的（隨工作演進），位階不屬於法典（SPEC/SYNTAX/REAL/
ORDER/APP），先前散落在 repo 根目錄，2026-07-05 歸檔於此。

## 索引

| 文件 | 內容 | 狀態 |
| :--- | :--- | :--- |
| **[integration_map.md](./integration_map.md)** | 論文 I–VI + L-S → spec 的整合地圖 | 完成（歷史文件） |
| **[integration_map_2.md](./integration_map_2.md)** | 論文 VII–XXII → spec 的整合地圖（含 P3 解凍） | 完成（歷史文件） |
| **[claims_ledger.md](./claims_ledger.md)** | 數學宣稱帳本：spec↔series 關係審計（R0/R1/R2/R3） | 活文件；初審通過 2026-07-03 |
| **[WORK_QUEUE.md](./WORK_QUEUE.md)** | 唯一施工佇列：Active／Ready／Blocked／Inbox 與下一弧 | 活文件；現行排序權威 |
| **[oo/STATUS.md](./oo/STATUS.md)** | oo 主題的已裁定／開放問題設計帳 | 活文件；不排施工順序 |
| **[ENGINE_SYNC.md](./ENGINE_SYNC.md)** | 參考引擎符合性、量測與版本交付史 | 追加式歷史；不排施工順序 |
| **[ROADMAP.md](./ROADMAP.md)** | 長程里程碑與 gate（取代 spec/zh_TW/README §4 的舊 TODO 表） | 活文件；不收逐弧待辦 |
| **[history_origins.md](./history_origins.md)** | 設計決策的發現鏈（口述歷史落檔）——未來對外 intro 的素材 | 素材（intro 待語言到一個段落才發表） |

## 兩個已決定但尚未啟用的位置

- **Changelog**：規格仍在大幅變動、引擎尚無正式版本——暫不設。啟用時**與 spec 同住**
  （`spec/` 側），不放這裡。
- **對外介紹（intro）**：草稿在 workspace 私人側（docs/intro.md，兩個未完成版本）；
  發表門檻 = 語言完成到一個段落。`history_origins.md` 是它的素材庫。

## 讀者提示

Review agents 慣例從 `spec/zh_TW/README.md` 開始讀；該檔 §4 現在只留路線圖快照與
指向本目錄的指標。研究側的對應物：`research/RESEARCH_FRONTIER.md`（數學開放問題）、
`research/worknotes/`（協作工作文件的公開櫥窗）。
