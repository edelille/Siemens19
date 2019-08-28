import sys
sys.path.insert(0, "..")
import logging
import time
import random
import datetime

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()


from opcua import Client
from opcua import ua


class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another 
    thread if you need to do such a thing
    """
    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)
        
    def testRET():
        print("1")
        

def print_node_info(node):
    # print("The nodes description: ", node.get_description())
    print("The nodes dava_value: ", node.get_data_value())
    print("The nodes value: ", node.get_value())
    # print("The nodes array_dimensions: ", node.get_array_dimensions())
    print("The nodes value_rank: ", node.get_value_rank())
    print('\n')

def print_all_attributes(node):
    badAttributes = [5,9,10,11,12,16]
    for x in range(1,20):
        if x not in badAttributes:
            print('Attribute %d: ' %x, node.get_attribute(x))


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    #logger = logging.getLogger("KeepAlive")
    #logger.setLevel(logging.DEBUG)

    client = Client("opc.tcp://192.168.0.1:4840")

    try:
        client.connect()
        # Getting Root node information
        print("Root node is: ", client.get_root_node())
        print("Objects node is: ", client.get_objects_node())
        print("Children of root are: ", client.get_root_node().get_children())

        # get a specific node knowing its node id
        pathNumber_node = client.get_node('ns=3;s="M_PathNumber"')
        testSignal_node = client.get_node('ns=3;s="M_TestSignal"')
        ShouldBeFalse = client.get_node('ns=3;s="M_ShouldBeFalse"')
        alwaysTrue = client.get_node('ns=3;s="AlwaysTRUE"')

         # Creating subscription handler
        handler = SubHandler()
        sub = client.create_subscription(500, handler)
        handle = sub.subscribe_data_change(pathNumber_node)
        sub.subscribe_events()

        print_node_info(pathNumber_node)
        print_all_attributes(pathNumber_node)
        # dv.ServerTimestamp = pathNumber_val.ServerTimestamp
        # TRY TO EXECUTE CHANGE TO VALUE
        bol = False
        while True:
            time.sleep(1)
            pathNumber_node.set_attribute(13, ua.DataValue(ua.Variant(!bol, ua.VariantType.Int16)))

            # print(dv)
            # pathNumber_node.set_value(ua.DataValue(ua.Variant(3, ua.VariantType.Int16)))
            # pathNumber_node.set_value(dv)
            #ua.uawrite()
            # print(pathNumber_node.get_data_value())
            # print('Test signal=', testSignal_node.get_value())

        #var.get_data_value() # get value of node as a DataValue object
        #var.get_value() # get value of node as a python builtin
        #var.set_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        #var.set_value(3.9) # set node value using implicit data type

        # gettting our namespace idx
        '''
        uri = "http://examples.freeopcua.github.io"
        idx = client.get_namespace_index(uri)
        '''
        
        # Now getting a variable node using its browse path
        # myvar = root.get_child(["0:Objects", "{}:MyObject".format(idx), "{}:MyVariable".format(idx)])
        # obj = root.get_child(["0:Objects", "{}:MyObject".format(idx)])
        
        # subscribing to a variable node
        

        # we can also subscribe to events from server
        sub.unsubscribe(handle)
        sub.delete()

        # calling a method on server
        # res = obj.call_method("{}:multiply".format(idx), 3, "klk")
        # print("method result is: ", res)
        
        # embed() #opens up the console
       
    finally:
        client.disconnect()