import src.desenho as dsn
import os

def main():

    # Abre camera e processa o desenho
    dsn.inicia_desenho()
    
    # Remove arquivo temporario
    os.remove('imagem_cinza.png')

if __name__ == '__main__':
    main()