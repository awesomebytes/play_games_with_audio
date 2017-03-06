#!/usr/bin/env python
from PyQt4 import QtGui, QtCore

import sys
import ui_main
import numpy as np
import pyqtgraph
import SWHear
# sudo pip install PyUserInput
from pykeyboard import PyKeyboard
import time

# Use audio to play super mario: http://supermarioemulator.com/mario.php
# A minimum volume of noise of 12.5% will make mario walk
# Any sound long enough with noise of >25.0% will make mario jump
# The louder the sound the higher the jump

# Author: Sammy Pfeiffer <sammypfeiffer at gmail.com>


class ExampleApp(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w')  # before loading widget
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.grFFT.plotItem.showGrid(True, True, 0.7)
        self.grPCM.plotItem.showGrid(True, True, 0.7)
        self.maxFFT = 0
        self.maxPCM = 32767  # Hardcoding it for S16_LE
        self.ear = SWHear.SWHear(rate=44100, updatesPerSecond=30)
        self.ear.stream_start()
        self.k = PyKeyboard()
        self.pressed_d = False
        self.pressed_w = False
        self.max_jump_time = 0.35
        self.jump_time = 0.0

    def update(self):
        if self.ear.data is not None and self.ear.fft is not None:
            pcmMax = np.max(np.abs(self.ear.data))
            if pcmMax > self.maxPCM:
                self.maxPCM = pcmMax
                self.grPCM.plotItem.setRange(yRange=[-pcmMax, pcmMax])
            if np.max(self.ear.fft) > self.maxFFT:
                self.maxFFT = np.max(np.abs(self.ear.fft))
                # self.grFFT.plotItem.setRange(yRange=[0,self.maxFFT])
                # self.grFFT.plotItem.setRange(yRange=[0, 1])
                self.grFFT.plotItem.setRange(yRange=[0, 0.5])

            self.pbLevel.setValue(1000 * pcmMax / self.maxPCM)

            pcmMax_pc = (float(pcmMax) / float(self.maxPCM)) * 100.0
            pcmAvg = np.average(np.abs(self.ear.data))
            pcmAvg_pc = (float(pcmAvg) / float(self.maxPCM)) * 100.0
            print "pcmMax: " + str(round(pcmMax_pc, 3)) + " % (" + str(pcmMax) + ")"
            print "pcmAvg: " + str(round(pcmAvg_pc, 3)) + " %",
            if self.pressed_d:
                print 'D ',
            else:
                print '  ',
            if self.pressed_w:
                print 'W'
            else:
                print
            print "Jump time: " + str(self.jump_time)
            print
            print
            if pcmAvg_pc > 12.5:
                if not self.pressed_d:
                    print "Down D"
                    self.k.press_key('d')
                    self.pressed_d = True
            else:
                if self.pressed_d:
                    print "Up D"
                    self.k.release_key('d')
                    self.pressed_d = False
            if pcmAvg_pc > 25.0:
                if not self.pressed_w:
                    print "Down W"
                    self.k.press_key('w')
                    self.pressed_w = True
                    curr_time = time.time()
                    self.jump_time = self.max_jump_time * (float(pcmMax_pc) / 100.0)
                    self.release_jump_time = curr_time + self.jump_time
            else:
                if self.pressed_w:
                    if time.time() >= self.release_jump_time:
                        print "Up W"
                        self.k.release_key('w')
                        self.pressed_w = False
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
