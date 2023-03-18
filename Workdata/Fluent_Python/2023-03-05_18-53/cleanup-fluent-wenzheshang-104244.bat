echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 1931 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 96204) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 104244) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 83776)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-03-05_18-53\cleanup-fluent-wenzheshang-104244.bat"
