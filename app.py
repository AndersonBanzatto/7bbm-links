from flask import Flask, render_template, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

app = Flask(__name__)

# Escopos da API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Credenciais
credentials_json = os.environ.get("GOOGLE_CREDENTIALS")
if not credentials_json:
    raise Exception("Variável de ambiente GOOGLE_CREDENTIALS não encontrada")

credentials_dict = json.loads(credentials_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(creds)

# Abrir planilha
SHEET_ID = "1JSpR61iLgxBjAJE2KNjSOQiXuAopfDIrBjDVwnYu2VU"
sheet = client.open_by_key(SHEET_ID).sheet1

# Página inicial
@app.route("/")
def index():
    return render_template("index.html")

# Obter todos os links
@app.route("/api/links", methods=["GET"])
def get_links():
    data = sheet.get_all_records()
    return jsonify(data)

# Salvar todos os links (substitui conteúdo da planilha)
@app.route("/api/links", methods=["POST"])
def save_links():
    data = request.get_json()

    # Validar dados
    if not isinstance(data, list):
        return "Formato inválido", 400

    # Limpar planilha e reescrever cabeçalho + dados
    sheet.clear()
    sheet.append_row(["titulo", "url"])
    for item in data:
        titulo = item.get("titulo", "")
        url = item.get("url", "")
        sheet.append_row([titulo, url])

    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True)

