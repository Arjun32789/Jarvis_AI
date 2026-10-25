Set objShell = CreateObject("WScript.Shell")
' Find the exact folder where this file is located
strPath = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\"))
objShell.CurrentDirectory = strPath

' 1. Start Node.js server completely hidden (0 = hidden window)
objShell.Run "cmd /c node server.js", 0, False

' 2. Wait 4 seconds for the server to boot up
WScript.Sleep 4000

' 3. Open the browser to your Avatar page
objShell.Run "http://localhost:3000/avatar.html", 1, False