import subprocess
import serial.tools.list_ports
import time
import threading

# 定义bin文件路径
bin_file = "./folotoy-23.38.1.2-increaseJsonSize.bin"  # 修改为你的bin文件路径

# 用一个集合来存储已经成功烧录的串口
burned_ports = set()


# 定义一个函数，用于检测串口连接状态
def check_connection():
    global burned_ports
    while True:
        for port in burned_ports.copy():  # 使用副本以防止在迭代时修改
            try:
                ser = serial.Serial(port, baudrate=9600, timeout=1)
                ser.close()  # 成功连接后关闭串口
            except serial.SerialException:
                print(f"串口连接异常: {port}")
                burned_ports.remove(port)  # 从集合中移除断开的串口

        time.sleep(5)  # 控制检测频率


# 启动检测连接的线程
connection_thread = threading.Thread(target=check_connection)
connection_thread.start()


# 定义一个函数，用于烧录操作
def flash_device(port):
    command = f'esptool --chip esp32 --port {port} --baud 921600 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size detect 0x00 {bin_file}'

    try:
        # 执行命令
        subprocess.run(command, shell=True, check=True)
        print(f"成功烧写到串口 {port}")
        burned_ports.add(port)  # 记录成功烧录的串口
    except subprocess.CalledProcessError as e:
        print(f"烧写到串口 {port} 失败，错误信息：{e}")


while True:
    # 获取所有可用串口信息
    available_ports = serial.tools.list_ports.comports()

    # 找到desc为"USB-SERIAL CH340"的设备
    ch340_ports = [port.device for port in available_ports if "USB-SERIAL CH340" in port.description]

    # 排除已经成功烧录的串口
    ch340_ports = [port for port in ch340_ports if port not in burned_ports]

    # 如果找到了符合条件的串口，就执行烧录命令
    if ch340_ports:
        threads = []

        # 遍历每个符合条件的串口，创建一个线程并启动
        for port in ch340_ports:
            thread = threading.Thread(target=flash_device, args=(port,))
            threads.append(thread)
            thread.start()

        # 等待所有线程执行完毕
        for thread in threads:
            thread.join()

    else:
        print("未找到符合条件的串口设备，等待中...")

    time.sleep(5)  # 等待5秒后重新检查
