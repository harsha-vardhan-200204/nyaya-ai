@echo off
title NyayaAI Launcher
echo ====================================================================
echo               NYAYAAI LEGAL TECH APPLICATION LAUNCHER
echo ====================================================================
echo.
echo Launching services...
echo.

:: Start Backend Uvicorn Server in a new window
start cmd /k "title NyayaAI Backend Server && echo [BACKEND] Starting FastAPI server on port 8000... && cd backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

:: Start Frontend Vite Server in a new window
start cmd /k "title NyayaAI Frontend Dev && echo [FRONTEND] Starting React dev server on port 5173... && cd frontend && npm run dev"

echo ====================================================================
echo   SERVICES INITIATED SUCCESSFUL
echo ====================================================================
echo.
echo   Frontend Application Portal:  http://localhost:5173
echo   Backend OpenAPI Swagger Docs: http://127.0.0.1:8000/docs
echo.
echo   DEFAULT DEMO LOGIN CREDENTIALS:
echo   --------------------------------------------------------------
echo   Role          Username      Password
echo   --------------------------------------------------------------
echo   Client:       client        client123
echo   Lawyer:       lawyer        lawyer123
echo   Admin:        admin         admin123
echo   --------------------------------------------------------------
echo.
echo Press any key to close this launcher console...
pause > nul
