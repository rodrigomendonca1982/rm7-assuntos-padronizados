/* ============================================================
   RM7-MSG-CMATFN-PY - Versão 2.0.6
   Interface com tabela no padrão da versão 1.0, autenticação,
   backup, restauração, exportação e paginação.
   ============================================================ */

let registros = [];
let administradorAutenticado = false;
let paginaAtual = 1;
let itensPorPagina = 25;

// ============================================================
// Seletores principais
// ============================================================

const btnAbrirMenu = document.getElementById("btnAbrirMenu");
const btnFecharMenu = document.getElementById("btnFecharMenu");
const menuLateral = document.getElementById("menuLateral");
const overlay = document.getElementById("overlay");

const areaLogin = document.getElementById("areaLogin");
const menuAdmin = document.getElementById("menuAdmin");
const senhaAdmin = document.getElementById("senhaAdmin");
const btnEntrar = document.getElementById("btnEntrar");
const btnBloquear = document.getElementById("btnBloquear");

const textoModo = document.getElementById("textoModo");
const seloModo = document.getElementById("seloModo");

const campoPesquisa = document.getElementById("campoPesquisa");
const cabecalhoTabela = document.getElementById("cabecalhoTabela");
const corpoTabela = document.getElementById("corpoTabela");

const totalRegistros = document.getElementById("totalRegistros");
const totalFiltrados = document.getElementById("totalFiltrados");
const totalPaginas = document.getElementById("totalPaginas");

const seletorItensPorPagina = document.getElementById("itensPorPagina");
const btnPaginaAnterior = document.getElementById("btnPaginaAnterior");
const btnProximaPagina = document.getElementById("btnProximaPagina");
const infoPaginacao = document.getElementById("infoPaginacao");

const toast = document.getElementById("toast");
const dataAtualMenu = document.getElementById("dataAtualMenu");

// Modal Registro
const modalRegistro = document.getElementById("modalRegistro");
const tituloModalRegistro = document.getElementById("tituloModalRegistro");
const registroId = document.getElementById("registroId");
const responsavel = document.getElementById("responsavel");
const assunto = document.getElementById("assunto");

const btnNovoRegistro = document.getElementById("btnNovoRegistro");
const btnCadastrarAssuntoTabela = document.getElementById("btnCadastrarAssuntoTabela");
const btnCancelarRegistro = document.getElementById("btnCancelarRegistro");
const btnSalvarRegistro = document.getElementById("btnSalvarRegistro");

// Modal Backup
const modalBackup = document.getElementById("modalBackup");
const btnBackup = document.getElementById("btnBackup");
const observacaoBackup = document.getElementById("observacaoBackup");
const contadorObservacaoBackup = document.getElementById("contadorObservacaoBackup");
const btnCancelarBackup = document.getElementById("btnCancelarBackup");
const btnConfirmarBackup = document.getElementById("btnConfirmarBackup");

// Modal Restaurar
const modalRestaurar = document.getElementById("modalRestaurar");
const btnRestaurar = document.getElementById("btnRestaurar");
const btnFecharRestaurar = document.getElementById("btnFecharRestaurar");
const listaBackups = document.getElementById("listaBackups");

// Exportar
const btnExportar = document.getElementById("btnExportar");


// ============================================================
// Funções utilitárias
// ============================================================

function mostrarToast(mensagem) {
  toast.textContent = mensagem;
  toast.classList.remove("oculto");

  setTimeout(() => {
    toast.classList.add("oculto");
  }, 3600);
}

async function apiGet(url) {
  const resposta = await fetch(url);
  return resposta.json();
}

async function apiPost(url, dados) {
  const resposta = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json; charset=utf-8"
    },
    body: JSON.stringify(dados || {})
  });

  return resposta.json();
}

function abrirMenu() {
  menuLateral.classList.remove("menu-fechado");
  menuLateral.classList.add("menu-aberto");
  overlay.classList.remove("oculto");
}

function fecharMenu() {
  menuLateral.classList.remove("menu-aberto");
  menuLateral.classList.add("menu-fechado");
  overlay.classList.add("oculto");
}

function atualizarDataMenu() {
  if (!dataAtualMenu) return;

  const hoje = new Date();
  dataAtualMenu.textContent = hoje.toLocaleDateString("pt-BR", {
    weekday: "long",
    day: "2-digit",
    month: "2-digit",
    year: "numeric"
  });
}

function atualizarEstadoAutenticacao() {
  if (administradorAutenticado) {
    areaLogin.classList.add("oculto");
    menuAdmin.classList.remove("oculto");
    textoModo.textContent = "Modo administrador";
    seloModo.textContent = "Administrador";
    if (btnCadastrarAssuntoTabela) btnCadastrarAssuntoTabela.classList.remove("oculto");
  } else {
    areaLogin.classList.remove("oculto");
    menuAdmin.classList.add("oculto");
    textoModo.textContent = "Modo visitante";
    seloModo.textContent = "Visitante";
    if (btnCadastrarAssuntoTabela) btnCadastrarAssuntoTabela.classList.add("oculto");
  }

  renderizarTabela();
}

function escaparHtml(valor) {
  return String(valor ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escaparAtributo(valor) {
  return String(valor ?? "")
    .replaceAll("\\", "\\\\")
    .replaceAll("'", "\\'")
    .replaceAll('"', "&quot;");
}


// ============================================================
// Dados, filtro, tabela e paginação
// ============================================================

async function carregarDados() {
  const resposta = await apiGet("/api/dados");

  if (resposta.sucesso) {
    registros = resposta.dados || [];
    atualizarResumo();
    renderizarTabela();
  } else {
    mostrarToast("Não foi possível carregar os dados.");
  }
}

function atualizarResumo() {
  totalRegistros.textContent = registros.length;
}

function registrosFiltrados() {
  const termo = campoPesquisa.value.trim().toLowerCase();

  return registros.filter(item => {
    const textoCompleto = [
      item.responsavel,
      item.assunto
    ].join(" ").toLowerCase();

    return !termo || textoCompleto.includes(termo);
  });
}

function calcularPagina(lista) {
  const total = lista.length;
  const paginas = Math.max(1, Math.ceil(total / itensPorPagina));

  if (paginaAtual > paginas) paginaAtual = paginas;
  if (paginaAtual < 1) paginaAtual = 1;

  const inicio = (paginaAtual - 1) * itensPorPagina;
  const fim = inicio + itensPorPagina;

  return {
    paginas,
    inicio,
    fim,
    itens: lista.slice(inicio, fim)
  };
}

function atualizarPaginacao(lista, pagina) {
  const total = lista.length;
  totalFiltrados.textContent = total;
  totalPaginas.textContent = pagina.paginas;

  if (total === 0) {
    infoPaginacao.textContent = "Nenhum registro encontrado.";
  } else {
    const primeiro = pagina.inicio + 1;
    const ultimo = Math.min(pagina.fim, total);
    infoPaginacao.textContent = `Exibindo ${primeiro} a ${ultimo} de ${total} registro(s). Página ${paginaAtual} de ${pagina.paginas}.`;
  }

  btnPaginaAnterior.disabled = paginaAtual <= 1;
  btnProximaPagina.disabled = paginaAtual >= pagina.paginas;
}

function renderizarTabela() {
  const lista = registrosFiltrados();
  const pagina = calcularPagina(lista);
  atualizarPaginacao(lista, pagina);

  cabecalhoTabela.innerHTML = administradorAutenticado
    ? `
      <tr>
        <th>RESPONSAVEL</th>
        <th>Assunto</th>
        <th class="coluna-acoes">Ações</th>
      </tr>
    `
    : `
      <tr>
        <th>RESPONSAVEL</th>
        <th>Assunto</th>
      </tr>
    `;

  if (pagina.itens.length === 0) {
    corpoTabela.innerHTML = `
      <tr>
        <td colspan="${administradorAutenticado ? 3 : 2}">Nenhum registro encontrado.</td>
      </tr>
    `;
    return;
  }

  corpoTabela.innerHTML = pagina.itens.map(item => {
    const colunaAcoes = administradorAutenticado
      ? `
        <td>
          <div class="acoes-linha">
            <button class="botao-icone botao-editar" type="button" title="Editar" aria-label="Editar registro" onclick="abrirEdicao(${item.id})">✏️</button>
            <button class="botao-icone botao-excluir" type="button" title="Excluir" aria-label="Excluir registro" onclick="excluirRegistro(${item.id})">🗑️</button>
          </div>
        </td>
      `
      : "";

    return `
      <tr>
        <td>${escaparHtml(item.responsavel || "")}</td>
        <td>${escaparHtml(item.assunto || "")}</td>
        ${colunaAcoes}
      </tr>
    `;
  }).join("");
}

function reiniciarPaginacao() {
  paginaAtual = 1;
  renderizarTabela();
}


// ============================================================
// Autenticação simples
// ============================================================

async function entrarComoAdministrador() {
  const senha = senhaAdmin.value;

  if (!senha) {
    mostrarToast("Digite a senha administrativa.");
    return;
  }

  const resposta = await apiPost("/api/login", { senha });

  if (resposta.sucesso) {
    administradorAutenticado = true;
    senhaAdmin.value = "";
    atualizarEstadoAutenticacao();
    mostrarToast("Menu administrativo liberado.");
  } else {
    mostrarToast(resposta.mensagem || "Senha incorreta.");
  }
}

function bloquearSistema() {
  administradorAutenticado = false;
  atualizarEstadoAutenticacao();
  fecharMenu();
  mostrarToast("Sistema voltou para o modo visitante.");
}


// ============================================================
// Cadastro, edição e exclusão
// ============================================================

function abrirNovoRegistro() {
  registroId.value = "";
  responsavel.value = "";
  assunto.value = "";

  tituloModalRegistro.textContent = "Novo Registro";
  modalRegistro.showModal();
}

function abrirEdicao(id) {
  if (!administradorAutenticado) {
    mostrarToast("A edição exige autenticação.");
    return;
  }

  const registro = registros.find(item => Number(item.id) === Number(id));

  if (!registro) {
    mostrarToast("Registro não encontrado.");
    return;
  }

  registroId.value = registro.id;
  responsavel.value = registro.responsavel || "";
  assunto.value = registro.assunto || "";

  tituloModalRegistro.textContent = "Editar Registro";
  modalRegistro.showModal();
}

async function salvarRegistro() {
  if (!administradorAutenticado) {
    mostrarToast("É necessário autenticar para salvar.");
    return;
  }

  const registroAtual = registros.find(item => Number(item.id) === Number(registroId.value));
  const payload = {
    id: registroId.value,
    responsavel: responsavel.value,
    assunto: assunto.value,
    padrao: registroAtual?.padrao || false
  };

  if (!payload.assunto.trim()) {
    mostrarToast("O campo assunto é obrigatório.");
    return;
  }

  const url = payload.id ? "/api/dados/editar" : "/api/dados/criar";
  const resposta = await apiPost(url, payload);

  if (resposta.sucesso) {
    modalRegistro.close();
    mostrarToast(resposta.mensagem || "Registro salvo.");
    await carregarDados();
  } else {
    mostrarToast(resposta.mensagem || "Não foi possível salvar.");
  }
}

async function excluirRegistro(id) {
  if (!administradorAutenticado) {
    mostrarToast("A exclusão exige autenticação.");
    return;
  }

  const confirmar = confirm("Tem certeza que deseja excluir este registro?");
  if (!confirmar) return;

  const resposta = await apiPost("/api/dados/excluir", { id });

  if (resposta.sucesso) {
    mostrarToast("Registro excluído com sucesso.");
    await carregarDados();
  } else {
    mostrarToast(resposta.mensagem || "Não foi possível excluir.");
  }
}


// ============================================================
// Backup
// ============================================================

function abrirModalBackup() {
  if (!administradorAutenticado) {
    mostrarToast("O backup exige autenticação.");
    return;
  }

  observacaoBackup.value = "";
  contadorObservacaoBackup.textContent = "0/30 caracteres";
  modalBackup.showModal();
}

async function confirmarBackup() {
  const observacao = observacaoBackup.value.trim();

  const resposta = await apiPost("/api/backup/criar", { observacao });

  if (resposta.sucesso) {
    modalBackup.close();
    mostrarToast(`Backup criado: ${resposta.arquivo}`);
  } else {
    mostrarToast(resposta.mensagem || "Não foi possível criar o backup.");
  }
}


// ============================================================
// Restauração
// ============================================================

async function abrirModalRestaurar() {
  if (!administradorAutenticado) {
    mostrarToast("A restauração exige autenticação.");
    return;
  }

  listaBackups.innerHTML = "Carregando backups...";
  modalRestaurar.showModal();

  const resposta = await apiGet("/api/backups");

  if (!resposta.sucesso || !resposta.backups || resposta.backups.length === 0) {
    listaBackups.innerHTML = "<p>Nenhum backup disponível.</p>";
    return;
  }

  listaBackups.innerHTML = resposta.backups.map(backup => `
    <div class="item-backup">
      <div>
        <strong>${escaparHtml(backup.nome)}</strong>
        <small>Observação: ${escaparHtml(backup.observacao || "Sem observação")}</small>
        <small>Modificado em: ${escaparHtml(backup.modificado_em)} | Tamanho: ${backup.tamanho} bytes</small>
      </div>
      <button type="button" onclick="restaurarBackup('${escaparAtributo(backup.nome)}')">Restaurar</button>
    </div>
  `).join("");
}

async function restaurarBackup(nomeArquivo) {
  const confirmar = confirm(
    `Tem certeza que deseja restaurar o backup abaixo?\n\n${nomeArquivo}\n\nOs dados atuais serão substituídos.`
  );

  if (!confirmar) return;

  const resposta = await apiPost("/api/backup/restaurar", { arquivo: nomeArquivo });

  if (resposta.sucesso) {
    modalRestaurar.close();
    mostrarToast("Backup restaurado com sucesso.");
    await carregarDados();
  } else {
    mostrarToast(resposta.mensagem || "Não foi possível restaurar o backup.");
  }
}


// ============================================================
// Exportação
// ============================================================

async function exportarHtml() {
  if (!administradorAutenticado) {
    mostrarToast("A exportação exige autenticação.");
    return;
  }

  const resposta = await apiPost("/api/exportar", {});

  if (resposta.sucesso) {
    mostrarToast(`Exportado com sucesso: ${resposta.caminho}`);

    const abrir = confirm(
      `Arquivo exportado com sucesso:\n\n${resposta.caminho}\n\nDeseja abrir o HTML exportado agora?`
    );

    if (abrir) {
      window.open("/" + resposta.caminho, "_blank");
    }
  } else {
    mostrarToast(resposta.mensagem || "Não foi possível exportar.");
  }
}


// ============================================================
// Eventos
// ============================================================

btnAbrirMenu.addEventListener("click", abrirMenu);
btnFecharMenu.addEventListener("click", fecharMenu);
overlay.addEventListener("click", fecharMenu);

btnEntrar.addEventListener("click", entrarComoAdministrador);
senhaAdmin.addEventListener("keydown", event => {
  if (event.key === "Enter") {
    entrarComoAdministrador();
  }
});

btnBloquear.addEventListener("click", bloquearSistema);

campoPesquisa.addEventListener("input", reiniciarPaginacao);

seletorItensPorPagina.addEventListener("change", () => {
  itensPorPagina = Number(seletorItensPorPagina.value) || 25;
  reiniciarPaginacao();
});

btnPaginaAnterior.addEventListener("click", () => {
  paginaAtual -= 1;
  renderizarTabela();
});

btnProximaPagina.addEventListener("click", () => {
  paginaAtual += 1;
  renderizarTabela();
});

btnNovoRegistro.addEventListener("click", abrirNovoRegistro);
if (btnCadastrarAssuntoTabela) {
  btnCadastrarAssuntoTabela.addEventListener("click", abrirNovoRegistro);
}
btnCancelarRegistro.addEventListener("click", () => modalRegistro.close());
btnSalvarRegistro.addEventListener("click", salvarRegistro);

btnBackup.addEventListener("click", abrirModalBackup);
btnCancelarBackup.addEventListener("click", () => modalBackup.close());
btnConfirmarBackup.addEventListener("click", confirmarBackup);

observacaoBackup.addEventListener("input", () => {
  contadorObservacaoBackup.textContent = `${observacaoBackup.value.length}/30 caracteres`;
});

btnRestaurar.addEventListener("click", abrirModalRestaurar);
btnFecharRestaurar.addEventListener("click", () => modalRestaurar.close());

btnExportar.addEventListener("click", exportarHtml);


// ============================================================
// Inicialização
// ============================================================

atualizarDataMenu();
atualizarEstadoAutenticacao();
carregarDados();
