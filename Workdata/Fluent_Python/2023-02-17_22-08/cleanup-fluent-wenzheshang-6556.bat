echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 63050 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 15120) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 6556) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 13248)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_22-08\cleanup-fluent-wenzheshang-6556.bat"
