echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 64593 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 14776) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 14636) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 5384)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_11-22\cleanup-fluent-wenzheshang-14636.bat"
