from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from backend_db import Database
from tag_counter import Tag_counter
from yaml_reader import Synonyms


class Window(object):

    def __init__(self, window):
        self.window = window
        window.wm_title('Tag counter')

        # connect to the database
        self.d = Database()

        # use Synonyms
        self.syn = Synonyms()

        # create combobox
        self.opts = StringVar()
        self.combo = ttk.Combobox(window, textvariable=self.opts, width=50)
        self.combo['values'] = self.combobox_urls()
        self.combo.grid(row=0, column=0, columnspan=4, sticky=W + E, padx=1, pady=3)
        self.combo.bind("<<ComboboxSelected>>", self.get_selected_row)

        # create Entry field under the combobox
        self.url_text = StringVar()
        self.url_entry = Entry(window, textvariable=self.url_text, width=50)
        self.url_entry.grid(row=1, column=0, columnspan=4, sticky=W + E, padx=1, pady=3)

        # create progressbar under the Entry field
        self.pb = ttk.Progressbar(window, orient='horizontal', mode='determinate')
        self.pb.grid(row=3, column=0, columnspan=4, sticky=W + E, pady=3)

        # create the Load button
        self.load_button = Button(window, text='Load', width=15, command=self.load_command)
        self.load_button.grid(row=2, column=0, sticky=W, pady=1)

        # create the button that get value from the combobox or entry field and shows related data from the Database
        self.show_from_db_button = Button(window, text='Show from DB', command=self.show_from_db,
                                          width=15)
        self.show_from_db_button.grid(row=2, column=1, sticky=W, pady=1)

        # create a button that get data from the entry fields in the special window and add it to the synonyms.yaml file
        self.add_synonym_button = Button(window, text='Add Synonym', width=15)
        self.add_synonym_button.grid(row=2, column=2, columnspan=2, sticky=E, pady=1)

        # label above the listbox
        self.l1 = Label(window, text='List of Synonyms')
        self.l1.grid(row=4, column=0, columnspan=4, sticky=W, pady=0)

        # create a listbox that contains all synonyms from the synonyms.yaml file
        self.list1 = Listbox(window)
        self.list1.grid(row=5, column=0, columnspan=2, rowspan=5, sticky=W + E)

        # scrollbar for the listbox
        sb = Scrollbar(window)
        sb.grid(row=5, column=2, rowspan=5)

        self.list1.configure(yscrollcommand=sb.set)
        sb.configure(command=self.list1.yview)

        # button that displays synonyms from the synonyms.yaml in the listbox
        self.view_synonyms_button = Button(window, text='View Synonyms', width=15, command=self.view_synonyms)
        self.view_synonyms_button.grid(row=5, column=3, sticky=E, pady=1)

        # button that displays certain synonym by the entering value in the entry field
        self.search_synonym_button = Button(window, text='Search Synonym', width=15, command=self.search_synonyms)
        self.search_synonym_button.grid(row=6, column=3, sticky=E, pady=1)

        # update certain synonym's value in the synonyms.yaml
        self.update_synonym_button = Button(window, text='Update Synonym', width=15)
        self.update_synonym_button.grid(row=7, column=3, sticky=E, pady=1)

        # delete synonym from the synonyms.yaml
        self.delete_synonym_button = Button(window, text='Delete Synonym', width=15)
        self.delete_synonym_button.grid(row=8, column=3, sticky=E, pady=1)

        # close the window
        self.close_button = Button(window, text='Quit', width=15)
        self.close_button.grid(row=9, column=3, sticky=E, pady=1)

    def get_selected_row(self, event):
        """get the selected value from the combobox"""
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

    def view_synonyms(self):
        self.list1.delete(0, END)
        for row in self.syn.view_synonyms():
            self.list1.insert(END, row)

    def search_synonyms(self):
        """take value from combobox field or from entry field and search it in the list of synonyms, return the message with related URL if exists"""
        if self.combo.get():
            if self.syn.check_synonym(self.combo.get()) is not None:
                messagebox.showinfo("Synonym exists", self.syn.check_synonym(self.combo.get()))
                self.combo.delete(0, END)
            else:
                messagebox.showinfo("Synonym error", f"Value for '{self.combo.get()}' doesn't exist")
                self.combo.delete(0, END)
        elif self.url_entry.get():
            if self.syn.check_synonym(self.url_entry.get()) is not None:
                messagebox.showinfo("Synonym exists", self.syn.check_synonym(self.url_entry.get()))
                self.url_entry.delete(0, END)
            else:
                messagebox.showinfo("Synonym error", f"Value for '{self.url_entry.get()}' doesn't exist")
                self.url_entry.delete(0, END)
        else:
            messagebox.showinfo("Error", f"Fill the any field and try again")


window = Tk()
Window(window)
window.mainloop()
