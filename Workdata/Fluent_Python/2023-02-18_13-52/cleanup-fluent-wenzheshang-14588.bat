echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 50386 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 10360) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 14588) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 18644)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-18_13-52\cleanup-fluent-wenzheshang-14588.bat"
