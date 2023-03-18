echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 63305 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 10584) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 13696) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 12660)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_22-15\cleanup-fluent-wenzheshang-13696.bat"
