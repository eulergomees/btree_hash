import csv
import logging
import argparse

class Page():
    def __init__(self, size, data=None):
        self._size = size
        self._data = []
        if data is not None:
            self._data = data

    @property
    def used_space(self):
        return get_size(self._data)

    def insert(self, record):
        if self.used_space + get_size(record) > self._size:
            raise ValueError("Page is full")
        self._data.append(record)

    def remove(self, key):
        self._data = [record for record in self._data if record[0] != key]

    @property
    def data(self):
        return self._data

    def set_data(self, data):
        self._data = data

    def search(self, key):
        return [record for record in self._data if record[0] == key]

    def __len__(self):
        return len(self._data)


class Index():
    def __init__(self, size, log, debbuging=False):
        self._size = size
        self.pages = [Page(size)]
        self._debbuging = debbuging
        self._config_log(log)
        self._debug("Creating index (page = %s)...", size)

    def insert(self, record):
        for page in self.pages:
            try:
                page.insert(record)
                return
            except ValueError:
                continue
        # Se nenhuma página puder armazenar o registro, cria uma nova página.
        new_page = Page(self._size)
        new_page.insert(record)
        self.pages.append(new_page)

    def remove(self, key):
        for page in self.pages:
            page.remove(key)

    def search(self, key):
        results = []
        for page in self.pages:
            results.extend(page.search(key))
        return results

    def _debug(self, msg, *args, **kwargs):
        self._log.debug(msg, *args, **kwargs)

    def _config_log(self, log):
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
        while True:
            print("\n=== MENU ===")
            print("Digite:")
            print(" + <chave> <valor> para inserir um registro")
            print(" - <chave> para remover um registro")
            print(" ? <chave> para buscar um registro")
            print(" q para sair")
            response = input("Opção: ").strip().lower()

            if response.startswith("+"):
                record = response[1:].split()
                if len(record) > 1:
                    record = (int(record[0]), record[1])
                    self.insert(record)
                    print("Registro inserido:", record)
                else:
                    print("Entrada inválida. Use: + <chave> <valor>")

            elif response.startswith("-"):
                key = response[1:].strip()
                if key.isdigit():
                    self.remove(int(key))
                    print("Registro com chave", key, "removido.")
                else:
                    print("Entrada inválida. Use: - <chave>")

            elif response.startswith("?"):
                key = response[1:].strip()
                if key.isdigit():
                    results = self.search(int(key))
                    if results:
                        print("Registro(s) encontrado(s):", results)
                    else:
                        print("Nenhum registro encontrado com a chave:", key)
                else:
                    print("Entrada inválida. Use: ? <chave>")

            elif response == "q":
                print("Saindo do menu...")
                break


def get_size(data):
    if isinstance(data, list):
        return sum(item.__sizeof__() for item in data)
    return data.__sizeof__()


def get_arguments(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-f", "--file", help='Input file (CSV)')
    parser.add_argument("-p", "--page-size", type=int, default=256)
    parser.add_argument("-d", "--debbuging", action="store_true", default=False, help="Debug")

    return parser.parse_args()

