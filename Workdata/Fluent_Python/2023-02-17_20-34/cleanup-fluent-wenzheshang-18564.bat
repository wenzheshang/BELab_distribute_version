echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 49212 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 15176) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 18564) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 14056)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_20-34\cleanup-fluent-wenzheshang-18564.bat"
