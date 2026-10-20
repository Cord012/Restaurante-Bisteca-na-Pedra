from datetime import date

from flask import Flask, jsonify, request, send_from_directory

from src.insumos import Insumo
from src.database.conexao import inicializar_banco
from src.database.insumos import (
    inserir_insumo,
    consultar_insumos,
    atualizar_insumo,
    deletar_insumo,
    contar_insumos,
    consultar_insumos_em_falta,
    consultar_insumos_estoque_baixo,
    consultar_insumos_a_vencer,
)

from src.database.movimentacoes import registrar_entrada, registrar_saida

app = Flask(__name__)

@app.route("/")
def pagina_inicial():
    return send_from_directory(".", "index.html")

@app.route("/css/<path:nome_arquivo>")
def arquivo_css(nome_arquivo):
    return send_from_directory("css", nome_arquivo)

@app.route("/js/<path:nome_arquivo>")
def arquivo_js(nome_arquivo):
    return send_from_directory("js", nome_arquivo)

@app.route("/pages/<path:nome_arquivo>")
def arquivo_pagina(nome_arquivo):
    return send_from_directory("pages", nome_arquivo)

def linha_para_dict(linha):
    return {
        "id": linha[0],
        "nome": linha[1],
        "quantidade": linha[2],
        "unidade": linha[3],
        "quantidade_minima": linha[4],
        "validade": linha[5],
    }

@app.route("/api/insumos", methods=["GET"])
def listar_insumos():
    linhas = consultar_insumos()
    return jsonify([linha_para_dict(linha) for linha in linhas])

@app.route("/api/resumo", methods=["GET"])
def resumo():
    vencimentos = []
    for linha in consultar_insumos_a_vencer():
        item = linha_para_dict(linha)
        validade = date.fromisoformat(item["validade"])
        item["dias"] = (validade - date.today()).days
        vencimentos.append(item)

    atencao = []

    for linha in consultar_insumos_em_falta():
        item = linha_para_dict(linha)
        item["situacao"] = "em_falta"
        atencao.append(item)
    
    for linha in consultar_insumos_estoque_baixo():
            item = linha_para_dict(linha)
            item["situacao"] = "estoque_baixo"
            atencao.append(item)
    
    return jsonify({
        "total": contar_insumos(),
        "em_falta": len(consultar_insumos_em_falta()),
        "a_vencer": len(consultar_insumos_a_vencer()),
        "vencimentos": vencimentos,
        "estoque_baixo": len(consultar_insumos_estoque_baixo()),
        "atencao": atencao,
    })


@app.route("/api/insumos", methods=["POST"])
def criar_insumo():
    dados = request.get_json()
    novo = Insumo(
        None,
        dados["nome"],
        dados["quantidade"],
        dados["unidade"],
        dados.get("quantidade_minima", 0),
        dados.get("validade"),
    )
    inserir_insumo(novo)
    return jsonify({"mensagem": "Insumo cadastrado com sucesso."}), 201

@app.route("/api/insumos/<int:insumo_id>", methods=["PUT"])
def editar_insumo(insumo_id):
    dados = request.get_json()
    editado = Insumo(
        insumo_id,
        dados["nome"],
        dados["quantidade"],
        dados["unidade"],
        dados.get("quantidade_minima", 0),
        dados.get("validade"),
    )
    if not atualizar_insumo(editado):
        return jsonify({"erro": "Insumo não encontrado."}), 404
    return jsonify({"mensagem": "Insumo atualizado com sucesso."})

@app.route("/api/insumos/<int:insumo_id>", methods=["DELETE"])
def remover_insumo(insumo_id):
    if not deletar_insumo(insumo_id):
        return jsonify({"erro": "Insumo não encontrado."}), 404
    return jsonify({"mensagem": "Insumo removido com sucesso."})

def ler_quantidade(dados):
    # devolve a quantidade se for um número maior que zero, senão None
    try:
        quantidade = float(dados["quantidade"])
    except (TypeError, KeyError, ValueError):
        return None
    return quantidade if quantidade > 0 else None

@app.route("/api/insumos/<int:insumo_id>/entrada", methods=["POST"])
def entrada_insumo(insumo_id):
    quantidade = ler_quantidade(request.get_json() or {})
    if quantidade is None:
        return jsonify({"erro": "Informe uma quantidade maior que zero."}), 400

    if registrar_entrada(insumo_id, quantidade) == "nao_encontrado":
        return jsonify({"erro": "Insumo não encontrado."}), 404
    return jsonify({"mensagem": "Entrada registrada com sucesso."}), 201

def saida_insumo(insumo_id):
    quantidade = ler_quantidade(request.get_json() or {})
    if quantidade is None:
        return jsonify({"erro": "Informe uma quantidade maior que zero."}), 400

    resultado = registrar_saida(insumo_id, quantidade)
    if resultado == "nao_encontrado":
        return jsonify({"erro": "Insumo não encontrado."}), 404
    if resultado == "estoque_insuficiente":
        return jsonify({"erro": "Estoque insuficiente."}), 409
    return jsonify({"mensagem": "Saída registrada com sucesso."}), 201

if __name__ == "__main__":
    inicializar_banco()
    app.run(debug=True)