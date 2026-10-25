Set objShell = CreateObject("WScript.Shell")

' Get the folder path where this VBS file is located
strPath = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\"))
objShell.CurrentDirectory = strPath

' 1. Start Node.js server completely hidden (0 = hidden, False = don't wait)
objShell.Run "cmd /c node server.js", 0, False

' 2. Wait 4 seconds for the server to boot up
WScript.Sleep 4000

' 3. Open Microsoft Edge in App Mode (borderless window)
objShell.Run "msedge --app=http://localhost:3000/avatar.html", 1, False

' If you use Chrome instead of Edge, comment out the line above and use this:
' objShell.Run "chrome --app=http://localhost:3000/avatar.html", 1, False