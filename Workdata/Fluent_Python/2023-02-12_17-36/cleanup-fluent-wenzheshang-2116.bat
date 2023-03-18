echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 63398 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 4696) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 2116) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 16300)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-12_17-36\cleanup-fluent-wenzheshang-2116.bat"
