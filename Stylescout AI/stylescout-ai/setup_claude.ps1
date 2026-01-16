# StyleScout Claude Config Setup Script

Write-Host "🎯 Setting up Claude Desktop configuration..." -ForegroundColor Cyan

# Create Claude folder if it doesn't exist
$claudePath = "$env:APPDATA\Claude"
if (!(Test-Path $claudePath)) {
    New-Item -ItemType Directory -Path $claudePath -Force
    Write-Host "✅ Created Claude folder" -ForegroundColor Green
}

# Get current directory
$currentDir = (Get-Location).Path -replace '\\', '\\'

# Create config content
$configContent = @"
{
  "mcpServers": {
    "stylescout-ai": {
      "command": "python",
      "args": [
        "-m",
        "stylescout_ai.server"
      ],
      "cwd": "$currentDir"
    }
  }
}
"@

# Write config file
$configFile = "$claudePath\claude_desktop_config.json"
$configContent | Out-File -FilePath $configFile -Encoding UTF8

Write-Host "✅ Configuration file created!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Location: $configFile" -ForegroundColor Yellow
Write-Host ""
Write-Host "🎯 Next steps:" -ForegroundColor Cyan
Write-Host "1. Close Claude Desktop completely"
Write-Host "2. Restart Claude Desktop"
Write-Host "3. Look for 🔌 tools icon"
Write-Host ""

# Open the folder
explorer $claudePath