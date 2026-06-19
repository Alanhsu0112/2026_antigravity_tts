# ANTIGRAVITY.md - 專案記憶與開發指南

本檔案由 AntiGravity 自動維護，用以記錄本專案的偏好設定、架構決策與開發進度。

## 📌 專案基本資訊
- **專案名稱**：2026_antigravity_tts
- **專案類型**：TTS (Text-to-Speech) 文字轉語音應用
- **本地路徑**：`/Users/alan/Library/CloudStorage/GoogleDrive-alanhsu0112@gmail.com/我的雲端硬碟/2026_antigravity_tts`
- **GitHub 儲存庫**：https://github.com/alanhsu0112/2026_antigravity_tts (預期)
- **Obsidian 專案筆記**：[2026_antigravity_tts.md](file:///Users/alan/Library/Mobile%20Documents/iCloud~md~obsidian/Documents/%E7%9F%A5%E8%AD%98%E5%BA%AB/2026_antigravity_tts.md)

## 🛠️ 開發規範與偏好
1. **程式碼風格**：
   - 保持檔案註解與 docstring 的完整性。
   - 所有說明及提交訊息皆使用**繁體中文**。
2. **Git 工作流**：
   - 不無差別執行 `git add .`，僅 stage 與本次變更相關的檔案。
   - commit 前必須檢查 diff 確保品質。
3. **Obsidian 連接**：
   - 在專案開工/收工時，將狀態與 TODO 同步更新至 Obsidian 筆記庫。

## 📝 當前狀態與下一步
- **[2026-06-19]**
  1. 初始化專案基礎結構並串接 GitHub 與 Obsidian `知識庫`。
  2. 複製克隆語音專案 `voxcpm2-voice-cloner`，並在 macOS 上以 `uv` 完成 Python 3.12 虛擬環境建立與 `voxcpm`、`sounddevice` 依賴安裝，測試成功。
  3. 將 Alan 聲音克隆打包為全域 AI 技能（Skill）[SKILL.md](file:///Users/alan/.gemini/config/skills/alan-voice-cloner/SKILL.md)，已完成指令綁定與功能測試。

