@echo off
chcp 65001 >nul
cd /d "%~dp0"
setlocal

rem Cong cu build (JDK 17, Android SDK, Gradle) nam trong %LOCALAPPDATA%\Android, khong can Android Studio.
set "ANDROID_HOME=%LOCALAPPDATA%\Android\Sdk"
for /d %%J in ("%LOCALAPPDATA%\Android\jdk\jdk-17*") do set "JAVA_HOME=%%~fJ"
set "GRADLE=%LOCALAPPDATA%\Android\gradle-8.14.3\bin\gradle.bat"
if not defined JAVA_HOME (echo LOI: khong thay JDK 17 trong %LOCALAPPDATA%\Android\jdk & pause & exit /b 1)
if not exist "%GRADLE%" (echo LOI: khong thay Gradle: %GRADLE% & pause & exit /b 1)

echo === Dung lai thu vien de tu data\ ===
python tools\build_library.py
if errorlevel 1 (echo LOI: khong dung duoc thu vien. & pause & exit /b 1)

echo.
echo === Build APK (lan dau mat vai phut) ===
call "%GRADLE%" -p android --console=plain -q assembleDebug
if errorlevel 1 (echo LOI: build APK that bai. & pause & exit /b 1)

copy /y "android\app\build\outputs\apk\debug\app-debug.apk" "MedMCQ.apk" >nul
echo.
echo Xong: %~dp0MedMCQ.apk
echo Chep file nay sang dien thoai roi mo de cai.
pause
