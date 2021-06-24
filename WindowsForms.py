import time
import tkinter as tk

def WindowsForm():
    #Création du Forms
    window = tk.Tk()
    window.title('Rise of Kingdom Bot')
    window.geometry('500x500')
    
    lbl = tk.Label(window, bg='white', width=20, text='Configuration')
    lbl.pack()
    
    def Selection():
        while (ckb1.get() == 1):
            window.update()

        while (ckb2.get() == 1):
            window.update()
    
    ckb1 = tk.IntVar()
    c1 = tk.Checkbutton(window, text='Collection',variable=ckb1, onvalue=1, offvalue=0, command=Selection)
    c1.pack()

    ckb2 = tk.IntVar()
    c2 = tk.Checkbutton(window, text='Formation Archer',variable=ckb2, onvalue=1, offvalue=0, command=Selection)
    c2.pack()

    window.mainloop()

WindowsForm()