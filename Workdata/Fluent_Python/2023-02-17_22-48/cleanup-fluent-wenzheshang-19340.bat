echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 55653 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 17856) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 19340) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 11328)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_22-48\cleanup-fluent-wenzheshang-19340.bat"
