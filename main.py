from tkinter import ttk
from tkinter import *
import webbrowser
import sqlite3


class ModManagerApp:
    def __init__(self):
        # Create database connection
        self.__connection = sqlite3.connect('mods.db')
        self.__cursor = self.__connection.cursor()

        # Set up root window
        self.__root = Tk()
        self.__root.title("PAYDAY 3 Mod Manager")
        self.__root.config(background="#FFFFFF")
        self.__root.geometry("1187x600")
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

        # Create the mod list
        self.__mods = ttk.Treeview(frame_modlist, columns=("id", "displayname", "filename", "directory", "status"), show="headings", height=25)
        self.__mods.column("#1", anchor="w", width=35)
        self.__mods.heading("#1", text="ID")
        self.__mods.column("#2", anchor="w", width=325)
        self.__mods.heading("#2", text="Display name")
        self.__mods.column("#3", anchor="w", width=325)
        self.__mods.heading("#3", text="File name")
        self.__mods.column("#4", anchor="w", width=150)
        self.__mods.heading("#4", text="Location")
        self.__mods.column("#5", anchor="w", width=100)
        self.__mods.heading("#5", text="Status")
        self.__mods.pack(side=TOP, fill=BOTH, expand=True)

        # Create the text variables as class elements for properties frame
        self.__mod_display_name = StringVar()
        self.__mod_file_name = StringVar()
        self.__mod_location = StringVar()
        self.__mod_category = StringVar()

        self.__mod_display_name.set("DISPLAY_NAME")
        self.__mod_file_name.set("FILE_NAME")
        self.__mod_location.set("Location: MOD_LOCATION")
        self.__mod_category.set("Category: MOD_CATEGORY")

        # Create the UI elements for the properties frame
        label_display_name = Label(frame_properties, textvariable=self.__mod_display_name, font=("Arial", 24), background="#D9D9D9", justify="left")
        label_file_name = Label(frame_properties, textvariable=self.__mod_file_name, font=("Arial", 16), background="#D9D9D9", justify="left")
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

    def launch(self):
        self.__displayMods()
        self.__root.mainloop()

    def __displayMods(self):
        self.__cursor.execute("SELECT id, displayname, filename, directory FROM mods;")
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

    def scanModFolder(self):
        pass

application = ModManagerApp()
application.launch()
