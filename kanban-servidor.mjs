#!/usr/bin/env node
/**
 * =====================================================================
 *  Kanban do Jira - servidor local  (API + interface)
 * =====================================================================
 *  - Serve a interface em  http://127.0.0.1:8099
 *  - Le, cria, edita, move, comenta, anexa e exclui issues
 *  - O token fica SO neste processo: nunca vai para a pagina
 *
 *  Uso:   node kanban-servidor.mjs
 *  Env:   KANBAN_PORT       (padrao 8099)
 *         KANBAN_PROJECT    (padrao CON)
 *         KANBAN_SITE       (padrao https://demelo.atlassian.net)
 *         KANBAN_EMAIL      (padrao victorcupinxa@gmail.com)
 *         KANBAN_APP_URL    (link do app de conformidade; opcional)
 * =====================================================================
 */
import { createServer } from 'node:http'
import { readFileSync } from 'node:fs'
import { homedir } from 'node:os'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const AQUI       = dirname(fileURLToPath(import.meta.url))
const SITE       = (process.env.KANBAN_SITE || 'https://demelo.atlassian.net').replace(/\/+$/, '')
const EMAIL      = process.env.KANBAN_EMAIL || 'victorcupinxa@gmail.com'
const PROJECT    = process.env.KANBAN_PROJECT || 'CON'
const PORT       = Number(process.env.KANBAN_PORT || 8099)
const TOKEN_FILE = process.env.KANBAN_TOKEN_FILE || join(homedir(), '.dsh', '.jira-token')
const UI_FILE    = join(AQUI, 'kanban-ui.html')

/**
 * App de conformidade. O quadro apenas LINK-A para ele, abrindo o processo
 * quando a issue menciona um numero de processo no padrao SEI/SUAP
 * (ex.: 23060.014520/2026-11). Sem isso o botao abre so o app.
 */
const APP_URL = process.env.KANBAN_APP_URL ||
  'https://ais-pre-rxxw4xraqndg73w5bkb6jj-213322120758.us-east1.run.app/'

/** Numero de processo no padrao dos processos deste orgao. */
const PROCESSO_RE = /\b\d{5}\.\d{6}\/\d{4}-\d{2}\b/

/** Ordem preferida das colunas; status fora da lista entra no fim. */
const ORDEM_STATUS = [
  'TO DO - not important',
  'In Progress - very important',
  'Review - important',
  'Concluído',
]

const CAMPOS_LISTA = [
  'summary', 'status', 'priority', 'issuetype', 'updated', 'created',
  'assignee', 'reporter', 'labels', 'duedate', 'parent', 'subtasks',
  'resolutiondate', 'components',
].join(',')

// ---------------------------------------------------------------- Jira
function authHeader () {
  const raw = readFileSync(TOKEN_FILE, 'utf8')
    .trim().replace(/^\uFEFF/, '').replace(/^"|"$/g, '').trim()
  if (!raw) throw new Error('Token vazio em ' + TOKEN_FILE)
  const cred = raw.includes(':') ? raw : EMAIL + ':' + raw
  return 'Basic ' + Buffer.from(cred, 'utf8').toString('base64')
}

/** Chamada JSON ao Jira. Lanca erro com a mensagem que o Jira devolveu. */
async function jira (caminho, init = {}) {
  const res = await fetch(SITE + caminho, {
    ...init,
    headers: {
      Authorization: authHeader(),
      Accept: 'application/json',
      ...(init.body ? { 'Content-Type': 'application/json; charset=utf-8' } : {}),
      ...(init.headers || {}),
    },
  })
  const texto = await res.text()
  let dados = null
  try { dados = texto ? JSON.parse(texto) : null } catch { /* nao-JSON */ }
  if (!res.ok) {
    const msgs = dados && dados.errorMessages && dados.errorMessages.length
      ? dados.errorMessages.join(' | ')
      : (dados && dados.message) || ('HTTP ' + res.status)
    const err = new Error(msgs)
    err.status = res.status
    throw err
  }
  return dados
}

/** Chamada crua (binario): devolve a Response para o chamador repassar. */
async function jiraBruto (caminho) {
  return fetch(SITE + caminho, {
    headers: { Authorization: authHeader(), Accept: '*/*' },
  })
}

// ------------------------------------------------------------ normalizar
/**
 * A `statusCategory` deste Jira tem `name` LOCALIZADO ("Itens concluídos").
 * So a `key` e estavel (done / indeterminate / new), entao e ela que vale.
 */
function catDe (status) {
  const sc = status && status.statusCategory
  return {
    categoria: (sc && sc.name) || '',
    catKey: (sc && sc.key) || '',
    concluido: !!(sc && sc.key === 'done'),
  }
}

function usuario (u) {
  return u ? { id: u.accountId || '', nome: u.displayName || '', email: u.emailAddress || '' } : null
}

function processoDe (...textos) {
  for (const t of textos) {
    if (typeof t !== 'string') continue
    const m = t.match(PROCESSO_RE)
    if (m) return m[0]
  }
  return ''
}

function resumirIssue (i) {
  const f = i.fields || {}
  const c = catDe(f.status)
  return {
    key: i.key,
    id: i.id,
    summary: f.summary || '',
    status: (f.status && f.status.name) || '',
    categoria: c.categoria,
    catKey: c.catKey,
    concluido: c.concluido,
    prioridade: (f.priority && f.priority.name) || '',
    tipo: (f.issuetype && f.issuetype.name) || '',
    tipoId: (f.issuetype && f.issuetype.id) || '',
    subtarefa: !!(f.issuetype && f.issuetype.subtask),
    atualizado: f.updated || '',
    criado: f.created || '',
    resolvido: f.resolutiondate || '',
    vencimento: f.duedate || '',
    labels: f.labels || [],
    componentes: (f.components || []).map((x) => x.name),
    responsavel: usuario(f.assignee),
    relator: usuario(f.reporter),
    pai: f.parent ? { key: f.parent.key, summary: (f.parent.fields && f.parent.fields.summary) || '' } : null,
    filhas: (f.subtasks || []).map((s) => s.key),
    processo: processoDe(f.summary),
  }
}

/** Texto de um campo que pode vir string (v2) ou ADF (v3). */
function textoDe (v) {
  if (!v) return ''
  if (typeof v === 'string') return v
  if (typeof v === 'object') {
    const partes = []
    const anda = (no) => {
      if (!no || typeof no !== 'object') return
      if (no.type === 'text' && no.text) partes.push(no.text)
      if (no.type === 'hardBreak') partes.push('\n')
      if (Array.isArray(no.content)) {
        no.content.forEach(anda)
        if (no.type === 'paragraph' || no.type === 'heading') partes.push('\n')
      }
    }
    anda(v)
    return partes.join('').trim()
  }
  return ''
}

// ------------------------------------------------------------ consultas
async function carregarIssues () {
  const jql = 'project = ' + PROJECT + ' ORDER BY updated DESC'
  let token = null
  let todas = []
  for (let p = 0; p < 30; p++) {
    let url = '/rest/api/3/search/jql?jql=' + encodeURIComponent(jql) +
              '&maxResults=100&fields=' + CAMPOS_LISTA
    if (token) url += '&nextPageToken=' + encodeURIComponent(token)
    const r = await jira(url)
    todas = todas.concat(r.issues || [])
    token = r.nextPageToken
    if (!token) break
  }
  return todas
}

async function carregarMeta () {
  const [prioridades, projeto, usuarios, tipos, statuses, eu] = await Promise.all([
    jira('/rest/api/2/priority').catch(() => []),
    jira('/rest/api/2/project/' + PROJECT).catch(() => ({})),
    jira('/rest/api/2/user/assignable/search?project=' + PROJECT + '&maxResults=100').catch(() => []),
    jira('/rest/api/2/issue/createmeta/' + PROJECT + '/issuetypes').catch(() => null),
    jira('/rest/api/2/project/' + PROJECT + '/statuses').catch(() => []),
    jira('/rest/api/2/myself').catch(() => null),
  ])

  const nomesStatus = []
  for (const t of statuses) {
    for (const s of (t.statuses || [])) {
      if (!nomesStatus.some((x) => x.nome === s.name)) {
        const c = catDe(s)
        nomesStatus.push({ nome: s.name, categoria: c.categoria, catKey: c.catKey, concluido: c.concluido })
      }
    }
  }
  nomesStatus.sort((a, b) => {
    const ia = ORDEM_STATUS.indexOf(a.nome)
    const ib = ORDEM_STATUS.indexOf(b.nome)
    return (ia < 0 ? 999 : ia) - (ib < 0 ? 999 : ib)
  })

  const listaTipos = (tipos && tipos.values)
    ? tipos.values.map((t) => ({ id: t.id, nome: t.name, subtarefa: !!t.subtask }))
    : ((projeto && projeto.issueTypes) || []).map((t) => ({ id: t.id, nome: t.name, subtarefa: !!t.subtask }))

  return {
    projeto: PROJECT,
    site: SITE,
    app: APP_URL,
    eu: usuario(eu),
    statuses: nomesStatus,
    prioridades: (prioridades || []).map((p) => p.name),
    tipos: listaTipos,
    usuarios: (usuarios || []).map(usuario),
  }
}

async function bootstrap () {
  const [cruas, meta] = await Promise.all([carregarIssues(), carregarMeta()])
  const issues = cruas.map(resumirIssue)
  const labels = [...new Set(issues.flatMap((i) => i.labels))].sort()
  const componentes = [...new Set(issues.flatMap((i) => i.componentes))].sort()
  return { ok: true, meta: { ...meta, labels, componentes }, issues, total: issues.length }
}

async function buscar (jql) {
  const r = await jira('/rest/api/3/search/jql?jql=' + encodeURIComponent(jql) +
    '&maxResults=100&fields=' + CAMPOS_LISTA)
  return { issues: (r.issues || []).map(resumirIssue), total: (r.issues || []).length }
}

async function detalheIssue (key) {
  if (!key) throw new Error('key obrigatoria')
  const i = await jira('/rest/api/2/issue/' + encodeURIComponent(key) +
    '?expand=changelog&fields=summary,description,status,priority,issuetype,assignee,reporter,' +
    'labels,duedate,created,updated,resolutiondate,parent,subtasks,issuelinks,attachment,comment,' +
    'components,timetracking,timespent,timeoriginalestimate')
  const f = i.fields || {}
  const c = catDe(f.status)

  const comentarios = ((f.comment && f.comment.comments) || []).map((x) => ({
    id: x.id,
    autor: (x.author && x.author.displayName) || '',
    texto: textoDe(x.body),
    quando: x.created || '',
    atualizado: x.updated || '',
  }))

  const anexos = (f.attachment || []).map((a) => ({
    id: a.id,
    nome: a.filename,
    mime: a.mimeType,
    tamanho: a.size,
    criado: a.created,
    autor: (a.author && a.author.displayName) || '',
    url: 'api/attachment?id=' + encodeURIComponent(a.id),
  }))

  const filhas = (f.subtasks || []).map((s) => ({
    key: s.key,
    summary: (s.fields && s.fields.summary) || '',
    status: (s.fields && s.fields.status && s.fields.status.name) || '',
    concluido: !!(s.fields && s.fields.status && s.fields.status.statusCategory &&
                 s.fields.status.statusCategory.key === 'done'),
    tipo: (s.fields && s.fields.issuetype && s.fields.issuetype.name) || '',
  }))

  const links = (f.issuelinks || []).map((l) => {
    const saida = l.outwardIssue
    const entrada = l.inwardIssue
    const alvo = saida || entrada
    return {
      tipo: (l.type && (saida ? l.type.outward : l.type.inward)) || (l.type && l.type.name) || '',
      direcao: saida ? 'saida' : 'entrada',
      key: alvo ? alvo.key : '',
      summary: (alvo && alvo.fields && alvo.fields.summary) || '',
      status: (alvo && alvo.fields && alvo.fields.status && alvo.fields.status.name) || '',
    }
  }).filter((l) => l.key)

  const historico = ((i.changelog && i.changelog.histories) || []).slice(-40).reverse().map((h) => ({
    autor: (h.author && h.author.displayName) || '',
    quando: h.created || '',
    itens: (h.items || []).map((it) => ({ campo: it.field, de: it.fromString || '', para: it.toString || '' })),
  }))

  const transicoes = await jira('/rest/api/2/issue/' + encodeURIComponent(key) + '/transitions')
    .then((t) => (t.transitions || []).map((x) => ({ id: x.id, nome: x.name, para: x.to && x.to.name })))
    .catch(() => [])

  const descricao = textoDe(f.description)

  return {
    key: i.key,
    summary: f.summary || '',
    descricao,
    status: (f.status && f.status.name) || '',
    categoria: c.categoria,
    catKey: c.catKey,
    concluido: c.concluido,
    prioridade: (f.priority && f.priority.name) || '',
    tipo: (f.issuetype && f.issuetype.name) || '',
    tipoId: (f.issuetype && f.issuetype.id) || '',
    subtarefa: !!(f.issuetype && f.issuetype.subtask),
    responsavel: usuario(f.assignee),
    relator: usuario(f.reporter),
    labels: f.labels || [],
    componentes: (f.components || []).map((x) => x.name),
    vencimento: f.duedate || '',
    criado: f.created || '',
    atualizado: f.updated || '',
    resolvido: f.resolutiondate || '',
    pai: f.parent ? { key: f.parent.key, summary: (f.parent.fields && f.parent.fields.summary) || '' } : null,
    filhas,
    links,
    comentarios,
    anexos,
    historico,
    transicoes,
    tempo: (f.timetracking && { original: f.timetracking.originalEstimate || '', gasto: f.timetracking.timeSpent || '' }) || null,
    processo: processoDe(f.summary, descricao),
    url: SITE + '/browse/' + i.key,
  }
}

// -------------------------------------------------------------- escrita
async function moverIssue (key, paraStatus) {
  const atual = await jira('/rest/api/2/issue/' + encodeURIComponent(key) + '?fields=status')
  const de = atual.fields.status.name
  if (de === paraStatus) return { key, de, para: paraStatus, mudou: false }

  const t = await jira('/rest/api/2/issue/' + encodeURIComponent(key) + '/transitions')
  const tr = (t.transitions || []).find((x) => x.to && x.to.name === paraStatus)
  if (!tr) {
    const possiveis = (t.transitions || []).map((x) => (x.to && x.to.name) || x.name).join(', ')
    throw new Error('Nao existe transicao de "' + de + '" para "' + paraStatus + '". Disponiveis: ' + possiveis)
  }
  await jira('/rest/api/2/issue/' + encodeURIComponent(key) + '/transitions', {
    method: 'POST',
    body: JSON.stringify({ transition: { id: tr.id } }),
  })
  return { key, de, para: paraStatus, transicao: tr.name, mudou: true }
}

async function atualizarIssue (key, c) {
  const fields = {}
  if (typeof c.summary === 'string' && c.summary.trim()) fields.summary = c.summary.trim()
  if (typeof c.descricao === 'string') fields.description = c.descricao
  // Troca de tipo da issue. O Jira pode recusar por regra de workflow; nesse
  // caso o erro dele sobe para a interface em vez de falhar em silencio.
  if (typeof c.tipoId === 'string' && c.tipoId) fields.issuetype = { id: c.tipoId }
  if (typeof c.priority === 'string' && c.priority) fields.priority = { name: c.priority }
  if (typeof c.duedate === 'string') fields.duedate = c.duedate || null
  if (Array.isArray(c.labels)) fields.labels = c.labels
  if ('assigneeAccountId' in c) {
    fields.assignee = c.assigneeAccountId ? { accountId: c.assigneeAccountId } : null
  }
  if ('parentKey' in c) {
    fields.parent = c.parentKey ? { key: c.parentKey } : null
  }
  if (Array.isArray(c.componentes)) {
    fields.components = c.componentes.map((nome) => ({ name: nome }))
  }
  if (!Object.keys(fields).length) return { key, alterado: false }

  await jira('/rest/api/2/issue/' + encodeURIComponent(key), {
    method: 'PUT',
    body: JSON.stringify({ fields }),
  })
  return { key, alterado: true, campos: Object.keys(fields) }
}

async function comentarIssue (key, texto) {
  if (!texto || !texto.trim()) throw new Error('Comentario vazio')
  const r = await jira('/rest/api/2/issue/' + encodeURIComponent(key) + '/comment', {
    method: 'POST',
    body: JSON.stringify({ body: texto }),
  })
  return { key, id: r.id, autor: (r.author && r.author.displayName) || '' }
}

async function editarComentario (key, id, texto) {
  if (!id) throw new Error('id do comentario obrigatorio')
  await jira('/rest/api/2/issue/' + encodeURIComponent(key) + '/comment/' + encodeURIComponent(id), {
    method: 'PUT',
    body: JSON.stringify({ body: texto || '' }),
  })
  return { key, id, editado: true }
}

async function excluirComentario (key, id) {
  if (!id) throw new Error('id do comentario obrigatorio')
  await jira('/rest/api/2/issue/' + encodeURIComponent(key) + '/comment/' + encodeURIComponent(id), {
    method: 'DELETE',
  })
  return { key, id, excluido: true }
}

async function criarIssue (d) {
  if (!d.summary || !d.summary.trim()) throw new Error('Resumo e obrigatorio')
  const fields = {
    project: { key: PROJECT },
    summary: d.summary.trim(),
    issuetype: { id: d.tipoId || '10001' },
  }
  if (d.descricao) fields.description = d.descricao
  if (d.priority) fields.priority = { name: d.priority }
  if (d.assigneeAccountId) fields.assignee = { accountId: d.assigneeAccountId }
  if (d.duedate) fields.duedate = d.duedate
  if (Array.isArray(d.labels) && d.labels.length) fields.labels = d.labels
  if (d.parentKey) fields.parent = { key: d.parentKey }

  const r = await jira('/rest/api/2/issue', { method: 'POST', body: JSON.stringify({ fields }) })
  return { key: r.key, url: SITE + '/browse/' + r.key }
}

async function excluirIssue (key) {
  if (!key) throw new Error('key obrigatoria')
  await jira('/rest/api/2/issue/' + encodeURIComponent(key), { method: 'DELETE' })
  return { key, excluido: true }
}

async function anexar (key, nome, mime, base64) {
  if (!nome) throw new Error('nome do arquivo obrigatorio')
  if (!base64) throw new Error('conteudo vazio')
  const buf = Buffer.from(base64, 'base64')
  const form = new FormData()
  form.append('file', new Blob([buf], { type: mime || 'application/octet-stream' }), nome)
  const res = await fetch(SITE + '/rest/api/2/issue/' + encodeURIComponent(key) + '/attachments', {
    method: 'POST',
    headers: { Authorization: authHeader(), 'X-Atlassian-Token': 'no-check' },
    body: form,
  })
  const txt = await res.text()
  if (!res.ok) throw new Error('Anexo recusado: ' + txt.slice(0, 300))
  const arr = JSON.parse(txt)
  return { key, anexos: arr.map((a) => ({ id: a.id, nome: a.filename, tamanho: a.size })) }
}

// ----------------------------------------------------------------- HTTP
function json (res, code, obj) {
  res.writeHead(code, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' })
  res.end(JSON.stringify(obj))
}

async function corpo (req) {
  const partes = []
  for await (const c of req) partes.push(c)
  const s = Buffer.concat(partes).toString('utf8')
  try { return JSON.parse(s || '{}') } catch { return {} }
}

async function servirAnexo (req, url, res) {
  const id = url.searchParams.get('id')
  if (!id) return json(res, 400, { ok: false, error: 'id obrigatorio' })
  const r = await jiraBruto('/rest/api/2/attachment/content/' + encodeURIComponent(id))
  if (!r.ok) return json(res, r.status, { ok: false, error: 'anexo indisponivel' })
  const cd = r.headers.get('content-disposition') || ''
  const buf = Buffer.from(await r.arrayBuffer())
  res.writeHead(200, {
    'Content-Type': r.headers.get('content-type') || 'application/octet-stream',
    'Content-Disposition': cd || 'attachment',
    'Content-Length': buf.length,
    'Cache-Control': 'no-store',
  })
  res.end(buf)
}

const rotas = {
  'GET /api/bootstrap':       async () => bootstrap(),
  'GET /api/issue':           async (req, url) => detalheIssue(url.searchParams.get('key') || ''),
  'GET /api/search':          async (req, url) => buscar(url.searchParams.get('jql') || ('project = ' + PROJECT)),
  'POST /api/move':           async (req) => { const b = await corpo(req); return moverIssue(b.key, b.to) },
  'POST /api/update':         async (req) => { const b = await corpo(req); return atualizarIssue(b.key, b.campos || {}) },
  'POST /api/comment':        async (req) => { const b = await corpo(req); return comentarIssue(b.key, b.texto || '') },
  'POST /api/comment.edit':   async (req) => { const b = await corpo(req); return editarComentario(b.key, b.id, b.texto) },
  'POST /api/comment.delete': async (req) => { const b = await corpo(req); return excluirComentario(b.key, b.id) },
  'POST /api/create':         async (req) => criarIssue(await corpo(req)),
  'POST /api/delete':         async (req) => { const b = await corpo(req); return excluirIssue(b.key) },
  'POST /api/attachment':     async (req) => { const b = await corpo(req); return anexar(b.key, b.nome, b.mime, b.base64) },
}

const server = createServer(async (req, res) => {
  const url = new URL(req.url, 'http://127.0.0.1')
  const chave = req.method + ' ' + url.pathname

  try {
    if (url.pathname === '/' && req.method === 'GET') {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' })
      return res.end(readFileSync(UI_FILE, 'utf8'))
    }
    if (url.pathname === '/api/attachment' && req.method === 'GET') {
      return servirAnexo(req, url, res)
    }
    if (url.pathname === '/api/health' && req.method === 'GET') {
      const eu = await jira('/rest/api/2/myself').catch((e) => ({ erro: e.message }))
      return json(res, 200, { ok: !eu.erro, site: SITE, projeto: PROJECT, eu, app: APP_URL })
    }
    const rota = rotas[chave]
    if (rota) {
      const r = await rota(req, url)
      return json(res, 200, { ok: true, ...r })
    }
    json(res, 404, { ok: false, error: 'rota desconhecida: ' + chave })
  } catch (e) {
    console.error('[' + chave + '] ' + e.message)
    json(res, e.status || 500, { ok: false, error: e.message })
  }
})

server.listen(PORT, '127.0.0.1', () => {
  console.log('')
  console.log('  Kanban do Jira:  http://127.0.0.1:' + PORT)
  console.log('  Projeto: ' + PROJECT + '     (Ctrl+C encerra)')
  console.log('')
})
