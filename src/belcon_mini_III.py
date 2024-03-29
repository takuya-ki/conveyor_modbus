#!/usr/bin/env python3

import time

import serial
from serial.tools import list_ports
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


class DMH():

    def __init__(self, usbport):
        if usbport is None:
            usbport = self.select_port()
        self.client = ModbusClient(
            method="rtu",
            port=usbport,
            stopbits=1,
            bytesize=8,
            parity='E',
            baudrate=19200,
            timeout=3,
            strict=False)
        self._max_freq_hz = 40000
        self.open_connection()

    def open_connection(self):
        """Opens the connection with a conveyor."""
        self.client.connect()

    def close_connection(self):
        """Closes the connection with the conveyor."""
        self.client.close()

    def select_port(self):
        """Selects a port."""
        ports = list_ports.comports()
        devices = [info.device for info in ports]

        if len(devices) == 0:
            print("Error: any devices not found")
            return None
        elif len(devices) == 1:
            print("%s is only found" % devices[0])
            selected_port = devices[0]
        else:
            for i in range(len(devices)):
                print("input %3d: open %s" % (i, devices[i]))
            print("input number of target port >> ", end="")
            num = int(input())
            selected_port = devices[num]

        return selected_port

    def get_status(self):
        """Reads current device status.
        This status field indicates the status of the conveyor and its motion.
        It is composed of 16 flags, described in the table below.
        Bit      Name                  Description
        0 (LSB): RUN                   1 when the inverter is in operation.
        1:       normal                1 when it is driven by normal rotation.
        2:       reverse               1 when it is driven by reverse rotation.
        3:       SU (reach freq)       1 when it reached target frequency.
        4:       OL (overload)         1 when it detects overload.
        5:       reserved              Not used. Always 0.
        6:       FU (detect freq)      1 when it detects frequency of Pr.42/43.
        7:       ABC (abnormal)        1 when it detects abnormal state.
        8:       reserved              Not used. Always 0.
        9:       SO (safety monitor)   1 when the safety stop is in operation.
        10 - 14: reserved              Not used. Always 0.
        15:      Abnormal occurrence   1 when an abnormal state is detected.
        """
        # address   : register number
        # count     : number of registers to be read
        # unit      : slave device address
        result = self.client.read_holding_registers(
            address=8, count=1, unit=1)
        status = format(result.registers[0], '016b')
        status_list = [0] * 16
        if int(status[-1]):
            print("RUN (in operation).")
            status_list[0] = 1
        if int(status[-2]):
            print("Normal rotation.")
            status_list[1] = 1
        if int(status[-3]):
            print("Reverse rotation.")
            status_list[2] = 1
        if int(status[-4]):
            print("Reached target frequency.")
            status_list[3] = 1
        if int(status[-5]):
            print("Overload was detected.")
            status_list[4] = 1
        if int(status[-7]):
            print("Overed frequency threshold (Pr. 42/43).")
            status_list[6] = 1
        if int(status[-8]):
            print("Abnormal state was detected.")
            status_list[7] = 1
        if int(status[-10]):
            print("Safety stop is in operation.")
            status_list[9] = 1
        if int(status[0]):
            print("Abnormal occurrence.")
            status_list[15] = 1

        return status_list

    def get_set_mode(self):
        """Reads current device set mode.
        0: EXT
        1: PU
        2: EXT JOG
        4: NET
        5: PU+ EXT
        """
        # address   : register number
        # count     : number of registers to be read
        # unit      : slave device address
        result = self.client.read_holding_registers(
            address=9, count=1, unit=1)
        mode_label = result.registers[0]
        if int(mode_label) == 0:
            model_str = "EXT"
        elif int(mode_label) == 1:
            model_str = "PU"
        elif int(mode_label) == 2:
            model_str = "EXT JOG"
        elif int(mode_label) == 4:
            model_str = "NET"
        elif int(mode_label) == 5:
            model_str = "PU+ EXT"
        print("Current set mode: " + model_str)

        return mode_label

    def get_set_parameters(self, pnum):
        """Reads parameters set on the inverter controller.
        Parameter number + 41000 = register number.
        """
        # address   : register number
        # count     : number of registers to be read
        # unit      : slave device address
        result = self.client.read_holding_registers(
            address=1000+pnum, count=1, unit=1)
        param_value = result.registers[0]

        return param_value

    def stop(self):
        """Stops operations."""
        # address   : register number
        # values    : data to be written
        # unit      : slave adress
        request = self.client.write_registers(
            address=8, values=[0], unit=1)

    def move(self, direction='normal', speed='low'):
        """Executes normal/reverse rotations with target speed."""
        # address   : register number
        # values    : data to be written
        # unit      : slave adress

        if direction == 'normal':
            set_value = 2
        elif direction == 'reverse':
            set_value = 4
        else:
            print("Select one from normal or reverse for direction.")

        if speed == 'low':
            speed_val = 32
        elif speed == 'middle':
            speed_val = 16
        elif speed == 'high':
            speed_val = 8
        else:
            speed_val = 0
            try:
                self.set_frequency_on_RAM(
                    min(self._max_freq_hz, int(speed)))
            except ValueError:
                print("Select low/middle/high or input frequency.")
                pass

        request = self.client.write_registers(
            address=8, values=[set_value+speed_val], unit=1)

    def set_net_mode(self):
        """Sets inverter operation mode as NET mode."""
        request = self.client.write_registers(
            address=9, values=[6], unit=1)

    def get_actual_frequency(self):
        """Gets realtime frequency."""
        result = self.client.read_holding_registers(
            address=200, count=1, unit=1)
        freq_value = result.registers[0]

        return freq_value

    def get_set_frequency(self):
        """Gets set frequency."""
        result = self.client.read_holding_registers(
            address=204, count=1, unit=1)
        freq_value = result.registers[0]

        return freq_value

    def get_frequency_from_RAM(self):
        """Gets target frequency on RAM."""
        result = self.client.read_holding_registers(
            address=13, count=1, unit=1)
        freq_value = result.registers[0]

        return freq_value

    def set_frequency_on_RAM(self, freq):
        """Sets target frequency on RAM."""
        request = self.client.write_registers(
            address=13, values=[freq], unit=1)

    def set_frequency_on_EEPROM(self):
        """Sets target frequency on EEPROM."""
        request = self.client.write_registers(
            address=14, values=[freq], unit=1)

    def sleep_with_displaying_freq(self, sleep_sec):
        """Sleeps and displays frequency currently set."""
        start = time.time()
        while True:
            time.sleep(0.1)
            print("Frequency: " +
                  str(self.get_actual_frequency()) +
                  " / " +
                  str(self.get_set_frequency()) +
                  " [Hz/100]")
            if (time.time() - start) > sleep_sec:
                break
