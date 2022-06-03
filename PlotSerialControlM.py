# !/usr/bin/python3
import serial
import threading
import time
import collections
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from tkinter import Tk,Label,Button,Entry,Scale

serialPortbt = "COM17"
baudRatebt = 9600
SerialConnection = serial.Serial(serialPortbt , baudRatebt) #ensure non-blocking

gData = []
gData.append([0])
gData.append([0])

resp=range(0)
#Configuramos la gráfica
fig = plt.figure()
ax = fig.add_subplot(111)
hl, = plt.plot(gData[0], gData[1])
plt.ylim(0, 250)
plt.xlim(0,100)
# Función que se va a ejecutar en otro thread
# y que guardará los datos del serial en 'out_data'

   

def GetData(out_data):
        global resp
        while True:
            try:
                line=SerialConnection.readline().decode('latin-1')
                
            except KeyboardInterrupt:
                print('error')
            # Si la línea tiene 'Roll' la parseamos y extraemos el valor
            try:
                out_data[1].append(float(line))
                if len(out_data[1]) > 100:
                    #out_data[1] = []
                    out_data[1].pop(0)
                time.sleep(0.01)
            except:
                pass

def ventana():
    top = Tk()
    top.geometry("300x300")
    txt = Entry(top,width=10)
    txt.place(x = 150, y = 130)
    def Izquierda():
        resp=str('I')+'\n'
        resp=resp.encode()
        SerialConnection.write(resp)
        label.config(text =(""+resp.decode()))
    def Derecha():
        resp=str('D')+'\n'
        resp=resp.encode()
        SerialConnection.write(resp)
        label.config(text =(""+resp.decode()))
    def Texto():
        res =txt.get()+'\n'
        res=res.encode()
        SerialConnection.write(res)
        label.config(text =(""+res.decode()))

    label = Label(top)
    label.place(x = 200,y = 50)
    b = Button(top, text = "Derecha", command =Derecha)
    b.place(x = 10,y = 10)
    c = Button(top, text = "Izquierda", command =Izquierda)
    c.place(x = 100,y = 10)
    d = Button(top, text = "Cerrar", command = quit)
    d.place(x = 150,y = 200)
    btn = Button(top, text="Escribir", command=Texto)
    btn.place(x=50,y=130)
    top.mainloop()
    
def update_line(num, hl, data):
    hl.set_data(range(len(data[1])), data[1])
    return hl
# Configuramos la función que "animará" nuestra gráfica
line_ani = animation.FuncAnimation(fig, update_line, fargs=(hl, gData),
                                    interval=50, blit=False)
# Configuramos y lanzamos el hilo encargado de leer datos del serial

dataCollector = threading.Thread(target = GetData, args=(gData,))
w = threading.Thread(target=ventana)
w.start()
dataCollector.start()
plt.show()
dataCollector.join()