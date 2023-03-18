echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 49317 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 13772) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 16780) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 7804)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-12_19-22\cleanup-fluent-wenzheshang-16780.bat"
