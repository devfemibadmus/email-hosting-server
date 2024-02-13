import socket
import struct

def get_mx_records(domain):
    DNS_SERVER = "8.8.8.8"
    QUERY_CLASS = 0x0001
    QUERY_FLAGS = 0x0100
    QUERY_TYPE_MX = 0x000f
    query_id = 1539
    questions = 1
    header = struct.pack('!HHHHHH', query_id, QUERY_FLAGS, questions, 0, 0, 0)
    formatted_domain = b''
    for part in domain.split('.'):
        formatted_domain += bytes([len(part)]) + part.encode()
    query = header + formatted_domain + b'\x00' + struct.pack('!HH', QUERY_TYPE_MX, QUERY_CLASS)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(query, (DNS_SERVER, 53))
            response = s.recv(1024)
    except socket.error as e:
        print(f"Socket error: {e}")
        return None

    mx_records = []
    offset = 12 + len(formatted_domain) + 4
    while offset < len(response):
        if response[offset] & 0xc0 == 0xc0:
            pointer_offset = struct.unpack('!H', response[offset:offset + 2])[0] & 0x3fff
            offset = pointer_offset
        else:
            length = response[offset]
            mx_records.append(response[offset + 1:offset + 1 + length])
            offset += 1 + length

    return mx_records

domain = "geeksforgeeks.org"
print(f"MX record for {domain}: {get_mx_records(domain)}")