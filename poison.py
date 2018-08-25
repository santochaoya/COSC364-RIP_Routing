table = {2: [1, 2, False, 0, 0], 3: [3, 2, False, 0, 0], 6: [5, 6, False, 0, 0], 7: [8, 7, False, 0, 0]}
output_ports = {2201: 2, 6602: 6, 7702: 7}


def poison(table, output_ports):
    for routing_info in table.values():
        if output_ports[port] == routing_info[1]:
            routing_info[0] = 16
    return table

from copy import deepcopy



for port in output_ports.keys():
    p_table = deepcopy(table)
    s_table = poison(p_table, output_ports)
    print(s_table)