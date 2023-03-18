echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 50749 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 9596) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 4060) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 9464)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_10-57\cleanup-fluent-wenzheshang-4060.bat"
