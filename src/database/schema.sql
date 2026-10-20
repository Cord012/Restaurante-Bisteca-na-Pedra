-- Estrutura do banco de dados do Bisteca na Pedra

CREATE TABLE IF NOT EXISTS insumos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    quantidade REAL NOT NULL DEFAULT 0,
    unidade TEXT NOT NULL DEFAULT 'un',
    quantidade_minima REAL NOT NULL DEFAULT 0,
    validade DATE
);

-- Histórico de entradas, saídas e perdas de cada insumo
CREATE TABLE IF NOT EXISTS movimentacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    insumo_id INTEGER NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('entrada', 'saida', 'perda')),
    quantidade REAL NOT NULL,
    motivo TEXT,
    data DATE NOT NULL DEFAULT (date('now', 'localtime')),
    FOREIGN KEY (insumo_id) REFERENCES insumos (id)
);
