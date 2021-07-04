# Create combinations of two lists
# updated 7/1/2021

from tkinter import *

def compile():
    # output
    combos = ''

    # vertical text box, split into list by \n, remove duplicates
    l1 = list(set(str(tb_1.get('1.0', END)).split('\n')))
    l2 = list(set(str(tb_2.get('1.0', END)).split('\n')))

    l1.remove('')
    l2.remove('')

    l1.sort(key=int)
    l2.sort(key=int)

    # compile
    for i in l1:
        for j in l2:
            combos += i + '\t' + j + '\n'

    # insert into third text boxs
    tb_3.insert(INSERT, str(combos))

def clear_1():
    tb_1.delete('1.0', END)

def clear_2():
    tb_2.delete('1.0', END)

def clear_3():
    tb_3.delete('1.0', END)

def clear_all():
    clear_1()
    clear_2()
    clear_3()

root = Tk()
root.title("Combinations")
root.geometry('365x470')

version = Label(root, text='Generate combos from two integer lists. Duplicates removed. ver.7/1/2021', font=('Arial',8))
version.grid(row=0, column=0, columnspan=3)

tb_1 = Text(root, width=10, bd=4)
tb_1.grid(row=1, column=0)

tb_2 = Text(root, width=10, bd=4)
tb_2.grid(row=1, column=1)

tb_3 = Text(root, width=20, bd=4)
tb_3.grid(row=1, column=2)

btn_clr1 = Button(root, text="Clear 1", command=clear_1)
btn_clr2 = Button(root, text="Clear 2", command=clear_2)
btn_clr3 = Button(root, text="Clear Combos", command=clear_3)
btn_clrA = Button(root, text="Clear All", command=clear_all)
btn_compile = Button(root, text="Compile", command=compile)

btn_clr1.grid(row=2, column=0, sticky='nsew', padx=1)
btn_clr2.grid(row=2, column=1, sticky='nsew', padx=1)
btn_clr3.grid(row=2, column=2, sticky='nsew', padx=1)
btn_clrA.grid(row=3, column=0, columnspan=2, sticky='nsew', padx=1)
btn_compile.grid(row=3, column=2, columnspan=2, sticky='nsew', padx=1)

root.mainloop()