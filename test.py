import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

if len(ports) > 0:
    print("可用串口:")
    for port, desc, hwid in sorted(ports):
        print(f"{port} - {desc}")
else:
    print("没有可用的串口")
