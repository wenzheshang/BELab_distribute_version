echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 55493 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 8916) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 976) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 12928)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-17_22-43\cleanup-fluent-wenzheshang-976.bat"
