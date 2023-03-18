echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 1207 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 87776) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 87420) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 88068)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-03-03_21-29\cleanup-fluent-wenzheshang-87420.bat"
