# !/usr/bin/python3
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
import numpy as np
import time
gData = []
gData.append([0])
gData.append([0])
#Configuramos la gráfica
fig = plt.figure()
ax = fig.add_subplot(111)
hl, = plt.plot(gData[0], gData[1])
plt.ylim(0, 600)
plt.xlim(0,300)
# Función que se va a ejecutar en otro thread
# y que guardará los datos del serial en 'out_data'
def GetData(out_data):
    with serial.Serial('COM29',9600, timeout=0) as ser:
        while True:
            line = ser.readline().decode('utf8')
            # Si la línea tiene 'Roll' la parseamos y extraemos el valor
            try:
                if float(line)<100:
                    continue    
                out_data[1].append(float(line))
                if len(out_data[1]) > 300:
                    out_data[1].pop(0)
                #time.sleep(0.01)
            except:
                pass
                    
def update_line(num, hl, data):
    hl.set_data(range(len(data[1])), data[1])
    return hl
# Configuramos la función que "animará" nuestra gráfica
line_ani = animation.FuncAnimation(fig, update_line, fargs=(hl, gData),
                                    interval=50, blit=False)
# Configuramos y lanzamos el hilo encargado de leer datos del serial
dataCollector = threading.Thread(target = GetData, args=(gData,))
dataCollector.start()
plt.show()
dataCollector.join()