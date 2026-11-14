# VS Codeのインストール先を自動取得
$codePath = Join-Path $env:LOCALAPPDATA "Programs\Microsoft VS Code\Code.exe"

# VS Codeの存在確認
if (-not (Test-Path $codePath)) {
    Write-Host "VS Code was not found."
    exit 1
}

# レジストリの登録先
$base = "HKCU:\Software\Classes"

$targets = @(
    @{ Key = "$base\*\shell\VSCode"; Argument = "%1" },
    @{ Key = "$base\Directory\shell\VSCode"; Argument = "%1" },
    @{ Key = "$base\Directory\Background\shell\VSCode"; Argument = "%V" }
)

# 右クリックメニューを登録
foreach ($target in $targets) {
    $key = $target.Key
    $commandKey = "$key\command"

    New-Item -Path $commandKey -Force | Out-Null

    Set-Item -Path $key -Value "Codeで開く"
    New-ItemProperty -Path $key -Name "Icon" `
        -Value $codePath -PropertyType String -Force | Out-Null

    $command = "`"$codePath`" `"$($target.Argument)`""
    Set-Item -Path $commandKey -Value $command
}

Write-Host "VS Code context menu registered successfully."
