echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 56395 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 13348) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 15208) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 15012)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-14_15-01\cleanup-fluent-wenzheshang-15208.bat"
