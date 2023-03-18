echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 49623 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 19252) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 2868) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 17272)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_20-44\cleanup-fluent-wenzheshang-2868.bat"
