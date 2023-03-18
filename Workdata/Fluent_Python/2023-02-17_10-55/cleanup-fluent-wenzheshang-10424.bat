echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 59934 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 16420) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 10424) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 15924)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_10-55\cleanup-fluent-wenzheshang-10424.bat"
