import os
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import *
import webbrowser
import sqlite3
import hashlib

class ModManagerApp:
    def __init__(self):
        # Create database connection
        self.__connection = sqlite3.connect('mods.db')
        self.__cursor = self.__connection.cursor()

        # Set up root window
        self.__root = Tk()
        self.__root.title("PAYDAY 3 Mod Manager")
        self.__root.config(background="#FFFFFF")
        self.__root.geometry("1480x600")
        self.__root.resizable(False, False)
        self.__root.iconbitmap("pd3.ico")

        # Create all menus
        self.__menu_main = Menu(self.__root, background="#D9D9D9")
        self.__menu_mods = Menu(self.__menu_main, tearoff=0)
        self.__menu_filters = Menu(self.__menu_main, tearoff=0)
        self.__menu_help = Menu(self.__menu_main, tearoff=0)

        self.__menu_main.add_cascade(label="Mods", menu=self.__menu_mods)
        self.__menu_main.add_cascade(label="Filters", menu=self.__menu_filters)
        self.__menu_main.add_cascade(label="Help", menu=self.__menu_help)

        # Add commands to menu entries
        self.__menu_mods.add_command(label="Change mod folder")
        self.__menu_mods.add_command(label="Rescan folder", accelerator="F5")

        self.__menu_filters.add_checkbutton(label="Show disabled mods")

        self.__menu_help.add_command(label="About")
        self.__menu_help.add_command(label="GitHub", command=self.__open_github)
        self.__menu_help.add_command(label="Modworkshop", command=self.__open_mws)

        # Set the main menu as the menu bar of the application
        self.__root.config(menu=self.__menu_main)

        # Create the 2 main frames
        frame_modlist = Frame(self.__root, background="#FFFFFF", width=900)
        frame_properties = Frame(self.__root, background="#D9D9D9", width=300)

        # Create the mod list and selector
        self.__mods = ttk.Treeview(frame_modlist, columns=("id", "displayname", "filename", "directory", "category", "status"), show="headings", height=25)
        self.__mods.column("#1", anchor="w", width=35)
        self.__mods.heading("#1", text="ID")
        self.__mods.column("#2", anchor="w", width=325)
        self.__mods.heading("#2", text="Display name")
        self.__mods.column("#3", anchor="w", width=325)
        self.__mods.heading("#3", text="File name")
        self.__mods.column("#4", anchor="w", width=150)
        self.__mods.heading("#4", text="Location")
        self.__mods.column("#5", anchor="w", width=150)
        self.__mods.heading("#5", text="Category")
        self.__mods.column("#6", anchor="w", width=100)
        self.__mods.heading("#6", text="Status")
        self.__mods.pack(side=TOP, fill=BOTH, expand=True)

        frame_selector = Frame(frame_modlist, background="#FFFFFF")
        Label(frame_selector, text="Mod ID: ", font=("Arial", 12), background="#FFFFFF").pack(side=LEFT)
        self.__var_mod_id = StringVar()
        entry_selector = Entry(frame_selector, textvariable=self.__var_mod_id)
        entry_selector.pack(side=LEFT)
        button_search = Button(frame_selector, text="OK", font=("Arial", 10), command=self.__select_mod)
        button_search.pack(side=LEFT)
        frame_selector.pack(side=TOP, fill=X, expand=True)

        # Create the text variables as class elements for properties frame
        self.__mod_display_name = StringVar()
        self.__mod_file_name = StringVar()
        self.__mod_location = StringVar()
        self.__mod_category = StringVar()

        self.__mod_display_name.set("")
        self.__mod_file_name.set("Please select a mod from the list")
        self.__mod_location.set("")
        self.__mod_category.set("")

        # Create the UI elements for the properties frame
        image = PhotoImage(file="pd3_banner.png")
        image_label = Label(frame_properties, image=image, background="#D9D9D9")
        image_label.image = image
        image_label.pack(side=TOP, fill=BOTH, expand=True)
        label_display_name = Label(frame_properties, textvariable=self.__mod_display_name, font=("Arial", 18), background="#D9D9D9", justify="left")
        label_file_name = Label(frame_properties, textvariable=self.__mod_file_name, font=("Arial", 12), background="#D9D9D9", justify="left")
        label_location = Label(frame_properties, textvariable=self.__mod_location, font=("Arial", 12), background="#D9D9D9", justify="left")
        label_category = Label(frame_properties, textvariable=self.__mod_category, font=("Arial", 12), background="#D9D9D9", justify="left")
        self.__button_rename = Button(frame_properties, text="Rename", font=("Arial", 20), background="#1E1E1E", foreground="#FFFFFF", activebackground="#2E2E2E", activeforeground="#FFFFFF")
        self.__button_category = Button(frame_properties, text="Set Category", font=("Arial", 20), background="#1E1E1E", foreground="#FFFFFF", activebackground="#2E2E2E", activeforeground="#FFFFFF")
        self.__button_toggle = Button(frame_properties, text="DISABLE", font=("Arial", 20), background="#DA0000", foreground="#FFFFFF", activebackground="#EA0000", activeforeground="#FFFFFF")
        self.__button_delete = Button(frame_properties, text="DELETE FILE", font=("Arial", 20), background="#DA0000", foreground="#FFFFFF", activebackground="#EA0000", activeforeground="#FFFFFF")

        label_display_name.pack(side=TOP, fill="x")
        label_file_name.pack(side=TOP, fill="x")
        ttk.Separator(frame_properties, orient="horizontal").pack(side="top", fill="x")
        label_location.pack(side="top", fill="x")
        label_category.pack(side="top", fill="x")
        ttk.Separator(frame_properties, orient="horizontal").pack(side="top", fill="x")
        self.__button_rename.pack(side="top", fill="x")
        self.__button_category.pack(side="top", fill="x")
        self.__button_toggle.pack(side="top", fill="x")
        self.__button_delete.pack(side="top", fill="x")

        # Pack both frames
        frame_modlist.pack(side=LEFT, fill="x")
        frame_properties.pack(side=LEFT, fill="y")

        # Set miscellaneous variables
        self.__selected_mod_id = None
        self.__mods_directory = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\PAYDAY3\\PAYDAY3\\Content\\Paks\\~mods"

    def launch(self):
        self.__displayMods()
        self.__root.mainloop()

    def __displayMods(self):
        self.__cursor.execute("SELECT id, displayname, filename, directory, category FROM mods;")
        rows = self.__cursor.fetchall()

        for row in rows:
            row = list(row)
            status = "DISABLED" if row[2].endswith("disabled") else "ENABLED"
            row.append(status)
            row[3] = row[3].split("Paks\\")[1]
            self.__mods.insert("", END, values=row)

    def __open_github(self):
        webbrowser.open("https://github.com/ZeMonsiM/PD3-ModManager") # TODO: Change URL to the repo URL instead of profile URL

    def __open_mws(self):
        webbrowser.open("https://modworkshop.net/user/cipherprotogen") # TODO: Change to Modworkshop page of the tool

    def __select_mod(self):
        try:
            mod_id = int(self.__var_mod_id.get())
            self.__cursor.execute("SELECT displayname, filename, directory, category FROM mods WHERE id = ?", (mod_id,))
            mod_data = self.__cursor.fetchone()
            if mod_data:
                self.__selected_mod_id = mod_id
                self.__mod_display_name.set(mod_data[0])
                self.__mod_file_name.set(mod_data[1])
                self.__mod_location.set(f"Location: {mod_data[2].split("Paks\\")[1]}")
                self.__mod_category.set(f"Category: {mod_data[3]}")
            else:
                showerror("ERROR", f"No mod is matching the ID {mod_id} !")
        except ValueError:
            showerror("ERROR", f"'{self.__var_mod_id.get()}' is not a valid mod ID!")

    def __rescan_folder(self):
        # Scan mod files
        files = os.walk(self.__mods_directory)
        list = []

        for loc in files:
            if ".git" in loc[0]:
                continue

            for file in loc[2]:
                if file.endswith(".pak") or file.endswith(".pak.disabled"):
                    list.append((loc[0], file))

        # Update local database with new mods
        for file in list:
            with open(os.path.join(file[0], file[1]), "rb") as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            display_name = file[1].split(".pak")[0]

            self.__cursor.execute(f"SELECT * FROM mods WHERE hash = '{file_hash}'")
            result = self.__cursor.fetchone()
            if not result:
                # Create new mod in database
                self.__cursor.execute(
                    f"INSERT INTO mods (filename, directory, displayname, hash) VALUES ('{file[1]}', '{file[0]}', '{display_name}', '{file_hash}')")
            else:
                # Mod already in database : check if the file location has been updated
                if result[1] != file[1]:
                    self.__cursor.execute(f"UPDATE mods SET filename='{file[1]}' WHERE hash='{file_hash}'")
                if result[2] != file[0]:
                    self.__cursor.execute(f"UPDATE mods SET directory='{file[0]}' WHERE hash='{file_hash}'")

        # TODO: Check for deleted mod files using MD5 hash

        # Render the updated mod list

application = ModManagerApp()
application.launch()
