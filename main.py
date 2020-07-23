import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QVBoxLayout
from ricerca_tumori import RicercaTumori
from malattie_frequenti import MalattieFrequenti


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Malattie professionali')

        self.resize(1100, 750)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.ricercaTumori = RicercaTumori(self)
        self.malattieFrequenti = MalattieFrequenti(self)

        self.tabs.addTab(self.ricercaTumori, "Ricerca tumori e asbesto")
        self.tabs.addTab(self.malattieFrequenti, "Malattie frequenti")

        self.layout.addWidget(self.tabs)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
