#!/bin/bash
# ============================================================
# 本地 Linux / macOS 開發啟動腳本（需要 ngrok）
# 使用方式: bash run_local.sh
# ============================================================

set -e

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║       LINE Bot AI 生活助理 - 本地開發模式           ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# ── 1. 確認 .env 存在 ───────────────────────────────────────
if [ ! -f ".env" ]; then
    echo "[錯誤] 找不到 .env 檔案"
    echo "       請先建立 .env（參考 template/.env.example）"
    exit 1
fi

# ── 2. 確認 ngrok 已安裝 ────────────────────────────────────
if ! command -v ngrok &> /dev/null; then
    echo "[錯誤] 未安裝 ngrok"
    echo ""
    echo "安裝方式（擇一）："
    echo "  macOS:  brew install ngrok/ngrok/ngrok"
    echo "  Linux:  snap install ngrok"
    echo "  或到 https://ngrok.com/download 下載"
    echo ""
    echo "安裝後請執行: ngrok config add-authtoken <你的token>"
    exit 1
fi

# ── 3. 啟動 Flask（背景執行）───────────────────────────────
echo "[1/2] 啟動 Flask 伺服器（port 5000）..."
python main_lifestyle.py &
FLASK_PID=$!

# 等待 Flask 啟動
sleep 3

# 確認 Flask 有在跑
if ! kill -0 $FLASK_PID 2>/dev/null; then
    echo "[錯誤] Flask 啟動失敗，請檢查錯誤訊息"
    exit 1
fi

echo "       Flask PID: $FLASK_PID"

# ── 4. 啟動 ngrok ───────────────────────────────────────────
echo "[2/2] 啟動 ngrok 公開隧道..."
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  ngrok 啟動後請複製 Forwarding URL                  ║"
echo "║  LINE Webhook URL = Forwarding URL + /callback      ║"
echo "║  範例: https://xxxx.ngrok-free.app/callback         ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Ctrl+C 時同時關掉 Flask
trap "echo ''; echo '關閉中...'; kill $FLASK_PID 2>/dev/null; exit 0" INT TERM

ngrok http 5000

# ngrok 結束後也關掉 Flask
kill $FLASK_PID 2>/dev/null
