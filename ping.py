import subprocess
import ipaddress
import os
import concurrent.futures
import socket
import netifaces  
import numpy as np
import matplotlib.pyplot as plt
from hilbertcurve.hilbertcurve import HilbertCurve

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS 
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Error retrieving local IP: {e}")
        return None

def get_subnet_mask():
    try:
        interfaces = netifaces.interfaces()
        for iface in interfaces:
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs:  # Look for IPv4 addresses
                ip_info = addrs[netifaces.AF_INET][0]
                local_ip = ip_info["addr"]
                subnet_mask = ip_info["netmask"]
                if not local_ip.startswith("127."):  # Exclude loopback
                    return local_ip, subnet_mask
    except Exception as e:
        print(f"Error retrieving subnet mask: {e}")
    return None, None

def get_network():
    local_ip, subnet_mask = get_subnet_mask()
    
    if local_ip and subnet_mask:
        try:
            network = ipaddress.IPv4Network(f"{local_ip}/{subnet_mask}", strict=False)
            return network
        except ValueError as e:
            print(f"Invalid network detected: {e}")
            return None
    else:
        print("Failed to determine network.")
        return None

network = get_network()
if not network:
    print("Network detection failed. Exiting.")
    exit(1)  

print(f"Detected Network: {network}")
ip_list = list(network.hosts())  

# Use a Hilbert curve to map the network range into a grid
num_ips = len(ip_list)
curve_order = int(np.ceil(np.log2(np.sqrt(num_ips))))  # dynamic adjust 
hilbert = HilbertCurve(curve_order, 2)

# results
active_ips = []
inactive_ips = []

def ping_ip(ip):
    ip_str = str(ip)
    ping_cmd = ['ping', '-c', '1', '-W', '1', ip_str] if os.name != 'nt' else ['ping', '-n', '1', ip_str]
    response = subprocess.run(ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return ip_str, response.returncode == 0  # True if ping succeeds

# Use threading to speed up scanning
cpu_count = os.cpu_count()
with concurrent.futures.ThreadPoolExecutor(cpu_count * 2) as executor:
    results = executor.map(ping_ip, ip_list)

# Process results
for ip, is_active in results:
    ip_int = int(ipaddress.IPv4Address(ip)) - int(ipaddress.IPv4Address(ip_list[0]))  
    x, y = hilbert.points_from_distances([ip_int])[0]  # Convert to 2D coordinate
    
    if is_active:
        active_ips.append((x, y))
        print(f"{ip} is in use!")
    else:
        inactive_ips.append((x, y))
        print(f"{ip} is silent...")


plt.figure(figsize=(8, 8), facecolor='black')  
ax = plt.gca()
ax.set_facecolor('black')  
plt.scatter(*zip(*inactive_ips), c='gray', label="Inactive", marker='s', s=40, alpha=0.6)  
plt.scatter(*zip(*active_ips), c='lime', label="Active", marker='s', s=40, alpha=0.8)  
plt.legend(frameon=False, fontsize=12, loc="upper left", facecolor="black", edgecolor="white", labelcolor="white")
plt.title("Hilbert Curve Visualization of Network IPs", color='white')
plt.grid(color='gray', linestyle='--', linewidth=0.3, alpha=0.4)  
plt.xticks([])  
plt.yticks([])
plt.show()
