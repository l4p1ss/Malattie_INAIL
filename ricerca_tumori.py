from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QComboBox, QCheckBox, QGridLayout, QGroupBox, QScrollArea
import PyQt5.QtGui as QtGui
from PyQt5 import QtCore
import pandas as pd
import json
from grafici import GraficoTorta, GraficoIstogramma


class RicercaTumori(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        self.setLayout(grid)

        with open('./json/province.json', 'r') as p:
            self.province = json.load(p)
        with open('./json/province_nomi.json', 'r') as pn:
            self.province_nomi = json.load(pn)
        with open('./json/malattie.json', 'r') as m:
            self.malattie = json.load(m)
        with open('./json/tumori.json', 'r') as t:
            self.tumori = json.load(t)

        # Valori di default
        self.currentRegione = 'Italia'
        self.currentTumore = 'tutti i tumori'
        self.asbesto = False
        self.titolo = QLabel('', self)
        self.descrizione = QLabel('', self)

        self.regioni = []
        for (k, v) in self.province.items():
            self.regioni.append(k)

        # Scegli regione
        self.reg_list = QComboBox(self)
        self.reg_list.currentIndexChanged.connect(self.changedRegione)
        self.reg_list.addItem('Italia')
        for r in self.regioni:
            self.reg_list.addItem(r)

        # Scegli tumore
        self.tum_list = QComboBox(self)
        self.tum_list.currentIndexChanged.connect(self.changedTumore)
        self.tum_list.addItem('Tutti i tumori')
        for c, t in self.tumori.items():
            self.tum_list.addItem('%s - %s' % (c, t))

        self.tumori_nomi = []
        for (k, v) in self.tumori.items():
            self.tumori_nomi.append(v)

        # Asbesto correlazione
        self.asbestoBox = QCheckBox("Solo asbesto correlati", self)
        self.asbestoBox.stateChanged.connect(self.changedAsbesto)

        # Cerca
        self.cercaButton = QPushButton('Cerca', self)
        self.cercaButton.clicked.connect(self.cerca)

        f = QLabel('FILTRI DI RICERCA')
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        f.setFont(font)
        f.setAlignment(QtCore.Qt.AlignCenter)

        r = QLabel("Scegli regione:")
        r.setAlignment(QtCore.Qt.AlignCenter)

        t = QLabel("Scegli tumore:")
        t.setAlignment(QtCore.Qt.AlignCenter)

        groupbox1 = QGroupBox()
        groupbox1_layout = QGridLayout()
        groupbox1_layout.addWidget(f, 0, 0, 1, 4)
        groupbox1_layout.addWidget(r, 1, 0, 1, 1)
        groupbox1_layout.addWidget(self.reg_list, 1, 1, 1, 3)
        groupbox1_layout.addWidget(t, 2, 0, 1, 1)
        groupbox1_layout.addWidget(self.tum_list, 2, 1, 1, 3)
        groupbox1_layout.addWidget(self.asbestoBox, 3, 0, 1, 2)
        groupbox1_layout.addWidget(self.cercaButton, 3, 2, 1, 2)
        groupbox1.setLayout(groupbox1_layout)

        # Titolo
        self.titolo.setAlignment(QtCore.Qt.AlignLeft)
        self.titolo.setWordWrap(True)
        self.titolo.setMaximumHeight(60)
        font1 = QtGui.QFont()
        font1.setPointSize(17)
        font1.setBold(True)
        self.titolo.setFont(font1)

        # Descrizione
        self.descrizione.setAlignment(QtCore.Qt.AlignTop)
        self.descrizione.setWordWrap(True)
        font2 = QtGui.QFont()
        font2.setPointSize(14)
        self.descrizione.setFont(font2)
        self.descrizione.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        groupbox2 = QGroupBox()
        groupbox2_layout = QGridLayout()
        self.grafico1 = GraficoIstogramma(self)
        self.grafico2 = GraficoIstogramma(self)
        self.grafico3 = GraficoTorta(self)
        self.grafico4 = GraficoTorta(self)
        groupbox2_layout.addWidget(self.grafico1, 0, 0, 1, 2)
        groupbox2_layout.addWidget(self.grafico2, 1, 0, 1, 2)
        groupbox2_layout.addWidget(self.grafico3, 2, 0, 1, 1)
        groupbox2_layout.addWidget(self.grafico4, 2, 1, 1, 1)
        groupbox2.setLayout(groupbox2_layout)

        groupbox3 = QGroupBox()
        groupbox3_layout = QGridLayout()
        groupbox3_layout.addWidget(self.titolo, 0, 0, 1, 0)

        a = QScrollArea()
        a.setWidgetResizable(True)
        a.setWidget(self.descrizione)
        a.setStyleSheet('padding: 5px')

        groupbox3_layout.addWidget(a, 1, 0, -1, -1)
        groupbox3.setLayout(groupbox3_layout)

        grid.addWidget(groupbox1, 0, 0, 1, 1)
        grid.addWidget(groupbox2, 0, 1, 0, 4)
        grid.addWidget(groupbox3, 1, 0, 3, 1)

        self.cerca()

        self.show()

    def updateTitolo(self):
        t = self.currentTumore
        if t != 'tutti i tumori':
            t = '\'%s\'' % t
        r = 'in'
        if self.currentRegione == 'Marche':
            r = 'nelle'
        elif self.currentRegione == 'Lazio':
            r = 'nel'

        tot = len(self.risultati.axes[0])
        ris = 'risultati trovati'
        if tot == 1:
            ris = 'risultato trovato'
        self.titolo.setText('%s %s per %s %s %s' % (tot, ris, t, r, self.currentRegione))
        if self.asbesto:
            self.titolo.setText(self.titolo.text() + ' correlati con asbesto')
        self.titolo.setText(self.titolo.text() + ' accertati nell\'ultimo semestre')

    def updateDescrizione(self):

        self.descrizione.setText('')

        tot = len(self.risultati.axes[0])
        a = self.risultati['SedeInailCompetente']

        if tot > 0:
            # Top categorie tumori
            if self.currentTumore == 'tutti i tumori':
                self.descrizione.setText(self.descrizione.text() + 'PRINCIPALI CATEGORIE DI TUMORI ACCERTATI\n')
                tum = self.risultati['ICD10accertato']
                lbls = []; cds = []
                for val, cnt in tum.value_counts().head(10).items():
                    c = 'casi'
                    if cnt == 1:
                        c = 'caso'
                    p = str(round(cnt / tot * 100, 2)) + '%'
                    it = self.getTumoreDalCodice(val)
                    lbls.append(it)
                    cds.append(val)
                    self.descrizione.setText(self.descrizione.text() + '• %s (%s) (%s %s, %s)\n' % (it, val, cnt, c, p))
                self.descrizione.setText(self.descrizione.text() + '\n')
                self.grafico1.update_figure(tum, cds, 'Principali categorie di tumori accertati', n=7)

            if self.currentRegione == 'Italia':

                # Top regioni INAIL
                self.descrizione.setText(self.descrizione.text() + 'PRINCIPALI REGIONI\n')
                d = {}
                for r in self.regioni:
                    d[r] = 0
                for v, c in a.value_counts().items():
                    d[self.getRegioneDaCodiceProvincia(v)] += c
                s = sorted(d.items(), key=lambda x: x[1], reverse=True)
                reg = []
                for k, v in s[:10]:
                    if v > 0:
                        reg.append(k)
                        p = str(round(v / tot * 100, 2)) + '%'
                        c = 'casi'
                        if v == 1:
                            c = 'caso'
                        t = '• %s (%s %s, %s)\n' % (k, v, c, p)
                        self.descrizione.setText(self.descrizione.text() + t)
                self.descrizione.setText(self.descrizione.text() + '\n')
                self.grafico2.update_figure(a, reg, 'Principali regioni interessate')

            # Top province INAIL
            self.descrizione.setText(self.descrizione.text() + 'PRINCIPALI PROVINCE\n')
            pro = []
            for val, cnt in a.value_counts().head(10).items():
                val = self.province_nomi[str(val)]
                pro.append(val)
                c = 'casi'
                if cnt == 1:
                    c = 'caso'
                p = str(round(cnt / tot * 100, 2)) + '%'
                self.descrizione.setText(self.descrizione.text() + '• %s (%s %s, %s)\n' % (val, cnt, c, p))
            if self.currentRegione != 'Italia':
                self.grafico2.update_figure(a, pro, 'Principali province interessate')

            # Asbesto correlazione
            a = ['Si', 'No']
            if not self.asbesto:
                asb = self.risultati[self.risultati['MalattiaAsbestoCorrelata'] == 'S']
                self.descrizione.setText(self.descrizione.text() + '\nASBESTO CORRELATI\n')
                fav = len(asb.axes[0])
                rel = str(round(fav / tot * 100, 2)) + '%'
                c = 'casi'
                if fav == 1:
                    c = 'caso'
                if fav < tot/2:
                    a = ['No', 'Si']
                self.descrizione.setText(self.descrizione.text() + '• %s %s su %s (%s)\n' % (fav, c, tot, rel))
            self.grafico3.update_figure(self.risultati['MalattiaAsbestoCorrelata'], 'Correlazione con asbesto', a)

            # Demografia
            b = ['Uomo', 'Donna']
            mf = self.risultati[self.risultati['Genere'] == 'M']
            self.descrizione.setText(self.descrizione.text() + '\nDEMOGRAFIA\n')
            m = len(mf.axes[0])
            mp = str(round(m / tot * 100, 2)) + '%'
            fp = str(round((tot - m) / tot * 100, 2)) + '%'
            self.descrizione.setText(self.descrizione.text() + '• %s uomo (%s), %s donna (%s)\n' % (m, mp, tot - m, fp))
            if m < tot - m:
                b = ['Donna', 'Uomo']
            self.grafico4.update_figure(self.risultati['Genere'], 'Demografia', b)


            # Denunciati vs Accertati
            df = self.datiTotali
            df = df[(df['ICD10denunciato'] == 'J61') | (df['ICD10denunciato'].str.startswith('C')) | (df['ICD10denunciato'].str.startswith('D'))]
            if self.currentRegione != 'Italia':
                df = df[df['SedeInailCompetente'].isin(self.province[self.currentRegione])]
            if self.currentTumore != 'tutti i tumori':
                df = df[df['ICD10denunciato'].str.startswith(self.getCodiceTumoreDalNome(self.currentTumore))]
            if self.asbesto:
                df = df[df['MalattiaAsbestoCorrelata'] == 'S']
            d = df[df['ICD10denunciato'] != df['ICD10accertato']]
            t1 = len(df.axes[0])
            if t1 != 0:
                t = len(d.axes[0])
                self.descrizione.setText(self.descrizione.text() + '\nTUMORI DENUNCIATI E ACCERTATI\n')
                acc = str(round(t / t1 * 100, 2)) + '%'
                self.descrizione.setText(self.descrizione.text() + '• %s casi su %s (%s) denunciati non sono poi stati accertati\n' % (t, t1, acc))

                d = self.risultati[self.risultati['ICD10accertato'] == self.risultati['ICD10denunciato']]
                t = len(d.axes[0])
                acc = str(round(t / tot * 100, 2)) + '%'
                self.descrizione.setText(
                    self.descrizione.text() + '• %s dei casi accertati erano stati correttamente denunciati (%s)\n' % (t, acc))
                if tot - t > 0:
                    acc2 = str(round((tot - t) / tot * 100, 2)) + '%'
                    self.descrizione.setText(self.descrizione.text() + '• %s casi accertati pur avendo denunciato un\'altra patologia (o non avendo denunciato nulla) (%s)\n' % (tot - t, acc2))

    def changedRegione(self, i):
        if i == 0:
            self.currentRegione = 'Italia'
        else:
            self.currentRegione = self.regioni[i-1]

    def changedTumore(self, i):
        if i == 0:
            self.currentTumore = 'tutti i tumori'
        else:
            self.currentTumore = self.tumori_nomi[i-1]

    def changedAsbesto(self, i):
        if i == 0:
            self.asbesto = False
        else:
            self.asbesto = True

    def getTumoreDalCodice(self, codice):
        if codice == 'C45.0' or codice == 'C45.1':
            return self.tumori[codice]
        for key, value in self.tumori.items():
            if codice.startswith(key):
                return value

    def getCodiceTumoreDalNome(self, nome):
        for key, value in self.tumori.items():
            if value == nome:
                return key

    def getRegioneDaCodiceProvincia(self, codice):
        for key, value in self.province.items():
            if codice in value:
                return key

    def cerca(self):
        df = pd.read_csv('DatiSemestraliMalattieProfessionaliDataProtItalia.csv', ';')
        self.datiTotali = df
        df = df[(df['ICD10accertato'] == 'J61') | (df['ICD10accertato'].str.startswith('C')) | (df['ICD10accertato'].str.startswith('D')) | (df['ICD10accertato'] == 'J92')]
        if self.currentRegione != 'Italia':
            df = df[df['SedeInailCompetente'].isin(self.province[self.currentRegione])]
        if self.currentTumore != 'tutti i tumori':
            df = df[df['ICD10accertato'].str.startswith(self.getCodiceTumoreDalNome(self.currentTumore))]
        if self.asbesto:
            df = df[df['MalattiaAsbestoCorrelata'] == 'S']
        self.risultati = df

        self.update()

    def update(self):
        self.updateTitolo()
        self.updateDescrizione()
