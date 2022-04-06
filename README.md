# conveyor_modbus

Controller for Belcon Mini III series DMH conveyor.

# Requirements

- Windows 10 machine
- Ubuntu machine (for an external machine)
- Python 3.7.3
  - pymodbus>=2.5.3

# Installation

1. Install driver for [DINV U4 cable](https://www.diatrend.com/IFcable/usb/dinv-u4.php)  
   Install USB serial converter from [here](https://www.diatrend.com/download/driver.htm)  
2. Install software  
	`$ git clone git@github.com:takuya-ki/conveyor_modbus.git; cd conveyor_modbus`  
	`$ pip install -r requirements.txt`

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

1. Set NET mode

# Usage examples
### Directly commanding on a Windows 10 machine (ip address: 169.0.0.1, subnet mask: 255:255:255:0)

1. Connect [DINV U4 cable](https://www.diatrend.com/IFcable/usb/dinv-u4.php) between the controller for inverter and your computer.
2. Execute scripts on the Windows 10 machine as below  
	`$ python src/demo_local.py --usbport COM11 --num_repeat 1 --speed high --initial_direction reverse`  
    `$ python src/check_params.py --usbport COM11 --params 160,117,118,120,122,123,124,343,502,549,77,79,551,340`  
    `$ python src/commands.py --usbport COM11 --command_from local`  

### Sending commands from an Ubuntu machine (ip address: 169.0.0.2, subnet mask: 255:255:255:0)

1. Connect [DINV U4 cable](https://www.diatrend.com/IFcable/usb/dinv-u4.php) between the controller for inverter and your computer.
2. Make a local area network via a network hub by connecting between computers and the hub
3. Execute scripts on the Windows 10 machine as below  
    `$ python src/commands.py --usbport COM11 --command_from external --ip 160.0.0.1 --sockport 50007`  
4. Execute scripts on the Ubuntu machine as below  
    `$ python src/demo_external.py --num_repeat 1 --speed high --initial_direction reverse --ip 160.0.0.1 --sockport 50007`  

# Author / Contributor

[Takuya Kiyokawa](https://takuya-ki.github.io/)

# License

This software is released under the MIT License, see [LICENSE](./LICENSE).
