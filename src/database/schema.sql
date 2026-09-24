-- Estrutura do banco de dados do Bisteca na Pedra

CREATE TABLE IF NOT EXISTS insumos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    quantidade REAL NOT NULL DEFAULT 0,
    unidade TEXT NOT NULL DEFAULT 'un',
    quantidade_minima REAL NOT NULL DEFAULT 0,
    validade DATE
);
