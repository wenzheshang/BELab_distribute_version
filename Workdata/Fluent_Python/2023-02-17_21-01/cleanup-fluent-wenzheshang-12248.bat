echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 52130 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 9648) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 12248) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 17660)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_21-01\cleanup-fluent-wenzheshang-12248.bat"
