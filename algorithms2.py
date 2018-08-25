table1 = {2: [1, 2, False, 0, 0], 3: [4, 3, False, 0, 0], 6: [16, 6, False, 0, 0], 7: [16, 7, False, 0, 0]}
table2 = {1: [1, 1, False, 0, 0], 3: [3, 3, False, 0, 0]}
table3 = {2: [3, 2, False, 0, 0], 4: [4, 4, False, 0, 0]}
table4 = {3: [4, 3, False, 0, 0], 5: [2, 5, False, 0, 0], 7: [6, 7, False, 0, 0]}
table5 = {4: [2, 4, False, 0, 0], 6: [1, 6, False, 0, 0]}
table6 = {1: [5, 1, False, 0, 0], 5: [1, 5, False, 0, 0]}

packet1 = {'header': [2, 2, 1], 'entry': [(1, 2), (5, 6), (8, 7)]}
packet2 = {'header': [2, 2, 2], 'entry': [(16, 1), (3, 3)]}
packet3 = {'header': [2, 2, 3], 'entry': [(3, 2), (4, 4)]}
packet4 = {'header': [2, 2, 4], 'entry': [(4, 3), (2, 5), (6, 7)]}
packet5 = {'header': [2, 2, 5], 'entry': [(2, 4), (1, 6)]}
packet6 = {'header': [2, 2, 6], 'entry': [(5, 1), (16, 5)]}



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

router_id = 1
routing_table = routing_algorithms(table1, packet2)
print(routing_table)