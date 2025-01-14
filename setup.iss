[Setup]
AppName=Text Or
AppVersion=1.4
DefaultDirName={pf}\Text Or
DefaultGroupName=Text Or
OutputDir=C:\wamp64\www\APP_desk_Text_Or\dist\Installers
OutputBaseFilename=Text_Or_Installer
Compression=lzma
SolidCompression=yes
SetupIconFile=C:\wamp64\www\APP_desk_Text_Or\dist\app.ico
LicenseFile=C:\wamp64\www\APP_desk_Text_Or\dist\License.txt

[Files]
Source: "C:\wamp64\www\APP_desk_Text_Or\dist\Text-Or.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\wamp64\www\APP_desk_Text_Or\dist\app.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Text Or"; Filename: "{app}\Text-Or.exe"; IconFilename: "{app}\app.ico"
Name: "{userdesktop}\Text Or"; Filename: "{app}\Text-Or.exe"; IconFilename: "{app}\app.ico"

[Registry]
Root: HKCU; Subkey: "Software\Text Or"; ValueType: string; ValueName: "Path"; ValueData: "{app}"
