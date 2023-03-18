echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 65018 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 5436) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 10500) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 8844)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_11-05\cleanup-fluent-wenzheshang-10500.bat"
