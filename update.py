table1 = {2: [1, 2, False, 0, 0], 6: [5, 6, False, 0, 0], 7: [8, 7, False, 0, 0]}
table2 = {1: [1, 1, False, 0, 0], 3: [3, 3, False, 0, 0]}
table3 = {2: [3, 2, False, 0, 0], 4: [4, 4, False, 0, 0]}
table4 = {3: [4, 3, False, 0, 0], 5: [2, 5, False, 0, 0], 7: [6, 7, False, 0, 0]}
table5 = {4: [2, 4, False, 0, 0], 6: [1, 6, False, 0, 0]}
table6 = {1: [5, 1, False, 0, 0], 5: [1, 5, False, 0, 0]}

def print_rtable(table):
    '''output format of routing table'''
    width = 12
    #Title of Routing Table
    print('Routing Table of Router : {}'.format(router_id).center(80, ' '))
    print('|' + 'Dst Router'.center(width, ' ') + '|' + 'Metric'.center(width, ' ')
           + '|' + 'Next Hop'.center(width, ' ') + '|' + 'Change Flag'.center(width, ' ')
           + '|' + 'Time Out'.center(width, ' ') + '|' + 'Garbage'.center(width, ' ') + '|')
    print('=' * 80)
    
    #Content of Routing Table
    for key in sorted(table.keys()):
        contxt = table[key]
        print('|' + str(key).center(width, ' ') + '|' + str(contxt[0]).center(width, ' ')
               + '|'  + str(contxt[1]).center(width, ' ') + '|' + str(contxt[2]).center(width, ' ')
               + '|' + str(contxt[3]).center(width, ' ') + '|' + str(contxt[4]).center(width, ' ')
               + '|')

def send_packet(message):
    print(message)

def receive_packet(table):
    ndst = [2, 6]
    for i in range(len(ndst)):
        table[ndst[i]][3] = 0
        table[ndst[i]][4] = 0  
    return table

def update_timer(table, time):
    
    for key in sorted(table.keys()):
        if table[key][3] < 30:
            table[key][3] += 1
        else:
            table[key][0] = 16
            garbage_flag = True
        
        if table[key][4] < 24 and garbage_flag == True:
            table[key][4] += 1
            if table[key][4] == 1:
                send(message)
            
            
            

    
import random
import time

message = 'send successed'
router_id = 1
incre_time = 0
rec_flag = False
garbage_flag = False

table = table1

while True: 
    time.sleep(2)
    incre_time += 1 
    
    print('Time is {}'.format(incre_time))
    
    periodic_time = int(random.randint(2, 4))
    print('periodic time : {}'.format(periodic_time))
    
    if incre_time == periodic_time:
        send_packet(message)
        incre_time = 0
        rec_flag = True
  
    else:
        garbage_flag = False
        
        
        for key in list(table):
            if rec_flag == True:
                table[key][3] = 0
                table[key][4] = 0
                garbage_flag = False 
                rec_flag = False                
            
            if table[key][3] < 5 and rec_flag == False:
                table[key][3] += 1
                if table[key][4] == 1:
                    send_packet(message)
                    
            elif table[key][3] >= 5 and int(key) != router_id:
                table[key][0] = 16
                garbage_flag = True
                
            if garbage_flag == True and table[key][4] < 3:
                table[key][4] += 1
        
            elif table[key][4] >= 3:
                del table[key]   
                     

    print_rtable(table)
    