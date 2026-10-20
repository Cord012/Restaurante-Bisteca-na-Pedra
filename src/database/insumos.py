from src.database.conexao import conectar
from src.insumos import Insumo

DIAS_ALERTA_VENCIMENTO = 5

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

def buscar_insumo_por_id(insumo_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM insumos WHERE id = ?", (insumo_id,))

    resultado = cursor.fetchone()
    conn.close()
    return resultado

def atualizar_insumo(insumo):
    if buscar_insumo_por_id(insumo.id) is None:
        print(f"Insumo com id {insumo.id} não encontrado.")
        return False

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE insumos SET nome = ?, quantidade = ?, unidade = ?, quantidade_minima = ?, validade = ? WHERE id = ?",
        (insumo.nome, insumo.quantidade, insumo.unidade, insumo.quantidade_minima, insumo.validade, insumo.id)
    )

    conn.commit()
    conn.close()
    return True

def deletar_insumo(insumo_id):
    if buscar_insumo_por_id(insumo_id) is None:
        print(f"Insumo com id {insumo_id} não encontrado.")
        return False

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM insumos WHERE id = ?", (insumo_id,))

    conn.commit()
    conn.close()
    return True

def contar_insumos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM insumos")

    resultado = cursor.fetchone()[0]
    conn.close()
    return resultado

def consultar_insumos_em_falta():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM insumos WHERE quantidade <= 0")

    resultado = cursor.fetchall()
    conn.close()
    return resultado

def consultar_insumos_estoque_baixo():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM insumos WHERE quantidade > 0 AND quantidade <= quantidade_minima")

    resultado = cursor.fetchall()
    conn.close()
    return resultado

def consultar_insumos_a_vencer():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM insumos WHERE validade IS NOT NULL AND validade BETWEEN date('now') AND date('now', '+{DIAS_ALERTA_VENCIMENTO} days')")

    resultado = cursor.fetchall()
    conn.close()
    return resultado


