[Setup]
AppName=MuhtasibWatch
AppVersion=1.0
DefaultDirName={commonpf}\MuhtasibWatch
DefaultGroupName=MuhtasibWatch
OutputBaseFilename=MuhtasibWatchInstaller
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
OutputDir=C:\pythonProject1\Output
OutputManifestFile=C:\MuhtasibWatchInstallerBuild.log

[Files]
; Include necessary application files
Source: "credentials.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "models\*"; DestDir: "{app}\models"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "resources\*"; DestDir: "{app}\resources"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "data\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "ui\*"; DestDir: "{app}\ui"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "src\*"; DestDir: "{app}\src"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Create a desktop shortcut with the icon
Name: "{commondesktop}\MuhtasibWatch"; Filename: "{app}\main.exe"; IconFilename: "{app}\resources\Logo.png"

[Run]
; Optionally launch the main application
Filename: "{app}\main.exe"; Description: "Launch MuhtasibWatch"; Flags: nowait postinstall skipifsilent

[Code]
// Initialize setup
function InitializeSetup(): Boolean;
begin
  Result := True; // Default to continue setup
  Log('DEBUG: Installer initialized.');
end;
