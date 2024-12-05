class BPlusNode:
    """
    Classe base para um nó da árvore B+.
    Pode ser nó interno ou folha, dependendo da estrutura.
    """

    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []  # Chaves armazenadas no nó
        self.children = []  # Ponteiros para filhos (ou valores, se for nó folha)


class BPlusTree:
    """
    Implementação de uma árvore B+.
    """

    def __init__(self, order):
        """
        Inicializa uma árvore B+ com uma ordem específica.
        :param order: Número máximo de chaves em um nó.
        """
        self.root = BPlusNode(is_leaf=True)  # Árvore começa com um nó folha
        self.order = order

    def search(self, key):
        """
        Busca por uma chave na árvore.
        :param key: Chave a ser buscada.
        :return: Valor associado à chave, ou None se não encontrada.
        """
        current = self.root
        while not current.is_leaf:
            # Busca no nó interno: localiza o filho correto
            i = 0
            while i < len(current.keys) and key >= current.keys[i]:
                i += 1
            current = current.children[i]

        # Busca no nó folha
        for i, item in enumerate(current.keys):
            if item == key:
                return current.children[i]  # Valor correspondente
        return None

    def insert(self, key, value):
        """
        Insere uma chave e valor na árvore.
        :param key: Chave a ser inserida.
        :param value: Valor associado à chave.
        """
        root = self.root
        if len(root.keys) == self.order - 1:  # Nó raiz cheio
            new_root = BPlusNode()
            new_root.children.append(self.root)
            self.split_child(new_root, 0)
            self.root = new_root

        self._insert_non_full(self.root, key, value)

    def _insert_non_full(self, node, key, value):
        """
        Insere uma chave e valor em um nó que não está cheio.
        :param node: Nó onde será feita a inserção.
        :param key: Chave a ser inserida.
        :param value: Valor associado à chave.
        """
        if node.is_leaf:
            # Insere no nó folha
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            node.keys.insert(i, key)
            node.children.insert(i, value)
        else:
            # Insere no nó interno
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            child = node.children[i]
            if len(child.keys) == self.order - 1:
                self.split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

    def split_child(self, parent, index):
        """
        Divide um nó filho cheio em dois.
        :param parent: Nó pai.
        :param index: Índice do filho a ser dividido.
        """
        child = parent.children[index]
        new_child = BPlusNode(is_leaf=child.is_leaf)

        mid = len(child.keys) // 2
        parent.keys.insert(index, child.keys[mid])
        parent.children.insert(index + 1, new_child)

        new_child.keys = child.keys[mid + 1:]
        child.keys = child.keys[:mid]

        if not child.is_leaf:
            new_child.children = child.children[mid + 1:]
            child.children = child.children[:mid + 1]

    def delete(self, key):
        """
        Remove uma chave da árvore B+.
        :param key: Chave a ser removida.
        """
        if not self.root:
            return

        self._delete(self.root, key)

        # Ajusta a raiz, se necessário
        if len(self.root.keys) == 0:
            if not self.root.is_leaf:
                self.root = self.root.children[0]
            else:
                self.root = None

    def _delete(self, node, key):
        """
        Realiza a remoção de uma chave em um nó.
        :param node: Nó onde a remoção será feita.
        :param key: Chave a ser removida.
        """
        if node.is_leaf:
            # Remoção no nó folha
            if key in node.keys:
                index = node.keys.index(key)
                node.keys.pop(index)
                node.children.pop(index)
        else:
            # Remoção no nó interno
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1

            if i < len(node.keys) and node.keys[i] == key:
                # Chave encontrada no nó interno
                if len(node.children[i].keys) >= (self.order + 1) // 2:
                    # Substituir pelo predecessor
                    predecessor = self._get_predecessor(node.children[i])
                    node.keys[i] = predecessor
                    self._delete(node.children[i], predecessor)
                elif len(node.children[i + 1].keys) >= (self.order + 1) // 2:
                    # Substituir pelo sucessor
                    successor = self._get_successor(node.children[i + 1])
                    node.keys[i] = successor
                    self._delete(node.children[i + 1], successor)
                else:
                    # Combinar os dois filhos
                    self._merge_nodes(node, i)
                    self._delete(node.children[i], key)
            else:
                # Chave não encontrada, seguir no filho correto
                if len(node.children[i].keys) < (self.order + 1) // 2:
                    self._balance(node, i)
                self._delete(node.children[i], key)

    def _get_predecessor(self, node):
        """
        Obtém o predecessor (maior chave na subárvore esquerda).
        :param node: Nó de onde buscar o predecessor.
        :return: A chave predecessora.
        """
        current = node
        while not current.is_leaf:
            current = current.children[-1]
        return current.keys[-1]

    def _get_successor(self, node):
        """
        Obtém o sucessor (menor chave na subárvore direita).
        :param node: Nó de onde buscar o sucessor.
        :return: A chave sucessora.
        """
        current = node
        while not current.is_leaf:
            current = current.children[0]
        return current.keys[0]

    def _merge_nodes(self, parent, index):
        """
        Combina dois nós filhos em um único nó.
        :param parent: Nó pai.
        :param index: Índice do nó a ser combinado.
        """
        child = parent.children[index]
        sibling = parent.children[index + 1]

        # Mover a chave do pai para o filho
        if not child.is_leaf:
            child.keys.append(parent.keys[index])

        child.keys.extend(sibling.keys)
        child.children.extend(sibling.children)

        parent.keys.pop(index)
        parent.children.pop(index + 1)

    def _balance(self, parent, index):
        """
        Balanceia um nó filho, pegando uma chave de um irmão ou combinando.
        :param parent: Nó pai.
        :param index: Índice do filho a ser balanceado.
        """
        child = parent.children[index]

        if index > 0 and len(parent.children[index - 1].keys) > (self.order + 1) // 2:
            # Pegar chave do irmão esquerdo
            sibling = parent.children[index - 1]
            child.keys.insert(0, parent.keys[index - 1])
            if not sibling.is_leaf:
                child.children.insert(0, sibling.children.pop(-1))
            parent.keys[index - 1] = sibling.keys.pop(-1)
        elif index < len(parent.children) - 1 and len(parent.children[index + 1].keys) > (self.order + 1) // 2:
            # Pegar chave do irmão direito
            sibling = parent.children[index + 1]
            child.keys.append(parent.keys[index])
            if not sibling.is_leaf:
                child.children.append(sibling.children.pop(0))
            parent.keys[index] = sibling.keys.pop(0)
        else:
            # Combinar com irmão
            if index < len(parent.children) - 1:
                self._merge_nodes(parent, index)
            else:
                self._merge_nodes(parent, index - 1)

    def range_query(self, start_key, end_key):
        """
        Realiza uma busca por intervalo na árvore B+.
        :param start_key: Chave inicial do intervalo.
        :param end_key: Chave final do intervalo.
        :return: Lista de pares (chave, valor) dentro do intervalo.
        """
        result = []
        current = self.root

        # Navegar até o nó folha que contém o start_key
        while not current.is_leaf:
            i = 0
            while i < len(current.keys) and start_key >= current.keys[i]:
                i += 1
            current = current.children[i]

        # Percorrer os nós folha e coletar chaves no intervalo
        while current:
            for i, key in enumerate(current.keys):
                if start_key <= key <= end_key:
                    result.append((key, current.children[i]))
                elif key > end_key:
                    return result
            current = current.children[-1] if not current.is_leaf else None

        return result
