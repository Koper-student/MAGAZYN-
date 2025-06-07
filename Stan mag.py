import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QHBoxLayout, QListWidget, QMessageBox, QInputDialog
)


class Filament:
    def __init__(self, typ, producent, waga_bazowa):
        self.typ = typ
        self.producent = producent
        self.waga_bazowa = waga_bazowa
        self.waga_pozostala = waga_bazowa
        self.historia = []

    def zuzyj(self, model_nazwa, zuzyta_waga):
        if zuzyta_waga > self.waga_pozostala:
            return False
        self.waga_pozostala -= zuzyta_waga
        self.historia.append((model_nazwa, zuzyta_waga))
        return True

    def __str__(self):
        return f"{self.typ} ({self.producent}) - {self.waga_pozostala}/{self.waga_bazowa}g"


class FilamentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Magazyn Filamentu")
        self.setFixedSize(400, 500)

        self.filamenty = []

        # Layouty
        layout = QVBoxLayout()

        # Dodawanie filamentu
        self.typ_input = QLineEdit()
        self.typ_input.setPlaceholderText("Typ filamentu (np. PLA)")
        self.prod_input = QLineEdit()
        self.prod_input.setPlaceholderText("Producent")
        self.waga_input = QLineEdit()
        self.waga_input.setPlaceholderText("Waga bazowa (g)")

        layout.addWidget(QLabel("Dodaj nowy filament:"))
        layout.addWidget(self.typ_input)
        layout.addWidget(self.prod_input)
        layout.addWidget(self.waga_input)

        add_btn = QPushButton("Dodaj filament")
        add_btn.clicked.connect(self.dodaj_filament)
        layout.addWidget(add_btn)

        layout.addWidget(QLabel("Lista filamentów:"))
        self.lista = QListWidget()
        layout.addWidget(self.lista)

        # Przyciski akcji
        action_btn = QPushButton("Dodaj akcję (wydruk)")
        action_btn.clicked.connect(self.dodaj_akcje)
        layout.addWidget(action_btn)

        self.setLayout(layout)

    def dodaj_filament(self):
        typ = self.typ_input.text()
        prod = self.prod_input.text()
        try:
            waga = float(self.waga_input.text())
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Waga musi być liczbą!")
            return

        if not typ or not prod:
            QMessageBox.warning(self, "Błąd", "Wypełnij wszystkie pola.")
            return

        f = Filament(typ, prod, waga)
        self.filamenty.append(f)
        self.odswiez_liste()

        # Czyszczenie pól
        self.typ_input.clear()
        self.prod_input.clear()
        self.waga_input.clear()

    def odswiez_liste(self):
        self.lista.clear()
        for f in self.filamenty:
            self.lista.addItem(str(f))

    def dodaj_akcje(self):
        idx = self.lista.currentRow()
        if idx == -1:
            QMessageBox.warning(self, "Błąd", "Wybierz filament z listy.")
            return

        model, ok1 = QInputDialog.getText(self, "Model", "Nazwa modelu:")
        if not ok1 or not model:
            return

        zuzycie_str, ok2 = QInputDialog.getText(self, "Zużycie", "Zużycie filamentu (g):")
        if not ok2:
            return

        try:
            zuzycie = float(zuzycie_str)
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Zużycie musi być liczbą!")
            return

        filament = self.filamenty[idx]
        if not filament.zuzyj(model, zuzycie):
            QMessageBox.critical(self, "Błąd", f"Za mało filamentu! Pozostało: {filament.waga_pozostala}g")
            return

        QMessageBox.information(self, "Sukces", f"Zużyto {zuzycie}g na '{model}'.")
        self.odswiez_liste()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    okno = FilamentApp()
    okno.show()
    sys.exit(app.exec_())
