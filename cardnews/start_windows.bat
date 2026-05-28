@echo off
chcp 65001 >nul
cd /d %~dp0

:menu
cls
echo ============================================
echo        카드뉴스 자동화 - 시작 메뉴
echo ============================================
echo.
echo   원하는 작업의 번호를 누르고 Enter 하세요.
echo.
echo   [1] 최초 설치        (맨 처음 한 번만)
echo   [2] 프로그램 실행    (매번 켤 때)
echo   [3] 클라우드 배포 안내 (컴퓨터 꺼도 예약 돌리기)
echo   [4] 종료
echo.
set /p choice="번호 입력: "

if "%choice%"=="1" goto setup
if "%choice%"=="2" goto run
if "%choice%"=="3" goto deploy
if "%choice%"=="4" exit /b 0
echo.
echo 1~4 중에서 선택하세요.
pause
goto menu

:setup
call setup_windows.bat
goto menu

:run
call run_windows.bat
goto menu

:deploy
echo.
echo 클라우드 배포 안내 문서를 엽니다...
start "" notepad DEPLOY.md
goto menu
