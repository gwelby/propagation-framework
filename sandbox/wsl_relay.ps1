$wshell = New-Object -ComObject Wscript.Shell
$wshell.Popup("Starting UDP Relay. Close this terminal to stop.", 3, "SOMA Relay")

$wsl_ip = (wsl.exe -e hostname -I).Trim().Split(" ")[0]

$listener = New-Object System.Net.Sockets.UdpClient(28888)
$sender = New-Object System.Net.Sockets.UdpClient
$endpoint = New-Object System.Net.IPEndPoint([System.Net.IPAddress]::Any, 28888)

Write-Host "========================================================="
Write-Host "🌟 THE SOMA / WSL RELAY IS ACTIVE 🌟"
Write-Host "Listening on 0.0.0.0:28888 (Windows)"
Write-Host "Forwarding to $wsl_ip`:28888 (WSL)"
Write-Host "Press Ctrl+C to stop."
Write-Host "========================================================="

try {
    while($true) {
        $bytes = $listener.Receive([ref]$endpoint)
        $sender.Send($bytes, $bytes.Length, $wsl_ip, 28888) | Out-Null
    }
} finally {
    $listener.Close()
    $sender.Close()
}
