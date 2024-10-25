# Classificador-de-Numeros
Um classificador de numeros feitos com base em desenhos do usuario.

## Descrição

Este projeto é um classificador de números desenhados à mão usando visão computacional e redes neurais. A interface permite desenhar números no ar com o dedo, reconhecendo-os em tempo real e exibindo a classificação do número desenhado.

## Tecnologias Utilizadas

- **OpenCV e MediaPipe**: utilizados para a captura e processamento de vídeo, reconhecendo a posição dos dedos para desenhar ou apagar os números.
- **NumPy**: empregado no pré-processamento das imagens para preparar os desenhos, adaptando-os para a rede neural.
- **Convolutional Neural Network (CNN)**: uma rede neural convolucional, treinada com o dataset **MNIST**, realiza a classificação dos números desenhados.

## Instalação

### 1. Clonando o repositorio 
Clone o repositório:
```bash
git clone https://github.com/elton-aq/https://github.com/elton-aq/Classificador-de-Numeros.git
```

Entre no repositório:
```bash
cd Classificador-de-Numeros
```

### 2. Configurando o ambiente
Crie um ambiente virtual (opcional, mas recomendado): 
```bash
python -m venv venv
source venv/bin/activate  # ou 'venv\Scripts\activate' no Windows
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

## Modo de Uso

Para executar o script, utilize o seguinte comando:

```bash
python main.py
```

Após iniciar o script, a câmera do dispositivo será ativada. A partir daí, você terá três opções para interação:

- Levante **1 dedo (indicador)** para desenhar na tela.
- Levante **3 dedos** para apagar o desenho.
- Levante **5 dedos** para enviar a imagem para o classificador.

A saída com o número identificado será exibida no terminal. 

> [!NOTE]
> Note que você pode levantar 2 dedos para "pausar" o desenho, facilitando o uso.