echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 1444 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 84800) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 81356) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 85408)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-03-04_17-23\cleanup-fluent-wenzheshang-81356.bat"
