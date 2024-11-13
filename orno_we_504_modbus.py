#!/usr/bin/env /home/user/pymodbus/bin/python3
#                     ^
#                     |
#                     `--- change to your username
#
# Install venv:
# sudo apt install python3-venv
#
# Creating venv:
# python3 -m venv ~/pymodbus
# cd ~/pymodbus/bin
# ./pip3 install pymodbus
# ./pip3 install pyserial
#
# --------------------------------------------------------------------------- #
# import the various client implementations
# --------------------------------------------------------------------------- #
import pymodbus.client as ModbusClient
from pymodbus import (
    ExceptionResponse,
    FramerType,
    ModbusException,
    pymodbus_apply_logging_config,
)

if __name__ == "__main__":
    # activate debugging
    #pymodbus_apply_logging_config("DEBUG")

    client = ModbusClient.ModbusSerialClient(
        port='/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0',
#        framer=framer,
        timeout=1,
        retries=3,
        baudrate=9600,
        bytesize=8,
        parity="E",
        stopbits=1,
        # handle_local_echo=False,
    )
    
#    print ("connecting")
    client.connect()

#    print ("read holding registers")
    try:
        holding_regs = client.read_holding_registers(0, 11, slave=1)
    except ModbusException as exc:
        print (f"Received ModbusException({exc}) from library")
    if holding_regs.isError():
        print (f"Received Modbus library error({holding_regs})")
    elif isinstance(holding_regs, ExceptionResponse):
        print (f"Received Modbus library exception ({holding_regs})")
        # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
    else:
#        print (holding_regs.registers)
        voltage_V = holding_regs.registers[0] * 0.1
        current_A = holding_regs.registers[1] * 0.1
        frequency_Hz = holding_regs.registers[2] * 0.1
        activePower_W = holding_regs.registers[3]
        reactivePower_var = holding_regs.registers[4]
        apparentPower_VA = holding_regs.registers[5]
        power_factor = holding_regs.registers[6] / 1000
        active_energy_Wh = holding_regs.registers[7] << 16
        active_energy_Wh += holding_regs.registers[8] 
        reactive_energy_varh = holding_regs.registers[9] << 16
        reactive_energy_varh += holding_regs.registers[10] 
        print ("Voltage: %.1f V" % voltage_V)
        print ("Current: %.1f A" % current_A)
        print ("Frequency: %.1f Hz" % frequency_Hz)
        print ("Active power: %d W" % activePower_W)
        print ("Reactive power: %d var" % reactivePower_var)
        print ("Apparent power: %d VA" % apparentPower_VA)
        print ("Power factor: %.3f" % power_factor)
        print ("Active energy: %.3f kWh" % (active_energy_Wh / 1000.0))
        print ("Reactive energy: %.3f kvarh" % (reactive_energy_varh / 1000.0))

#    print ("close connection")
    client.close()


