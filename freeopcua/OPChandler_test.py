import OPChandler as opc

# MUST be initialized with the IP_ADDRESS as an argument
OPChandler = opc.OPChandler("opc.tcp://192.168.0.1:4840")


if __name__ == '__main__':
    # Try to read root node for first debug
    OPChandler.print_rootnode_info()

    # Try to fetch an example node
    pathNumber_node = OPChandler.get_node('ns=3;s="M_Motor_IO1"')

    # Print the example node's info
    OPChandler.print_node_info(pathNumber_node)

    # Print Display name
    print('Display name', pathNumber_node.get_display_name().Text)

    # Subscribe changes to the node
    OPChandler.subscribe_changes(pathNumber_node)

    # Set the node's value
    OPChandler.set_node_value(pathNumber_node, 3)

    # Print the example node's data and type after the change
    OPChandler.print_node_value(pathNumber_node)

    # Must close client after running programs
    OPChandler.close()


