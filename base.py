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
    if isinstance(data, list):
        return sum(item.__sizeof__() for item in data)
    return data.__sizeof__()


def get_arguments(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-f", "--file", help='Input file')
    parser.add_argument("-p", "--page-size", type=int, default=256)
    parser.add_argument("-d", "--debbuging", action="store_true", default=False, help="Debug")

    return parser.parse_args()
