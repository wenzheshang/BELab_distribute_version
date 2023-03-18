echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 33686 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 82632) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 85492) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 83504)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-03-03_20-52\cleanup-fluent-wenzheshang-85492.bat"
