import struct

Format = 'I3sf'
def RIP_Header(router_id):
    command = '2'
    version = '2'
    source = router_id
    header = str(command) + ', ' + version + ', ' + str(source)
    packed_header = struct.pack(Format, int(command), version, source)
    unpacked_header = struct.unpack(Format, packed_header)
    print("RIP Header : command {}, version {}, source {}".format(command, version, source))
    return packed_header, header, unpacked_header

def RIP_Entry(table):
    address = table['output'][0:4]
    metric = table['output'][5]
    next_hop = table['output'][7]
    print(address, metric, next_hop)
    if int(metric) < 0 and int(metric) >= 16:
        raise ValueError
    entry = address + ', ' + metric + ', ' + next_hop
    packed_entry = struct.pack(Format, int(address), metric, int(next_hop))
    unpacked_entry = struct.unpack(Format, packed_entry)
    print("RIP Entry : address {}, metric {}, next_hop {}".format(address, metric, next_hop))
    return packed_entry, entry, unpacked_entry
    
print(RIP_Header(5))

table = {'output':'1025-4-5'}
print(RIP_Entry(table))