echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 65091 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 10564) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 10576) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 5884)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_11-34\cleanup-fluent-wenzheshang-10576.bat"
