echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 49545 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 13656) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 13380) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 16952)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-18_15-28\cleanup-fluent-wenzheshang-13380.bat"
