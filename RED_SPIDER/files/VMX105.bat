@echo off
color 0D
setlocal EnableDelayedExpansion

echo.
echo === System Information Collection and Display ===
echo.
echo -------------------------------------------------------------------------
echo 1.
echo -------------------------------------------------------------------------
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set "LOCAL_IP=%%a"
    echo Local IP Address : !LOCAL_IP:~1!
    goto :IP_FOUND
)
:IP_FOUND
echo.

echo -------------------------------------------------------------------------
echo 2.
echo -------------------------------------------------------------------------
echo Computer Name : %COMPUTERNAME%
echo.

echo -------------------------------------------------------------------------
echo 3.
echo -------------------------------------------------------------------------
echo List of Users :
powershell -Command "Get-LocalUser | Select-Object -ExpandProperty Name"
echo.

pause
endlocal