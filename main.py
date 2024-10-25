import src.Dcnn as dcnn
import src.desenho as dsn
import cv2
import os

def main():

    # Abre camera e processa o desenho
    desenho = dsn.inicia_desenho()
    desenho_reduzido = dsn.ajusta_desenho(desenho)
    cv2.imwrite('imagem_cinza.png', desenho_reduzido)       

    # Identifica o numero
    print(f'O numero identificado foi: {dcnn.identificaNumero("imagem_cinza.png")}')

    # Remove arquivo temporario
    os.remove('imagem_cinza.png')

if __name__ == '__main__':
    main()