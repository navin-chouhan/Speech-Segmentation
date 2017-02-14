import scipy.io.wavfile as wavfile
import numpy as np
from PyQt4 import QtCore, QtGui, uic
import sys
import os
import glob
import sip

sip.setapi('QString', 2)


qtCreatorFile1 = "MainWindow.ui"  # Enter file here.
Ui_MainWindow1, QtBaseClass1 = uic.loadUiType(qtCreatorFile1)
qtCreatorFile2 = "MethodWindow.ui"  # Enter file here.
Ui_MainWindow2, QtBaseClass2 = uic.loadUiType(qtCreatorFile2)


class MyApp(QtGui.QMainWindow, Ui_MainWindow1):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow1.__init__(self)
        self.setupUi(self)
        self.segment.clicked.connect(self.function_call)
        self.save.clicked.connect(self.file_save)
        self.open_file.triggered.connect(self.file_open)
        self.actionQbout.triggered.connect(self.About)
        self.actionQuit.triggered.connect(self.Quit_Win)
        self.energy_method.triggered.connect(self.Quit_Win)
        self.method_1.triggered.connect(self.Quit_Win)
        self.method_2.triggered.connect(self.Quit_Win)
        self.window1 = None

    def About(self):
        pass

    def Quit_Win(self):
        sys.exit()

    file_content = ''
    temp = 0
    temp2 = 0
    temp1 = ''
    temp4 = ''
    temp3 = ''

    def file_open(self):
        self.temp=1
        self.temp+=1
        name= QtGui.QFileDialog.getExistingDirectory(None)
        t = ''
        x = []
        i = 0
        while True:
            if len(glob.glob(os.path.join(name, t, '*.wav'))) == 0:
                if os.path.isdir(os.path.join(name, t)) == False:
                    break
                else:
                    pass
            else:
                for a in glob.glob(os.path.join(name, t, '*.wav')):
                    x.append(a)
                    i += 1
            t = os.path.join(t, '*')
            print(t)
        self.temp1=x
        self.temp3=name
        self.result.setText('folder open :'+self.temp3+'\n\n')

    def file_save(self):
        if len(self.temp1)==0:
            QtGui.QMessageBox.information(self, 'Information', "Please select a file", )
            pass
        else:
            self.temp4 = QtGui.QFileDialog.getExistingDirectory(None)

    def function_call(self):
        if len(self.temp4) == 0 or len(self.temp1) == 0:
            QtGui.QMessageBox.information(self, 'Information', "Please Open a Directory and select Destination for txt file", )
            pass
        else:
            self.window1 = MyApp1()
            self.window1.exec_()
            self.segment_fun()

    def segment_fun(self):
        for self.SNDF in self.temp1:
            samplerate, snd = wavfile.read(self.SNDF)
            tsample = snd.shape[0]
            time = tsample / samplerate
            self.temp3 = self.temp3 + '\n' + self.SNDF + '\n' + 'Sample Rate = ' + str(
                samplerate) + '\n' + 'Total Time =' + str(time) + ' sec\n'
            self.result.setText(self.temp3)
            if self.temp2 == 1:
                self.Energy_method(self.SNDF)
                pass
            if self.temp2 == 2:
                pass
            if self.temp2 == 3:
                pass

    def Energy_method(self,SNDFile):
        ETHK = (self.thershold.value())
        l = (self.frame_size.value())
        shift = (self.shift.value())
        SNDF=SNDFile
        samplerate, data = wavfile.read(SNDF)
        if len(data.shape)==1:
            snd = data[:]
        if len(data.shape)==2:
            snd = data[:,0]
        tsample = snd.shape[0]
        time = tsample / samplerate
        timeArray = np.arange(0, snd.shape[0], 1)
        timeArray = timeArray / samplerate
        l = int(l * samplerate / 1000)
        shift = int(shift * samplerate / 1000)
        no_of_window = ((tsample - l) / shift) + 1
        if no_of_window - int(no_of_window) > 0:
            no_of_window = int(no_of_window) + 1
        else:
            no_of_window = int(no_of_window)
        window_energy = np.zeros([no_of_window], dtype='float64')
        lk = 0
        for i in range(no_of_window):
            temp1 = 0
            temp = np.zeros([l], dtype='float64')
            if i == no_of_window - 1:
                temp[:len(snd[int(i * shift):-1])] = snd[int(i * shift):-1]
            else:
                temp[:] = snd[int(i * shift):int(i * shift + l)]
            temp = temp * temp
            for k in temp:
                temp1 = temp1 + k
            lk += 1
            window_energy[i] = temp1
        scilince = np.zeros([no_of_window], dtype='float64')
        rtl = 0
        ETH = sum(window_energy)
        ETH = ETH * ETHK / len(window_energy)
        for et in window_energy:
            if et > ETH:
                scilince[rtl] = 1
            else:
                scilince[rtl] = 0
            rtl += 1

        for w in range(len((scilince))):
            if scilince[w] == 1:
                d1 = w
                for ff in range(w + 1, len(scilince)):
                    if scilince[ff] == 1:
                        d2 = ff
                        break
                if d2 - d1 <= samplerate/1000:
                    scilince[d1:d2 + 1] = 1
        for w in range(len((scilince))):
            if scilince[w] == 0:
                d1 = w
                for ff in range(w + 1, len(scilince)):
                    if scilince[ff] == 0:
                        d2 = ff
                        break
                if d2 - d1 <= samplerate/1000:
                    scilince[d1:d2 + 1] = 0
        count1 = 0
        count2 = 1
        self.file_content=''
        for sat in range(len(scilince)):
            interval = sat * time / no_of_window
            if scilince[sat] == 1:
                if count1 == 1:
                    self.file_content = self.file_content + '-' + str("{0:.2f}".format(interval)) + '  Silence\n'
                if count1 == 0:
                    continue
                count1 = 0

            else:
                if count1 == 0:
                    self.file_content = self.file_content + str("{0:.2f}".format(interval))
                if count1 == 1:
                    continue
                count1 = 1
        self.file_content = self.file_content + str('Silence\n')
        start = []
        stop = []
        for sat in range(len(scilince)):
            interval = sat * time / no_of_window
            if scilince[sat] == 1:
                if count2 == 1:
                    self.file_content = self.file_content + str("{0:.2f}".format(interval))
                    start.append(int(interval*tsample/time))
                if count2 == 0:
                    continue
                count2 = 0

            else:
                if count2 == 0:
                    self.file_content = self.file_content + '-' + str("{0:.2f}".format(interval)) + '  Voice\n'
                    stop.append(int(interval*tsample/time))
                if count2 == 1:
                    continue
                count2 = 1
        word = self.SNDF.split(os.path.join(' ','')[1])
        words = word[-1]
        words = words[:len(words)-4]
        overwrit=0
        try:
            os.makedirs(os.path.join(self.temp4, words))
        except FileExistsError:
            while os.path.isdir(os.path.join(self.temp4, words)) == True:
                overwrit +=1
                words = words + '(' + str(overwrit) + ')'
            os.makedirs(os.path.join(self.temp4, words))

        txtfile = os.path.join(self.temp4, words,'SpeechFile.txt')
        f = open(txtfile, 'w+')
        f.write(self.SNDF + '\n' + self.file_content)
        f.close()
        partno=0
        for tempp in range(len(start)):
            partno = partno + 1
            filename=os.path.join(self.temp4, words, 'p'+str(partno)+'.wav')
            if not (len(start)-len(stop) == 0):
                wavfile.write(filename,samplerate,snd[start[tempp]:])
            else:
                wavfile.write(filename, samplerate, snd[start[tempp]:stop[tempp]])



class MyApp1(QtGui.QDialog, Ui_MainWindow2):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        Ui_MainWindow2.__init__(self)
        self.setupUi(self)
        self.energy_button.clicked.connect(self.n1)
        self.method1_button.clicked.connect(self.n2)
        self.method2_button.clicked.connect(self.n3)
    def n1(self):
        window.temp2=1
        self.close()
    def n2(self):
        window.temp2=2
        self.close()
    def n3(self):
        window.temp2=3
        self.close()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())