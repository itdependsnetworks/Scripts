#!/usr/bin/env python

def main():
    '''show without reverse and with partial and full matches'''
    print normalize_interfaces(r"Eth1", 'cisco')
    print normalize_interfaces(r"Ethernet1/1", 'cisco')
    print normalize_interfaces(r"Tun1001", 'cisco')
    print normalize_interfaces(r"Ethernet3/2/1", 'eos')

    ''' alternate vendor, only supported by eos  '''
    print normalize_interfaces(r"Ether3/4", 'eos')

    ''' test reverse and if not found'''
    print normalize_interfaces(r"Eth1/1", 'cisco', True)
    print normalize_interfaces(r"NewUnknown_int1/1", 'cisco')

def mysplit(s):
    ''' simple fuction to split on first digit match'''
    head = s.rstrip(r'/\0123456789')
    tail = s[len(head):]
    return head, tail

def normalize_interfaces (interface, vendor, reverse=False):

    ''' define dictionary and assign list to each potential, the first element is the full and the last is the reverse shorthand (always)'''
    all_interfaces = {}
    all_interfaces['GigabitEthernet'] = ['GigabitEthernet' 'GigEthernet' 'GigEth' 'GE' 'Gi']
    all_interfaces['Ethernet'] = ['Ethernet' , 'Eth', 'Et']
    ''' alternate way to buiid list '''
    all_interfaces['FastEthernet'] = 'FastEthernet FastEth Fast FE Fa'.split()
    all_interfaces['Tunnel'] = 'Tunnel Tun Tu'.split()

    ''' Per Vendor attributes'''
    if vendor == 'eos':
        ''' add Ether only if eos'''
        all_interfaces['Ethernet'] = ['Ethernet' , 'Ether', 'Eth', 'Et']
    elif vendor == 'cisco':
        ''' bogus, just to show elif '''
        all_interfaces['FastEthernet'] = 'FastEthernet FastEth Fast FE Fa'.split()

    strip_interface = mysplit(interface)
    interface_type = strip_interface[0]
    interface_number = strip_interface[1]

    ''' go through dictionary and each list within value pair, if match, pull out either long or short form '''
    for key, value in all_interfaces.items():
        for current_interface in value:
            if current_interface == interface_type:
                if reverse:
                    return value.pop() + str(interface_number)
                else:
                    return all_interfaces[key][0] + str(interface_number)
    ''' if nothing matched, at least return the original'''
    return interface


if __name__ == "__main__":
    main()
