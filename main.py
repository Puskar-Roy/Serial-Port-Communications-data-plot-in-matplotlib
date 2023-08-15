import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def read_bluetooth_data(port, baud_rate=9600, timeout=1):
    bluetooth_serial = None
    try:
        bluetooth_serial = serial.Serial(port, baud_rate, timeout=timeout)
        
        while True:
            data = bluetooth_serial.readline().decode().strip()
            if data.startswith("$:"):
                parts = data.split(':')[1].split(',')
                if len(parts) >= 3:  # Check for the correct number of gyro values
                    gyro_x = float(parts[0])
                    gyro_y = float(parts[1])
                    gyro_z = float(parts[2])
                    print('Gyro X - '+str(gyro_x))
                    print('Gyro y - '+str(gyro_y))
                    print('Gyro Z - '+str(gyro_z))
                    yield gyro_x, gyro_y, gyro_z
    
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Stopping the program.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if bluetooth_serial:
            bluetooth_serial.close()

def update_plot(i, y_vals_x, y_vals_y, y_vals_z):
    gyro_x, gyro_y, gyro_z = next(data_generator)
    y_vals_x.append(gyro_x)  # gyro_x data as y axis
    y_vals_y.append(gyro_y)  # gyro_y data as z axis
    y_vals_z.append(gyro_z)  # gyro_z data as x axis
    
    if len(y_vals_x) > 120:
        y_vals_x.pop(0)
        y_vals_y.pop(0)
        y_vals_z.pop(0)
        
    ax.clear()
    ax.plot(y_vals_x, label='Gyro X-axis', color='blue')
    ax.plot(y_vals_y, label='Gyro Y-axis', color='green')
    ax.plot(y_vals_z, label='Gyro Z-axis', color='red')


    ax.set_ylabel("Gyro Data")
    ax.set_xlabel("Time")
    ax.set_title("Gyro Data Graph")
    ax.legend()

if __name__ == "__main__":
    bluetooth_port = 'COM4'
    data_generator = read_bluetooth_data(bluetooth_port)
    
    fig, ax = plt.subplots()
    y_vals_x = []
    y_vals_y = []
    y_vals_z = []
    
    ani = FuncAnimation(fig, update_plot, fargs=(y_vals_x, y_vals_y, y_vals_z), interval=1)
    plt.show()
