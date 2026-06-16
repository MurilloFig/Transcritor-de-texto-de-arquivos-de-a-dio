# Audio Transcriber PT/EN - Flet + Whisper

Aplicação local feita em Python com interface em Flet para transcrever arquivos de áudio em português e inglês.

## Recursos

- Interface gráfica com Flet
- Upload/seleção de arquivo de áudio
- Detecção automática de idioma
- Suporte a português e inglês
- Modelo Whisper otimizado com faster-whisper
- Geração de arquivo `.txt` com a transcrição
- Projeto pronto para abrir no VS Code

## Formatos suportados

- `.mp3`
- `.wav`
- `.m4a`
- `.ogg`
- `.flac`
- `.mp4`
- `.webm`

## Requisitos

Você precisa ter:

- Python 3.10 ou superior
- VS Code
- FFmpeg instalado

No Linux/Kali/Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y ffmpeg
```

No Windows, instale o FFmpeg e adicione ao PATH.

## Como rodar no VS Code

Abra a pasta do projeto no VS Code e rode:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/app.py
```

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src\app.py
```

## Sobre o modelo

Por padrão, o projeto usa o modelo `medium`.

Você pode alterar no arquivo:

```python
MODEL_SIZE = "medium"
```

Opções comuns:

- `small`: mais leve
- `medium`: equilíbrio entre qualidade e desempenho
- `large-v3`: melhor qualidade, porém mais pesado

## Observação

Na primeira execução, o modelo será baixado automaticamente. Isso pode demorar dependendo da internet e do tamanho do modelo escolhido.
