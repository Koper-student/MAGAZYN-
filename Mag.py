import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QListWidget, QMessageBox, QInputDialog

app = QApplication(sys.argv)
okno = QWidget()
okno.setWindowTitle("Magazyn filamentu")
okno.setFixedSize(400, 500)

layout = QVBoxLayout()

filamenty = []

typ_input = QLineEdit()
typ_input.setPlaceholderText("Typ (np. PLA)")
layout.addWidget(typ_input)

prod_input = QLineEdit()
prod_input.setPlaceholderText("Producent")
layout.addWidget(prod_input)

waga_input = QLineEdit()
waga_input.setPlaceholderText("Waga całkowita (g)")
layout.addWidget(waga_input)

lista = QListWidget()
layout.addWidget(lista)

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

    filamenty.append([typ, prod, waga, waga, []])  # + historia
    pokaz_filamenty()
    typ_input.clear()
    prod_input.clear()
    waga_input.clear()

def pokaz_filamenty():
    lista.clear()
    for f in filamenty:
        lista.addItem(f"{f[0]} ({f[1]}) - {f[2]}/{f[3]}g")

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
    filamenty[i][4].append((model, ile))  # dopisujemy do historii
    pokaz_filamenty()
    QMessageBox.information(okno, "OK", f"Zużyto {ile}g na {model}")

def pokaz_historie():
    i = lista.currentRow()
    if i == -1:
        QMessageBox.warning(okno, "Błąd", "Nie wybrałeś filamentu!")
        return

    historia = filamenty[i][4]
    if not historia:
        QMessageBox.information(okno, "Historia", "Brak historii zużyć.")
        return

    tekst = ""
    for wpis in historia:
        tekst += f"• {wpis[0]} – {wpis[1]}g\n"

    QMessageBox.information(okno, "Historia zużycia", tekst)

btn_dodaj = QPushButton("Dodaj filament")
btn_dodaj.clicked.connect(dodaj_filament)
layout.addWidget(btn_dodaj)

btn_akcja = QPushButton("Zużyj filament")
btn_akcja.clicked.connect(dodaj_zuzycie)
layout.addWidget(btn_akcja)

btn_historia = QPushButton("Pokaż historię zużycia")
btn_historia.clicked.connect(pokaz_historie)
layout.addWidget(btn_historia)

okno.setLayout(layout)
okno.show()
sys.exit(app.exec_())
