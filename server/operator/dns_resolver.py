import socket
import struct

class DomainResolver:
    def __init__(self, dns_server='8.8.8.8'):
        self.DNS_SERVER = dns_server
        self.QUERY_CLASS = 0x0001
        self.QUERY_FLAGS = 0x0100
        self.QUERY_TYPE_MX = 0x000f
        self.QUERY_TYPE_TXT = 0x0010
        self.QUERY_TYPE = self.QUERY_TYPE_MX
    
    def domain_existence(self,domain):
        try:
            socket.gethostbyname(domain)
            return True
        except socket.error:
            return False

    def get_mx_records(self, domain):
        query_id = 1234
        questions = 1
        header = struct.pack('!HHHHHH', query_id, self.QUERY_FLAGS, questions, 0, 0, 0)
        formatted_domain = b''
        for part in domain.split('.'):
            formatted_domain += bytes([len(part)]) + part.encode()
        query = header + formatted_domain + b'\x00' + struct.pack('!HH', self.QUERY_TYPE, self.QUERY_CLASS)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.sendto(query, (self.DNS_SERVER, 53))
                response = s.recv(1024)
        except socket.error as e:
            print(f"Socket error: {e}")
            return None
        mx_records = []
        offset = 12 + len(formatted_domain) + 4
        while offset < len(response) and response[offset] != 0:
            if response[offset] & 0xc0 == 0xc0:
                pointer_offset = struct.unpack('!H', response[offset:offset + 2])[0] & 0x3fff
                offset = pointer_offset
            else:
                length = response[offset]
                mx_records.append(response[offset + 1:offset + 1 + length])
                offset += 1 + length
        return mx_records

    def resolve_domain(self, domain):
        mx_records = self.get_mx_records(domain) if self.domain_existence(domain) else None

        if mx_records and mx_records != None:
            decoded_records = []
            try:
                for exdata in mx_records:
                    if exdata[0] & 0xc0 != 0xc0:
                        decoded_records.append(exdata.decode())
                if decoded_records:
                    decoded_records = decoded_records[1:]
                    mx_record = '.'.join(decoded_records)
                    return mx_record
                else:
                    return None
            except Exception as e:
                print(f"Error {domain} decode_records {decoded_records} error {e}")
                return None
        else:
            return None

