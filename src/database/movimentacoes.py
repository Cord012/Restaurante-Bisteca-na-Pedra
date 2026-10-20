from src.database.conexao import conectar


def registrar_entrada(insumo_id, quantidade):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT quantidade FROM insumos WHERE id = ?", (insumo_id,))
    linha = cursor.fetchone()
    if linha is None:
        conn.close()
        return "nao_encontrado"

    # soma ao estoque e guarda no histórico (as duas coisas no mesmo commit)
    cursor.execute(
        "UPDATE insumos SET quantidade = quantidade + ? WHERE id = ?",
        (quantidade, insumo_id)
    )
    cursor.execute(
        "INSERT INTO movimentacoes (insumo_id, tipo, quantidade) VALUES (?, 'entrada', ?)",
        (insumo_id, quantidade)
    )

    conn.commit()
    conn.close()
    return "ok"


def registrar_saida(insumo_id, quantidade, tipo="saida", motivo=None):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT quantidade FROM insumos WHERE id = ?", (insumo_id,))
    linha = cursor.fetchone()
    if linha is None:
        conn.close()
        return "nao_encontrado"

    # não deixa o estoque ficar negativo
    if linha[0] < quantidade:
        conn.close()
        return "estoque_insuficiente"

    cursor.execute(
        "UPDATE insumos SET quantidade = quantidade - ? WHERE id = ?",
        (quantidade, insumo_id)
    )
    cursor.execute(
        "INSERT INTO movimentacoes (insumo_id, tipo, quantidade, motivo) VALUES (?, ?, ?, ?)",
        (insumo_id, tipo, quantidade, motivo)
    )

    conn.commit()
    conn.close()
    return "ok"
