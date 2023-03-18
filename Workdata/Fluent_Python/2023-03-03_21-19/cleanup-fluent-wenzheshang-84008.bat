echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 17504 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 85888) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 84008) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 88248)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-03-03_21-19\cleanup-fluent-wenzheshang-84008.bat"
