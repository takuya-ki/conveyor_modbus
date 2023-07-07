# conveyor_modbus

[![support level: community](https://img.shields.io/badge/support%20level-community-lightgray.svg)](http://rosindustrial.org/news/2016/10/7/better-supporting-a-growing-ros-industrial-software-platform)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Controller for [Belcon Mini III series DMH](https://www.okurayusoki.co.jp/eng/product/conveyor/lightweight/belcon_mini/) conveyor of Okura Yusoki.

# Requirements

- Windows 10 machine
- Ubuntu machine (for an external machine)
- Python 3.7.3
  - pyserial==3.5
  - pymodbus==2.5.3

# Installation

1. Install driver for [DINV U4 cable](https://www.diatrend.com/IFcable/usb/dinv-u4.php)  
   Install USB serial converter from [here](https://www.diatrend.com/download/driver.htm)  
2. Install software  
```bash
git clone https://github.com/takuya-ki/conveyor_modbus.git --depth 1
cd conveyor_modbus; pip install -r requirements.txt
```

### Setting of inverter controller

1. Set parameters as below (For the deteil of parameters, please refer to manual.)  

|  Number  |  Value  |
| ---- | ---- |
|  Pr. 160  |  0  |
|  Pr. 117  |  1  |
|  Pr. 118  |  192  |
|  Pr. 120  |  2  |
|  Pr. 122  |  9999 (65535)  |
|  Pr. 123  |  9999 (65535)  |
|  Pr. 124  |  1  |
|  Pr. 343  |  0  |
|  Pr. 502  |  0  |
|  Pr. 549  |  1  |
|  Pr. 77  |  2  |
|  Pr. 79  |  0  |
|  Pr. 551  |  9999 (65535)  |
|  Pr. 340  |  1  |

2. Set NET mode


# Usage examples
## Preparations

#### 1. Check the port numer with device manager (e.g. COM3)  
<img src=image/device_manager.png width=500>  

#### 2. Connect [DINV U4 cable](https://www.diatrend.com/IFcable/usb/dinv-u4.php) between the controller for inverter and your computer.
<img src=image/connection.jpg width=200>  

## Directly commanding on a Windows 10 machine (ip address: 169.0.0.1, subnet mask: 255:255:255:0)
#### 1. Change the network connection setting of the ethernet adaptor  
<img src=image/network_windows.png width=400>  

#### 2. Execute scripts (Check no objects on the conveyor!)  
```bash
python src/demo.py --num_repeat 1 --speed high --initial_direction reverse
```
```bash
python src/check_params.py --params 160,117,118,120,122,123,124,343,502,549,77,79,551,340
```
```bash
python src/commands.py --command_from local
```

## Sending commands from an Ubuntu machine (ip address: 169.0.0.2, subnet mask: 255:255:255:0)

1. Make a local area network via a network hub by connecting between computers and the hub  
<img src=image/network_ubuntu.png width=400>  

2. Execute scripts on the Windows 10 machine as below (Check no objects on the conveyor!)  
```bash
python src/commands.py --command_from external --ip 169.0.0.1 --sockport 50007
```

#### Programmed demonstration  
3. Execute scripts on the Ubuntu machine as below (Check no objects on the conveyor!)  
```bash
python src/demo_external.py --num_repeat 1 --speed high --initial_direction reverse --ip 169.0.0.1 --sockport 50007
```

#### User's input commands  
3. Execute scripts on the Ubuntu machine as below (Check no objects on the conveyor!)  
```bash
python src/commands_external.py --ip 169.0.0.1 --sockport 50007
```

# Author / Contributor

[Takuya Kiyokawa](https://takuya-ki.github.io/)

# License

This software is released under the MIT License, see [LICENSE](./LICENSE).
