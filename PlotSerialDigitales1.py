# !/usr/bin/python3
import serial
import threading
import time
import collections
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from tkinter import Tk,Label,Button,Entry,Scale
import paho.mqtt.client as paho


serialPortbt = "COM24"
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
plt.ylim(0, 100)
plt.xlim(0,200)
# Función que se va a ejecutar en otro thread
# y que guardará los datos del serial en 'out_data'

broker="192.168.0.9"
port=1883

client1= paho.Client("control1")
client1.connect(broker,port)   

def GetData(out_data):
        global resp
        while True:
            try:
                line=SerialConnection.readline().decode('latin-1')
                ret= client1.publish("casa/despacho/temperatura",line)
                print(line)
            except KeyboardInterrupt:
                print('error')
            # Si la línea tiene 'Roll' la parseamos y extraemos el valor
            try:
                out_data[1].append(float(line))
                if len(out_data[1]) > 300:
                    out_data[1].pop(0)
                time.sleep(0.3)
            except:
                pass

def ventana():
    top = Tk()
    top.geometry("300x300")
    txt = Entry(top,width=10)
    txt.place(x = 150, y = 130)
    def acelerometro():
        resp=str('acelero')+'\n'
        resp=resp.encode()
        SerialConnection.write(resp)
        label.config(text =(""+resp.decode()))
        topace = Tk()
        topace.geometry("300x300")
        label1 = Label(topace)
        label1.place(x = 200,y = 50)
        def xx1():
            resp=str('x')+'\n'
            resp=resp.encode()
            SerialConnection.write(resp)
            label1.config(text =(""+resp.decode()))
        def yy1():
            resp=str('y')+'\n'
            resp=resp.encode()
            SerialConnection.write(resp)
            label1.config(text =(""+resp.decode()))
        def zz1():
            resp=str('z')+'\n'
            resp=resp.encode()
            SerialConnection.write(resp)
            label1.config(text =(""+resp.decode()))    
        x1 = Button(topace, text = "x", command =xx1)
        x1.place(x = 10,y = 10)
        y1 = Button(topace, text = "y", command =yy1)
        y1.place(x = 100,y = 10)
        z1 = Button(topace, text = "z", command =zz1)
        z1.place(x = 180,y = 10)
        sal = Button(topace, text = "salir", command =quit)
        sal.place(x = 100,y = 50)
        topace.mainloop()
    def giroscopio():
        resp=str('giro')+'\n'
        resp=resp.encode()
        SerialConnection.write(resp)
        label.config(text =(""+resp.decode()))
        topgir = Tk()
        topgir.geometry("300x300")
        label2 = Label(topgir)
        label2.place(x = 200,y = 50)
        def xx2():
            resp=str('x')+'\n'
            resp=resp.encode()
            SerialConnection.write(resp)
            label2.config(text =(""+resp.decode()))
        def yy2():
            resp=str('y')+'\n'
            resp=resp.encode()
            SerialConnection.write(resp)
            label2.config(text =(""+resp.decode()))
        def zz2():
            resp=str('z')+'\n'
            resp=resp.encode()
            SerialConnection.write(resp)
            label2.config(text =(""+resp.decode()))
        x2 = Button(topgir, text ="x", command =xx2)
        x2.place(x = 10,y = 10)
        y2 = Button(topgir, text = "y", command =yy2)
        y2.place(x = 100,y = 10)
        z2 = Button(topgir, text = "z", command =zz2)
        z2.place(x = 180,y = 10)
        sal = Button(topgir, text = "salir", command =quit)
        sal.place(x = 100,y = 50)
        topgir.mainloop()
    def Texto():
        res =txt.get()+'\n'
        res=res.encode()
        SerialConnection.write(res)
        label.config(text =(""+res.decode()))

    label = Label(top)
    label.place(x = 200,y = 50)
    #b = Button(top, text = "act. giroscopio", command =giroscopio)
    #b.place(x = 10,y = 10)
    #c = Button(top, text = "act. acelerometro", command =acelerometro)
    #c.place(x = 100,y = 10)
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