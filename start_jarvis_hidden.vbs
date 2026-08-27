Set shell = CreateObject("WScript.Shell")
projectDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
pythonw = projectDir & "\.venv\Scripts\pythonw.exe"
command = Chr(34) & pythonw & Chr(34) & " -m app.wake_listener"
shell.CurrentDirectory = projectDir
shell.Run command, 0, False
