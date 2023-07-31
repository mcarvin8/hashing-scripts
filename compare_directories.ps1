function Get-RelativePath {
    param (
        [string]$basePath,
        [string]$targetPath
    )

    $relativePath = (Get-Item $targetPath).FullName.Replace((Get-Item $basePath).FullName, '')
    if ($relativePath -eq '') {
        $relativePath = '.\'
    } elseif ($relativePath[0] -eq '\') {
        $relativePath = $relativePath.Substring(1)
    }

    return $relativePath
}

function Get-FileHashes {
    param (
        [string]$Path
    )
    Get-ChildItem -Path $Path -Recurse | ForEach-Object {
        if (-Not $_.PSIsContainer) {
            $hash = Get-FileHash -Path $_.FullName -Algorithm SHA256
            [PSCustomObject]@{
                Path = $_.FullName
                RelativePath = Get-RelativePath -basePath $Path -targetPath $_.FullName
                Hash = $hash.Hash
            }
        }
    }
}

function Compare-FileHashes {
    param (
        [array]$Hashes1,
        [array]$Hashes2
    )

    $hashTable1 = @{}
    $hashTable2 = @{}

    foreach ($hash in $Hashes1) {
        $hashTable1[$hash.RelativePath] = $hash.Hash
    }

    foreach ($hash in $Hashes2) {
        $hashTable2[$hash.RelativePath] = $hash.Hash
    }

    $allPaths = $hashTable1.Keys + $hashTable2.Keys | Get-Unique

    $differences = @()
    $identicalFiles = @()
    foreach ($path in $allPaths) {
        $hash1 = $hashTable1[$path]
        $hash2 = $hashTable2[$path]

        if ($hash1 -eq $hash2) {
            $identicalFiles += [PSCustomObject]@{
                Path = $path
            }
        } else {
            $differences += [PSCustomObject]@{
                Path = $path
                InDirectory1 = $hash1 -ne $null
                InDirectory2 = $hash2 -ne $null
            }
        }
    }

    [PSCustomObject]@{
        Differences = $differences
        IdenticalFiles = $identicalFiles
    }
}

# Input directories
$directory1 = Read-Host "Enter the first directory path:"
$directory2 = Read-Host "Enter the second directory path:"

# Calculate hashes for each directory
$hashes1 = Get-FileHashes -Path $directory1
$hashes2 = Get-FileHashes -Path $directory2

# Compare the hashes and identify differences and identical files
$results = Compare-FileHashes -Hashes1 $hashes1 -Hashes2 $hashes2

# Display the differences and identical files
if ($results.Differences.Count -eq 0) {
    Write-Host "No differences found. All files in both directories have the same SHA256 hash."
} else {
    Write-Host "Differences found:"
    $results.Differences | Format-Table -AutoSize
}

if ($results.IdenticalFiles.Count -eq 0) {
    Write-Host "No identical files found. All files in both directories are different."
} else {
    Write-Host "Identical files found:"
    $results.IdenticalFiles | Format-Table -AutoSize
}
