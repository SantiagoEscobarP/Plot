# !/usr/bin/python3
import serial
import threading
import time
import collections
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from tkinter import Tk,Label,Button,Entry,Scale


def getSerialData(self,Samples,SerialConnection,lines,lineValueText,lineLabel):
    print(SerialConnection.readable())
    aux = SerialConnection.readline().strip()

    try:
        value = float(aux) #leer sensor
    except:
        value = float(aux.decode('utf-8').replace('\r','\n').split('\n')[0])
    
    time.sleep(0.14)
    data.append(value) #guarda lectura en la ultima posición
    lines.set_data(range(Samples),data) #dibujar nueva linea
    lineValueText.set_text(lineLabel+str(round(value,2)))

try:
    SerialConnection = serial.Serial('COM29',9600,timeout=0)
except:
    print('cannot connect to the port')

Samples = 400 #Muestras
data = collections.deque([0]*Samples,maxlen=Samples)
sampleTime = 1 #tiemplo de muestreo

#límites de los ejes
xmin = 0
xmax = Samples
ymin =  0
ymax = 1000

fig = plt.figure(figsize=(13,6))
ax = plt.axes(xlim=(xmin,xmax),ylim=(ymin,ymax))
plt.title("gráfica en tiempo real")
ax.set_xlabel("Samples")
ax.set_ylabel("sensor value")

lineLabel = "RPM: " 
#grafica datos iniciales y retorna lineas que representan la 
lines=ax.plot([],[],label=lineLabel)[0]
lineValueText=ax.text(0.85,0.95,'',transform=ax.transAxes)

anim = animation.FuncAnimation(fig,getSerialData, 
                                                fargs=(Samples,SerialConnection,lines,lineValueText,lineLabel)
                                                , interval=sampleTime)

    
def ventana():
    top = Tk()
    top.geometry("300x300")
    txt = Entry(top,width=10)
    txt.place(x = 150, y = 130)
    def Rpm2():
        resp=str(barra1.get()*2)
        label.config(text =("RPM: "+resp))
        resp="mA"+resp+'0'+'\n\r'
        resp=resp.encode()
        SerialConnection.write(resp)
        SerialConnection.write(resp)
        SerialConnection.write(resp)
        SerialConnection.write(resp)
    def Rpm():
        res = str(int(txt.get())*2)
        label.config(text =("RPM: "+res))
        res ='mA'+res+'0'+'\n\r'
        res=res.encode()
        SerialConnection.write(res)
        SerialConnection.write(res)
        SerialConnection.write(res)
        SerialConnection.write(res)
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
w = threading.Thread(target=ventana)
w.start()
plt.show()
SerialConnection.close()