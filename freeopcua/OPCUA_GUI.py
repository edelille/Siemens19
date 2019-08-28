'''
Lam Nguyen
OPC UA GUI
'''

from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
import time
import sys
import OPChandler as opc
import threading

class OPCUA_GUI():
    def __init__(self):
        self.app = QApplication([])
        visibleGui = QWidget()
        self.ipAddressBox = QLineEdit('opc.tcp://192.168.0.1:4840')
        self.ipAddressBox.setFixedWidth(200)
        self.ipStatusLabel = QLabel('Connection Status:')
        self.ipStatusButton = QPushButton("Not Connected")
        self.ipLabel = QLabel('&IP Address:')
        self.ipLabel.setBuddy(self.ipAddressBox)
        self.ipLabel.setBuddy(self.ipStatusButton)
        self.ipConnectPushButton = QPushButton('Connect')
        self.ipConnectPushButton.clicked.connect(self.tryConnect)

        topLayout = QHBoxLayout()
        topLayout.addWidget(self.ipLabel)
        topLayout.addWidget(self.ipAddressBox)
        topLayout.addWidget(self.ipConnectPushButton)
        topLayout.addStretch(1)
        topLayout.addWidget(self.ipStatusLabel)
        topLayout.addWidget(self.ipStatusButton)

        self.mainControlButtons = []
        self.mainControlButtons.append(QPushButton("External Servo ON"))    #[0] = EXSVON
        self.mainControlButtons.append(QPushButton("Safety Speed Enable"))  #[1] = Safety Speed Enable
        self.mainControlButtons.append(QPushButton("Emergency STOP"))       #[2] = ESTOP
        self.mainControlButtons.append(QPushButton("Play Mode Select"))     #[3] = PlayModeSel
        self.mainControlButtons.append(QPushButton("Master Job Call"))      #[4] = MasterJobCall
        self.mainControlButtons.append(QPushButton("External Start"))       #[5] = ExtStart
        self.mainControlButtons.append(QPushButton("External Hold"))        #[6] = ExtHold
        self.mainControlButtons.append(QPushButton("Start Pour Task"))      #[7] = StartPourTask
        self.mainControlButtons.append(QPushButton("Start Cap Task"))       #[8] = StartCapTask
        self.mainControlButtons.append(QPushButton("Return to Home Position"))      #[9] = ReturnHome

        leftLayout = QVBoxLayout()
        for button in self.mainControlButtons:
            button.setCheckable(True)
            leftLayout.addWidget(button)

        leftGroup = QGroupBox('Main Controls')
        leftGroup.setLayout(leftLayout)


        self.sensorReadouts = ['not a readout']
        for i in range(1,16):
            self.sensorReadouts.append(QPushButton("Sensor {}".format(i)))
        upper8SensorsLayout = QHBoxLayout()
        lower8SensorsLayout = QHBoxLayout()
        for i in range(1,16):
            if i < 9: upper8SensorsLayout.addWidget(self.sensorReadouts[i])
            else: lower8SensorsLayout.addWidget(self.sensorReadouts[i])
        refreshButton = QPushButton("Refresh Values")
        refreshButton.clicked.connect(self.updateValues)

        rightLayout = QGridLayout()
        rightLayout.addLayout(upper8SensorsLayout, 1,0,1,2)
        rightLayout.addLayout(lower8SensorsLayout, 1,0,2,2)
        rightLayout.addWidget(refreshButton)
        rightLayout.setRowStretch(1,1)
        rightLayout.setRowStretch(1,2)

        rightGroup = QGroupBox('Signal Readback')
        rightGroup.setLayout(rightLayout)



        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0,0,1,2)
        mainLayout.addWidget(leftGroup,1,0)
        mainLayout.addWidget(rightGroup,1,1)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0,1)
        mainLayout.setColumnStretch(1,1)

        visibleGui.setLayout(mainLayout)
        visibleGui.setWindowTitle('OPCUA Siemens 2019 GUI')
        visibleGui.show()
        self.app.exec_()

    def tryConnect(self):
        try:
            self.OPChandler = opc.OPChandler(self.ipAddressBox.text())
            self.ipStatusButton.setText("GOOD")
            self.ipStatusButton.setStyleSheet('QPushButton {background-color: green}')

            self.nodeList = []
            self.SensorIO = ["Not a Node"]
            # Try grabbing all nodes

            for i in range(1,16):
                self.SensorIO.append(self.OPChandler.get_node('ns=3;s="M_Sensor{}"'.format(i)))

            self.nodeList.append(self.OPChandler.get_node('ns=3;s="MC_EXSVON"'))
            self.nodeList.append(self.OPChandler.get_node('ns=3;s="MC_EXTServoOff_2"'))
            self.nodeList.append(self.OPChandler.get_node('ns=3;s="MC_SafetySpeedEnable"'))
            self.nodeList.append(self.OPChandler.get_node('ns=3;s="MC_PlayModeSel"'))
            self.nodeList.append(self.OPChandler.get_node('ns=3;s="MC_MasterJobCall"'))
            self.nodeList.append(self.OPChandler.get_node('ns=3;s="MC_ExtStart"'))
            self.nodeList.append(self.OPChandler.get_node('ns=3;s="MC_ExtHold"'))
            self.nodeList.append(self.OPChandler.get_node('ns=3;s="MC_Input1"'))
            self.nodeList.append(self.OPChandler.get_node('ns=3;s="MC_Input2"'))
            self.nodeList.append(self.OPChandler.get_node('ns=3;s="MC_R1ReturnHome"'))    

            # Setting Button status akin to current status
            for i in range(len(self.mainControlButtons)):
                self.mainControlButtons[i].setChecked(self.OPChandler.get_node_value(self.nodeList[i]))

            # Activating the buttons
            self.mainControlButtons[0].toggled.connect(self.tryEXSVON)
            self.mainControlButtons[1].toggled.connect(self.trySafetySpeedEnable)
            self.mainControlButtons[2].toggled.connect(self.tryEXTServoOff_2)
            self.mainControlButtons[3].toggled.connect(self.tryPlayModeSel)
            self.mainControlButtons[4].toggled.connect(self.tryMasterJobCall)
            self.mainControlButtons[5].toggled.connect(self.tryExtStart)
            self.mainControlButtons[6].toggled.connect(self.tryExtHold)
            self.mainControlButtons[7].toggled.connect(self.tryInput1)
            self.mainControlButtons[8].toggled.connect(self.tryInput2)
            self.mainControlButtons[9].toggled.connect(self.tryR1ReturnHome)

            for i in range(1, len(self.sensorReadouts)):
                self.setButtonState(self.sensorReadouts[i], self.SensorIO[i])

        except Exception as e:
            print(e)
            self.ipStatusButton.setText("BAD")
            self.ipStatusButton.setStyleSheet('QPushButton {background-color: red}') 


    def tryEXSVON(self): self.toggleNode(self.nodeList[0])
    def tryEXTServoOff_2(self): self.toggleNode(self.nodeList[1])
    def trySafetySpeedEnable(self): self.toggleNode(self.nodeList[2])
    def tryPlayModeSel(self): self.toggleNode(self.nodeList[3])
    def tryMasterJobCall(self): self.toggleNode(self.nodeList[4])
    def tryExtStart(self): self.toggleNode(self.nodeList[5])
    def tryExtHold(self): self.toggleNode(self.nodeList[6])
    def tryInput1(self): self.toggleNode(self.nodeList[7])
    def tryInput2(self): self.toggleNode(self.nodeList[8])
    def tryR1ReturnHome(self): self.toggleNode(self.nodeList[9])

    def toggleNode(self, NODE):
        self.OPChandler.set_node_value(NODE, not self.OPChandler.get_node_value(NODE))

    def setButtonState(self, button, node):
        if bool(self.OPChandler.get_node_value(node)): button.setStyleSheet('QPushButton {background-color: green}') 
        else: button.setStyleSheet('QPushButton {background-color: red}') 

    def updateValues(self):
        for i in range(1, len(self.sensorReadouts)):
            self.setButtonState(self.sensorReadouts[i], self.SensorIO[i])
        time.sleep(0.01)
        self.app.processEvents()


if __name__ == '__main__':
    global opcClient, guiWindow
    guiWindow = OPCUA_GUI()
