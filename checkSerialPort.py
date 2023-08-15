# import serial.tools.list_ports

# def show_active_serial_port_connections():
#     available_ports = serial.tools.list_ports.comports()
#     for port in available_ports:
#         print(port)

# if __name__ == "__main__":
#     show_active_serial_port_connections()


import tkinter as tk
import serial.tools.list_ports
import serial
import subprocess

def show_active_com_ports():
    available_ports = serial.tools.list_ports.comports()
    com_port_list = []
    for port in available_ports:
        com_port_list.append(port.device)
    return com_port_list

def connect_to_com_port():
    selected_com_port = com_port_var.get()
    try:
        serial_connection = serial.Serial(selected_com_port, baudrate=9600, timeout=1)
        print(f"Connected to {selected_com_port}")
        command = ["python", 'main.py']
        subprocess.run(command)
    except serial.SerialException as e:
        print(f"Error connecting to {selected_com_port}: {e}")

root = tk.Tk()
root.title("Serial Port Connector")

com_port_var = tk.StringVar(root)
com_port_var.set("Select COM Port")  # Default value for dropdown

com_port_label = tk.Label(root, text="Select COM Port:")
com_port_label.pack()

com_port_dropdown = tk.OptionMenu(root, com_port_var, *show_active_com_ports())
com_port_dropdown.pack()

connect_button = tk.Button(root, text="Connect", command=connect_to_com_port)
connect_button.pack()

root.mainloop()

