import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QPushButton,
                        QFormLayout, QLabel, QCheckBox, QLineEdit, QDialog,
                        QHBoxLayout)

class filePreferencesGUI(QDialog):
    def __init__(self, filePreferences, parent = None):
        super(filePreferencesGUI, self).__init__(parent)
        self.filePreferences = filePreferences
        #self.setupUi(self)
        layout = QFormLayout()

        # is WSP file
        self.WSPPythonLabel = QLabel()
        self.WSPPythonLabel.setText('WSP file? ')
        self.WSPPythonUIn = QCheckBox()
        layout.addRow(self.WSPPythonLabel,self.WSPPythonUIn)

        # file version
        self.fileversionLabel = QLabel()
        self.fileversionLabel.setText('File version: ')
        self.fileversionUIn = QLineEdit()
        layout.addRow(self.fileversionLabel,self.fileversionUIn)

        # Experiment Type
        self.ExperimentTypeLabel = QLabel()
        self.ExperimentTypeLabel.setText('Experiment Type: ')
        self.ExperimentTypeUIn = QLineEdit()
        layout.addRow(self.ExperimentTypeLabel,self.ExperimentTypeUIn)

        #OK - Cancel
        self.OKbutton = QPushButton('OK')
        self.CancelButton = QPushButton('Cancel')
        self.OKbutton.clicked.connect(self.OKfunction)
        self.CancelButton.clicked.connect(self.Cancelfunction)
        layout.addRow(self.OKbutton,self.CancelButton)

        self.setLayout(layout)
        self.setWindowTitle("File preferences")

        self.ok = False

        self.load_filePreferences()
        self.exec_()

    def OKfunction(self):
        self.save_filePreferences()
        self.ok = True
        self.accept()
        self.close()

    def Cancelfunction(self):
        self.ok = False
        self.reject()

    def load_filePreferences(self):
        if self.filePreferences['WSPPython']:
            self.WSPPythonUIn.setCheckState(2)
        else:
            self.WSPPythonUIn.setCheckState(0)
        self.fileversionUIn.setText(str(self.filePreferences['fileversion']))
        self.ExperimentTypeUIn.setText(self.filePreferences['ExperimentType'])

    def save_filePreferences(self):
        if self.WSPPythonUIn.checkState() == 2:
            self.filePreferences['WSPPython'] = True
        else:
            self.filePreferences['WSPPython'] = False
        self.filePreferences['fileversion'] = float(self.fileversionUIn.text())
        self.filePreferences['ExperimentType'] = self.ExperimentTypeUIn.text()
