import struct
import socket
import select
import re
import json

Format = 'iii'

HOST = '127.0.0.1'

output_ports = {}
input_ports = []    

def configParser(filename):
    '''Read the config file and construct the routing table'''
    lines = []
    table = {}

    file = open(filename, 'r')
    for line in file.readlines():
        line = re.split(', | |\n',line)
        lines.append(line)
    router_id = lines[0][1]
    
    print(lines[1])
    
    for i in range(1,len(lines[1]) - 1):
        input_ports.append(int(lines[1][i]))
    
    for n in range(1,len(lines[2])):
        line = lines[2][n]
        output = line.split('-')
        output_port = int(output[0])
        metric = int(output[1])
        dest_id = int(output[2])
        output_ports[output_port] = dest_id   
        next_hop = dest_id
        flag = False
        timers = [0,0]
        table[dest_id] = [metric, next_hop, flag,timers]
    print('input ports : {},\noutput ports : {}'.format(input_ports, output_ports))
    return table

def rip_header(router_id):
    '''the header of rip packet'''
    command = 2
    version = 2
    source = int(router_id)
    print("RIP Header : command {}, version {}, source {}".format(command, version, source))
    header = [command, version, source]
    return header

def rip_entry(table):
    '''the entry of rip packet'''
    entry = []
    for dst in table.keys():
        metric = table[dst][0]
        print("RIP Entry : metric {}, destination {}".format(metric, dst))
        entry.append((metric, dst))     
    return entry

def rip_packet(header, entry):
    '''pack header and every entry together'''
    packet = {}
    packet['header'] = header
    packet['entry'] = entry
    return packet

def listen_packet(input_ports):
    '''listen all the input port'''
    listen_table = []
    for port in input_ports:
        inSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        inSock.bind(('0.0.0.0', port))
        listen_table.append(inSock)
    return listen_table

def send_packet(packet, output_ports):
    '''send packet to destination router'''
    for port in output_ports.keys():
        print('port', port)
        outSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        outSock.sendto(packet, ("0.0.0.0", port))
    return 'packet send successed'

def routing_algorithms(table, packet):
    '''return a format of current routing table'''
    #initilize received routing table
    dst = table.keys()
    ndst = []
    for i in packet['entry']:
        ndst.append(i[1])
        i[0] += 1
        i[1] = packet['header'][2] 

    #produrce routing table
    for j in range(len(ndst)):
        if ndst[j] not in dst:
            table[ndst[j]] = rec_packet['entry'][j]
        
        for k in dst:
            if k == ndst[j]:
                if table[k][1] == rec_packet['entry'][j][1]:
                    table[k] = rec_packet['entry'][j]
                    
                elif table[k][0] > rec_packet['entry'][j][0]:
                    table[k] = rec_packet['entry'][j]

    return table

def receive_packet(listen_list, packet):
    '''receive packet from source router'''
    r, w, e = select.select(listen_list, [], [], 30)
    if r != []:
        sock = r[0]
        unpacked_packet, address = sock.recvfrom(2048)
        rev_packet = json.loads(unpacked_packet) 
        new_table = routing_algorithms(table, rev_packet)
        
    return new_table


filename = 'router4.cfg'
router_id = filename[6]

table = configParser(filename)
print('table : {}'.format(table))

header = rip_header(router_id)
entry = rip_entry(table)
packet = rip_packet(header, entry)

print('packet: {}'.format(packet))

packed_packet = json.dumps(packet)
print('packed_packet : {}'.format(packed_packet))

listen_list = listen_packet(input_ports)
print('listen list : {}'.format(listen_list))

send_packet(packed_packet, output_ports)

rev_packet = receive_packet(listen_list, packed_packet)
print('receive packet : {}'.format(rev_packet))

