from base import Index

if __name__ == '__main__':
    page_size = 256 # Tamanho da pagina
    log_file = "index.log"
    debbuging = True

    index = Index(size= page_size, log=log_file, debbuging=debbuging)

    index.menu()
