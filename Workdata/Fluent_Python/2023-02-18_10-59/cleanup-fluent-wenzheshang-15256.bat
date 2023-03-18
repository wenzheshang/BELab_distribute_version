echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 58002 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 15224) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 15256) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 15032)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-18_10-59\cleanup-fluent-wenzheshang-15256.bat"
