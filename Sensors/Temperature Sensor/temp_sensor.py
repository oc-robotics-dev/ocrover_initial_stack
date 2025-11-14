import serial
import matplotlib.pyplot as plt
from collections import deque
import time

# Initialize the serial connection, my port is COM7, but yours may be different
serialPort = serial.Serial("COM7", 9600)  
time.sleep(2)   # apparently this is highly recommended

# creating the graph
plt.ion()   # make the graph update dynamically
fig, ax = plt.subplots()    # creates the canvas
queue_temp = deque(maxlen=100)  # queue to store temp values, if queue exceeds 100, oldest values are removed (the removed values will be removed from the graph)
queue_time = deque(maxlen=100)  # same thing as above with time
line, = ax.plot([], [], 'r-')   # ax plot returnns a tuple, the little comma unpacks the first value
ax.set_xlabel("timemeeee")  
ax.set_ylabel("ooo that\'s hot")
start_time = time.time()

continue_loop = True

while continue_loop:
    try:
        if serialPort.in_waiting:       # if there is data to be read. depending on your sampliing rate of arduino
            line_data = serialPort.readline().decode("utf-8").strip()
            temp = float(line_data)
            current_time = time.time() - start_time
            queue_temp.append(temp)
            queue_time.append(current_time)

            line.set_xdata(queue_time)
            line.set_ydata(queue_temp)
            ax.relim()
            ax.autoscale_view()
            plt.draw()
            plt.pause(0.01)
    except KeyboardInterrupt:
        break
    except:
        continue

serialPort.close() # Make sure to do this. Otherwise, your other programs may not be able to access the port