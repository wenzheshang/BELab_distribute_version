echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 1354 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 87904) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 84836) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 83656)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-03-03_21-33\cleanup-fluent-wenzheshang-84836.bat"
