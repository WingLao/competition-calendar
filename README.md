# 比賽日曆

網站：https://winglao.github.io/competition-calendar/ （GitHub Pages 由 `main` 分支根目錄發布）

科技類學生比賽的下一屆日期、報名、官方網址及升學作用。頁面設有 noindex；不含學生姓名。

| 檔案 | 用途 |
| --- | --- |
| `data.json` | **唯一的資料來源**：比賽清單、日期及最新消息 |
| `index.html` | 讀取 `data.json` 的頁面 |
| `ROUTINE.md` | 每天檢查的工作說明（雲端排程的助手按它執行） |
| `admissions-watch.json` | 升學加分條文追蹤清單（香港為重點，另有澳門四校及內地）；每週一由同一排程檢查，有新簡章或條文改動時電郵通知 |
| `check.py` | 提交前檢查格式及不可公開的資料 |

## 怎樣更新

- **每天自動**：雲端排程每天檢查官方消息，有來源的新資料寫入 `data.json` 並直接上線；有新消息時電郵通知老師。
- **人手**：直接修改 `data.json`（可在 GitHub 網頁上編輯），執行 `python3 check.py` 後提交到 `main`。新增或刪除比賽、修改分類（`group`）及升學作用（`advice`）只由老師決定。

## 相關資料

- 升學作用的依據：[升學加分問答指南](https://winglao.github.io/admissions/)
- CDSJ5 比賽與升學整合網站的「比賽日曆」按鈕前往本網站；該網站的更新檢查會讀取本網站的 `data.json`，提醒校內文件要跟進的地方。
