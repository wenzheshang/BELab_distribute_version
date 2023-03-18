echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 55775 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 11456) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 13820) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 12420)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-18_14-09\cleanup-fluent-wenzheshang-13820.bat"
