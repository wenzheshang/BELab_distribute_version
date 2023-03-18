echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 65289 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 14240) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 7672) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 12356)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_20-22\cleanup-fluent-wenzheshang-7672.bat"
