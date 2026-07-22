$ErrorActionPreference = 'Stop'
$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$installer = Join-Path $repoRoot 'install.ps1'
$sourcePath = Join-Path $repoRoot 'skills\truth-first-counterargument'
$tempBase = [IO.Path]::GetFullPath([IO.Path]::GetTempPath())
$testRoot = Join-Path $tempBase ("truth-first-counterargument-test-" + [guid]::NewGuid().ToString('N'))

try {
    & $installer -DestinationRoot $testRoot
    & $installer -DestinationRoot $testRoot

    $installed = Join-Path $testRoot 'truth-first-counterargument'
    $backups = @(Get-ChildItem -LiteralPath $testRoot -Directory -Filter 'truth-first-counterargument.backup-*')
    if (-not (Test-Path -LiteralPath (Join-Path $installed 'SKILL.md'))) {
        throw 'Installed SKILL.md is missing'
    }
    if ($backups.Count -ne 1) {
        throw "Expected one backup after reinstall; found $($backups.Count)"
    }

    $overlapRejected = $false
    try {
        & $installer -DestinationRoot (Join-Path $repoRoot 'skills')
    }
    catch {
        $overlapRejected = $_.Exception.Message -like '*Unsafe install path overlap*'
    }
    if (-not $overlapRejected) {
        throw 'Source/destination overlap was not rejected'
    }
    if (-not (Test-Path -LiteralPath (Join-Path $sourcePath 'SKILL.md'))) {
        throw 'Overlap test damaged the active source skill'
    }

    Write-Host 'WINDOWS_INSTALLER_TEST_OK'
}
finally {
    $testFull = [IO.Path]::GetFullPath($testRoot)
    if ($testFull.StartsWith($tempBase, [StringComparison]::OrdinalIgnoreCase) -and
        (Split-Path -Leaf $testFull).StartsWith('truth-first-counterargument-test-') -and
        (Test-Path -LiteralPath $testFull)) {
        Remove-Item -Recurse -Force -LiteralPath $testFull
    }
}
