echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="F:\ANASYS\ANSYS Inc\v202\fluent/ntbin/win64/winkill.exe"

"F:\ANASYS\ANSYS Inc\v202\fluent\ntbin\win64\tell.exe" wenzheshang 56616 CLEANUP_EXITING
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 16320) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 10740) 
if /i "%LOCALHOST%"=="wenzheshang" (%KILL_CMD% 15568)
del "f:\Thinking\program\BELab1.0\Workdata\Fluent_Python\2023-02-12_17-42\cleanup-fluent-wenzheshang-10740.bat"
