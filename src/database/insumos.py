from src.database.conexao import conectar
from src.insumos import Insumo


def inserir_insumo(insumo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO insumos (nome, quantidade, unidade, quantidade_minima, validade) VALUES (?, ?, ?, ?, ?)",
        (insumo.nome, insumo.quantidade, insumo.unidade, insumo.quantidade_minima, insumo.validade)
    )

    conn.commit()
    conn.close()

def consultar_insumos():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM insumos")
    
    resultado = cursor.fetchall()
    conn.close()
    return resultado
