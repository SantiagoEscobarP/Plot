# !/usr/bin/python3
import serial
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


def getSerialData(self,Samples,SerialConnection,lines,lineValueText,lineLabel):
    value = float(SerialConnection.readline().strip()) #leer sensor
    data.append(value) #guarda lectura en la ultima posición
    lines.set_data(range(Samples),data) #dibujar nueva linea
    lineValueText.set_text(lineLabel+str(round(value,2)))



try:
    SerialConnection = serial.Serial('COM25',9600,timeout=0)
except:
    print('cannot connect to the port')

Samples = 400 #Muestras
data = collections.deque([0]*Samples,maxlen=Samples)
sampleTime = 1 #tiemplo de muestreo

#límites de los ejes
xmin = 0
xmax = Samples
ymin =  0
ymax = 200

fig = plt.figure(figsize=(13,6))
ax = plt.axes(xlim=(xmin,xmax),ylim=(ymin,ymax))
plt.title("gráfica en tiempo real")
ax.set_xlabel("Samples")
ax.set_ylabel("sensor value")

lineLabel = "RPM:_" 
#grafica datos iniciales y retorna lineas que representan la 
lines=ax.plot([],[],label=lineLabel)[0]
lineValueText=ax.text(0.85,0.95,'',transform=ax.transAxes)

anim = animation.FuncAnimation(fig,getSerialData, 
                                                fargs=(Samples,SerialConnection,lines,lineValueText,lineLabel)
                                                , interval=sampleTime)
plt.show()
SerialConnection.close()

