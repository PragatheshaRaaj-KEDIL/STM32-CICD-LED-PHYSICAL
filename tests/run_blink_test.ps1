$renode = "C:\Program Files\Renode\bin\Renode.exe"
$script = "E:\STM32\CICD-LED\tests\blink.resc"

$output = & $renode --console --disable-xwt --execute "include @$script" 2>&1 | Out-String

Write-Host $output

$high = $output -match "0x00000020"
$low  = $output -match "0x00000000"

if ($high -and $low) {
    Write-Host "TEST PASS: GPIO toggled."
    exit 0
}

Write-Host "TEST FAIL: GPIO did not toggle."
exit 1
