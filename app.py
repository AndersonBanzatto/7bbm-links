from flask import Flask, render_template, request, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Autenticação com a API do Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Abrir a planilha pelo ID
SHEET_ID = "1JSpR61iLgxBjAJE2KNjSOQiXuAopfDIrBjDVwnYu2VU"
sheet = client.open_by_key(SHEET_ID).sheet1  # Primeira aba da planilha

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
