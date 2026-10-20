// Busca o resumo no backend e preenche a tela de Início.

// Evita que um nome com caracteres como < ou > quebre o HTML.
function escapar(texto) {
  const div = document.createElement("div");
  div.textContent = texto;
  return div.innerHTML;
}

function preencherCards(resumo) {
  document.getElementById("num-em-falta").textContent = resumo.em_falta;
  document.getElementById("num-estoque-baixo").textContent = resumo.estoque_baixo;
  document.getElementById("num-a-vencer").textContent = resumo.a_vencer;
  document.getElementById("num-total").textContent = resumo.total;
}

function preencherAtencao(lista) {
  const caixa = document.getElementById("lista-atencao");

  if (lista.length === 0) {
    caixa.innerHTML = '<div class="linha"><div>Nenhum produto precisa de atenção.</div></div>';
    return;
  }

  let html = "";
  for (const item of lista) {
    const emFalta = item.situacao === "em_falta";
    const classeLinha = emFalta ? "linha critico" : "linha";
    const classeBadge = emFalta ? "badge vermelho" : "badge laranja";
    const textoBadge = emFalta ? "Em falta" : "Estoque baixo";

    html += `
      <div class="${classeLinha}">
        <div>${escapar(item.nome)} (${escapar(item.unidade)})</div>
        <div>${item.quantidade}</div>
        <div class="${classeBadge}">${textoBadge}</div>
      </div>`;
  }
  caixa.innerHTML = html;
}

function textoDias(dias) {
  if (dias === 0) return "Vence hoje";
  if (dias === 1) return "Vence em 1 dia";
  return `Vence em ${dias} dias`;
}

function corDoPonto(dias) {
  if (dias <= 1) return "vermelho";
  if (dias <= 3) return "laranja";
  return "verde";
}

function preencherVencimentos(lista) {
  const caixa = document.getElementById("lista-vencimentos");

  if (lista.length === 0) {
    caixa.innerHTML = '<div class="vencimento"><div class="nome">Nada perto de vencer.</div></div>';
    return;
  }

  let html = "";
  for (const item of lista) {
    html += `
      <div class="vencimento">
        <div class="nome">
          <div class="ponto ${corDoPonto(item.dias)}"></div>
          ${escapar(item.nome)}
        </div>
        <div class="dias">${textoDias(item.dias)}</div>
      </div>`;
  }
  caixa.innerHTML = html;
}

async function carregarResumo() {
  try {
    const resposta = await fetch("/api/resumo");
    const resumo = await resposta.json();

    preencherCards(resumo);
    preencherAtencao(resumo.atencao);
    preencherVencimentos(resumo.vencimentos);
  } catch (erro) {
    console.error("Não foi possível carregar o resumo:", erro);
  }
}

carregarResumo();
