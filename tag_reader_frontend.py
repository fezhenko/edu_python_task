from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from backend_db import Database
from tag_counter import Tag_counter
from pickle_the_data import Pickle
from timeit import timeit


def get_selected_row(event):
    return combo.get()


def load_command():
    # нужно добавить проверку что если у нас есть значение из комбобокса мы использеум его урл, в ином случае урл из энтри бокса
    # нужно как-то задизейблить ентри если выбран комбобокс и наоборот
    pickling_dict = Pickle(Tag_counter(url_text.get()))
    Database.insert(pickling_dict)
    Database.insert_url(url_text.get())
    url_entry.delete(0, END)


def combobox_urls():
    return [row[2] for row in Database.view_urls()]


def show_from_db():
    messagebox.showinfo('All found tags on the loaded page', 'Текст')


def view_command():
    pass


window = Tk()

window.wm_title('Tag counter')

opts = StringVar()
combo = ttk.Combobox(window, textvariable=opts, width=50)
combo['values'] = combobox_urls()
combo.grid(row=0, column=0, columnspan=2)
combo.bind("<<ComboboxSelected>>", get_selected_row)

url_text = StringVar()
url_entry = Entry(window, textvariable=url_text, width=53)
url_entry.grid(row=1, column=0, columnspan=2)

pb = ttk.Progressbar(window, orient='horizontal', mode='determinate', length=322)
pb.grid(row=3, column=0, columnspan=2)

load_button = Button(window, text='Load', width=20, command=pb.start and load_command)
load_button.grid(row=2, column=0)

showfromdb_button = Button(window, text='Show from DB', command=pb.start and show_from_db, width=23)
showfromdb_button.grid(row=2, column=1)

window.mainloop()
