echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 33890 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 87500) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 88468) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 83504)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-03-03_20-57\cleanup-fluent-wenzheshang-88468.bat"
