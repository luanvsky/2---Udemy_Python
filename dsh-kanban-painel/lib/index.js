/**
 * dsh-kanban-painel - metade HOST.
 *
 * Intencionalmente vazia. Este plugin existe para colocar uma aba na barra
 * lateral DIREITA do DSH Web, e essa aba e construida inteiramente na metade
 * cliente (lib/client.js), declarada em package.json -> dsh.client.platform.
 *
 * O quadro em si NAO mora aqui: ele e servido por kanban-servidor.mjs em
 * http://127.0.0.1:8099, e a aba apenas o embute num iframe. Isso mantem o
 * token do Jira fora do navegador: quem fala com o Jira e o processo Node.
 */

/** Nome de diagnostico do plugin. */
export const name = 'kanban-painel'

/** Nada e injetado: a metade host nao consome servico nenhum. */
export const inject = []

/** No-op por desenho. */
export function apply () {}
