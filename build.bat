@echo off
echo ========================================
echo ARMR Mirror Tool - Build Script
echo ========================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.7+ and try again.
    pause
    exit /b 1
)

echo.
echo Checking dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo Building distribution...
python build.py
if errorlevel 1 (
    echo ERROR: Build failed. Check the error messages above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Your distribution is ready in: ARMR_Mirror_Tool_Distribution/
echo.
echo You can now distribute this folder to your clients.
echo.
pause 