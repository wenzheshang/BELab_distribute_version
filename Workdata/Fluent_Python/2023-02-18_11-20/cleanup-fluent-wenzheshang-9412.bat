echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 51412 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 18824) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 9412) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 9076)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-18_11-20\cleanup-fluent-wenzheshang-9412.bat"
