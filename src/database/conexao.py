import sqlite3
import os

CAMINHO_BANCO = os.path.join(os.path.dirname(__file__), "bisteca.db")
CAMINHO_SCHEMA = os.path.join(os.path.dirname(__file__), "schema.sql")


def conectar():
    conn = sqlite3.connect(CAMINHO_BANCO)
    return conn


def inicializar_banco():
    conn = conectar()
    with open(CAMINHO_SCHEMA, "r", encoding="utf-8") as arquivo:
        script_sql = arquivo.read()

    cursor = conn.cursor()
    cursor.executescript(script_sql)
    conn.commit()
    conn.close()
