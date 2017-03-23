from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout
from libs.MultiDimExperiment import MultiDimExperiment

class QWidgetUSPM(QWidget):
  def __init__( self, parent = None, XP = MultiDimExperiment()):
      super(QWidgetUSPM, self).__init__(parent)
      self.XP = XP

      self.pushButton = QPushButton('I am in Test widget')

      layout = QHBoxLayout()
      layout.addWidget(self.pushButton)
      self.setLayout(layout)
