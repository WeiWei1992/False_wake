@echo off  ！！！！！！！！！！！！！

cls
:start
TIMEOUT /T 12 /NOBREAK
Echo WScript.Echo((new Date()).getTime())>sjc.vbs
for /f %%i in ('cscript -nologo -e:jscript sjc.vbs') do set sjc=%%i

adb -s JYZ4222 pull /tmp/audio 


goto start