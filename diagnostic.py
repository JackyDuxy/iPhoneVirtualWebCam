# # from scapy.all import conf

# # conf.ifaces.show()

# from scapy.all import ARP, Ether, srp
# import socket

# phone_ip = "192.168.0.87"

# arp = ARP(pdst=phone_ip)
# ether = Ether(dst="ff:ff:ff:ff:ff:ff")

# packet = ether / arp

# answered, unanswered = srp(
#     packet,
#     timeout=5,
#     verbose=True
# )

# for sent, received in answered:
#     print("FOUND!")
#     print("IP:", received.psrc)
#     print("MAC:", received.hwsrc)

# hostname = socket.gethostname()
# local_ip = socket.gethostbyname(hostname)

# pointIndicator = local_ip.rfind('.')
# network = local_ip[:pointIndicator + 1]

# print("PC:", local_ip)
# print("Network:", network + "0/24")

# from scapy.all import conf

# print("Scapy interface:", conf.iface)
# print("Scapy IP:", conf.iface.ip)

import socket
from scapy.all import ARP, Ether, srp, conf

# CHANGE THIS to your iPhone's actual IP
phone_ip = "192.168.0.87"

# Get Scapy's current interface
interface = conf.iface
local_ip = conf.iface.ip

print("Interface:", interface)
print("PC IP:", local_ip)
print("Phone IP:", phone_ip)
print()

# First: test the phone directly
print("Testing phone directly...")

arp = ARP(pdst=phone_ip)
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
packet = ether / arp

answered, _ = srp(
    packet,
    iface=interface,
    timeout=3,
    verbose=False
)

if answered:
    for _, received in answered:
        print("PHONE FOUND!")
        print("IP:", received.psrc)
        print("MAC:", received.hwsrc)
else:
    print("Phone NOT found.")
    
print()

# Now determine the subnet FROM THE PHONE'S IP
pointIndicator = phone_ip.rfind('.')
network = phone_ip[:pointIndicator + 1]
target = network + "0/24"

print("Scanning:", target)
print()

# Scan entire subnet
arp = ARP(pdst=target)
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
packet = ether / arp

answered, _ = srp(
    packet,
    iface=interface,
    timeout=5,
    verbose=False
)

for _, received in answered:

    ip = received.psrc
    mac = received.hwsrc

    try:
        name = socket.gethostbyaddr(ip)[0]
    except:
        name = "Unknown"

    print(
        "IP:", ip,
        "| MAC:", mac,
        "| Name:", name
    )

print()
print("Found", len(answered), "devices.")
print("Scan complete.")
