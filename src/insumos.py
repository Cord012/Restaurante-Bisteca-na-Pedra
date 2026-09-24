class Insumo:
    def __init__(self, id, nome, quantidade, unidade, quantidade_minima, validade):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.unidade = unidade
        self.quantidade_minima = quantidade_minima
        self.validade = validade

if __name__ == "__main__":
    item1 = Insumo(1, "Arroz", 2, "Kg", 1, "2026-12-20")
    print(item1.nome)
