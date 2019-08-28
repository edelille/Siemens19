'''
Lam Nguyen
4/2/2019
'''
import OPChandler as opc
import time

def init():
    global OPChandler, nodeList, SensorIO
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
    SensorIO = ["Not a Node"]
    try:
        for i in range(1,16):
            SensorIO.append(OPChandler.get_node('ns=3;s="M_Sensor{}"'.format(i)))
        success = True
    except Exception as e:
        success = False
        print(e)
    finally:
        print('Grabbing nodes...', 'SUCCESS' if success else 'FAILURE')
        # Printing SensorIO
        '''
        for x in range(1,len(SensorIO)):
            name = SensorIO[x].get_display_name().Text
            print('\t', name, '\t' if len(name) < 10 else '',
                '\tat index ',x,',\t current value: ', OPChandler.get_node_value(SensorIO[x]))
        '''
        nodeList.append(OPChandler.get_node('ns=3;s="MC_EXSVON"'))
        nodeList.append(OPChandler.get_node('ns=3;s="MC_EXTServoOff_2"'))
        nodeList.append(OPChandler.get_node('ns=3;s="MC_SafetySpeedEnable"'))


if __name__ == '__main__':
    print('\nStarting program...')
    init()
    for x in nodeList:
        OPChandler.set_node_value(x, False)

    try:
        OPChandler.set_node_value(nodeList[2], True)
        OPChandler.set_node_value(nodeList[0], True)
        time.sleep(5)
        OPChandler.set_node_value(nodeList[1], True)
        OPChandler.set_node_value(nodeList[0], False)
        OPChandler.set_node_value(nodeList[2], False)

        time.sleep(10)
        for x in nodeList:
            OPChandler.set_node_value(x, False)

    except Exception as  e:
        print(e)
        OPChandler.close()