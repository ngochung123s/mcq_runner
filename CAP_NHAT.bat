@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === Cap nhat thu vien de tu thu muc data ===
python tools\build_library.py
if errorlevel 1 (
  echo LOI: khong dung duoc thu vien. Kiem tra file JSON trong data\.
  pause
  exit /b 1
)
echo.
echo === Sao luu len GitHub ===
git add -A
git diff --cached --quiet
if errorlevel 1 (
  git commit -q -m "Cap nhat %date% %time:~0,5%"
  git push -q
  if errorlevel 1 (echo LOI: push that bai, kiem tra mang.) else (echo Da sao luu len GitHub.)
) else (
  echo Khong co thay doi moi.
)
echo.
pause
