from tkinter import *
from tkinter import messagebox
from yaml_reader import Synonyms


class update_synonym_window:
    def __init__(self, parent, title='Update synonym', width=300, height=147):
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
        current_key = self.key_entry.get()
        new_key = self.new_key_entry.get()
        new_value = self.new_value_entry.get()
        if current_key:
            if new_key and new_value:
                self.syn.update_synonym(current_key, new_value,
                                        new_key)
                messagebox.showinfo('Success', f"Data has been successfully updated in the 'synonyms.yaml'")
                self.key_entry.delete(0, END)
                self.new_key_entry.delete(0, END)
                self.new_value_entry.delete(0, END)
            elif new_key and not new_value:
                messagebox.showinfo('New value error', f"Fill the 'New value' field and try again")
                self.new_key_entry.delete(0, END)
            elif not new_key and new_value:
                self.syn.update_synonym(current_key, new_value)
                messagebox.showinfo('Success', f"Data has been successfully updated in the 'synonyms.yaml'")
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
    def __init__(self, parent, title='Add synonym', width=300, height=132):
        self.root = Toplevel(parent)
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")

        self.syn = Synonyms()

        # create label 'Synonym name'
        self.synonym_name_label = Label(self.root, text='*Synonym name')
        self.synonym_name_label.grid(row=0, column=0, sticky=W, pady=5)

        # create entry field for a Synonym name
        synonym_name_text = StringVar()
        self.synonym_name_entry = Entry(self.root, textvariable=synonym_name_text, width=50)
        self.synonym_name_entry.grid(row=1, column=0, sticky=W + E)

        # create label 'Synonym value' (URL)
        self.synonym_url_label = Label(self.root, text="*Synonym's URL")
        self.synonym_url_label.grid(row=2, column=0, sticky=W, pady=5)

        # create entry field for 'Synonym value' (URL)
        synonym_url_text = StringVar()
        self.synonym_url_entry = Entry(self.root, textvariable=synonym_url_text, width=50)
        self.synonym_url_entry.grid(row=3, column=0, sticky=W + E)

        # create add_synonym_button
        self.add_synonym_button = Button(self.root, text='Add', command=self.add_synonym)
        self.add_synonym_button.grid(row=4, column=0, sticky=W + E, pady=5)

        self.grab_focus()

    def add_synonym(self):
        """get key and value from the 'add_synonym_window' fields and add this data to the synonyms.yaml as key:[key] plus as [key]['synonym_name'], value: [key]['synonym_value']"""
        key_value = self.synonym_name_entry.get()
        value_value = self.synonym_url_entry.get()
        if key_value and value_value:
            self.syn.add_synonym(key_value, value_value)
            messagebox.showinfo('Success', f"Data has been successfully added to the 'synonyms.yaml'")
            self.root.destroy()
        elif key_value and not value_value:
            messagebox.showinfo('Empty URL', "Please fill the *Synonym's URL field and try again")
        else:
            messagebox.showinfo('Empty Name', "Please fill the *Synonym name field and try again")

    def grab_focus(self):
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()
