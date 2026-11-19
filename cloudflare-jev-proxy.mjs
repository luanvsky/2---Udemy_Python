#!/usr/bin/env node
/**
 * cloudflare-jev-proxy.mjs
 *
 * Ponte local entre o dsh e o Cloudflare Workers AI.
 *
 * O plugin `dsh-jev-tools` fala o contrato da TypeSafe:
 *     POST {baseUrl}/v1/systemone     { state, questions, model }
 *
 * O Cloudflare hospeda o MESMO modelo (typesafe/jev), mas com outro formato:
 *     POST https://api.cloudflare.com/client/v4/accounts/{conta}/ai/run
 *          { model: "typesafe/jev", input: { state, questions } }
 *
 * Este processo escuta em 127.0.0.1 e faz a tradução. A resposta do Cloudflare
 * já vem no formato da TypeSafe, então volta sem conversão.
 *
 * Uso:
 *   node cloudflare-jev-proxy.mjs --test    # faz um julgamento de teste, imprime e sai
 *   node cloudflare-jev-proxy.mjs           # sobe o servidor (fica em primeiro plano)
 *   node cloudflare-jev-proxy.mjs --verbose # idem, registrando cada requisição
 *
 * Credenciais, nesta ordem: variável de ambiente, depois o arquivo de
 * credenciais do dsh (~/.dsh/.credentials.yaml):
 *   CLOUDFLARE_ACCOUNT_ID
 *   CLOUDFLARE_API_TOKEN
 *
 * Sem dependências. Requer Node 20+ (usa `fetch` global).
 */

import { createServer } from 'node:http'
import { readFileSync, existsSync } from 'node:fs'
import { homedir } from 'node:os'
import { join } from 'node:path'

const PORT = Number(process.env.JEV_PROXY_PORT ?? 8788)
const HOST = '127.0.0.1'
const CLOUDFLARE_MODEL = 'typesafe/jev'
const CF_API = 'https://api.cloudflare.com/client/v4/accounts'
const TIMEOUT_MS = 60_000

const VERBOSE = process.argv.includes('--verbose')
const TEST_MODE = process.argv.includes('--test')

const DSH_HOME = process.env.DSH_HOME ?? join(homedir(), '.dsh')
const CREDENTIALS_FILE =
  process.env.DSH_CREDENTIALS_FILE ?? join(DSH_HOME, '.credentials.yaml')

/**
 * Lê uma referência do arquivo de credenciais do dsh.
 * O formato é YAML simples: linhas `NOME: "valor"` sob a chave `refs:`.
 * Leitura linha a linha, sem parser de YAML — o suficiente e sem dependência.
 * @param {string} name nome da referência.
 * @returns {string | undefined} o valor, ou undefined quando ausente/vazio.
 */
function fromCredentialsFile(name) {
  if (!existsSync(CREDENTIALS_FILE)) return undefined
  let texto
  try {
    texto = readFileSync(CREDENTIALS_FILE, 'utf8')
  } catch {
    return undefined
  }
  const re = new RegExp(`^[ \\t]*${name}[ \\t]*:[ \\t]*(.+?)[ \\t]*$`, 'm')
  const m = texto.match(re)
  if (!m) return undefined
  const valor = m[1].replace(/^["']|["']$/g, '').trim()
  return valor.length > 0 ? valor : undefined
}

/** Resolve uma credencial: ambiente primeiro, arquivo do dsh depois. */
function credential(name) {
  const doAmbiente = process.env[name]
  if (doAmbiente && doAmbiente.trim().length > 0) return doAmbiente.trim()
  return fromCredentialsFile(name)
}

/** @returns {{account?: string, token?: string}} */
function credentials() {
  return {
    account: credential('CLOUDFLARE_ACCOUNT_ID'),
    token: credential('CLOUDFLARE_API_TOKEN'),
  }
}

/**
 * Envia um julgamento ao Cloudflare e devolve o corpo já no formato da TypeSafe.
 * @param {{state: unknown, questions: unknown}} payload
 * @returns {Promise<{status: number, body: string, ms: number}>}
 */
async function judge(payload) {
  const { account, token } = credentials()
  if (!account || !token) {
    const faltando = [!account && 'CLOUDFLARE_ACCOUNT_ID', !token && 'CLOUDFLARE_API_TOKEN']
      .filter(Boolean)
      .join(', ')
    const erro = new Error(`credencial ausente: ${faltando}`)
    erro.code = 'NO_CREDENTIALS'
    throw erro
  }

  const inicio = Date.now()
  const resposta = await fetch(`${CF_API}/${account}/ai/run`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: CLOUDFLARE_MODEL,
      input: { state: payload.state, questions: payload.questions },
    }),
    signal: AbortSignal.timeout(TIMEOUT_MS),
  })

  const texto = await resposta.text()
  const ms = Date.now() - inicio

  // O Cloudflare pode devolver o corpo direto (formato TypeSafe) ou embrulhado
  // no envelope padrão da API dele. Trata os dois casos.
  let corpo = texto
  try {
    const json = JSON.parse(texto)
    if (json && typeof json === 'object' && 'result' in json && 'success' in json) {
      if (json.success === false) {
        const detalhe = JSON.stringify(json.errors ?? json)
        return { status: resposta.status, body: detalhe, ms }
      }
      corpo = JSON.stringify(json.result)
    }
  } catch {
    // corpo não-JSON: devolve como veio
  }

  return { status: resposta.status, body: corpo, ms }
}

/** Lê o corpo inteiro de uma requisição HTTP. */
function readBody(req) {
  return new Promise((resolve, reject) => {
    const partes = []
    let bytes = 0
    req.on('data', (c) => {
      bytes += c.length
      if (bytes > 8_000_000) {
        reject(new Error('corpo grande demais'))
        req.destroy()
        return
      }
      partes.push(c)
    })
    req.on('end', () => resolve(Buffer.concat(partes).toString('utf8')))
    req.on('error', reject)
  })
}

function enviarJson(res, status, objeto) {
  const corpo = JSON.stringify(objeto)
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(corpo),
  })
  res.end(corpo)
}

// ---------------------------------------------------------------------------
// Modo de teste: um julgamento real, com diagnóstico.
// ---------------------------------------------------------------------------
async function rodarTeste() {
  const { account, token } = credentials()
  console.log('Cloudflare / Jev — teste de conectividade')
  console.log('  account id :', account ? `${account.slice(0, 6)}… (${account.length} chars)` : 'AUSENTE')
  console.log('  api token  :', token ? `presente (${token.length} chars)` : 'AUSENTE')
  console.log('  arquivo    :', CREDENTIALS_FILE)
  console.log()

  if (!account || !token) {
    console.log('Faltam credenciais. Defina CLOUDFLARE_ACCOUNT_ID e CLOUDFLARE_API_TOKEN,')
    console.log('ou acrescente as duas referências no arquivo acima.')
    process.exit(1)
  }

  const payload = {
    state:
      'A relevância é operacionalizada pelo score Okapi BM25, que mede similaridade lexical, ' +
      'não pertinência semântica. Por isso não se reporta Precision@k.',
    questions: {
      portugues: {
        type: 'noul',
        instructions: 'Is this text written in Portuguese?',
        criteria: { true: 'The text is in Portuguese', false: 'The text is not in Portuguese' },
      },
      categoria: {
        type: 'choice',
        instructions: 'Which validity threat does this passage address?',
        criteria: {
          constructo: 'Conceptual operationalization of a measure',
          interna: 'Measurement or methodology error',
          externa: 'Generalization beyond the study',
        },
      },
    },
  }

  try {
    const { status, body, ms } = await judge(payload)
    console.log(`HTTP ${status} em ${ms} ms`)
    if (status === 200) {
      console.log()
      console.log('RESPOSTA:')
      console.log(JSON.stringify(JSON.parse(body), null, 2))
      console.log()
      console.log('>>> FUNCIONOU: o Jev respondeu pelo Cloudflare.')
      process.exit(0)
    }
    console.log('CORPO:', body)
    console.log()
    console.log('>>> NAO FUNCIONOU. Veja o corpo acima.')
    process.exit(2)
  } catch (erro) {
    console.log('ERRO:', erro.message)
    if (erro.code === 'NO_CREDENTIALS') {
      console.log('>>> Configure as credenciais e rode de novo.')
    }
    process.exit(3)
  }
}

// ---------------------------------------------------------------------------
// Modo servidor: expõe o contrato da TypeSafe para o plugin do dsh.
// ---------------------------------------------------------------------------
function subirServidor() {
  const { account, token } = credentials()
  const servidor = createServer(async (req, res) => {
    const inicio = Date.now()
    const url = new URL(req.url ?? '/', `http://${HOST}:${PORT}`)

    if (req.method === 'GET' && (url.pathname === '/health' || url.pathname === '/')) {
      const c = credentials()
      enviarJson(res, 200, {
        ok: true,
        credenciais: { account: Boolean(c.account), token: Boolean(c.token) },
        modelo: CLOUDFLARE_MODEL,
        upstream: `${CF_API}/<conta>/ai/run`,
      })
      return
    }

    // O plugin pode consultar a lista de modelos; devolve o formato da TypeSafe.
    if (req.method === 'GET' && url.pathname === '/v1/models') {
      enviarJson(res, 200, {
        models: [
          {
            name: CLOUDFLARE_MODEL,
            description: 'Jev via Cloudflare Workers AI (proxy local).',
            release_date: '2026-09-15',
          },
        ],
      })
      return
    }

    if (req.method !== 'POST' || url.pathname !== '/v1/systemone') {
      enviarJson(res, 404, { message: `rota não encontrada: ${req.method} ${url.pathname}`, error_type: 'not_found' })
      return
    }

    let payload
    try {
      payload = JSON.parse(await readBody(req))
    } catch (erro) {
      enviarJson(res, 422, { message: `corpo inválido: ${erro.message}`, error_type: 'invalid_request' })
      return
    }

    if (!payload || typeof payload !== 'object' || payload.questions === undefined) {
      enviarJson(res, 422, { message: 'corpo precisa conter `questions`', error_type: 'invalid_request' })
      return
    }

    const nPerguntas = Object.keys(payload.questions ?? {}).length
    const tamEstado =
      typeof payload.state === 'string' ? payload.state.length : JSON.stringify(payload.state ?? '').length

    try {
      const { status, body, ms } = await judge(payload)
      if (VERBOSE) {
        console.log(
          `[jev-proxy] ${status} em ${ms} ms · ${nPerguntas} pergunta(s) · estado ${tamEstado} chars`,
        )
      }
      res.writeHead(status, {
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Length': Buffer.byteLength(body),
      })
      res.end(body)
    } catch (erro) {
      if (VERBOSE) console.log(`[jev-proxy] erro após ${Date.now() - inicio} ms:`, erro.message)
      const status = erro.code === 'NO_CREDENTIALS' ? 500 : 502
      enviarJson(res, status, {
        message: erro.message,
        error_type: erro.code === 'NO_CREDENTIALS' ? 'no_credentials' : 'upstream_error',
      })
    }
  })

  servidor.listen(PORT, HOST, () => {
    console.log('Jev proxy (Cloudflare) no ar')
    console.log(`  escutando   : http://${HOST}:${PORT}`)
    console.log(`  endpoint    : http://${HOST}:${PORT}/v1/systemone`)
    console.log(`  upstream    : ${CF_API}/<conta>/ai/run  (modelo ${CLOUDFLARE_MODEL})`)
    console.log(`  account id  : ${account ? 'ok' : 'AUSENTE — o proxy responderá 500'}`)
    console.log(`  api token   : ${token ? 'ok' : 'AUSENTE — o proxy responderá 500'}`)
    console.log()
    console.log('Aponte o plugin do dsh para http://127.0.0.1:' + PORT + ' e reinicie o dsh web.')
    console.log('Ctrl+C encerra.')
  })

  servidor.on('error', (erro) => {
    if (erro.code === 'EADDRINUSE') {
      console.error(`Porta ${PORT} já está em uso. Use JEV_PROXY_PORT=8799 para trocar.`)
    } else {
      console.error('Erro no servidor:', erro.message)
    }
    process.exit(1)
  })
}

if (TEST_MODE) {
  await rodarTeste()
} else {
  subirServidor()
}
