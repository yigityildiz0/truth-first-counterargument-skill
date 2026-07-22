[CmdletBinding()]
param(
    [string]$OutputDirectory
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillName = 'truth-first-counterargument'
$sourcePath = Join-Path $repoRoot "skills\$skillName"
$version = (Get-Content -Raw -LiteralPath (Join-Path $repoRoot 'VERSION')).Trim()
if (-not $OutputDirectory) {
    $OutputDirectory = Join-Path $repoRoot 'dist'
}

$allowedTopLevel = @('SKILL.md', 'LICENSE.txt', 'agents', 'references', 'scripts', 'assets')
$stageRoot = Join-Path $repoRoot ('.release-stage-' + [guid]::NewGuid().ToString('N'))
$stageSkill = Join-Path $stageRoot $skillName
$archivePath = Join-Path $OutputDirectory "$skillName.zip"
$temporaryArchive = Join-Path $OutputDirectory (".$skillName-" + [guid]::NewGuid().ToString('N') + '.tmp.zip')

try {
    New-Item -ItemType Directory -Force -Path $stageRoot, $OutputDirectory | Out-Null
    Copy-Item -Recurse -LiteralPath $sourcePath -Destination $stageSkill

    $generatedDirectories = @(Get-ChildItem -Recurse -Directory -LiteralPath $stageSkill -Filter '__pycache__')
    foreach ($generatedDirectory in $generatedDirectories) {
        Remove-Item -Recurse -Force -LiteralPath $generatedDirectory.FullName
    }
    $generatedFiles = @(Get-ChildItem -Recurse -File -LiteralPath $stageSkill -Include '*.pyc', '*.pyo')
    foreach ($generatedFile in $generatedFiles) {
        Remove-Item -Force -LiteralPath $generatedFile.FullName
    }

    $unexpected = @(Get-ChildItem -LiteralPath $stageSkill | Where-Object { $_.Name -notin $allowedTopLevel })
    if ($unexpected.Count) {
        throw "Unexpected skill-root entries: $($unexpected.Name -join ', ')"
    }
    foreach ($required in @('SKILL.md', 'LICENSE.txt', 'agents\openai.yaml')) {
        if (-not (Test-Path -LiteralPath (Join-Path $stageSkill $required) -PathType Leaf)) {
            throw "Required release file missing: $required"
        }
    }

    Compress-Archive -CompressionLevel Optimal -LiteralPath $stageSkill -DestinationPath $temporaryArchive
    if (Test-Path -LiteralPath $archivePath) {
        Remove-Item -Force -LiteralPath $archivePath
    }
    Move-Item -LiteralPath $temporaryArchive -Destination $archivePath

    $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $archivePath).Hash.ToLowerInvariant()
    $fileCount = @(Get-ChildItem -Recurse -File -LiteralPath $stageSkill).Count
    $manifest = [ordered]@{
        name = $skillName
        version = $version
        archive = "$skillName.zip"
        sha256 = $hash
        bytes = (Get-Item -LiteralPath $archivePath).Length
        files = $fileCount
        created_utc = [DateTime]::UtcNow.ToString('o')
    }
    $manifest | ConvertTo-Json | Set-Content -Encoding utf8 -LiteralPath (Join-Path $OutputDirectory 'manifest.json')
    "$hash  $skillName.zip" | Set-Content -Encoding ascii -LiteralPath (Join-Path $OutputDirectory 'SHA256SUMS.txt')

    Write-Host "RELEASE_BUILD_OK: $archivePath"
    Write-Host "SHA256: $hash"
}
finally {
    if (Test-Path -LiteralPath $temporaryArchive) {
        Remove-Item -Force -LiteralPath $temporaryArchive
    }
    if (Test-Path -LiteralPath $stageRoot) {
        Remove-Item -Recurse -Force -LiteralPath $stageRoot
    }
}
