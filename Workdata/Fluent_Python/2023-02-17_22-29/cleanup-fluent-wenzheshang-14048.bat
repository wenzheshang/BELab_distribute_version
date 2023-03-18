echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 55124 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 10312) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 14048) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 14640)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_22-29\cleanup-fluent-wenzheshang-14048.bat"
