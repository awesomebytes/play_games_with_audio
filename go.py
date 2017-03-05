from PyQt4 import QtGui, QtCore

import sys
import ui_main
import numpy as np
import pyqtgraph
import SWHear


class ExampleApp(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w')  # before loading widget
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.grFFT.plotItem.showGrid(True, True, 0.7)
        self.grPCM.plotItem.showGrid(True, True, 0.7)
        self.maxFFT = 0
        self.maxPCM = 0
        self.ear = SWHear.SWHear(rate=44100, updatesPerSecond=10)
        self.ear.stream_start()

    def update(self):
        if self.ear.data is not None and self.ear.fft is not None:
            pcmMax = np.max(np.abs(self.ear.data))
            if pcmMax > self.maxPCM:
                self.maxPCM = pcmMax
                self.grPCM.plotItem.setRange(yRange=[-pcmMax, pcmMax])
            if np.max(self.ear.fft) > self.maxFFT:
                self.maxFFT = np.max(np.abs(self.ear.fft))
                # self.grFFT.plotItem.setRange(yRange=[0,self.maxFFT])
                self.grFFT.plotItem.setRange(yRange=[0, 1])
            self.pbLevel.setValue(1000 * pcmMax / self.maxPCM)
            if pcmMax > (self.maxPCM / 2):
                print "pcmMax > (self.maxPCM / 2) (" + str(pcmMax) + " > " + str(self.maxPCM) + ")"
            pen = pyqtgraph.mkPen(color='b')
            self.grPCM.plot(self.ear.datax, self.ear.data, pen=pen, clear=True)
            pen = pyqtgraph.mkPen(color='r')
            self.grFFT.plot(self.ear.fftx, self.ear.fft /
                            self.maxFFT, pen=pen, clear=True)
        QtCore.QTimer.singleShot(1, self.update)  # QUICKLY repeat


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    form.update()  # start with something
    app.exec_()
    print("DONE")
