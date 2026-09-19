@echo off
setlocal enabledelayedexpansion

REM ============================================================
REM build_exe_CORREGIDO.bat
REM Proyecto: FOLLOW_the_CATAPUM
REM
REM IMPORTANTE:
REM - El ejecutable correcto sale en: dist\FOLLOW_the_CATAPUM\FOLLOW_the_CATAPUM.exe
REM - NO ejecutes nada desde la carpeta build\
REM - Si usas --onedir, hay que copiar SIEMPRE toda la carpeta dist\FOLLOW_the_CATAPUM
REM ============================================================

cd /d "%~dp0"

REM -------- CONFIGURACION --------
set "APP_NAME=FOLLOW_the_CATAPUM"
set "ENTRY=main.py"
set "PACKAGE_NAME=follow_catapum"
set "APP_ICON=assets\icono.ico"
set "ASSETS_DIR=assets"
set "CONFIG_DIR=config"

REM Recomendado para CustomTkinter/PIL/pandas/serial
set "BUILD_MODE=--onedir"
set "CONTENTS_DIR=_internal"

REM -------- COMPROBACIONES --------
if not exist "%ENTRY%" (
    echo.
    echo [ERROR] No encuentro %ENTRY%.
    echo Este .bat debe estar en la carpeta raiz del proyecto, junto a main.py.
    echo.
    pause
    exit /b 1
)

if not exist "%PACKAGE_NAME%" (
    echo.
    echo [ERROR] No encuentro la carpeta %PACKAGE_NAME%.
    echo.
    pause
    exit /b 1
)

if not exist "%APP_ICON%" (
    echo.
    echo [ERROR] No encuentro el icono: %APP_ICON%
    echo.
    pause
    exit /b 1
)

REM Usar entorno virtual si existe. Si no, usar Python global.
if exist ".venv\Scripts\python.exe" (
    set "PYTHON=.venv\Scripts\python.exe"
) else (
    set "PYTHON=python"
)

echo.
echo ============================================
echo  Generando EXE de %APP_NAME%
echo ============================================
echo Python:  %PYTHON%
echo Entrada: %ENTRY%
echo Modo:    %BUILD_MODE%
echo.

REM -------- INSTALAR / ACTUALIZAR --------
"%PYTHON%" -m pip install --upgrade pip
"%PYTHON%" -m pip install --upgrade pyinstaller

REM Si existe requirements.txt, instala dependencias del proyecto.
if exist "requirements.txt" (
    echo.
    echo Instalando requirements.txt...
    "%PYTHON%" -m pip install -r requirements.txt
)

REM -------- ARGUMENTOS DE DATOS --------
set "DATA_ARGS="

if exist "%ASSETS_DIR%" (
    set "DATA_ARGS=!DATA_ARGS! --add-data=%ASSETS_DIR%;%ASSETS_DIR%"
)

if exist "%CONFIG_DIR%" (
    set "DATA_ARGS=!DATA_ARGS! --add-data=%CONFIG_DIR%;%CONFIG_DIR%"
)

REM -------- LIMPIEZA --------
echo.
echo Limpiando build, dist y spec anteriores...
echo.

if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "%APP_NAME%.spec" del /q "%APP_NAME%.spec"

REM -------- COMPILACION --------
echo.
echo Compilando con PyInstaller...
echo.

"%PYTHON%" -m PyInstaller ^
    %BUILD_MODE% ^
    --contents-directory "%CONTENTS_DIR%" ^
    --noconfirm ^
    --windowed ^
    --clean ^
    --name "%APP_NAME%" ^
    --icon "%APP_ICON%" ^
    %DATA_ARGS% ^
    --paths "." ^
    --collect-all customtkinter ^
    --collect-all PIL ^
    --collect-submodules "%PACKAGE_NAME%" ^
    --hidden-import serial.tools.list_ports ^
    --hidden-import openpyxl ^
    "%ENTRY%"

if errorlevel 1 (
    echo.
    echo ============================================
    echo  ERROR al generar el .exe
    echo ============================================
    echo Revisa los mensajes anteriores de PyInstaller.
    echo.
    pause
    exit /b 1
)

REM -------- COMPROBACION DEL RESULTADO --------
echo.
echo Comprobando salida...
echo.

if not exist "dist\%APP_NAME%\%APP_NAME%.exe" (
    echo [ERROR] No se ha encontrado el ejecutable final.
    echo Esperado: dist\%APP_NAME%\%APP_NAME%.exe
    echo.
    pause
    exit /b 1
)

if not exist "dist\%APP_NAME%\%CONTENTS_DIR%\python311.dll" (
    echo [AVISO] No encuentro dist\%APP_NAME%\%CONTENTS_DIR%\python311.dll
    echo Si tu Python no es 3.11 puede llamarse python310.dll, python312.dll, etc.
    echo Mira dentro de dist\%APP_NAME%\%CONTENTS_DIR%.
) else (
    echo OK: encontrada dist\%APP_NAME%\%CONTENTS_DIR%\python311.dll
)

REM -------- CREAR ZIP DISTRIBUIBLE --------
echo.
echo Creando ZIP distribuible...
echo.

if exist "dist\%APP_NAME%_DISTRIBUIBLE.zip" del /q "dist\%APP_NAME%_DISTRIBUIBLE.zip"
powershell -NoProfile -ExecutionPolicy Bypass -Command "Compress-Archive -Path 'dist\%APP_NAME%' -DestinationPath 'dist\%APP_NAME%_DISTRIBUIBLE.zip' -Force"

echo.
echo ============================================
echo  EXE generado correctamente
echo ============================================
echo.
echo Ejecutable correcto:
echo   dist\%APP_NAME%\%APP_NAME%.exe
echo.
echo ZIP correcto para enviar/copiar:
echo   dist\%APP_NAME%_DISTRIBUIBLE.zip
echo.
echo MUY IMPORTANTE:
echo - No ejecutes el .exe desde build\%APP_NAME%.
echo - No copies solo el .exe.
echo - Copia toda la carpeta dist\%APP_NAME% o usa el ZIP generado.
echo.
explorer "dist\%APP_NAME%"
pause
