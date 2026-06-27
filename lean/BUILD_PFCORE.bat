@echo off
REM === Build PFCore.lean for Greg ===
REM Run this from the Windows side where Devin originally built.
REM Save as: D:\fundamentals\lean\BUILD_PFCORE.bat

cd /d D:\fundamentals\lean

REM Find lake — check common locations
set LAKE=
if exist "%USERPROFILE%\.elan\bin\lake.exe" set LAKE=%USERPROFILE%\.elan\bin\lake.exe
if exist "C:\Users\greg\.elan\bin\lake.exe" set LAKE=C:\Users\greg\.elan\bin\lake.exe
if exist "%USERPROFILE%\.elan\bin\lake" set LAKE=%USERPROFILE%\.elan\bin\lake

REM If elan not found, try WSL
if "%LAKE%"=="" (
    echo lake not found in Windows PATH. Trying WSL...
    wsl bash -c "cd /mnt/d/fundamentals/lean && ~/.elan/bin/lake build PfLean.PFCore"
    goto :done
)

echo Found lake at: %LAKE%
echo Building PfLean.PFCore...
%LAKE% build PfLean.PFCore

:done
echo.
echo === Check result ===
if exist ".lake\build\lib\lean\PfLean\PFCore.olean" (
    echo SUCCESS: PFCore.olean created.
    echo Size: 
    dir .lake\build\lib\lean\PfLean\PFCore.olean
) else (
    echo PFCore.olean not found. Check errors above.
)
pause
