import time
import tkinter as tk
from riseOfKingdom import Exploration

def WindowsForm():
    #Création du Forms
    window = tk.Tk()
    window.title('Rise of Kingdom Bot')
    window.geometry('500x500')
    
    lbl = tk.Label(window, bg='white', width=20, text='Configuration')
    lbl.pack()
    
    def Selection():
        if (ckb1.get() == 1):
            time.sleep(10)
            Exploration()
            window.update()
    
    ckb1 = tk.IntVar()
    ckb2 = tk.IntVar()
    c1 = tk.Checkbutton(window, text='Exploration',variable=ckb1, onvalue=1, offvalue=0, command=Selection)
    c1.pack()

    window.mainloop()

WindowsForm()