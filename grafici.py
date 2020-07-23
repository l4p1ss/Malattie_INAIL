from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy


class Grafico(FigureCanvas):

    def __init__(self, parent):
        fig = Figure(figsize=(5, 4), dpi=80)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class GraficoTorta(Grafico):

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [0, 0, 0, 0], 'r')

    def update_figure(self, ris, title, xt=None, legend=False):
        self.axes.cla()

        ris.value_counts().head(5).plot(kind='pie', ax=self.axes, title=title, labels=xt, legend=legend, autopct='%1.1f%%')
        self.axes.set_ylabel('')

        self.draw()

class GraficoIstogramma(Grafico):

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [0, 0, 0, 0], 'r')

    def update_figure(self, ris, xt, title, n=5):
        self.axes.cla()

        ris.value_counts().head(n).plot(kind='bar', ax=self.axes, title=title, rot=0)
        self.axes.xaxis.set_ticklabels(xt)

        self.draw()
