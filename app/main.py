import logging
import os
from flask import Flask, request, jsonify, Response
import requests
app = Flask(__name__)

# Configure logging at INFO level
logging.basicConfig(level=logging.INFO)

API_TRANSFER_PORT = int(os.getenv('PORT', '80'))
###########################################
API_WHISPER_URL = os.getenv('API_WHISPER_URL', '192.168.15.4')
API_WHISPER_PORT =  os.getenv('API_WHISPER_PORT', '9000')
API_WHISPER_URL_COMPLETE = 'http://' + API_WHISPER_URL + ':' + API_WHISPER_PORT + '/asr'
API_WHISPER_TIMEOUT =  int(os.getenv('API_WHISPER_TIMEOUT', '30000'))
###########################################

@app.route("/audio/transcriptions", methods=["POST"])
def transcribe():
    # Log da requisição recebida para depuração
    logging.info(f"Headers: {request.headers}")
    logging.info(f"Form data: {request.form}")
    logging.info(f"Files: {request.files}")

    # Verifica se o arquivo foi enviado na requisição
    file = request.files.get('file')
    if file is None:
        logging.info("Erro: Arquivo de áudio não encontrado na requisição")
        return jsonify({"error": "Arquivo de áudio não encontrado na requisição"}), 400

    # Define o modelo padrão (pode ser alterado conforme necessário)
    model = request.form.get('model', 'medium')  # Usa "medium" como padrão, se não for especificado

    # Envia a requisição para o Whisper com o nome de campo correto
    try:
        response = requests.post(
            API_WHISPER_URL_COMPLETE,
            files={'audio_file': (file.filename, file, 'audio/wav')},
            data={'model': model},
            timeout=API_WHISPER_TIMEOUT
        )

        logging.info(f"Whisper Response Status Code: {response.status_code}")
        logging.info(f"Whisper Response Content: {response.text}")
        
        # Verifica o tipo de conteúdo da resposta do Whisper
        if response.headers.get("Content-Type") == "application/json":
            # Se for JSON, retorna como JSON
            return jsonify(response.json()), response.status_code
        else:
            # Caso contrário, encapsula o texto simples em um JSON com a chave "text"
            return jsonify({"text": response.text}), response.status_code

    except requests.exceptions.RequestException as e:
        # Lida com qualquer erro de requisição e retorna uma mensagem de erro apropriada
        logging.info(f"Erro na requisição para o Whisper: {e}")
        return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=API_TRANSFER_PORT)
