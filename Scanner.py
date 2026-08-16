import socket
from scapy.all import ARP, Ether, srp, conf

# Get Scapy's active interface and local IP
interface = conf.iface
local_ip = conf.iface.ip

# Get network portion
pointIndicator = local_ip.rfind('.')
network = local_ip[:pointIndicator + 1]

print("Interface:", interface)
print("Local IP:", local_ip)
print("Scanning:", network + "1-254")
print()

devices = []

# Scan each IP individually
for i in range(1, 255):

    ip = network + str(i)

    # ARP request for ONE specific IP
    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    answered, _ = srp(
        packet,
        iface=interface,
        timeout=0.2,
        verbose=False
    )

    for _, received in answered:

        device_ip = received.psrc
        mac = received.hwsrc

        try:
            name = socket.gethostbyaddr(device_ip)[0]
        except (socket.herror, socket.gaierror):
            name = "Unknown"

        devices.append({
            "ip": device_ip,
            "mac": mac,
            "name": name
        })

        print(
            "IP:", device_ip,
            "| MAC:", mac,
            "| Name:", name
        )

print()
print("Found", len(devices), "devices.")
print("Scan complete.")