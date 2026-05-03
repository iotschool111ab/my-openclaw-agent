#!/bin/bash
# ============================================================
# GitHub Codespaces 啟動腳本
# 使用方式: bash run_codespace.sh
# ============================================================

set -e

# ── 1. 確認在 Codespaces 環境 ──────────────────────────────
if [ -z "$CODESPACE_NAME" ]; then
    echo "[錯誤] 此腳本需在 GitHub Codespaces 中執行"
    echo "       本地開發請使用 run_local.sh 或 run_local.bat"
    exit 1
fi

# ── 2. 確認 .env 存在 ───────────────────────────────────────
if [ ! -f ".env" ]; then
    echo "[警告] 找不到 .env 檔案"
    echo "       請先建立 .env（參考 template/.env.example）"
    echo ""
    echo "最低需要設定："
    echo "  LINE_CHANNEL_ACCESS_TOKEN=..."
    echo "  LINE_CHANNEL_SECRET=..."
    echo "  GROQ_API_KEY=..."
    exit 1
fi

# ── 3. 確認 port 5000 為公開狀態 ────────────────────────────
echo ""
echo "正在設定 port 5000 為公開..."
# 使用 GitHub CLI 設定 port visibility（若 gh 可用）
if command -v gh &> /dev/null; then
    gh codespace ports visibility 5000:public -c "$CODESPACE_NAME" 2>/dev/null || true
fi

# ── 4. 顯示 Webhook URL ─────────────────────────────────────
WEBHOOK_URL="https://${CODESPACE_NAME}-5000.app.github.dev/callback"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║         LINE Webhook URL（請複製到 LINE Console）    ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║  $WEBHOOK_URL"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "設定步驟："
echo "  1. 前往 https://developers.line.biz/console/"
echo "  2. 選擇你的 Messaging API channel"
echo "  3. 貼上以上 URL 到 Webhook URL 欄位"
echo "  4. 點擊「Verify」確認連線"
echo ""
echo "啟動伺服器中..."
echo "────────────────────────────────────────────────────────"

# ── 5. 啟動 Flask ────────────────────────────────────────────
python main_lifestyle.py
