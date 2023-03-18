echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 1757 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 101776) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 100508) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 105448)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-03-05_18-48\cleanup-fluent-wenzheshang-100508.bat"
