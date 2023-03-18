echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 2181 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 106300) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 105572) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 25484)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-03-05_18-58\cleanup-fluent-wenzheshang-105572.bat"
