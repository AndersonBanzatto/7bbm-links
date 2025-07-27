from flask import Flask, render_template, request, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

app = Flask(__name__)

# Escopos para o Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Pega a variável de ambiente com o JSON das credenciais
credentials_json = os.environ.get("GOOGLE_CREDENTIALS")

if not credentials_json:
    raise Exception("Variável de ambiente GOOGLE_CREDENTIALS não encontrada")

# Converte string JSON para dicionário
credentials_dict = json.loads(credentials_json)

# Cria as credenciais a partir do dicionário
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)

# Autoriza o gspread
client = gspread.authorize(creds)

# ID da planilha
SHEET_ID = "1JSpR61iLgxBjAJE2KNjSOQiXuAopfDIrBjDVwnYu2VU"
sheet = client.open_by_key(SHEET_ID).sheet1

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form.get("nome")
        url = request.form.get("url")
        if nome and url:
            sheet.append_row([nome, url])
            return redirect("/")
    registros = sheet.get_all_records()
    return render_template("index.html", registros=registros)

if __name__ == "__main__":
    app.run(debug=True)
