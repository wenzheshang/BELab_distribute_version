echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 64654 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 6284) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 17784) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 14928)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-12_19-42\cleanup-fluent-wenzheshang-17784.bat"
