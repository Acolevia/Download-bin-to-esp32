# Download bin to esp32

* 批量下载 bin 固件到 esp32

* 自动找到 Windows 下标识为 `USB-SERIAL CH340` 的串口，进行烧录

* 支持多串口同时烧录

* 串口烧录成功之后，除非串口断开重连，否则不会继续烧录

## requirement

```
pip install -r requirement.txt
```

## run

```
python main.py
```
