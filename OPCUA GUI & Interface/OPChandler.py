'''
Lam Nguyen
4/2/2019
'''

import sys
sys.path.insert(0, "..")
import logging
import time
import random
import datetime
from opcua import Client
from opcua import ua

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()

# Global final variables
VALUE_ATTRIBUTE_ID = 13
SUBSCRIPTION = HANDLE = client = None
       
class OPChandler(object):
    def __init__(self, IP_ADDRESS):
        '''
        The constructor must be initialized with IP_ADDRESS as an arguement
        '''
        global client
        logging.basicConfig(level=logging.WARN)
        client = Client(IP_ADDRESS)
        try:
            client.connect()
        except Exception as e:
            print(e)

    def get_node(self, NODEID):
        '''
        This method takes the (str) NodeID of a node and returns the Node object
        '''
        global client
        try:
            NODE = client.get_node(NODEID)
        except:
            print('ERROR: Node not found or NODEID not formatted correctly')
            return
        finally:
            return NODE

    def print_node_value(self, NODE):
        '''
        This metod is used to return the value and varianttype of the node,
        most useful when trying to quickly check the VariantType of the node
        '''
        VALUE = NODE.get_value()
        DATATYPE = NODE.get_data_type_as_variant_type()

        print("The nodes value is:", VALUE,"of type:", DATATYPE)

    def get_node_value(self, NODE):
        '''
        This will only return the strict value of the node
        '''
        return NODE.get_value()

    def set_node_value(self, NODE, VALUE):
        '''
        This method will autodetect DataType of the current node data type
        to set onto the node's value. This is currently only able to detect
        datatype from the underlying NODE, but must take care to make sense with
        your data types
        s
        TODO: add more potential DataTypes
        '''
        try:
            DATATYPE = NODE.get_data_type_as_variant_type()
            VARIANT = ua.Variant(VALUE, DATATYPE) 
            NODE.set_attribute(VALUE_ATTRIBUTE_ID, ua.DataValue(VARIANT))
        except Exception as e:
            print(e)

    

    def print_rootnode_info(self):
        '''
        this method is a simple debug to test whether or not the client is finding
        the root nodes properly, preliminary test
        '''
        global client
        print("Root node is: ", client.get_root_node())
        print("Objects node is: ", client.get_objects_node())
        print("Children of root are: ", client.get_root_node().get_children())

    def print_node_info(self, NODE): 
        '''
        Debug purposes, uncomment the pieces of information you want to read
        '''

        print("The nodes dava_value: ", NODE.get_data_value())
        print("The nodes value: ", NODE.get_value())
        # print("The nodes array_dimensions: ", NODE.get_array_dimensions())
        # print("The nodes value_rank: ", NODE.get_value_rank())
        print('\n')

    def print_all_attributes(self, node):
        '''
        For debug purposes to print out all attributes, their id number, and their
        values/datatypes
        '''

        badAttributes = [5,9,10,11,12,16]
        for x in range(1,20):
            if x not in badAttributes:
                print('Attribute %d: ' %x, node.get_attribute(x))

    def open_console(self):
        embed()

    def subscribe_changes(self, NODE):
        '''
        This method will take a NODE and allow you to subscribe changes to the node
        '''
        global SUBSCRIPTION, HANDLE
        try:
            HANDLE = SubHandler()
            SUBSCRIPTION = client.create_subscription(500, HANDLE)
            HANDLE = SUBSCRIPTION.subscribe_data_change(NODE)
            SUBSCRIPTION.subscribe_events()
        except Exception as e:
            print(e)

    def close(self):
        # Should be run at the end, to free up memory
        global client, SUBSCRIPTION, HANDLE
        if SUBSCRIPTION is not None:
            SUBSCRIPTION.unsubscribe(HANDLE)
            SUBSCRIPTION.delete()
        client.disconnect()

class SubHandler(object):
    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)
    def event_notification(self, event):
        print("Python: New event", event)