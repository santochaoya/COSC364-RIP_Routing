import struct

class Packet:
    def __init__(self, packet_format, ptype, seqno, datalen, data, magicno = "0x497E"):
        self.magicno = magicno 
        self.ptype = ptype # dataPacket (0) or acknowledgementPacket (1)
        self.seqno = seqno # 0 or 1
        self.datalen = datalen # between 0 - 512
        self.packet_format = 'i5sf'
        self.data = data
             
    def header(self):
        '''the header of the RIP packet'''
        command = "2" #'1' for request, '2' for response
        version = "2"
        src = router_id
        header = command + ',' + version + ',' + src
        return "RIP header : command type = {}, version = {}, source = {}".format(self.command,
                                                                                  self.version,
                                                                                sef.src)
    def entry(self):
        '''the routing information of the RIP packet'''
        nxt_hop = table[dst][3] # destination router-id
        metric = table[dst][2] # distance to destination router-id
        return nxt_hop, metric
    
    def encode(self):
        '''Converts input message into bytes stream'''
        packed_data = struct.Struct(self.packet_format)
        encoded = packed_data.pack(self.magicno, self.packet_type, self.seqno, self.dataLen)
        return encoded
    
    def decoder(self):
        '''Converts packed message from bytes stream to string'''
        packet_format = "i5sf"
        decoded = struct.unpack(packet_format, packed_data)
        return decoded
        