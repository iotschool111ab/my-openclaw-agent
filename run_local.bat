@echo off
chcp 65001 >nul
:: ============================================================
:: 本地 Windows 開發啟動腳本（需要 ngrok）
:: 使用方式: 雙擊 run_local.bat 或在 cmd 執行
:: ============================================================

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║         LINE Bot AI 生活助理 - 本地開發模式         ║
echo ╚══════════════════════════════════════════════════════╝
echo.

:: ── 1. 確認 .env 存在 ──────────────────────────────────────
if not exist ".env" (
    echo [錯誤] 找不到 .env 檔案
    echo        請先建立 .env，參考 template\.env.example
    echo.
    pause
    exit /b 1
)

:: ── 2. 確認 ngrok 已安裝 ───────────────────────────────────
where ngrok >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [錯誤] 未安裝 ngrok
    echo.
    echo 安裝方式（擇一）：
    echo   方法1 - 官網下載: https://ngrok.com/download
    echo   方法2 - winget:   winget install ngrok.ngrok
    echo   方法3 - Chocolatey: choco install ngrok
    echo.
    echo 安裝後請執行: ngrok config add-authtoken ^<你的token^>
    echo Token 取得: https://dashboard.ngrok.com/get-started/your-authtoken
    pause
    exit /b 1
)

:: ── 3. 確認 Python 已安裝 ──────────────────────────────────
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [錯誤] 未安裝 Python
    echo        請從 https://python.org 下載安裝
    pause
    exit /b 1
)

:: ── 4. 啟動 Flask（新視窗）─────────────────────────────────
echo [1/2] 啟動 Flask 伺服器（port 5000）...
start "LINE Bot - Flask Server" cmd /k "python main_lifestyle.py"

:: 等待 Flask 啟動
timeout /t 3 /nobreak >nul

:: ── 5. 啟動 ngrok ──────────────────────────────────────────
echo [2/2] 啟動 ngrok 公開隧道...
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║  ngrok 啟動後請複製 Forwarding URL                  ║
echo ║  LINE Webhook URL = Forwarding URL + /callback      ║
echo ║  範例: https://xxxx.ngrok-free.app/callback         ║
echo ╚══════════════════════════════════════════════════════╝
echo.
echo 設定步驟：
echo   1. 複製下方 ngrok 顯示的 Forwarding https:// 網址
echo   2. 加上 /callback 後貼到 LINE Developer Console
echo   3. 點擊 Verify 確認
echo.
ngrok http 5000
