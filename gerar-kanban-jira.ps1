# =====================================================================
#  Gerador de Kanban HTML a partir do Jira
#  Le as tarefas do projeto e monta um quadro visual em portugues.
#  Uso:  pwsh -File gerar-kanban-jira.ps1
#  Saida: kanban-jira.html  (mesma pasta) - abra no navegador
# =====================================================================

param(
    [string]$Projeto = "CON",
    [string]$Saida   = "$PSScriptRoot\kanban-jira.html"
)

$ErrorActionPreference = 'Stop'
$site      = "https://demelo.atlassian.net"
$email     = "victorcupinxa@gmail.com"
$tokenFile = "$env:USERPROFILE\.dsh\.jira-token"

# --- 1) credencial ---------------------------------------------------
if (-not (Test-Path $tokenFile)) { throw "Token nao encontrado em $tokenFile" }
$raw  = (Get-Content $tokenFile -Raw -Encoding UTF8).Trim().Trim([char]0xFEFF).Trim('"').Trim()
$cred = if ($raw.Contains(':')) { $raw } else { "$email`:$raw" }
$b64  = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($cred))
$hdr  = @{ Authorization = "Basic $b64"; Accept = 'application/json' }

# --- 2) buscar as tarefas (paginado) ---------------------------------
$jql    = "project = $Projeto ORDER BY updated DESC"
$fields = 'summary,status,priority,issuetype,updated,created,assignee,labels'
$todas  = New-Object System.Collections.ArrayList
$token  = $null
$paginas = 0
do {
    $url = "$site/rest/api/3/search/jql?jql=" + [uri]::EscapeDataString($jql) +
           "&maxResults=100&fields=$fields"
    if ($token) { $url += "&nextPageToken=" + [uri]::EscapeDataString($token) }
    $r = Invoke-RestMethod $url -Headers $hdr -TimeoutSec 60
    foreach ($i in $r.issues) { [void]$todas.Add($i) }
    $token = $r.nextPageToken
    $paginas++
} while ($token -and $paginas -lt 20)

Write-Host ("Tarefas lidas: " + $todas.Count + " em " + $paginas + " pagina(s)") -ForegroundColor Green

# --- 3) helpers ------------------------------------------------------
function Esc([string]$s) {
    if ([string]::IsNullOrEmpty($s)) { return '' }
    $s.Replace('&','&amp;').Replace('<','&lt;').Replace('>','&gt;').Replace('"','&quot;')
}

$corPri = @{
    'Highest' = '#ff5c5c'; 'High' = '#ff9f43'; 'Medium' = '#4da3ff'
    'Low' = '#7bd88f'; 'Lowest' = '#9aa0a6'
}
$corCat = @{
    'Itens Pendentes'  = '#8b949e'
    'Em andamento'     = '#4da3ff'
    'Itens concluídos' = '#3fb950'
}

# ordem das colunas (status reais deste Jira)
$ordem = @('TO DO - not important','In Progress - very important','Review - important','Concluído')

$porStatus = @{}
foreach ($i in $todas) {
    $st = $i.fields.status.name
    if (-not $porStatus.ContainsKey($st)) { $porStatus[$st] = New-Object System.Collections.ArrayList }
    [void]$porStatus[$st].Add($i)
}
$colunas = @($ordem | Where-Object { $porStatus.ContainsKey($_) })
$extras  = @($porStatus.Keys | Where-Object { $ordem -notcontains $_ } | Sort-Object)
$colunas += $extras

# --- 4) montar o HTML ------------------------------------------------
$sb = New-Object System.Text.StringBuilder
[void]$sb.Append(@'
<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kanban &middot; Jira CON</title>
<style>
  :root{
    --bg:#0d1117; --col:#161b22; --card:#1c2129; --line:#30363d;
    --txt:#e6edf3; --dim:#8b949e; --accent:#4da3ff;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--txt);
       font:14px/1.5 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
  header{padding:20px 24px 12px;border-bottom:1px solid var(--line)}
  h1{margin:0 0 4px;font-size:19px;font-weight:650}
  .sub{color:var(--dim);font-size:12.5px}
  .board{display:flex;gap:14px;padding:18px 24px 40px;overflow-x:auto;align-items:flex-start}
  .col{background:var(--col);border:1px solid var(--line);border-radius:10px;
       min-width:290px;width:290px;flex:0 0 auto;display:flex;flex-direction:column;
       max-height:calc(100vh - 150px)}
  .colhead{display:flex;align-items:center;gap:8px;padding:11px 13px;
           border-bottom:1px solid var(--line);position:sticky;top:0;
           background:var(--col);border-radius:10px 10px 0 0}
  .dot{width:9px;height:9px;border-radius:50%;flex:0 0 auto}
  .colname{font-weight:600;font-size:13px;flex:1;
           white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .count{background:#21262d;color:var(--dim);border-radius:20px;
         padding:1px 8px;font-size:11.5px;font-variant-numeric:tabular-nums}
  .cards{padding:9px;display:flex;flex-direction:column;gap:8px;overflow-y:auto}
  .card{background:var(--card);border:1px solid var(--line);border-left-width:3px;
        border-radius:7px;padding:9px 10px;transition:border-color .12s,transform .12s}
  .card:hover{transform:translateX(2px);border-color:#4b5563}
  .card.extra{display:none}
  body.alldone .card.extra{display:block}
  .toggle{display:inline-flex;align-items:center;gap:6px;margin-top:9px;
          color:var(--dim);font-size:12px;cursor:pointer;user-select:none}
  .toggle input{accent-color:var(--accent);cursor:pointer}
  .more{color:var(--dim);font-size:11.5px;text-align:center;padding:7px;
        border:1px dashed var(--line);border-radius:7px}
  .key{font:600 11.5px ui-monospace,SFMono-Regular,Consolas,monospace;
       color:var(--accent);text-decoration:none}
  .key:hover{text-decoration:underline}
  .sum{margin:5px 0 7px;font-size:13px;word-wrap:break-word}
  .meta{display:flex;flex-wrap:wrap;gap:5px;font-size:10.5px;color:var(--dim)}
  .tag{border:1px solid var(--line);border-radius:5px;padding:1px 6px;white-space:nowrap}
  .empty{color:var(--dim);font-size:12px;padding:10px;text-align:center}
</style></head><body>
'@)

[void]$sb.Append("<header><h1>Kanban &middot; projeto " + (Esc $Projeto) + "</h1>")
[void]$sb.Append('<div class="sub">' + $todas.Count + ' tarefas &middot; gerado em ' +
                 (Get-Date).ToString('dd/MM/yyyy HH:mm') + '</div>')
[void]$sb.Append('<label class="toggle"><input type="checkbox" ' +
                 'onchange="document.body.classList.toggle(''alldone'', this.checked)">' +
                 ' mostrar todas as concluidas</label></header>')
[void]$sb.Append('<div class="board">')

foreach ($st in $colunas) {
    $issues = $porStatus[$st]
    $cat = if ($issues.Count -gt 0) { $issues[0].fields.status.statusCategory.name } else { '' }
    $cor = if ($corCat.ContainsKey($cat)) { $corCat[$cat] } else { '#8b949e' }

    [void]$sb.Append('<div class="col"><div class="colhead">')
    [void]$sb.Append('<span class="dot" style="background:' + $cor + '"></span>')
    [void]$sb.Append('<span class="colname">' + (Esc $st) + '</span>')
    [void]$sb.Append('<span class="count">' + $issues.Count + '</span></div>')
    [void]$sb.Append('<div class="cards">')

    if ($issues.Count -eq 0) {
        [void]$sb.Append('<div class="empty">nenhuma tarefa</div>')
    }

    $idx     = 0
    $limite  = if ($cat -eq 'Itens concluídos' -and $issues.Count -gt 25) { 25 } else { [int]::MaxValue }
    $ocultas = if ($limite -eq [int]::MaxValue) { 0 } else { $issues.Count - $limite }

    foreach ($i in $issues) {
        $idx++
        $f   = $i.fields
        $pri = if ($f.priority) { $f.priority.name } else { '' }
        $bc  = if ($corPri.ContainsKey($pri)) { $corPri[$pri] } else { '#30363d' }
        $upd = ([datetime]$f.updated).ToString('dd/MM/yy')
        $tipo = if ($f.issuetype) { $f.issuetype.name } else { '' }

        $cls = if ($idx -gt $limite) { 'card extra' } else { 'card' }
        [void]$sb.Append('<div class="' + $cls + '" style="border-left-color:' + $bc + '">')
        [void]$sb.Append('<a class="key" target="_blank" href="' + $site + '/browse/' + $i.key + '">' + $i.key + '</a>')
        [void]$sb.Append('<div class="sum">' + (Esc $f.summary) + '</div>')
        [void]$sb.Append('<div class="meta">')
        if ($tipo) { [void]$sb.Append('<span class="tag">' + (Esc $tipo) + '</span>') }
        if ($pri)  { [void]$sb.Append('<span class="tag" style="color:' + $bc + ';border-color:' + $bc + '55">' + (Esc $pri) + '</span>') }
        [void]$sb.Append('<span class="tag">atualizado ' + $upd + '</span>')
        [void]$sb.Append('</div></div>')
    }

    if ($ocultas -gt 0) {
        [void]$sb.Append('<div class="more">+ ' + $ocultas +
                         ' concluidas ocultas &mdash; marque a caixa acima para mostrar</div>')
    }

    [void]$sb.Append('</div></div>')
}

[void]$sb.Append('</div></body></html>')

[System.IO.File]::WriteAllText($Saida, $sb.ToString(), (New-Object System.Text.UTF8Encoding($false)))
Write-Host ("Quadro salvo em: " + $Saida) -ForegroundColor Green
