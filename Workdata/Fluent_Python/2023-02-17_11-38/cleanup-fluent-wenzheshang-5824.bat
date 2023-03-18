echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 65241 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 18520) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 5824) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 2004)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_11-38\cleanup-fluent-wenzheshang-5824.bat"
