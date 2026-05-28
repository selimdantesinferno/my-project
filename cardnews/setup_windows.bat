@echo off
chcp 65001 >nul
cd /d %~dp0
echo ============================================
echo   카드뉴스 자동화 - 최초 설치 (한 번만)
echo ============================================
echo.

echo [1/3] 파이썬 가상환경 생성 중...
python -m venv .venv
if errorlevel 1 (
  echo.
  echo [오류] 파이썬을 찾을 수 없습니다.
  echo python.org 에서 Python 3.11 이상을 설치하세요.
  echo 설치 시 "Add Python to PATH" 를 꼭 체크하세요!
  pause
  exit /b 1
)

echo [2/3] 필요한 패키지 설치 중... (몇 분 걸릴 수 있어요)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo [3/3] 설정 파일 준비 중...
if not exist .env copy .env.example .env

echo.
echo ============================================
echo   설치 완료!
echo ============================================
echo.
echo 다음 순서로 진행하세요:
echo   1. 같은 폴더의 .env 파일을 메모장으로 열어 API 키/토큰을 입력
echo   2. run_windows.bat 을 더블클릭해서 실행
echo.
pause
