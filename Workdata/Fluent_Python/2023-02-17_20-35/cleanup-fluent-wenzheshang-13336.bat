echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 49325 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 5408) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 13336) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 17248)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_20-35\cleanup-fluent-wenzheshang-13336.bat"
