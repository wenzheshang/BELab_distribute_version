echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 62639 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 12768) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 18652) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 1312)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_22-00\cleanup-fluent-wenzheshang-18652.bat"
