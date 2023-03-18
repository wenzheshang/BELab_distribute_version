echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 54933 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 10820) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 13108) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 12696)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_22-23\cleanup-fluent-wenzheshang-13108.bat"
