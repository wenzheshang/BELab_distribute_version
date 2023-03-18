echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 62863 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 17932) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 8412) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 12160)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_22-03\cleanup-fluent-wenzheshang-8412.bat"
