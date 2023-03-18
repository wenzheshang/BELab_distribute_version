echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 65053 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 7048) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 10252) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 2928)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_20-17\cleanup-fluent-wenzheshang-10252.bat"
