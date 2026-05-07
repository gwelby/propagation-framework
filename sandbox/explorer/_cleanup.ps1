$c = Get-Content 'index.html'
$c[0..347] | Out-File 'index.html' -Encoding UTF8
Write-Host "Done. Lines: $((Get-Content 'index.html').Count)"
