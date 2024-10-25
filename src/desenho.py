import numpy as np
import cv2
from cvzone.HandTrackingModule import HandDetector

def conectar_pontos(matriz, inicio, fim):
    """
    Conecta dois pontos em uma matriz preenchendo o caminho com um valor 
    específico.
    """

    x1, y1 = inicio
    x2, y2 = fim
    
    # Algoritmo de interpolação linear (Bresenham)
    distancia = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    num_pontos = int(distancia)    

    x_vals = np.linspace(x1, x2, num=num_pontos, dtype=int)
    y_vals = np.linspace(y1, y2, num=num_pontos, dtype=int)
    
    # Preenche a linha entre os pontos com "255"
    matriz[y1, x1] = 255
    matriz[y2, x2] = 255
    for x, y in zip(x_vals, y_vals):
        matriz[y, x] = 255
    
    return matriz


def encontrar_extremos(matriz, valor_procurado):
    """
    Encontra as bordas da matriz para fins de recorte da imagem.
    """
    
    x_min, x_max = None, None
    y_min, y_max = None, None

    # Percorre a matriz para encontrar os extremos
    for i, linha in enumerate(matriz):
        indices = np.where(linha == valor_procurado)[0]  # Encontra os índices do valor_procurado na linha
        if len(indices) > 0:
            # Calcula o menor e maior índice de y para o valor procurado
            if x_min is None or indices[0] < x_min:
                x_min = indices[0]
            if x_max is None or indices[-1] > x_max:
                x_max = indices[-1]

            # Calcula o menor e maior valor de x onde o valor foi encontrado
            if y_min is None:
                y_min = i
            y_max = i

    return y_max, x_max, y_min, x_min

def enquadra_desenho(x_min, y_min, x_max, y_max, matriz, sub):
    """
    Coloca uma matriz menor no centro de uma matriz maior.
    """

    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if i >= x_min and i <= x_max and j >= y_min and j <= y_max:
                matriz[i][j] = sub[i - x_min][j - y_min]

    return matriz

def inicia_desenho():
    video = cv2.VideoCapture(0)
    video.set(3, 900)
    video.set(4, 900)

    # Inicializa o detector de mãos
    detector = HandDetector(maxHands=1)
    desenho_coord = []
    desenho_array = np.zeros((1120, 1120))  


    while True:
        check, img = video.read()

        if not check:
            print("Erro: Não foi possível capturar a imagem da câmera")
            break

        # Detecta e desenha as mãos
        resultado = detector.findHands(img, draw=True)
        hands, img = resultado  # Atualiza a variável `img` com o resultado do detector

        if hands:
            hand = hands[0]  # Obter os dados da primeira mão detectada
            lmlist = hand['lmList']  # Lista dos pontos de referência (landmarks) da mão
            dedos = detector.fingersUp(hand)  # Verifica quais dedos estão levantados
            dedosLev = dedos.count(1)  # Conta quantos dedos estão levantados

            if dedosLev == 1:
                x, y = lmlist[8][0], lmlist[8][1]  # Coordenadas do ponto do dedo indicador
                cv2.circle(img, (x, y), 10, (0, 0, 255), cv2.FILLED)
                desenho_coord.append((x, y))

            if dedosLev == 3:
                desenho_coord = []
                desenho_array = np.zeros((1120, 1120))

            if dedosLev == 5 and len(desenho_coord) > 0:
                break

            # Faz desenho com base nos pontos
            for id, ponto in enumerate(desenho_coord):
                x, y = ponto[0], ponto[1]
                if id >= 1:
                    ax, ay = desenho_coord[id - 1][0], desenho_coord[id - 1][1]
                    desenho_array = conectar_pontos(desenho_array, (x, y), (ax, ay)) # Conecta pontos formando um desenho continuo
                    if x != 0 and ax != 0:
                        cv2.line(img, (x, y), (ax, ay), (0, 0, 255), 20)

        # Para com Esc
        key = cv2.waitKey(1)
        if key == 27:
            break    

        imgFlip = cv2.flip(img, 1)
        cv2.imshow('Img', imgFlip)

    video.release()
    cv2.destroyAllWindows()

    return desenho_array

def ajusta_desenho(desenho_array):

    # Flipa desenho
    desenho_array = np.fliplr(desenho_array)

    # Encontra os extremos do desenho para recorte 
    y_max, x_max, y_min, x_min = encontrar_extremos(desenho_array, 255)

    # Pega recorte e adiciona um padding de 50 pixels
    padding = 50
    submatriz = desenho_array[y_min:y_max+1, x_min:x_max+1]
    desenho_enquadrado = np.pad(submatriz, pad_width=padding, mode='constant', constant_values=0)

    # Reduz a imagem para 28x28 pixels
    desenho_reduzido = cv2.resize(desenho_enquadrado, (28, 28), interpolation=cv2.INTER_AREA)

    # Aumenta relevancia de cada pixel no desenho
    for i in range(len(desenho_reduzido)):
        for j in range(len(desenho_reduzido[0])):
            value = desenho_reduzido[i][j] 
            if value**2 >= 255:
                desenho_reduzido[i][j] = 255
            else:
                desenho_reduzido[i][j] = value**2
    
    return desenho_reduzido