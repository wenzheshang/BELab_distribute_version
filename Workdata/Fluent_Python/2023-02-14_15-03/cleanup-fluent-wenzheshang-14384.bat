echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 56519 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 10640) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 14384) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 12748)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-14_15-03\cleanup-fluent-wenzheshang-14384.bat"
