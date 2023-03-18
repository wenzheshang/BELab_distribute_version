echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 13858 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 93036) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 92308) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 90688)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-03-04_17-11\cleanup-fluent-wenzheshang-92308.bat"
