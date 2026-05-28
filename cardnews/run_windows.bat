@echo off
chcp 65001 >nul
cd /d %~dp0

if not exist .venv (
  echo [오류] 먼저 setup_windows.bat 을 실행해 설치하세요.
  pause
  exit /b 1
)

call .venv\Scripts\activate.bat

echo 서버를 시작합니다. 잠시 후 브라우저가 자동으로 열립니다...
echo (종료하려면 이 창에서 Ctrl+C 를 누르거나 창을 닫으세요)
echo.

REM 4초 뒤 브라우저 자동 열기
start "" cmd /c "timeout /t 4 >nul & start http://localhost:8000"

python -m uvicorn app.main:app --port 8000

pause
