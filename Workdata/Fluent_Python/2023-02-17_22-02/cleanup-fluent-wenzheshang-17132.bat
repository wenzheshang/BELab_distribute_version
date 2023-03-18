echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 62754 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 11928) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 17132) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 10472)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_22-02\cleanup-fluent-wenzheshang-17132.bat"
