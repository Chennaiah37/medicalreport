@echo off
echo === MedReport AI — Windows Launcher ===
echo.

REM Check if venv exists, create if not
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install packages if needed
echo Installing / checking packages...
pip install -r requirements.txt --quiet

REM Launch app
echo.
echo Starting MedReport AI...
echo Open your browser at: http://localhost:8501
echo Press Ctrl+C to stop
echo.
python -m streamlit run app.py

pause
