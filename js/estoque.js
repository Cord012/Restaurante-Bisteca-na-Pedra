// Busca os insumos no backend e preenche a tela de Estoque.

const DIAS_ALERTA_VENCIMENTO = 5;

let insumos = [];

function escapar(texto) {
  const div = document.createElement("div");
  div.textContent = texto;
  return div.innerHTML;
}

function formatarData(iso) {
  if (!iso) return "-";
  const [ano, mes, dia] = iso.split("-");
  return `${dia}/${mes}/${ano}`;
}

function calcularStatus(insumo) {
  if (insumo.quantidade <= 0) {
    return { classe: "vermelho", texto: "Em falta" };
  }
  if (insumo.quantidade <= insumo.quantidade_minima) {
    return { classe: "laranja", texto: "Baixo" };
  }
  if (insumo.validade) {
    const dias = Math.ceil((new Date(insumo.validade) - new Date()) / 86400000);
    if (dias <= DIAS_ALERTA_VENCIMENTO) {
      return { classe: "roxo", texto: "Próximo do vencimento" };
    }
  }
  return { classe: "verde", texto: "Normal" };
}

function renderizarInsumos(lista) {
  const caixa = document.getElementById("lista-insumos");

  if (lista.length === 0) {
    caixa.innerHTML = '<div class="linha-estoque"><div>Nenhum insumo encontrado.</div></div>';
    return;
  }

  let html = "";
  for (const insumo of lista) {
    const status = calcularStatus(insumo);
    html += `
      <div class="linha-estoque">
        <div>${escapar(insumo.nome)}</div>
        <div>${escapar(insumo.unidade)}</div>
        <div>${insumo.quantidade}</div>
        <div>${insumo.quantidade_minima}</div>
        <div>${formatarData(insumo.validade)}</div>
        <div><span class="badge ${status.classe}">${status.texto}</span></div>
        <div class="col-acoes">
          <span class="acao-icone-tabela editar" data-id="${insumo.id}"><svg viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 013 3L7 19l-4 1 1-4z"/></svg></span>
          <span class="acao-icone-tabela excluir" data-id="${insumo.id}"><svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a1 1 0 011-1h4a1 1 0 011 1v2"/></svg></span>
        </div>
      </div>`;
  }
  caixa.innerHTML = html;
}

function aplicarFiltro() {
  const termo = document.getElementById("busca-insumo").value.trim().toLowerCase();
  const filtrados = termo
    ? insumos.filter((insumo) => insumo.nome.toLowerCase().includes(termo))
    : insumos;
  renderizarInsumos(filtrados);
}

async function carregarInsumos() {
  try {
    const resposta = await fetch("/api/insumos");
    insumos = await resposta.json();
    aplicarFiltro();
  } catch (erro) {
    console.error("Não foi possível carregar os insumos:", erro);
  }
}

async function adicionarInsumo() {
  const nome = prompt("Nome do insumo:");
  if (!nome) return;
  const quantidade = Number(prompt("Quantidade:", "0"));
  const unidade = prompt("Unidade (kg, unidade, fardo...):", "kg");
  const quantidadeMinima = Number(prompt("Quantidade mínima:", "0"));
  const validade = prompt("Validade (AAAA-MM-DD, deixe vazio se não tiver):", "") || null;

  await fetch("/api/insumos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nome, quantidade, unidade, quantidade_minima: quantidadeMinima, validade }),
  });

  carregarInsumos();
}

async function editarInsumo(id) {
  const insumo = insumos.find((item) => item.id === Number(id));
  if (!insumo) return;

  const nome = prompt("Nome do insumo:", insumo.nome);
  if (!nome) return;
  const quantidade = Number(prompt("Quantidade:", insumo.quantidade));
  const unidade = prompt("Unidade:", insumo.unidade);
  const quantidadeMinima = Number(prompt("Quantidade mínima:", insumo.quantidade_minima));
  const validade = prompt("Validade (AAAA-MM-DD):", insumo.validade || "") || null;

  await fetch(`/api/insumos/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nome, quantidade, unidade, quantidade_minima: quantidadeMinima, validade }),
  });

  carregarInsumos();
}

async function excluirInsumo(id) {
  const insumo = insumos.find((item) => item.id === Number(id));
  if (!insumo || !confirm(`Remover "${insumo.nome}" do estoque?`)) return;

  await fetch(`/api/insumos/${id}`, { method: "DELETE" });
  carregarInsumos();
}

document.getElementById("botao-adicionar-insumo").addEventListener("click", adicionarInsumo);
document.getElementById("busca-insumo").addEventListener("input", aplicarFiltro);

document.getElementById("lista-insumos").addEventListener("click", (evento) => {
  const editar = evento.target.closest(".editar");
  const excluir = evento.target.closest(".excluir");
  if (editar) editarInsumo(editar.dataset.id);
  if (excluir) excluirInsumo(excluir.dataset.id);
});

carregarInsumos();
