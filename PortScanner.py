import socket
import threading

while True:

    selection = input("do you want to scan a range of ports or specific ports (ra/sp): ").lower()

    while selection not in ["ra","sp"]:
        print("invalid input, try agin")
        selection = input("do you want to scan a range of ports or specific ports (ra/sp): ").lower()

    if selection == "ra":
        print("you selected range")
    elif selection == "sp":
        print("you selected specific")

    if selection == "ra":
        host = input("enter IP or domian: ")
        start_port = int(input("start port: "))
        end_port = int(input("end port: "))
        port_range = range(start_port, end_port +1)

    if selection == "sp":
        host = input("enter IP or domian: ")
        specific_ports = input("enter ports you want to scan seperated by comas: ")
        seperated_ports = specific_ports.split(",")
        numports = [int(x) for x in seperated_ports]

    if selection == "ra":
        ports_to_scan = port_range

    if selection == "sp":
        ports_to_scan = numports

    ops = []
    lock = threading.Lock()
    def scan_port (port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((host,port))
        with lock:
            print("checking port: ", port)
            if result == 0:
                print(f"port {port} is open")
                ops.append(port)
            else:
                print("port is closed")
        s.close()

    thread = []
    for port in ports_to_scan:
        t = threading.Thread(target=scan_port, args=(port,))
        thread.append(t)
        t.start()

    for t in thread:
        t.join()

    print("Scan complete")
    print(f"Open ports on {host}:")
    if ops:
        for port in ops:
            print(f"→ {port}")
    else:
        print("no open ports")

    repeat = input("whould like to scan again (yes/No): ").lower()
    if repeat == "no":
        break
