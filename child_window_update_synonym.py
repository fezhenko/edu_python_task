from tkinter import *
from tkinter import messagebox
from yaml_reader import Synonyms


class update_synonym_window:
    def __init__(self, parent, title='Update synonym', width=300, height=150):
        self.root = Toplevel(parent)
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")

        self.syn = Synonyms()

        self.key_label = Label(self.root, text='*Current key')
        self.key_label.grid(row=0, column=0, sticky=W)

        self.key_text = StringVar()
        self.key_entry = Entry(self.root, textvariable=self.key_text, width=50)
        self.key_entry.grid(row=1, column=0, sticky=W + E)

        self.new_key_lable = Label(self.root, text='New key')
        self.new_key_lable.grid(row=2, column=0, sticky=W)

        self.new_key_text = StringVar()
        self.new_key_entry = Entry(self.root, textvariable=self.new_key_text, width=50)
        self.new_key_entry.grid(row=3, column=0, sticky=W + E)

        self.new_value_label = Label(self.root, text='*New value')
        self.new_value_label.grid(row=4, column=0, sticky=W)

        self.new_value_text = StringVar()
        self.new_value_entry = Entry(self.root, textvariable=self.new_value_text, width=50)
        self.new_value_entry.grid(row=5, column=0, sticky=W + E)

        self.update_button = Button(self.root, text='Update', command=self.update_synonym)
        self.update_button.grid(row=6, column=0, sticky=W + E)

        self.grab_focus()

    def update_synonym(self):
        if self.key_entry.get():
            if self.new_key_entry.get() and self.new_value_entry.get():
                self.syn.update_synonym(self.key_entry.get(), self.new_value_entry.get(),
                                        self.new_key_entry.get())
                self.key_entry.delete(0, END)
                self.new_key_entry.delete(0, END)
                self.new_value_entry.delete(0, END)
            elif self.new_key_entry.get() and not self.new_value_entry.get():
                messagebox.showinfo('New value error', f"Fill the 'New value' field and try again")
            elif not self.new_key_entry.get() and self.new_value_entry.get():
                self.syn.update_synonym(self.key_entry.get(), self.new_value_entry.get())
                self.key_entry.delete(0, END)
                self.new_value_entry.delete(0, END)
            else:
                messagebox.showinfo('New value error', "Fill 'New value' field and try again")
        else:
            messagebox.showinfo('Current key error',
                                "Fill the 'Current key' field plus at least 'New value' field and try again")

    def grab_focus(self):
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()


class add_synonym_window:
    def __init__(self, parent, title='Add synonym', width=300, height=150):
        self.root = Toplevel(parent)
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")

        self.syn = Synonyms()

        # create label 'Synonym name'
        self.synonym_name_label = Label(self.root, text='*Synonym name')
        self.synonym_name_label.grid(row=0, column=0, sticky=W)

        # create entry field for a Synonym name
        synonym_name_text = StringVar()
        self.synonym_name_entry = Entry(self.root, textvariable=synonym_name_text, width=50)
        self.synonym_name_entry.grid(row=1, column=0, sticky=W + E)

        # create label 'Synonym value' (URL)
        self.synonym_url_label = Label(self.root, text="*Synonym's URL")
        self.synonym_url_label.grid(row=2, column=0, sticky=W)

        # create entry field for 'Synonym value' (URL)
        synonym_url_text = StringVar()
        self.synonym_url_entry = Entry(self.root, textvariable=synonym_url_text, width=50)
        self.synonym_url_entry.grid(row=3, column=0, sticky=W + E)

        #create add_synonym_button


    def add_synonym_button(self):
        pass
