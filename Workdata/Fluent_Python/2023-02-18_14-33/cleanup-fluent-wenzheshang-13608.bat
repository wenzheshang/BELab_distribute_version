echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 58542 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 6612) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 13608) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 11604)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-18_14-33\cleanup-fluent-wenzheshang-13608.bat"
