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
        self.combo.grid(row=0, column=0, columnspan=2, sticky=W + E, padx=1, pady=5)
        self.combo.bind("<<ComboboxSelected>>", self.get_selected_row)

        self.url_text = StringVar()
        self.url_entry = Entry(window, textvariable=self.url_text, width=50)
        self.url_entry.grid(row=1, column=0, columnspan=2, sticky=W + E, padx=1, pady=5)

        self.pb = ttk.Progressbar(window, orient='horizontal', mode='determinate')
        self.pb.grid(row=3, column=0, columnspan=2, sticky=W + E)

        self.load_button = Button(window, text='Load', width=20, command=self.load_command)
        self.load_button.grid(row=2, column=0, sticky=W)

        self.showfromdb_button = Button(window, text='Show from DB', command=self.show_from_db,
                                        width=20)
        self.showfromdb_button.grid(row=2, column=1, sticky=E)



    def get_selected_row(self, event):
        return self.combo.get()

    def load_command(self):
        # нужно добавить проверку что если у нас есть значение из комбобокса мы использеум его урл, в ином случае урл из энтри бокса
        # нужно как-то задизейблить ентри если выбран комбобокс и наоборот
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

    def view_command(self):
        pass


window = Tk()
Window(window)
window.mainloop()
