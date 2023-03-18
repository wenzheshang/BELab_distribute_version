echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 58403 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 3088) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 2992) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 16440)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-12_19-02\cleanup-fluent-wenzheshang-2992.bat"
