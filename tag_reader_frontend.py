from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from backend_db import Database
from tag_counter import Tag_counter


class Window(object):

    def __init__(self, window):
        self.window = window
        window.wm_title('Tag counter')
        self.d = Database()
        self.opts = StringVar()

        self.combo = ttk.Combobox(window, textvariable=self.opts, width=50)
        self.combo['values'] = self.combobox_urls()
        self.combo.grid(row=0, column=0, columnspan=4, sticky=W + E, padx=1, pady=3)
        self.combo.bind("<<ComboboxSelected>>", self.get_selected_row)

        self.url_text = StringVar()
        self.url_entry = Entry(window, textvariable=self.url_text, width=50)
        self.url_entry.grid(row=1, column=0, columnspan=4, sticky=W + E, padx=1, pady=3)

        self.pb = ttk.Progressbar(window, orient='horizontal', mode='determinate')
        self.pb.grid(row=3, column=0, columnspan=4, sticky=W + E, pady=3)

        self.load_button = Button(window, text='Load', width=15, command=self.load_command)
        self.load_button.grid(row=2, column=0, sticky=W, pady=1)

        self.showfromdb_button = Button(window, text='Show from DB', command=self.show_from_db,
                                        width=15)
        self.showfromdb_button.grid(row=2, column=1, sticky=E, pady=1)

        self.add_synonym_button = Button(window, text='Add Synonym', width=15)
        self.add_synonym_button.grid(row=2, column=2, columnspan=2,sticky=E, pady=1)

        self.l1 = Label(window, text='List of Synonyms')
        self.l1.grid(row=4, column=0, columnspan=4, sticky=W, pady=0)

        self.list1 = Listbox(window)
        self.list1.grid(row=5, column=0, columnspan=2,  rowspan=5, sticky=W+E)



    def get_selected_row(self, event):
        return self.combo.get()

    def load_command(self):
        if self.combo.get():
            for i in range(101):
                self.pb.configure(value=i)
                self.pb.update()
            t = Tag_counter(self.combo.get())
            tags = t.tags_to_dict()
            name = t.site_name()
            self.d.insert(tags, name, t.HOST)
            messagebox.showinfo(f"Loaded tags", f"{tags} of the {t.HOST} has been loaded to DB")
            self.pb.configure(value=0)
            self.combo.delete(0, END)
        elif self.url_text.get():
            if self.combo.get():
                for i in range(101):
                    self.pb.configure(value=i)
                    self.pb.update()
            t = Tag_counter(self.url_text.get())
            tags = t.tags_to_dict()
            name = t.site_name()
            self.d.insert(tags, name, t.HOST)
            messagebox.showinfo(f"Loaded tags", f"{tags} of the {t.HOST} has been loaded to DB")
            self.url_entry.delete(0, END)

    def combobox_urls(self):
        return [row for row in self.d.view_urls()]

    def show_from_db(self):
        if self.combo.get():
            t = Tag_counter(self.combo.get())
            tags = self.d.get_from_db(t.HOST)
            messagebox.showinfo(f"Tags of the {t.HOST}", f"{tags}")
            self.combo.delete(0, END)
        elif self.url_text.get():
            t = Tag_counter(self.url_text.get())
            tags = self.d.get_from_db(t.HOST)
            messagebox.showinfo(f"{tags}")
            self.url_entry.delete(0, END)



window = Tk()
Window(window)
window.mainloop()
