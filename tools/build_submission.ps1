$ErrorActionPreference = "Stop"

$repo = Split-Path -Parent $PSScriptRoot
$source = Join-Path $repo "final_model"
$dist = Join-Path $repo "dist"
$archive = Join-Path $dist "submit.zip"

$required = @(
    "script.py",
    "requirements.txt",
    "model/current_season_lgbm_095.txt",
    "model/current_season_lgbm_101.txt",
    "model/current_season_catboost.cbm",
    "model/current_batter_catboost.cbm",
    "model/current_batter_id_catboost.cbm",
    "model/count_regime_batter_ahead.cbm",
    "model/count_regime_even.cbm",
    "model/count_regime_pitcher_ahead.cbm",
    "model/hand_relation_same.cbm",
    "model/hand_relation_opposite.cbm",
    "model/candidate_453.json",
    "model/candidate_472.json",
    "model/pitcher_season_baseline.csv",
    "model/batter_season_baseline.csv"
)

foreach ($relative in $required) {
    $path = Join-Path $source $relative
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Missing required asset: $relative"
    }
}

$manifest = Join-Path $source "MANIFEST.sha256"
foreach ($line in Get-Content -LiteralPath $manifest) {
    if (-not $line.Trim()) { continue }
    $parts = $line -split "\s+", 2
    $expected = $parts[0].ToUpperInvariant()
    $relative = $parts[1].Trim()
    $actual = (Get-FileHash -LiteralPath (Join-Path $source $relative) -Algorithm SHA256).Hash
    if ($actual -ne $expected) { throw "Checksum mismatch: $relative" }
}

New-Item -ItemType Directory -Path $dist -Force | Out-Null
if (Test-Path -LiteralPath $archive) {
    Remove-Item -LiteralPath $archive -Force
}

# bsdtar writes portable POSIX '/' entry names, even when invoked on Windows.
Push-Location $source
try {
    & tar -a -c -f $archive model script.py requirements.txt
    if ($LASTEXITCODE -ne 0) { throw "tar failed with exit code $LASTEXITCODE" }
}
finally {
    Pop-Location
}

$entries = @(& tar -tf $archive)
if ($LASTEXITCODE -ne 0) { throw "Cannot inspect generated ZIP" }
foreach ($relative in $required) {
    $zipName = $relative.Replace("\", "/")
    if ($entries -notcontains $zipName) { throw "ZIP is missing: $zipName" }
}
if ($entries | Where-Object { $_ -match "\\" }) {
    throw "ZIP contains Windows backslash paths"
}

$hash = Get-FileHash -LiteralPath $archive -Algorithm SHA256
Write-Host "Created: $archive"
Write-Host "SHA256: $($hash.Hash)"
