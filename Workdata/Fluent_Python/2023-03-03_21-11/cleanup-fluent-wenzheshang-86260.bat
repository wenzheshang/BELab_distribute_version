echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 17233 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 81236) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 86260) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 87724)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-03-03_21-11\cleanup-fluent-wenzheshang-86260.bat"
