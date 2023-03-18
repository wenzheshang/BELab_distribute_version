echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 63322 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 18608) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 14112) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 10528)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-09_20-52\cleanup-fluent-wenzheshang-14112.bat"
