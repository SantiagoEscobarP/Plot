class Index(object):
    ind = 0

    def next(self, event):
        ser.close()
        plt.draw()
        plt.close('all')
    
        
        
callback = Index()
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'cerrar')
bnext.on_clicked(callback.next)