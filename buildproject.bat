del *.msi
call c:\Python26\Scripts\cxfreeze.bat atomia_manager\atomia.py --target-dir dist
IF %ERRORLEVEL% NEQ 0 GOTO lexit
%SystemRoot%\Microsoft.NET\Framework\v4.0.30319\MSBuild.exe WindowsInstaller/WindowsInstaller.sln /p:Configuration=Release
IF %ERRORLEVEL% NEQ 0 GOTO lexit
copy /y WindowsInstaller\bin\Release\*.msi .
:lexit
exit %ERRORLEVEL%
