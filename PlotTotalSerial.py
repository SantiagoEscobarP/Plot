# !/usr/bin/python3
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
import numpy as np
import time
from tkinter import Tk,Label,Button,Entry,Scale
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
try:
    ser=serial.Serial('COM2',9600, timeout=0)
except:
    print('error')

def GetData(out_data):
        global ser
        while True:
            line = ser.readline().decode('utf8')
            # Si la línea tiene 'Roll' la parseamos y extraemos el valor
            try:
                if float(line)<100:
                    continue    
                out_data[1].append(float(line))
                if len(out_data[1]) > 300:
                    out_data[1].pop(0)
            except:
                pass

def ventana():
    global ser
    top = Tk()
    top.geometry("300x300")
    txt = Entry(top,width=10)
    txt.place(x = 150, y = 130)
    def Rpm2():
        resp=str(barra1.get())+'\n'
        resp=resp.encode()
        ser.write(resp)
        label.config(text =("RPM: "+resp.decode()))
    def Rpm():
        res =txt.get()+'\n'
        res=res.encode()
        ser.write(res)
        label.config(text =("RPM: "+res.decode()))
    barra1 = Scale(top, from_=0, to=500)
    barra1.pack()    
    label = Label(top)
    label.place(x = 200,y = 30)
    #label.pack()
    c = Button(top, text = "RPM_scroll", command = Rpm2)
    c.place(x = 50,y = 10)
    d = Button(top, text = "Cerrar", command = quit)
    d.place(x = 150,y = 200)
    btn = Button(top, text="RPMtext", command=Rpm)
    btn.place(x=50,y=130)
    top.mainloop()
    
def update_line(num, hl, data):
    hl.set_data(range(len(data[1])), data[1])
    return hl
# Configuramos la función que "animará" nuestra gráfica
line_ani = animation.FuncAnimation(fig, update_line, fargs=(hl, gData),
                                    interval=50, blit=False)
# Configuramos y lanzamos el hilo encargado de leer datos del serial
w = threading.Thread(target=ventana)
w.start()
dataCollector = threading.Thread(target = GetData, args=(gData,))
dataCollector.start()
plt.show()
dataCollector.join()