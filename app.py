from flask import Flask, jsonify, request, send_from_directory

from src.insumos import Insumo
from src.database.conexao import inicializar_banco
from src.database.insumos import (
    inserir_insumo,
    consultar_insumos,
    atualizar_insumo,
    deletar_insumo,
)

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

if __name__ == "__main__":
    inicializar_banco()
    app.run(debug=True)