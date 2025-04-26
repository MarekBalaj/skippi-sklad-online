import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'skippi-sklad-api-108809a10b38.json', scope)
client = gspread.authorize(creds)

spreadsheet = client.open("Produkty Sklad")
worksheet = spreadsheet.worksheet("databaza")

hlavicka = [
    "Čiarový kód", "EAN", "Kód produktu", "Názov produktu", "Farba / Dekor",
    "Rozmery", "Rozmery balenia", "Váha (kg)", "Množstvo", "Kamión", "Dátum", "Sklad"
]

worksheet.insert_row(hlavicka, index=1)
