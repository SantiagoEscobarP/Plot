# !/usr/bin/python3
import serial
import threading
import time
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from tkinter import Tk,Label,Button,Entry,Scale
com_serial=serial.Serial('COM2',9600, timeout=0)
total=[0 for _ in range(40)] #crear el vector y lo llena de 0 a 40 consecutivamente.
b=range(40)
def operacion_serial(a):
    if a == b'':
        return []
    a=a.decode('latin-1')
    a=a.split('#@')
    a = a[1:-1]
    a=list(map(float,a))
    #print(a)
    return a

def helloCallBack():
    global total
    global b
    #plt.plot(b,total)
    #com_serial.write(b'recibido\n\r')
    #plt.show()
    fig, ax = plt.subplots()

    x = np.arange(20)
    y=total
    line, = ax.plot(x, y)


    def init():  # only required for blitting to give a clean slate.
        line.set_ydata([np.nan] * len(x))
        return line,


    def animate(i):
        time.sleep(0.1)
        aux = y[0]
        y.remove(aux)
        y.append(aux)
        line.set_ydata(y)  # update the data.
        return line,


    ani = animation.FuncAnimation(
        fig, animate, init_func=init, interval=2, blit=True, save_count=40)

    # To save the animation, use e.g.
    #
    # ani.save("movie.mp4")
    #
    # or
    #
    # from matplotlib.animation import FFMpegWriter
    # writer = FFMpegWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    # ani.save("movie.mp4", writer=writer)
    plt.show()
def adios():
    top = Tk()
    top.geometry("300x300")
    txt = Entry(top,width=10)
    txt.place(x = 150, y = 130)
    def Rpm2():
        resp=str(barra1.get())+'\r'
        resp=resp.encode()
        com_serial.write(resp)
        label.config(text =("RPM: "+resp.decode()))
    def Rpm():
        res =txt.get()+'\r'
        res=res.encode()
        com_serial.write(res)
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
def arreglo_serial():
    global total
    global b
    while True:
        val=com_serial.readline()
        #print(val)
        total=total+operacion_serial(val)
        total=total[-20:]
        #print(b)
        #print(total)
        time.sleep(0.5)
t = threading.Thread(target=helloCallBack)
w = threading.Thread(target=adios)
s = threading.Thread(target=arreglo_serial)
w.start()
t.start()
s.start()