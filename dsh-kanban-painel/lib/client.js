/**
 * dsh-kanban-painel - metade CLIENTE (bundle web do DSH).
 *
 * Faz duas coisas:
 *   1. registra um TIPO de aba na barra lateral direita
 *      (ctx.sidebarRightTabs.register, do @deepseek-ai/dsh-client-ui-sidebar-right);
 *   2. registra o CORPO dessa aba no slot `sidebar.right.pane.tab`
 *      (ctx.slots.register, do @deepseek-ai/dsh-client-ui-slots).
 *
 * O corpo e apenas um <iframe> apontando para o quadro servido localmente por
 * kanban-servidor.mjs. Assim o token do Jira continua fora do navegador: esta
 * pagina nao tem credencial nenhuma, so mostra o que o processo Node devolve.
 */
window.__ModuleLoader__.load({
  id: "dsh-kanban-painel",
  factory: (require) => {
    var module = { exports: {} };
    var exports = module.exports;
    Object.defineProperty(exports, Symbol.toStringTag, { value: "Module" });

    var React = require("react");
    var h = React.createElement;

    /** Identidade desta implementacao no sistema de abas (unica). */
    var ID = "dsh-kanban-painel";
    /** O "kind" da aba: e por ele que a pagina e aberta. */
    var KIND = "kanban-jira";
    /** Onde o quadro esta servido. */
    var URL_QUADRO = "http://127.0.0.1:8099";

    /**
     * Marcador de versao. Existe para diagnostico: se o bundle antigo ainda
     * estiver no cache do navegador, esta linha NAO aparece no console e da
     * para distinguir "codigo velho" de "codigo novo que nao registrou".
     */
    var VERSAO = "v3-diagnostico";
    try {
      console.log("[kanban-painel] bundle cliente carregado: " + VERSAO);
    } catch (e) { /* console indisponivel */ }

    /**
     * Corpo da aba. Mede o container com ResizeObserver e fixa a altura do
     * iframe em pixels — `height: 100%` num pai sem altura definida colapsa
     * para a altura padrao do iframe (150px), e o quadro ficaria espremido.
     */
    function Corpo() {
      var wrapRef = React.useRef(null);
      var frameRef = React.useRef(null);

      React.useEffect(function () {
        var wrap = wrapRef.current;
        var frame = frameRef.current;
        if (!wrap || !frame) return;

        function ajustar() {
          var altura = wrap.clientHeight || Math.round(wrap.getBoundingClientRect().height);
          if (altura > 0) frame.style.height = altura + "px";
        }

        ajustar();
        var observador = null;
        if (typeof window.ResizeObserver === "function") {
          observador = new window.ResizeObserver(ajustar);
          observador.observe(wrap);
        }
        window.addEventListener("resize", ajustar);
        return function () {
          if (observador) observador.disconnect();
          window.removeEventListener("resize", ajustar);
        };
      }, []);

      return h(
        "div",
        {
          ref: wrapRef,
          style: {
            position: "relative",
            width: "100%",
            height: "100%",
            minHeight: "360px",
            overflow: "hidden"
          }
        },
        h("iframe", {
          ref: frameRef,
          src: URL_QUADRO,
          title: "Kanban do Jira",
          style: {
            position: "absolute",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            border: "0",
            display: "block",
            background: "#0d1117"
          }
        })
      );
    }

    function apply(ctx) {
      var slots = ctx.get("slots");
      var tabs = ctx.get("sidebarRightTabs");
      // Diagnostico: o `return` mudo antigo escondia a causa. Agora a falha
      // fica visivel no console.
      if (!slots || !tabs) {
        try {
          console.error(
            "[kanban-painel] " + VERSAO + " ABORTADO: servico ausente -> slots=" +
            (slots ? "ok" : "AUSENTE") + ", sidebarRightTabs=" + (tabs ? "ok" : "AUSENTE")
          );
        } catch (e) { /* console indisponivel */ }
        return;
      }
      try {
        console.log("[kanban-painel] " + VERSAO + " ativo: registrando aba kind=" + KIND);
      } catch (e) { /* console indisponivel */ }

      // 1) O tipo de aba. `keepMounted` mantem o iframe vivo ao trocar de aba,
      //    entao o quadro nao recarrega toda vez que voce sai e volta.
      //    ATENCAO: a suposicao antiga de "exatamente UM guia, entao a barra
      //    abre o Kanban direto" nao se sustenta -- terminal, arquivos e
      //    navegador tambem contribuem entradas de guia, entao o DSH abre a
      //    pagina de guia (titulo "Start") e a capsula e que leva ao Kanban.
      ctx.effect(function () {
        return tabs.register({
          id: ID,
          kind: KIND,
          keepMounted: true,
          title: function () {
            return "Kanban";
          },
          guide: [
            {
              id: "abrir",
              // `order` e OBRIGATORIO em SidebarRightGuideEntry
              // (readonly order: number); a guia ordena as capsulas por ele.
              order: 10,
              // `title` e `description` sao THUNKS no contrato
              // (readonly title: () => string). A guia os INVOCA --
              // `children: entry.title()` e `entry.description?.()`. Passar
              // string crua faz o render lancar TypeError e a barra fica presa
              // na guia "Start", sem a capsula do Kanban: era o sintoma.
              title: function () { return "Kanban do Jira"; },
              description: function () { return "Quadro das tarefas, direto do Jira"; }
              // Sem `kind`: o proprio registro o acrescenta, devolvendo
              // SidebarRightGuideBox.
            }
          ]
        });
      }, "kanban-painel: tipo de aba");

      // 2) O corpo da aba, no slot que a barra lateral direita renderiza.
      ctx.effect(function () {
        return slots.inject("sidebar.right.pane.tab", function () {
          return slots.register({ name: "sidebar.right.pane.tab", key: ID }, Corpo);
        });
      }, "kanban-painel: corpo da aba");
    }

    exports.inject = ["slots", "sidebarRightTabs"];
    exports.apply = apply;
    return module.exports;
  }
});
