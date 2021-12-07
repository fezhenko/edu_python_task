from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from backend_db import Database
from tag_counter import Tag_counter
from yaml_reader import yaml_reader
import pickle_the_data

from timeit import timeit


class Window(object):

    def __init__(self, window):
        self.window = window
        window.wm_title('Tag counter')
        self.d = Database()

        self.opts = StringVar()
        self.combo = ttk.Combobox(window, textvariable=self.opts, width=50)
        self.combo['values'] = self.combobox_urls()
        self.combo.grid(row=0, column=0, columnspan=2)
        self.combo.bind("<<ComboboxSelected>>", self.get_selected_row)

        self.url_text = StringVar()
        self.url_entry = Entry(window, textvariable=self.url_text, width=53)
        self.url_entry.grid(row=1, column=0, columnspan=2)
        self.user_input = self.url_text.get()

        self.pb = ttk.Progressbar(window, orient='horizontal', mode='determinate', length=322)
        self.pb.grid(row=3, column=0, columnspan=2)

        self.load_button = Button(window, text='Load', width=20, command=self.load_command) # and self.pb.start)
        self.load_button.grid(row=2, column=0)

        self.showfromdb_button = Button(window, text='Show from DB', command=self.pb.start and self.show_from_db,
                                        width=23)
        self.showfromdb_button.grid(row=2, column=1)

    def get_selected_row(self, event):
        return self.combo.get()

    def load_command(self):
        # нужно добавить проверку что если у нас есть значение из комбобокса мы использеум его урл, в ином случае урл из энтри бокса
        # нужно как-то задизейблить ентри если выбран комбобокс и наоборот
        yaml = yaml_reader()
        url_for_using = yaml.synonym_value(self.url_text.get())
        t = Tag_counter(url_for_using)
        tags_to_dict = t.tags_to_dict()
        pickling_dict = pickle_the_data.pickle_dict(tags_to_dict)
        self.d.insert(pickling_dict)
        self.d.insert_url(self.url_text.get())
        self.url_entry.delete(0, END)

    def combobox_urls(self):
        return [row[2] for row in self.d.view_urls()]

    def show_from_db(self):
        messagebox.showinfo('All found tags on the loaded page', 'Текст')

    def view_command(self):
        pass


window = Tk()
Window(window)
window.mainloop()
