from bplus_tree import BPlusTree

def main():
    # Criar uma árvore B+ com ordem 4
    tree = BPlusTree(order=4)

    # Inserir dados
    data = [(10, "A"), (20, "B"), (5, "C"), (6, "D"), (30, "E"), (25, "F")]
    for key, value in data:
        tree.insert(key, value)

    # Testar busca simples
    print("Busca por chave 10:", tree.search(10))  # Deve retornar "A"

    # Testar busca por intervalo
    print("Busca por intervalo (5 a 25):", tree.range_query(5, 25))
    # Deve retornar [(5, "C"), (6, "D"), (10, "A"), (20, "B"), (25, "F")]

    # Testar remoção
    tree.delete(20)
    print("Busca por intervalo após remoção (5 a 30):", tree.range_query(5, 30))
    # Deve retornar [(5, "C"), (6, "D"), (10, "A"), (25, "F"), (30, "E")]

if __name__ == "__main__":
    main()
