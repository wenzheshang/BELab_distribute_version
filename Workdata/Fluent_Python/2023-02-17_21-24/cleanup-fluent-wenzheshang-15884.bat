echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 52650 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 15652) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 15884) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 17180)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_21-24\cleanup-fluent-wenzheshang-15884.bat"
