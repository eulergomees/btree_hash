import logging
import argparse

class Page:
    def __init__(self, size, data=None):
        # Inicializa uma página com tamanho máximo e dados opcionais.
        self._size = size
        self._data = data if data else []

    @property
    def used_space(self):
        # Retorna o espaço usado na página.
        return get_size(self._data)

    def insert(self, record):
        # Insere um registro se houver espaço disponível.
        if self.used_space + get_size(record) > self._size:
            raise ValueError("Page is full")
        self._data.append(record)

    def remove(self, key):
        # Remove registros com a chave especificada.
        self._data = [record for record in self._data if record[0] != key]

    @property
    def data(self):
        # Retorna os dados armazenados na página.
        return self._data

    def set_data(self, data):
        # Substitui os dados da página.
        self._data = data

    def search(self, key):
        # Busca registros com a chave especificada.
        return [record for record in self._data if record[0] == key]

    def __len__(self):
        # Retorna o número de registros na página.
        return len(self._data)


class Index:
    def __init__(self, size, log, debbuging=False):
        # Inicializa o índice com páginas e configura o log.
        self._size = size
        self.pages = [Page(size)]
        self._debbuging = debbuging
        self._config_log(log)
        self._debug("Creating index (page = %s)...", size)

    def insert(self, record):
        # Insere um registro no índice, criando novas páginas, se necessário.
        for page in self.pages:
            try:
                page.insert(record)
                return
            except ValueError:
                continue
        new_page = Page(self._size)
        new_page.insert(record)
        self.pages.append(new_page)

    def remove(self, key):
        # Remove registros com a chave especificada em todas as páginas.
        for page in self.pages:
            page.remove(key)

    def search(self, key):
        # Busca registros com a chave especificada em todas as páginas.
        results = []
        for page in self.pages:
            results.extend(page.search(key))
        return results

    def _debug(self, msg, *args, **kwargs):
        # Registra mensagens de depuração.
        self._log.debug(msg, *args, **kwargs)

    def _config_log(self, log):
        # Configura logs para arquivo e console.
        self._log = logging.getLogger(log)
        log_formatter = logging.Formatter('%(levelname)s - %(message)s')

        file_handler = logging.FileHandler(log)
        file_handler.setFormatter(log_formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)

        self._log.addHandler(file_handler)
        self._log.addHandler(console_handler)
        self._log.setLevel(logging.DEBUG if self._debbuging else logging.INFO)

    def menu(self):
        # Apresenta o menu para inserir, buscar ou remover registros.
        while True:
            print(" + <key> <value> to insert a new record")
            print(" - <key> to remove an existing record")
            print(" ? <key> to search an existing record")
            print(" q to exit")
            response = input("Select: ").strip().lower()

            if response.startswith("+"):
                record = response[1:].split()
                if len(record) > 1:
                    record = (int(record[0]), record[1])
                    self.insert(record)
                    print("Record inserted:", record)
                else:
                    print("Unknow response. Use: + <key> <value>")

            elif response.startswith("-"):
                key = response[1:].strip()
                if key.isdigit():
                    self.remove(int(key))
                    print("Record with key", key, "removed.")
                else:
                    print("Unknow response. Use: - <key>")

            elif response.startswith("?"):
                key = response[1:].strip()
                if key.isdigit():
                    results = self.search(int(key))
                    if results:
                        print("Record found:", results)
                    else:
                        print("Not found:", key)
                else:
                    print("Unknow response")

            elif response == "debug":
                for i, page in enumerate(self.pages):
                    print(f"Page {i + 1}: {page.data}")

            elif response == "q":
                print("Exit")
                break


def get_size(data):
    # Calcula o tamanho em memória do dado ou lista de dados.
    if isinstance(data, list):
        return sum(item.__sizeof__() for item in data)
    return data.__sizeof__()


def get_arguments(description):
    # Configura e retorna argumentos da linha de comando.
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-f", "--file", help='Input file')
    parser.add_argument("-p", "--page-size", type=int, default=256)
    parser.add_argument("-d", "--debbuging", action="store_true", default=False, help="Debug")

    return parser.parse_args()
