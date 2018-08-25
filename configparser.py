import re

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
    print(lines)
    
    for i in range(1,len(lines[1]) - 1):
        input_ports.append(int(lines[1][i]))
    
    print(input_ports)
    
    for n in range(1,len(lines[2])):
        line = lines[2][n]
        
        output = re.split('-',line)
        output_port = int(output[0])
       
        metric = int(output[1])
        dest_id = int(output[2])
        output_ports[output_port] = dest_id   
        next_hop = dest_id
        flag = False
        time_out = 0
        garbage_time = 0
        table[dest_id] = [metric, next_hop, flag, time_out, garbage_time]
    
    return table

table = configParser('router1.cfg')
print(table)