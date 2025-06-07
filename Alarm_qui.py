import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QListWidget, QMessageBox, QInputDialog

app = QApplication(sys.argv)
okno = QWidget()
okno.setWindowTitle("Magazyn filamentu")
okno.setFixedSize(400, 400)

layout = QVBoxLayout()

# dane
filamenty = []

# pola tekstowe
typ_input = QLineEdit()
typ_input.setPlaceholderText("Typ (np. PLA)")
layout.addWidget(typ_input)

prod_input = QLineEdit()
prod_input.setPlaceholderText("Producent")
layout.addWidget(prod_input)

waga_input = QLineEdit()
waga_input.setPlaceholderText("Waga całkowita (g)")
layout.addWidget(waga_input)

# lista
lista = QListWidget()
layout.addWidget(lista)

# przycisk dodawania
def dodaj_filament():
    typ = typ_input.text()
    prod = prod_input.text()
    try:
        waga = float(waga_input.text())
    except:
        QMessageBox.warning(okno, "Błąd", "Podaj liczbę w polu wagi!")
        return

    if typ == "" or prod == "":
        QMessageBox.warning(okno, "Błąd", "Wpisz dane!")
        return

    filamenty.append([typ, prod, waga, waga])  # typ, prod, pozostało, oryginał
    pokaz_filamenty()
    typ_input.clear()
    prod_input.clear()
    waga_input.clear()

def pokaz_filamenty():
    lista.clear()
    for f in filamenty:
        lista.addItem(f"{f[0]} ({f[1]}) - {f[2]}/{f[3]}g")

btn_dodaj = QPushButton("Dodaj filament")
btn_dodaj.clicked.connect(dodaj_filament)
layout.addWidget(btn_dodaj)

# przycisk zużycia
def dodaj_zuzycie():
    i = lista.currentRow()
    if i == -1:
        QMessageBox.warning(okno, "Błąd", "Nie wybrałeś filamentu!")
        return

    model, ok = QInputDialog.getText(okno, "Model", "Nazwa modelu:")
    if not ok or model == "":
        return

    zuzycie, ok2 = QInputDialog.getText(okno, "Zużycie", "Ile g zużyto:")
    if not ok2:
        return

    try:
        ile = float(zuzycie)
    except:
        QMessageBox.warning(okno, "Błąd", "Zużycie ma być liczbą!")
        return

    if ile > filamenty[i][2]:
        QMessageBox.critical(okno, "Błąd", "Za mało filamentu!")
        return

    filamenty[i][2] -= ile
    pokaz_filamenty()
    QMessageBox.information(okno, "OK", f"Zużyto {ile}g na {model}")

btn_akcja = QPushButton("Zużyj filament")
btn_akcja.clicked.connect(dodaj_zuzycie)
layout.addWidget(btn_akcja)

# ustaw layout i start
okno.setLayout(layout)
okno.show()
sys.exit(app.exec_())
