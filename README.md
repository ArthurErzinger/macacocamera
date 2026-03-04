# macacocamera

Reconhecimento de gestos usando webcam, OpenCV e MediaPipe. O script abre a câmera e identifica dois gestos:

- "Dedo na Boca" (mostra uma imagem).
- "Dedo para Cima" (mostra outra imagem).

## Requisitos

- Python 3.9+ (recomendado)
- Webcam funcionando
- Dependências Python: `opencv-python`, `mediapipe`, `numpy`

## Instalação

Crie e ative um ambiente virtual (opcional, mas recomendado):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configurar imagens

No topo do arquivo `macacocamera.py`, altere os caminhos das imagens:

```python
img_x = cv2.resize(cv2.imread("/caminho/para/sua/imagem_x.jpg"), (400, 400))
img_y = cv2.resize(cv2.imread("/caminho/para/sua/imagem_y.jpg"), (400, 400))
```

Se preferir, coloque as imagens na pasta do projeto e use caminhos relativos.

## Execução

```bash
python macacocamera.py
```

Pressione `q` para sair.

## Problemas comuns

- **Câmera não encontrada**: verifique se a webcam está conectada e se nenhum outro app está usando a câmera.
- **Erro de biblioteca gráfica (Linux)**: em algumas distros pode ser necessário instalar pacotes do OpenCV/GL (ex.: `libgl1`).

