echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 1086 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 90924) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 99168) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 104012)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-03-05_19-12\cleanup-fluent-wenzheshang-99168.bat"
