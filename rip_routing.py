import socket
import re
import select
import json
import time
import random
import sys
from copy import deepcopy
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

    for i in range(1,len(lines[1]) - 1):
        if int(lines[1][i]) in range(1024, 64000) and int(lines[1][i]) not in input_ports:
            input_ports.append(int(lines[1][i]))      
        else:
            print('Invalid port number')
            break
        
    for n in range(1,len(lines[2])):
        line = lines[2][n]
        output = line.split('-')
        output_port = int(output[0])
        metric = int(output[1])
        dest_id = int(output[2])
        if output_port in range(1024, 64000) and output_port not in output_ports.keys():
            output_ports[output_port] = dest_id 
        else:
            print('Invalid port number')
            break        
        next_hop = dest_id
        flag = False
        time_out = 0
        garbage_time = 0
        table[dest_id] = [metric, next_hop, flag, time_out, garbage_time]
    
    return table
    
def routing_algorithms(table, packet):
    '''return a format of current routing table'''
    #initilize received routing table
    dst = table.keys()
    ndst = []
    for k in packet['entry']:
        ndst.append(k[1])
    src = packet['header'][2]
    
    if src not in table.keys():
        for m in range(len(packet['entry'])):
            if packet['entry'][m][1] == router_id:
                table[src] = [packet['entry'][m][0], src, False, 0, 0]
    
    else:
        #produrce routing table
        for i in range(len(ndst)):
            if ndst[i] != router_id:
                next_hop = src
                metric = min(table[src][0] + packet['entry'][i][0], 16) 
                
                if ndst[i] not in dst:
                    if metric < 16:
                        table[ndst[i]] = [metric, next_hop, False, 0, 0]
                    elif metric == 16:
                        continue
                    
                elif next_hop == table[ndst[i]][1]:
                    if table[ndst[i]][0] == metric and metric == 16:
                        continue
                    else:
                        table[ndst[i]][0] = metric
                        table[ndst[i]][3] = 0
                        table[ndst[i]][4] = 0
                        table[ndst[i]][2] = False
                    
                elif metric < table[ndst[i]][0]:
                    table[ndst[i]][0] = metric
                    table[ndst[i]][1] = next_hop 
            else:
                for m in range(len(packet['entry'])):
                    if packet['entry'][m][1] == router_id:
                        table[src][2] = False
                        table[src][3] = 0
                        table[src][4] = 0                        
                        if packet['entry'][m][0]< 16:
                            table[src] = [packet['entry'][m][0], src, False, 0, 0]
                        else:
                            continue                    
    return table
    
def rip_header(router_id):
    '''the header of rip packet'''
    command = 2
    version = 2
    source = int(router_id)
    #print("RIP Header : command {}, version {}, source {}".format(command, version, source))
    header = [command, version, source]
    return header

def rip_entry(table):
    '''the entry of rip packet'''
    entry = []
    for dst in table.keys():
        metric = table[dst][0]
        #print("RIP Entry : metric {}, destination {}".format(metric, dst))
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
        inSock.bind(('', port))
        listen_table.append(inSock)
    return listen_table

def poison(table, output_ports, port):
    '''posion packet with metric set to 16'''    
    for routing_info in table.values():
        if output_ports[port] == routing_info[1]:
            routing_info[0] = 16
    return table

def send_packet1(table):
    '''send packet to destination router'''
    header = rip_header(router_id)
    entry = rip_entry(table)
    packet = rip_packet(header, entry)
    json_packet = json.dumps(packet).encode('utf-8')    
    for port in output_ports.keys():
        outSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        outSock.sendto(json_packet, ('0.0.0.0', port))
    print('first packet send')

def send_packet2(table, output_ports):
    '''send packet to destination router with poison'''
    for port in output_ports.keys():
        p_table = deepcopy(table)   #make a copy of router's own table and only modify the copied table
        s_table = poison(p_table, output_ports, port)
        header = rip_header(router_id)
        entry = rip_entry(s_table)
        packet = rip_packet(header, entry)
        json_packet = json.dumps(packet).encode('utf-8')        
        outSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        outSock.sendto(json_packet, ('0.0.0.0', port))
    print('packet sent successful')

def valid_packet(packet):
    '''check if content in received packet is well formatted'''
    isValid = True
    if int(packet['header'][0])!= 2: isValid=False
    elif int(packet['header'][1])!= 2: isValid = False
    elif int(packet['header'][2]) not in range(1,64000): isValid = False
    for i in packet['entry']:
        if int(i[0]) > 16: isValid = False
        elif int(i[1]) not in range(1, 64000): isValid = False
    return isValid

def receive_packet(listen_list, table):
    '''receive packet from source router'''
    new_table = table
    r, w, e = select.select(listen_list, [], [], 1)
    if r != []:
        sock = r[0]
        unpacked_packet, address = sock.recvfrom(2048)
        json_packet = unpacked_packet.decode('utf-8')
        rec_packet = json.loads(json_packet)
        print('Received:')
        print(rec_packet)        
        isValid = valid_packet(rec_packet)
        if isValid == True:
            new_table = routing_algorithms(table, rec_packet)
        else:
            print('Invalid packet.Dropped')
            new_table = table
    return new_table

  
def print_rtable(table):
    '''output format of routing table'''
    dst_routers = sorted(table.keys())
    width = 12
    #Title of Routing Table
    print('Routing Table of Router : {}'.format(router_id).center(80, ' '))
    print('|' + 'Dst Router'.center(width, ' ') + '|' + 'Metric'.center(width, ' ')
           + '|' + 'Next Hop'.center(width, ' ') + '|' + 'Time Out'.center(width, ' ') 
           + '|' + 'Garbage'.center(width, ' ') + '|')
    print('=' * 80)
    
    #Content of Routing Table
    for key in dst_routers:
        contxt = table[key]
        print('|' + str(key).center(width, ' ') + '|' + str(contxt[0]).center(width, ' ')
               + '|'  + str(contxt[1]).center(width, ' ') + '|' + str(contxt[3]).center(width, ' ')
               + '|' + str(contxt[4]).center(width, ' ') + '|')
    
def rip_routing(filename):
    '''running function'''
    incre_time = 0
    
    #read the routing table from config file
    routing_table = configParser(filename)
    #print('table = {}'.format(routing_table))
    
    send_packet1(routing_table)
    
    #put all the input ports in the listen list
    listen_list = listen_packet(input_ports)
    
    periodic_time = int(random.randint(24, 36)) # 0.8 of 30 seconds and 1.2 of 30 seconds
   # periodic_time = int(random.randint(2, 10)) # used for testing
 
    #procedure receive packet 
    while True:
        #time.sleep(1)
           
        incre_time += 1
     #   print(time.time())
      #  print('Time is {} second'.format(incre_time))
        
        
        print_rtable(routing_table)   
        
        if incre_time == periodic_time:
            send_packet2(routing_table, output_ports)
            incre_time = 0    
        
        for key in sorted(routing_table.keys()):
            if routing_table[key][3] < 180:
            #if routing_table[key][3] < 20: #used for testing

                routing_table[key][3] += 1
            else:
                routing_table[key][0] = 16
                routing_table[key][2] = True
            
            if routing_table[key][2] == True:
                routing_table[key][4] += 1
                if routing_table[key][4] == 1:
                    send_packet2(routing_table, output_ports)
            
                elif routing_table[key][4] > 120:
              #  elif routing_table[key][4] > 16: #used for testing
            
                    del routing_table[key]
        
        routing_table = receive_packet(listen_list, routing_table)
 

    
filename = sys.argv[1]
router_id = int(filename[6])
rip_routing(filename)