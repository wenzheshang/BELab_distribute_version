echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 52066 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 10460) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 11600) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 15748)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-18_15-03\cleanup-fluent-wenzheshang-11600.bat"
