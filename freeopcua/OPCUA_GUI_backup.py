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

class OPCUA_GUI():
    def __init__(self):
        app = QApplication([])
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

        self.exsvonButton = QPushButton("External Servo ON")
        self.safetySpeedENButton = QPushButton("Safety Speed Enable")
        self.ESTOPButton = QPushButton("Emergency STOP")
        self.playmodeButton = QPushButton("Play Mode Select")
        self.masterJobCallButton = QPushButton("Master Job Call")
        self.extStartButton = QPushButton("External Start")
        self.extHoldButton = QPushButton("External Hold")
        self.input1Button = QPushButton("Start Pour Task")
        self.input2Button = QPushButton("Start Cap Task")
        self.exsvonButton.setCheckable(True)
        self.safetySpeedENButton.setCheckable(True)
        self.ESTOPButton.setCheckable(True)
        self.playmodeButton.setCheckable(True)
        self.masterJobCallButton.setCheckable(True)
        self.extStartButton.setCheckable(True)
        self.extHoldButton.setCheckable(True)
        self.input1Button.setCheckable(True)
        self.input2Button.setCheckable(True)
        self.exsvonButton.toggled.connect(self.exsvonToggle)
        self.safetySpeedENButton.toggled.connect(self.safetyspeedToggle)
        self.ESTOPButton.toggled.connect(self.estopToggle)
        self.playmodeButton.toggled.connect(self.playmodeselToggle)
        self.masterJobCallButton.toggled.connect(self.masterjobcallToggle)
        self.extStartButton.toggled.connect(self.extstartToggle)
        self.extHoldButton.toggled.connect(self.extholdToggle)
        self.input1Button.toggled.connect(self.input1Toggle)
        self.input2Button.toggled.connect(self.input2Toggle)

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.exsvonButton)
        leftLayout.addWidget(self.safetySpeedENButton)
        leftLayout.addWidget(self.ESTOPButton)
        leftLayout.addWidget(self.playmodeButton)
        leftLayout.addWidget(self.masterJobCallButton)
        leftLayout.addWidget(self.extStartButton)
        leftLayout.addWidget(self.extHoldButton)
        leftLayout.addWidget(self.input1Button)
        leftLayout.addWidget(self.input2Button)

        leftGroup = QGroupBox('Main Controls')
        leftGroup.setLayout(leftLayout)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0,0,1,2)
        mainLayout.addWidget(leftGroup,1,0)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0,1)
        mainLayout.setColumnStretch(1,1)

        visibleGui.setLayout(mainLayout)
        visibleGui.setWindowTitle('OPCUA Siemens 2019 GUI')
        visibleGui.show()
        app.exec_()

    def tryConnect(self):
        status = opcClient.tryConnect(self.ipAddressBox.text())
        if status is 0:
            self.ipStatusButton.setText("BAD")
            self.ipStatusButton.setStyleSheet('QPushButton {background-color: red}')
        else:
            self.ipStatusButton.setText("GOOD")
            self.ipStatusButton.setStyleSheet('QPushButton {background-color: green}')

        opcClient.tryGrabNodes()


    def exsvonToggle(self): opcClient.tryEXSVON()
    def estopToggle(self): opcClient.tryEXTServoOff_2()
    def safetyspeedToggle(self): opcClient.trySafetySpeedEnable()
    def playmodeselToggle(self): opcClient.tryPlayModeSel()
    def masterjobcallToggle(self): opcClient.tryMasterJobCall()
    def extstartToggle(self): opcClient.tryExtStart()
    def extholdToggle(self): opcClient.tryExtHold()
    def input1Toggle(self): opcClient.tryInput1()
    def input2Toggle(self): opcClient.tryInput2()
    def returnhomeToggle(self): opcClient.tryR1ReturnHome()

class OPC_Client():
    def __init__(self):
        print('Successful OPC init')

    def tryConnect(self, IP_ADDRESS):
        try:
            self.OPChandler = opc.OPChandler(IP_ADDRESS)
        except:
            print(e)
    def tryGrabNodes(self):
        self.nodeList = []
        self.SensorIO = ["Not a Node"]
        try:
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
            success = True
        except Exception as e:
            success = False
            print(e)
        finally:
            print('Grabbing nodes...', 'SUCCESS' if success else 'FAILURE')

    def tryEXSVON(self): self.toggleNode(self.nodeList[0])
    def tryEXTServoOff_2(self): self.toggleNode(self.nodeList[1])
    def trySafetySpeedEnable(self): self.toggleNode(self.nodeList[2])
    def tryPlayModeSel(self): self.toggleNode(self.nodeList[3])
    def tryMasterJobCall(self): self.toggleNode(self.nodeList[4])
    def tryExtStart(self): self.toggleNode(self.nodeList[5])
    def tryExtHold(self): self.toggleNode(self.nodeList[6])
    def tryInput1(self): self.toggleNode(self.nodeList[7])
    def tryInput2(self): self.toggleNode(self.nodelList[8])
    def tryR1ReturnHome(self): self.toggleNode(self.nodeList[9])

    def toggleNode(self, NODE):
        self.OPChandler.set_node_value(NODE, not self.OPChandler.get_node_value(NODE))



if __name__ == '__main__':
    global opcClient, guiWindow

    opcClient = OPC_Client()
    guiWindow = OPCUA_GUI()
