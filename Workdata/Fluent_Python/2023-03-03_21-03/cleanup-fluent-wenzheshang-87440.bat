echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 34064 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 82596) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 87440) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 81312)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-03-03_21-03\cleanup-fluent-wenzheshang-87440.bat"
