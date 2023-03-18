echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 32885 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 83472) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 84116) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 85564)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-03-03_20-39\cleanup-fluent-wenzheshang-84116.bat"
