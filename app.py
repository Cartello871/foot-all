from flask import Flask, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Авторизация
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("football-456507-5c6b1de03485.json", scope)
client = gspread.authorize(creds)

# Открытие таблицы
sheet = client.open("Рейтинг Игроков").sheet1

@app.route("/")
def index():
    data = sheet.get_all_records()
    # Автоматически считаем очки
    for player in data:
        player["Очки"] = player["Голы"] + player["Ассисты"] + player["Сейвы"] + player["Отборы"]
    return render_template("index.html", players=data)

if __name__ == "__main__":
    app.run(debug=True)
