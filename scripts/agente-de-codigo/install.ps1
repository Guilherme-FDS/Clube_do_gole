<#
.SYNOPSIS
  Instala o "agente-de-codigo" (documentacao automatica) nesta maquina.

.DESCRIPTION
  - Copia a definicao do agente para  ~/.claude/agents/agente-de-codigo.md
  - Instala o git hook  .git/hooks/post-commit  no repositorio atual
  - Configura o token OAuth do Claude headless em  .git/agente-de-codigo.token
  A cada 'git commit', o agente atualiza a documentacao tecnica no vault do Obsidian.

.PARAMETER VaultPath
  Caminho do vault Obsidian (a pasta "05 - Produto & Tecnologia").

.EXAMPLE
  .\scripts\agente-de-codigo\install.ps1
  .\scripts\agente-de-codigo\install.ps1 -VaultPath "D:\Drive\Clube do Gole - Full\05 - Produto & Tecnologia"
#>
param(
  [string]$VaultPath = "G:\Meu Drive\Clube do Gole - Full\05 - Produto & Tecnologia"
)

$ErrorActionPreference = "Stop"
$here = $PSScriptRoot

Write-Host "== Instalador do agente-de-codigo ==" -ForegroundColor Cyan

# 1) Raiz do repositorio
$repo = (git rev-parse --show-toplevel 2>$null)
if (-not $repo) { Write-Error "Rode este script de dentro do repositorio git (clonado)."; exit 1 }
$repo = ($repo -replace '/', '\').TrimEnd('\')

# 2) Resolver o claude.exe (app empacotado: fica no LocalCache do pacote)
$claude = Get-ChildItem "$env:LOCALAPPDATA\Packages\*laude*\LocalCache\Roaming\Claude\claude-code\*\claude.exe" -ErrorAction SilentlyContinue |
          Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $claude) {
  $claude = Get-ChildItem "$env:APPDATA\Claude\claude-code\*\claude.exe" -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTime -Descending | Select-Object -First 1
}
if (-not $claude) { Write-Error "claude.exe nao encontrado. O app Claude (Claude Code) esta instalado nesta maquina?"; exit 1 }
$claude = $claude.FullName

Write-Host "Repo : $repo"
Write-Host "Vault: $VaultPath"
Write-Host "CLI  : $claude"
if (-not (Test-Path $VaultPath)) {
  Write-Warning "Vault nao encontrado em '$VaultPath'. Reexecute com -VaultPath apontando para o caminho correto."
}

# 3) Agente -> ~/.claude/agents/agente-de-codigo.md
$agentsDir = Join-Path $env:USERPROFILE ".claude\agents"
New-Item -ItemType Directory -Force -Path $agentsDir | Out-Null
$agent = Get-Content (Join-Path $here "agente-de-codigo.agent.md") -Raw
$agent = $agent.Replace('__REPO__', $repo).Replace('__VAULT__', $VaultPath)
Set-Content -Path (Join-Path $agentsDir "agente-de-codigo.md") -Value $agent -Encoding utf8
Write-Host "[ok] agente -> $agentsDir\agente-de-codigo.md"

# 4) Hook -> .git/hooks/post-commit (gravado com LF)
$hook = Get-Content (Join-Path $here "post-commit") -Raw
$hook = $hook.Replace('__VAULT__', ($VaultPath -replace '\\', '/'))
$hook = $hook -replace "`r`n", "`n"
$hookPath = Join-Path $repo ".git\hooks\post-commit"
[IO.File]::WriteAllText($hookPath, $hook, (New-Object System.Text.UTF8Encoding($false)))
Write-Host "[ok] hook  -> $hookPath"

# 5) Token OAuth
$tokenPath = Join-Path $repo ".git\agente-de-codigo.token"
if (Test-Path $tokenPath) {
  Write-Host "[ok] token ja existe -> $tokenPath"
} else {
  Write-Host ""
  Write-Host "Falta o token OAuth do Claude (necessario para o modo headless):" -ForegroundColor Yellow
  Write-Host "  1) Em outra janela rode:  & `"$claude`" setup-token"
  Write-Host "  2) Autorize no navegador e copie o token (comeca com sk-ant-oat01-...)"
  $tok = Read-Host "  3) Cole o token aqui e tecle Enter"
  if ($tok.Trim()) {
    [IO.File]::WriteAllText($tokenPath, $tok.Trim(), (New-Object System.Text.ASCIIEncoding))
    Write-Host "[ok] token -> $tokenPath"
  } else {
    Write-Warning "Token vazio. Crie depois salvando o token (sk-ant-oat01-...) em: $tokenPath"
  }
}

# 6) Verificacao de auth headless
if (Test-Path $tokenPath) {
  Write-Host ""
  Write-Host "Verificando autenticacao headless..." -ForegroundColor Cyan
  $env:CLAUDE_CODE_OAUTH_TOKEN = (Get-Content $tokenPath -Raw).Trim()
  $resp = & $claude -p "Responda com exatamente uma palavra: OK" --model sonnet 2>&1 | Select-Object -Last 1
  if ("$resp" -match "OK") { Write-Host "[ok] auth headless funcionando." -ForegroundColor Green }
  else { Write-Warning "Resposta inesperada: $resp  (verifique o token)" }
}

Write-Host ""
Write-Host "Pronto! A cada 'git commit', o agente atualiza a documentacao no vault." -ForegroundColor Green
Write-Host "Logs: $repo\.git\agente-de-codigo.log"
Write-Host "Desligar pontual: git commit --no-verify  |  Desligar de vez: apague .git/hooks/post-commit"
