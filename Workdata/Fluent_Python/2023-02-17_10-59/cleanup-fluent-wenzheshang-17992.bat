echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 50853 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 18988) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 17992) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 2588)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_10-59\cleanup-fluent-wenzheshang-17992.bat"
