from tkinter import *
from tkinter import ttk
from timeit import timeit



def combo_values(*x):
    values = [i for i in x if isinstance(i, str)]
    return values

def view_command():
    #view all from db


# def start_and_finish():
#     timeit module ??


window = Tk()
combo_text = StringVar()
combo = ttk.Combobox(window, postcommand=view_command, state="readonly", width=50)
combo.grid(row=0, column=0, columnspan=2)

url_text = StringVar()
url_entry = Entry(window, textvariable=url_text, width=53)
url_entry.grid(row=1, column=0, columnspan=2)

pb = ttk.Progressbar(window, orient='horizontal', mode='determinate', length=322)
pb.grid(row=3, column=0, columnspan=2)

load_button = Button(window, text='Load', width=20, command=pb.start)
load_button.grid(row=2, column=0)

showfromdb_button = Button(window, text='Show from DB', command=pb.start, width=23)
showfromdb_button.grid(row=2, column=1)

window.mainloop()

# print(combo_values('Hello', "Byebye"))
