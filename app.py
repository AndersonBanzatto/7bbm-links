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
SHEET_ID = "1J5pR6iILpXBjAJE2KNjSQQiXuAopfDIrBjDVmYu2VU"
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

@app.route("/delete/<int:index>", methods=["POST"])
def delete_link(index):
    try:
        # gspread rows are 1-indexed, and header is row 1, so data starts from row 2
        # The HTML loop.index0 is 0-indexed, so we need to add 2 to get the correct row number
        sheet.delete_rows(index + 2)
        return '', 204  # No Content
    except Exception as e:
        print(f"Erro ao excluir link: {e}")
        return 'Erro ao excluir o link.', 500

if __name__ == "__main__":
    app.run(debug=True)

