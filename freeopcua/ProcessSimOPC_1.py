'''
Lam Nguyen
4/2/2019
'''
import OPChandler as opc
import time

def init():
    global OPChandler, nodeList
    try:
        OPChandler = opc.OPChandler("opc.tcp://192.168.0.1:4840")
        success = True
    except:
        success = False
    finally:
        print('Connecting...','SUCCESS' if success else 'FAILURE')
    '''
    All nodes can be grabbed using nodeList[i], with all nodes and their described indices
    printed out below.
    '''
    nodeList = []
    SensorIO = []
    try:
        nodeList.append(OPChandler.get_node('ns=3;s="IF_button1"'))
        nodeList.append(OPChandler.get_node('ns=3;s="IF_button2"'))
        nodeList.append(OPChandler.get_node('ns=3;s="IF_button3"'))
        nodeList.append(OPChandler.get_node('ns=3;s="M_PathNumber"'))
        nodeList.append(OPChandler.get_node('ns=3;s="M_StartRobot"'))
        nodeList.append(OPChandler.get_node('ns=3;s="M_button1"'))
        nodeList.append(OPChandler.get_node('ns=3;s="M_button2"'))
        nodeList.append(OPChandler.get_node('ns=3;s="M_greenLED"'))
        nodeList.append(OPChandler.get_node('ns=3;s="M_redLED"'))
        success = True
    except:
        success = False
    finally:
        print('Grabbing nodes...', 'SUCCESS' if success else 'FAILURE')
        # Printing nodeList
        for x in range(len(nodeList)):
            name = nodeList[x].get_display_name().Text
            print('\t', name, '\t' if len(name) < 10 else '',
                '\tat index ',x,',\t current value: ', OPChandler.get_node_value(nodeList[x]))

def simulate_button_press(button):
    OPChandler.set_node_value(button, True) 
    time.sleep(0.5)
    OPChandler.set_node_value(button, False)

if __name__ == '__main__':
    print('\nStarting program...')
    init()
    pathNumber = nodeList[3]
    button1 = nodeList[0]
    button2 = nodeList[1]
    button3 = nodeList[3]
    OPChandler.subscribe_changes(pathNumber) # nodeList[2] is M_PathNumber
    '''
    TODO
    Replace all simulate button presses with value assignment to remove PLC reliance
    '''
    while(pathNumber.get_value() != 1):
        simulate_button_press(button1)
        time.sleep(0.5)
    for x in range(5):
        simulate_button_press(button2)
        simulate_button_press(button1)
        time.sleep(6)
    simulate_button_press(button3)

    OPChandler.close()