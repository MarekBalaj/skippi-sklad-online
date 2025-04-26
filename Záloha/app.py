from flask import Flask, render_template, request, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

USERS = {
    "Viskup Peter": "1234",
    "Hollý Patrik": "1234",
    "Ostružlík Rastislav": "1234"
}

def nacitaj_data_z_google_sheetu():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'skippi-sklad-api-108809a10b38.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("Produkty Sklad").worksheet("databaza")
    data = sheet.get_all_records()
    return data

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        meno = request.form['meno']
        heslo = request.form['heslo']
        if meno in USERS and USERS[meno] == heslo:
            return redirect(url_for('menu', user=meno))
        return 'Nesprávne meno alebo heslo'
    return render_template('login.html')

@app.route('/menu')
def menu():
    meno = request.args.get('user')
    return render_template('menu.html', meno=meno)

@app.route('/prijem')
def prijem():
    return render_template('prijem.html')

@app.route('/prijem/qr')
def qr_prijem():
    return render_template('qr_prijem.html')

@app.route('/prijem/manual', methods=['GET', 'POST'])
def manual_prijem():
    produkty = nacitaj_data_z_google_sheetu()

    produkt_filter = ""
    filtered_produkty = produkty

    if request.method == 'POST':
        produkt_filter = request.form['produkt_filter'].lower()
        filtered_produkty = [
            produkt for produkt in produkty
            if produkt_filter in str(produkt['Názov produktu']).lower()
        ]

    return render_template('manual_prijem.html', produkty=filtered_produkty, produkt_filter=produkt_filter)

@app.route('/hľadanie', methods=['GET', 'POST'])
def hladanie():
    produkty = nacitaj_data_z_google_sheetu()

    produkt_filter = ""
    filtered_produkty = produkty

    if request.method == 'POST':
        produkt_filter = request.form['produkt_filter'].lower()
        filtered_produkty = [
            produkt for produkt in produkty
            if produkt_filter in str(produkt['Názov produktu']).lower()
        ]

    return render_template('manual_prijem.html', produkty=filtered_produkty, produkt_filter=produkt_filter)

@app.route('/aktualizuj_mnozstvo', methods=['POST'])
def aktualizuj_mnozstvo():
    nazov = request.form['nazov']
    farba = request.form['farba']
    nove_mnozstvo = request.form['mnozstvo']

    produkty = nacitaj_data_z_google_sheetu()
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'skippi-sklad-api-108809a10b38.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("Produkty Sklad").worksheet("databaza")

    for idx, produkt in enumerate(produkty):
        if produkt['Názov produktu'] == nazov and produkt['Farba / Dekor'] == farba:
            riadok = idx + 2  # +1 index, +1 hlavička
            stlpec = sheet.row_values(1).index('Množstvo') + 1
            sheet.update_cell(riadok, stlpec, nove_mnozstvo)
            break

    return redirect(url_for('manual_prijem', show=1))

@app.route('/vydaj')
def vydaj():
    return "<h3>Výdaj zo skladu – zatiaľ testovacia stránka</h3>"

@app.route('/kamiony')
def kamiony():
    return "<h3>Kamióny – zatiaľ testovacia stránka</h3>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
