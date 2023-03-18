echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 59994 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 6216) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 12296) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 16236)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-12_17-11\cleanup-fluent-wenzheshang-12296.bat"
