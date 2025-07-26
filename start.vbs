' run_app_hidden.vbs - Python kontrolü ve otomatik kurulum ile
Dim objShell, objFSO
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Python yüklü mü kontrol et
Function IsPythonInstalled()
    On Error Resume Next
    Dim result
    result = objShell.Run("python --version", 0, True)
    If Err.Number = 0 And result = 0 Then
        IsPythonInstalled = True
    Else
        ' python komutu çalışmazsa py komutunu dene
        result = objShell.Run("py --version", 0, True)
        If Err.Number = 0 And result = 0 Then
            IsPythonInstalled = True
        Else
            IsPythonInstalled = False
        End If
    End If
    On Error GoTo 0
End Function

' Python'u indir ve yükle
Sub DownloadAndInstallPython()
    Dim pythonUrl, tempPath, installerPath
    
    ' Python 3.11.7 indirme linki (64-bit)
    pythonUrl = "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
    tempPath = objShell.ExpandEnvironmentStrings("%TEMP%")
    installerPath = tempPath & "\python_installer.exe"
    
    WScript.Echo "Python indiriliyor, lütfen bekleyin..."
    
    ' Python installer'ı indir
    Dim http
    Set http = CreateObject("MSXML2.XMLHTTP")
    http.Open "GET", pythonUrl, False
    http.Send
    
    If http.Status = 200 Then
        ' Dosyayı kaydet
        Dim stream
        Set stream = CreateObject("ADODB.Stream")
        stream.Type = 1 ' Binary
        stream.Open
        stream.Write http.ResponseBody
        stream.SaveToFile installerPath, 2
        stream.Close
        Set stream = Nothing
        
        WScript.Echo "Python yükleniyor, lütfen bekleyin..."
        
        ' Python'u sessiz modda yükle (PATH'e ekle, pip dahil)
        objShell.Run """" & installerPath & """ /quiet InstallAllUsers=1 PrependPath=1 Include_test=0", 1, True
        
        ' Installer dosyasını sil
        objFSO.DeleteFile installerPath
        
        WScript.Echo "Python başarıyla yüklendi!"
        WScript.Sleep 2000
    Else
        WScript.Echo "Python indirilemedi. İnternet bağlantınızı kontrol edin."
        WScript.Quit
    End If
    
    Set http = Nothing
End Sub

' Ana program
If IsPythonInstalled() Then
    ' Python yüklü, app klasörüne git ve uygulamayı çalıştır
    If objFSO.FolderExists("app") Then
        objShell.Run "cmd /c cd app && python app.py", 0, False
    Else
        WScript.Echo "Hata: 'app' klasörü bulunamadı!"
    End If
Else
    ' Python yüklü değil, kullanıcıya sor
    Dim response
    response = MsgBox("Python yüklü değil. Python'u otomatik olarak yüklemek ister misiniz?" & vbCrLf & vbCrLf & "Bu işlem birkaç dakika sürebilir.", vbYesNo + vbQuestion, "Python Kurulumu")
    
    If response = vbYes Then
        DownloadAndInstallPython()
        
        ' Kurulum sonrası uygulamayı çalıştır
        If objFSO.FolderExists("app") Then
            WScript.Echo "Uygulama başlatılıyor..."
            objShell.Run "cmd /c cd app && python app.py", 0, False
        Else
            WScript.Echo "Hata: 'app' klasörü bulunamadı!"
        End If
    Else
        WScript.Echo "Python kurulumu iptal edildi. Uygulama çalıştırılamaz."
    End If
End If

' Temizlik
Set objShell = Nothing
Set objFSO = Nothing