[CmdletBinding()]
param(
    [string]$DestinationRoot
)

$ErrorActionPreference = 'Stop'
$skillName = 'truth-first-counterargument'
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourcePath = Join-Path $repoRoot "skills\$skillName"

if (-not (Test-Path -LiteralPath $sourcePath -PathType Container)) {
    throw "Skill source not found: $sourcePath"
}

if (-not $DestinationRoot) {
    if ($env:CODEX_HOME) {
        $DestinationRoot = Join-Path $env:CODEX_HOME 'skills'
    }
    else {
        $DestinationRoot = Join-Path $env:USERPROFILE '.codex\skills'
    }
}

$destinationPath = Join-Path $DestinationRoot $skillName
New-Item -ItemType Directory -Force -Path $DestinationRoot | Out-Null

function Test-SameOrDescendant {
    param(
        [Parameter(Mandatory)][string]$Candidate,
        [Parameter(Mandatory)][string]$Parent
    )
    $comparison = [StringComparison]::OrdinalIgnoreCase
    $candidateFull = [IO.Path]::GetFullPath($Candidate).TrimEnd([char[]]'\/')
    $parentFull = [IO.Path]::GetFullPath($Parent).TrimEnd([char[]]'\/')
    if ($candidateFull.Equals($parentFull, $comparison)) {
        return $true
    }
    $prefix = $parentFull + [IO.Path]::DirectorySeparatorChar
    return $candidateFull.StartsWith($prefix, $comparison)
}

$sourceFull = [IO.Path]::GetFullPath($sourcePath)
$destinationFull = [IO.Path]::GetFullPath($destinationPath)
if ((Test-SameOrDescendant -Candidate $destinationFull -Parent $sourceFull) -or
    (Test-SameOrDescendant -Candidate $sourceFull -Parent $destinationFull)) {
    throw "Unsafe install path overlap: source=$sourceFull destination=$destinationFull"
}

$stagePath = Join-Path $DestinationRoot ".$skillName.installing-$([guid]::NewGuid().ToString('N'))"
$backupPath = $null
try {
    Copy-Item -Recurse -LiteralPath $sourcePath -Destination $stagePath
    $generatedDirectories = @(Get-ChildItem -Recurse -Directory -LiteralPath $stagePath -Filter '__pycache__')
    foreach ($generatedDirectory in $generatedDirectories) {
        Remove-Item -Recurse -Force -LiteralPath $generatedDirectory.FullName
    }
    $generatedFiles = @(Get-ChildItem -Recurse -File -LiteralPath $stagePath -Include '*.pyc', '*.pyo')
    foreach ($generatedFile in $generatedFiles) {
        Remove-Item -Force -LiteralPath $generatedFile.FullName
    }

    if (Test-Path -LiteralPath $destinationPath) {
        $timestamp = Get-Date -Format 'yyyyMMdd-HHmmss-fff'
        $suffix = [guid]::NewGuid().ToString('N').Substring(0, 8)
        $backupPath = "$destinationPath.backup-$timestamp-$suffix"
        Move-Item -LiteralPath $destinationPath -Destination $backupPath
        Write-Host "Existing install backed up to: $backupPath"
    }

    try {
        Move-Item -LiteralPath $stagePath -Destination $destinationPath
    }
    catch {
        $installError = $_
        if ($backupPath -and
            -not (Test-Path -LiteralPath $destinationPath) -and
            (Test-Path -LiteralPath $backupPath)) {
            Move-Item -LiteralPath $backupPath -Destination $destinationPath
        }
        throw $installError
    }
}
finally {
    if (Test-Path -LiteralPath $stagePath) {
        Remove-Item -Recurse -Force -LiteralPath $stagePath
    }
}

Write-Host "Installed $skillName to: $destinationPath"
Write-Host 'Restart Codex so the skill list refreshes.'
