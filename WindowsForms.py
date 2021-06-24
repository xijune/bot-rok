from re import T
from riseOfKingdom import *
import tkinter as tk

def WindowsForm():
    #Création du Forms
    window = tk.Tk()
    window.title('Rise of Kingdom Bot')
    window.geometry('500x500')
    
    lbl = tk.Label(window, bg='white', width=20, text='Configuration')
    lbl.pack()
    
    def Selection():
        if ckb1.get() == 1:
            Collecte()
            window.update()

        elif ckb2.get() == 1:
            Archer()
            window.update()

        elif ckb3.get() == 1:
            Infenterie()
            window.update()
    
        elif ckb4.get() == 1:
            Exploration()
            window.update()

        elif ckb5.get() == 1:
            Alliance()
            window.update()

        elif ckb6.get() == 1:
            AideAlly()
            window.update()

        elif ckb7.get() == 1:
            Recrute()
            window.update()


    ckb1 = tk.IntVar()
    c1 = tk.Checkbutton(window, text='Collection',variable=ckb1, onvalue=1, offvalue=0, command=Selection)
    c1.pack()

    ckb2 = tk.IntVar()
    c2 = tk.Checkbutton(window, text='Formation Archer',variable=ckb2, onvalue=1, offvalue=0, command=Selection)
    c2.pack()

    ckb3 = tk.IntVar()
    c3 = tk.Checkbutton(window, text='Formation Infenterie',variable=ckb3, onvalue=1, offvalue=0, command=Selection)
    c3.pack()

    ckb4 = tk.IntVar()
    c4 = tk.Checkbutton(window, text='Exploration',variable=ckb4, onvalue=1, offvalue=0, command=Selection)
    c4.pack()

    ckb5 = tk.IntVar()
    c5 = tk.Checkbutton(window, text='Alliance',variable=ckb5, onvalue=1, offvalue=0, command=Selection)
    c5.pack()

    ckb6 = tk.IntVar()
    c6 = tk.Checkbutton(window, text='Aide Alliance',variable=ckb6, onvalue=1, offvalue=0, command=Selection)
    c6.pack()

    ckb7 = tk.IntVar()
    c7 = tk.Checkbutton(window, text='Ouverture des Coffres',variable=ckb7, onvalue=1, offvalue=0, command=Selection)
    c7.pack()

    window.mainloop()


WindowsForm()