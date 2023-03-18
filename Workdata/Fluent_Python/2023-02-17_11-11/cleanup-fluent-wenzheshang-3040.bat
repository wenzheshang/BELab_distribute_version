echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 59053 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 14460) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 3040) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 2108)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_11-11\cleanup-fluent-wenzheshang-3040.bat"
