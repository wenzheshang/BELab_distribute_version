echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 53583 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 16536) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 13788) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 17716)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_21-49\cleanup-fluent-wenzheshang-13788.bat"
