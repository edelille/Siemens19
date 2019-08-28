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
        for x in range(1,len(SensorIO)):
            name = SensorIO[x].get_display_name().Text
            print('\t', name, '\t' if len(name) < 10 else '',
                '\tat index ',x,',\t current value: ', OPChandler.get_node_value(SensorIO[x]))

if __name__ == '__main__':
    print('\nStarting program...')
    init()

    SensorMBits = ["Not a MBit"]
    for i in range(1,len(SensorIO)):
        SensorMBits.append(OPChandler.get_node_value(SensorIO[i]))
    try:
        while True:
            for i in range(1, len(SensorIO)):
                i_value = OPChandler.get_node_value(SensorIO[i])
                if SensorMBits[i] is not i_value and i_value is True:
                    print("{} detects an object.".format(SensorIO[i].get_display_name().Text))
                SensorMBits[i] = i_value
                time.sleep(0.01)
    except:
        OPChandler.close()