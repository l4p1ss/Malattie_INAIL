from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QComboBox, QGridLayout, QGroupBox, QScrollArea
import PyQt5.QtGui as QtGui
from PyQt5 import QtCore
import pandas as pd
from grafici import GraficoTorta, GraficoIstogramma
import json


class MalattieFrequenti(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):

        with open('./json/province.json', 'r') as p:
            self.province = json.load(p)
        with open('./json/province_nomi.json', 'r') as pn:
            self.province_nomi = json.load(pn)
        with open('./json/malattie.json', 'r') as m:
            self.malattie = json.load(m)
        with open('./json/agenti_causali.json', 'r') as a:
            self.agenti_causali = json.load(a)

        grid = QGridLayout()
        self.setLayout(grid)

        # Valori di default
        self.currentRegione = 'Italia'
        self.currentMalattia = 'tutte le malattie'
        self.currentAgente = 'Tutti gli agenti causali'
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

        # Scegli malattia
        self.mal_list = QComboBox(self)
        self.mal_list.setMaximumWidth(400)
        self.mal_list.currentIndexChanged.connect(self.changedMalattia)
        self.mal_list.addItem('Tutte le malattie')
        for c, t in self.malattie.items():
            self.mal_list.addItem('%s - %s' % (c, t))

        self.malattie_nomi = []
        for (k, v) in self.malattie.items():
            self.malattie_nomi.append(v)


        # Scegli Agente Causale
        self.ag_list = QComboBox(self)
        self.ag_list.setMaximumWidth(400)
        self.ag_list.currentIndexChanged.connect(self.changedAgente)
        self.ag_list.addItem('Tutti gli agenti causali')
        for c, t in self.agenti_causali.items():
            self.ag_list.addItem('%s - %s' % (c, t))

        self.agenti_nomi = []
        for (k, v) in self.agenti_causali.items():
            self.agenti_nomi.append(v)



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

        t = QLabel("Scegli malattia:")
        t.setAlignment(QtCore.Qt.AlignCenter)

        a = QLabel("Scegli agente:")
        a.setAlignment(QtCore.Qt.AlignCenter)

        groupbox1 = QGroupBox()
        groupbox1_layout = QGridLayout()
        groupbox1_layout.addWidget(f, 0, 0, 1, 4)
        groupbox1_layout.addWidget(r, 1, 0, 1, 1)
        groupbox1_layout.addWidget(self.reg_list, 1, 1, 1, 3)
        groupbox1_layout.addWidget(t, 2, 0, 1, 1)
        groupbox1_layout.addWidget(self.mal_list, 2, 1, 1, 3)
        groupbox1_layout.addWidget(a, 3, 0, 1, 1)
        groupbox1_layout.addWidget(self.ag_list, 3, 1, 1, 3)
        groupbox1_layout.addWidget(self.cercaButton, 4, 2, 1, 2)
        groupbox1.setLayout(groupbox1_layout)

        # Titolo
        self.titolo.setAlignment(QtCore.Qt.AlignLeft)
        self.titolo.setWordWrap(True)
        self.titolo.setMaximumHeight(80)
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
        t = self.currentMalattia
        if t != 'tutte le malattie':
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
        if self.currentAgente != 'Tutti gli agenti causali':
            self.titolo.setText(self.titolo.text() + ' correlate con agente ' + self.getCodiceAgenteDalNome(self.currentAgente))
        self.titolo.setText(self.titolo.text() + ' accertate nell\'ultimo semestre')

    def updateDescrizione(self):

        self.descrizione.setText('')

        tot = len(self.risultati.axes[0])
        a = self.risultati['SedeInailCompetente']

        if tot > 0:
            # Top categorie malattie
            if self.currentMalattia == 'tutte le malattie':
                self.descrizione.setText(self.descrizione.text() + 'PRINCIPALI CATEGORIE DI MALATTIE\n')
                tum = self.risultati['ICD10accertato']
                lbls = []; cds = [];
                for val, cnt in tum.value_counts().head(10).items():
                    c = 'casi'
                    if cnt == 1:
                        c = 'caso'
                    p = str(round(cnt / tot * 100, 2)) + '%'
                    it = self.getMalattiaDalCodice(val)
                    lbls.append(it)
                    cds.append(val)
                    self.descrizione.setText(self.descrizione.text() + '• %s (%s) (%s %s, %s)\n' % (it, val, cnt, c, p))
                self.descrizione.setText(self.descrizione.text() + '\n')
                self.grafico1.update_figure(tum, cds, 'Malattie più frequenti', n=7)

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

            # Categorie
            i = len(self.risultati[self.risultati['Gestione'] == 'I'].axes[0])
            a = len(self.risultati[self.risultati['Gestione'] == 'A'].axes[0])
            s = len(self.risultati[self.risultati['Gestione'] == 'S'].axes[0])
            self.descrizione.setText(self.descrizione.text() + '\nCATEGORIE\n')
            ip = str(round(i / tot * 100, 2)) + '%'
            ap = str(round(a / tot * 100, 2)) + '%'
            sp = str(round(s / tot * 100, 2)) + '%'
            s = '• %s relativi all\'industria (%s)\n• %s relativi all\'agricoltura (%s)\n• %s relativi agli enti pubblici (%s)\n' % (i, ip, a, ap, s, sp)
            self.descrizione.setText(self.descrizione.text() + s)
            self.grafico3.update_figure(self.risultati['Gestione'], 'Categorie', ['I', 'A', 'S'])

            # Codici agenti
            mf = self.risultati['AgenteCausale']
            self.descrizione.setText(self.descrizione.text() + '\nPRINCIPALI AGENTI CAUSALI\n')
            for val, cnt in mf.value_counts().head(10).items():
                p = str(round(cnt / tot * 100, 2)) + '%'
                self.descrizione.setText(self.descrizione.text() + '• %s (%s casi, %s)\n' % (self.agenti_causali.get(val, val), cnt, p))

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

    def changedRegione(self, i):
        if i == 0:
            self.currentRegione = 'Italia'
        else:
            self.currentRegione = self.regioni[i-1]

    def changedMalattia(self, i):
        if i == 0:
            self.currentMalattia = 'tutte le malattie'
        else:
            self.currentMalattia = self.malattie_nomi[i-1]

    def changedAgente(self, i):
        if i == 0:
            self.currentAgente = 'Tutti gli agenti causali'
        else:
            self.currentAgente = self.agenti_nomi[i-1]

    def getMalattiaDalCodice(self, codice):
        for key, value in self.malattie.items():
            if codice.startswith(key):
                return value

    def getCodiceMalattiaDalNome(self, nome):
        for key, value in self.malattie.items():
            if value == nome:
                return key

    def getRegioneDaCodiceProvincia(self, codice):
        for key, value in self.province.items():
            if codice in value:
                return key

    def getCodiceAgenteDalNome(self, nome):
        for key, value in self.agenti_causali.items():
            if value == nome:
                return key

    def cerca(self):
        df = pd.read_csv('DatiSemestraliMalattieProfessionaliDataProtItalia.csv', ';')
        if self.currentRegione != 'Italia':
            df = df[df['SedeInailCompetente'].isin(self.province[self.currentRegione])]
        if self.currentMalattia != 'tutte le malattie':
            df = df[df['ICD10accertato'].str.startswith(self.getCodiceMalattiaDalNome(self.currentMalattia))]
        if self.currentAgente != 'Tutti gli agenti causali':
            df = df[df['AgenteCausale'] == self.getCodiceAgenteDalNome(self.currentAgente)]

        self.risultati = df

        self.update()

    def update(self):
        self.updateTitolo()
        self.updateDescrizione()
