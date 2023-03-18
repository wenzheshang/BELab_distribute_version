echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 58720 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 2680) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 7184) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 16804)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-18_14-39\cleanup-fluent-wenzheshang-7184.bat"
