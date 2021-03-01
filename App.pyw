from tkinter import *

import tkinter.filedialog as tkdialog
import tkinter.messagebox as tkmessage

from shutil import copytree
from os import makedirs, listdir, getcwd
import json
import random

def create_dirs(path):
        try:
            makedirs(path)
        except FileExistsError:
            pass

"""Reference: https://tkdocs.com/shipman/"""
class App(Frame):

    version = "v0.1"
    author = "Geegaz"

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()

        try:
            with open("Resources/styles.json") as styles_file:
                styles = json.load(styles_file)

            self.configure(styles["mainFrame"])
            self.createWidgets(styles)
        except Exception as ex:
            self.show_error(str(ex), True)
    
    def show_error(self, message:str, fatal:bool):
        tkmessage.showerror("Error", message)
        if fatal:
            raise SystemExit

    # ┌1────────────────────────┐  ┌5────┐
    # │┌2───────┐┌3─────────┐   │  └─────┘
    # ││        ││          │   │
    # ││        │├4─────────┴──┐│
    # ││        │└─────────────┘│
    # │└────────┘               │
    # └─────────────────────────┘
    # -6----------------------------------
    # ┌7───────────────────────┐
    # ├8───────────────────────┴───────┬9┐
    # └────────────────────────────────┴─┘
    # -10---------------------------------
    # ┌11─────────┬12───┐
    # └───────────┴─────┘
    # ┌11─────────┬12─────────────────┐
    # └───────────┼13─────────────────┤
    #             └───────────────────┘
    # ┌14─────────┬15─────────────────┐
    # └───────────┼16─────────────────┤
    #             └───────────────────┘
    # ┌14─────────┬15─────────────────┐
    # └───────────┤                   │
    #             │                   │
    #             └───────────────────┘
    # -17---------------------------------
    # ┌18──────────────────────┐
    # ├19──────────────────────┴───────┬20
    # └────────────────────────────────┴─┘
    # ┌21──────────────────────┐
    # ├22──────────────────────┴───────┬23
    # └────────────────────────────────┴─┘
    # -24---------------------------------
    #             ┌25────────┐
    #             │          │
    #             └──────────┘
    #  1: headerFrame
    #  2: ├ headerLabelImage
    #  3: ├ headerLabelGGPI
    #  4: └ headerLabelTitle
    #  5: headerLabelAuthor
    #  6: separator1
    # 21: sourcepathLabel
    # 22: sourcepathEntry
    # 23: sourcepathButton
    # 10: separator1
    # 11: nameLabel
    # 12: nameEntry
    # 13: iconLabel
    # 14: iconEntry
    # 15: descriptionLabel
    # 16: descriptionText
    # 17: separator2
    # 18: resourcespathLabel
    # 19: resourcespathEntry
    # 20: resourcespathButton
    # 21: datapathLabel
    # 22: datapathEntry
    # 23: datapathButton
    # 24: separator3
    # 25: generateButton
    def createWidgets(self, styles):
        """Create and place all the widgets"""

        self.openImage = PhotoImage(file="Resources/open.png")
        self.titleImage = PhotoImage(file="Resources/icon.png")

        self.nameVar = StringVar()
        self.idVar = StringVar()
        self.sourcepathVar = StringVar()
        self.resourcespathVar = StringVar()
        self.datapathVar = StringVar()

        self.generate_status = ""
        def generate_callback():
            try:
                self.generate()
            except Exception as ex:
                self.show_error(f"Stopped at: {self.generate_status}\n{str(ex)}", False)

        current_row = 0
        self.headerFrame = Frame(self, bg="#222034")
        self.headerFrame.grid(column=0, row= current_row, columnspan=3, sticky=E+W)
        self.headerLabelImage = Label(self.headerFrame, styles["title"], image=self.titleImage, compound=LEFT)
        self.headerLabelImage.grid(column=0, row=0, rowspan=3, sticky=W)
        self.headerLabelGGPI = Label(self.headerFrame, styles["title"], text="GGPI", font=("Courier New", "60", "bold"), padx=10)
        self.headerLabelGGPI.grid(column=1, row=0, sticky=SW)
        self.headerLabelTitle = Label(self.headerFrame, styles["title"], text="Prop pack helper", font=("Courier New", "20", "bold"), padx=10)
        self.headerLabelTitle.grid(column=1, row=1, sticky=NW)
        self.headerLabelAuthor = Label(self, styles["gridHint"], text=f"{self.version} by {self.author}")
        self.headerLabelAuthor.grid(column=0, columnspan=3, row= current_row, sticky=NE)
        
        current_row += 1
        self.separator0 = Label(self, styles["separator"])
        self.separator0.grid(column=0, row= current_row, columnspan=3, sticky=E+W)

        current_row += 1
        self.sourcepathLabel = Label(self, styles["gridLabel"], text="Source resources directory:")
        self.sourcepathLabel.grid(column=0, row= current_row, columnspan=3, sticky=NW)
        current_row += 1
        self.sourcepathEntry = Entry(self, styles["entry"], textvar=self.sourcepathVar)
        self.sourcepathEntry.grid(column=0, row= current_row, columnspan=2, sticky=E+W)
        self.sourcepathButton = Button(self, styles["button"], image=self.openImage, compound=LEFT,
            command= lambda target=self.sourcepathVar: self.set_folder_path(target))
        self.sourcepathButton.grid(column=2, row= current_row, sticky=W)

        current_row += 1
        self.separator1 = Label(self, styles["separator"])
        self.separator1.grid(column=0, row= current_row, columnspan=3, sticky=E+W)

        current_row += 1
        self.idLabel = Label(self, styles["gridLabel"], text="Base model id: ")
        self.idLabel.grid(column=0, row= current_row, sticky=NW)
        self.idEntry = Entry(self, styles["entry"], width=3, textvar=self.idVar)
        self.idEntry.grid(column=1, row= current_row, sticky=W)
        current_row += 1
        self.idHint = Label(self, styles["gridHint"])
        self.idHint.grid(column=1, row= current_row, sticky=NW)

        current_row += 1
        self.nameLabel = Label(self, styles["gridLabel"], text="Pack name:")
        self.nameLabel.grid(column=0, row= current_row, sticky=NW)
        self.nameEntry = Entry(self, styles["entry"], width=60, textvar=self.nameVar)
        self.nameEntry.grid(column=1, row= current_row, sticky=W)
        current_row += 1
        self.nameHint = Label(self, styles["gridHint"], height=2, justify=LEFT)
        self.nameHint.grid(column=1, row= current_row, sticky=NW)

        current_row += 1
        self.iconLabel = Label(self, styles["gridLabel"], text="Pack icon: ")
        self.iconLabel.grid(column=0, row= current_row, sticky=NW)
        self.iconEntry = Entry(self, styles["entry"], width=60)
        self.iconEntry.grid(column=1, row= current_row, sticky=W)
        current_row += 1
        self.iconHint = Label(self, styles["gridHint"], text="minecraft:... or @model:... to use a model from the pack")
        self.iconHint.grid(column=1, row= current_row, sticky=NW)

        current_row += 1
        self.descriptionLabel = Label(self, styles["gridLabel"], text="Pack description: ")
        self.descriptionLabel.grid(column=0, row= current_row, sticky=NW)
        self.descriptionText = Text(self, styles["entry"], height=5, width=60)
        self.descriptionText.grid(column=1, row= current_row, sticky=W)

        current_row += 1
        self.separator2 = Label(self, styles["separator"])
        self.separator2.grid(column=0, row= current_row, columnspan=3, sticky=E+W)

        current_row += 1
        self.resourcespathLabel = Label(self, styles["gridLabel"], text="Exported resource pack directory:")
        self.resourcespathLabel.grid(column=0, row= current_row, columnspan=3, sticky=NW)
        current_row += 1
        self.resourcespathEntry = Entry(self, styles["entry"], textvar=self.resourcespathVar)
        self.resourcespathEntry.grid(column=0, row= current_row, columnspan=2, sticky=E+W)
        self.resourcespathButton = Button(self, styles["button"], image=self.openImage, compound=LEFT,
            command= lambda target=self.resourcespathVar: self.set_folder_path(target))
        self.resourcespathButton.grid(column=2, row= current_row, sticky=W)

        current_row += 1
        self.datapathLabel = Label(self, styles["gridLabel"], text="Exported data pack directory:")
        self.datapathLabel.grid(column=0, row= current_row, columnspan=3, sticky=NW)
        current_row += 1
        self.datapathEntry = Entry(self, styles["entry"], textvar=self.datapathVar)
        self.datapathEntry.grid(column=0, row= current_row, columnspan=2, sticky=E+W)
        self.datapathButton = Button(self, styles["button"], image=self.openImage, compound=LEFT,
            command= lambda target=self.datapathVar: self.set_folder_path(target))
        self.datapathButton.grid(column=2, row= current_row, sticky=W)

        current_row += 1
        self.separator3 = Label(self, styles["separator"])
        self.separator3.grid(column=0, row= current_row, columnspan=3, sticky=E+W)

        current_row += 1
        self.generateButton = Button(self, styles["button"], text="Generate", command=generate_callback)
        self.generateButton.grid(column=0, row= current_row, columnspan=3)

        self.idVar.trace_add("write", self.set_id)
        self.nameVar.trace_add("write", self.set_namespace)
        self.sourcepathVar.trace_add("write", self.set_namespace)
        self.bind_class("Entry","<Enter>", lambda event,style=styles["entry-hover"]: self.set_style(event,style))
        self.bind_class("Entry","<Leave>", lambda event,style=styles["entry"]: self.set_style(event,style))
        self.bind_class("Text","<Enter>", lambda event,style=styles["entry-hover"]: self.set_style(event,style))
        self.bind_class("Text","<Leave>", lambda event,style=styles["entry"]: self.set_style(event,style))

        self.set_namespace()
        self.set_id()
    
    def set_namespace(self, var=None, index=None, mode=None):
        namespace = self.nameEntry.get().lower().replace(" ", "_")
        source = self.sourcepathEntry.get()
        if namespace == "":
            if source == "":
                self.nameHint.configure(text="Please specify a pack name")
            else:
                name = source.rsplit("/")[0]
                namespace = name.lower().replace(" ", "_")
                self.nameHint.configure(text=f"Using source folder name \"{name}\"\nDatapack will be generated with the namespace \"{namespace}\"")
        else:
            self.nameHint.configure(text=f"Datapack will be generated with the namespace \"{namespace}\"")
    
    def set_id(self, var=None, index=None, mode=None):
        textid = self.idEntry.get()[:3]
        self.idVar.set(textid)
        if textid == "":
            self.idHint.configure(text="ex: 170, 500, 483...")
        else:
            if textid.isnumeric():
                self.idHint.configure(text=f"will be used as {int(textid[:3])*10000}")
            else:
                self.idHint.configure(text="invalid id")
    
    def set_style(self, event, style):
        event.widget.configure(style)
    
    def set_folder_path(self, target_var:StringVar):
        path = tkdialog.askdirectory()
        if path != "":
            target_var.set(path)

    def generate(self):
        paths = {
            "source": self.sourcepathEntry.get(),
            "target_resources": self.resourcespathEntry.get(),
            "target_data": self.datapathEntry.get()
        }
        for path in paths:
            if paths[path] == "":
                paths[path] = "."

        name = self.nameEntry.get()
        namespace = self.nameEntry.get().lower().replace(" ", "_")
        description = self.descriptionText.get("1.0",END)
        icon = self.iconEntry.get()
        base_id = self.idEntry.get()

        if icon.startswith("@model"):
            custom_icon = True
            custom_icon_name = icon.rsplit(":")[0]
            custom_icon_id = 0
        else:
            custom_icon = False

        source_modelpath = f"{paths['source']}/assets/minecraft/models"
        target_modelpath = f"{paths['target_resources']}/assets/minecraft/models"
        loottablespath = f"{paths['target_data']}/data/{namespace}/loot_tables/ggpi/items/prop"
        advancementspath = f"{paths['target_data']}/data/{namespace}/advancements/ggpi"

        mcmeta = {
            "pack": {
                "description": f"{description}",
                "pack_format": 6
            }
        }
        
        #───────────────────────────────────── Resource pack generation ─────────────────────────────────────#
        self.generate_status = "Resource pack generation"

        if base_id.isnumeric():
            model_id = int(base_id[:3])*10000
        elif base_id == "":
            raise Exception("Empty id")
        else:
            raise TypeError(f"Invalid id: {base_id}")

        model_overrides = []
        model_file = {
            "parent": "item/generated",
            "textures": {
                "layer0": "item/clay_ball"
            }
        }

        copytree(source_modelpath, target_modelpath, dirs_exist_ok=True)
        self.generate_status += "\n- Copied source resources to destination"
        

        with open(f"{paths['target_resources']}/pack.mcmeta", "w") as f:
            f.write(json.dumps(mcmeta, indent=4))
            self.generate_status += f"\n- Finished writing {f.name}"

        for filepath in listdir(f"{source_modelpath}/prop"):
            if filepath.endswith(".json"):
                model_id += 1
                name = filepath.rsplit('.', 1)[0]
                if model_id//10000 > 170:
                    raise IndexError(
                        "Too many models (>10000)")
                model_overrides.append(
                    {
                        "predicate": {
                            "custom_model_data": model_id
                        },
                        "model": f"prop/{name}"
                    }
                )
                if custom_icon:
                    if custom_icon_name == name:
                        custom_icon_id = model_id

        model_file["overrides"] = model_overrides
        
        with open(f"{target_modelpath}/item/clay_ball.json", "w") as f:
            f.write(json.dumps(model_file, indent=4))
            self.generate_status += f"\n- Finished writing {f.name}"
            
        
        #───────────────────────────────────── Data pack generation ─────────────────────────────────────#
        self.generate_status += "Data Pack generation"
        
        create_dirs(loottablespath)
        create_dirs(advancementspath)

        with open(f"{paths['target_data']}/pack.mcmeta", "w") as f:
            f.write(json.dumps(mcmeta, indent=4))
            self.generate_status += f"\n- Finished writing {f.name}"

        # Will be used to write the final loot table
        pools = []
        
        self.generate_status += "\n- Finished writing:"

        for model in model_overrides:
            model_name = model["model"].split("/")[-1]
            model_id = model["predicate"]["custom_model_data"]
            loot_table = {
                "pools": [
                    {
                        "rolls": 1,
                        "entries": [
                            {
                                "type": "minecraft:item",
                                "name": "minecraft:clay_ball",
                                "functions": [
                                    {
                                        "function": "minecraft:set_name",
                                        "name": {
                                            "text": "%s" % model_name.replace("_", " ").title(),
                                            "italic": "false"
                                        },
                                        "entity": "this"
                                    },
                                    {
                                        "function": "minecraft:set_lore",
                                        "lore":[
                                            {
                                                "text": "prop",
                                                "color": "gray",
                                                "italic": "false"
                                            }
                                        ],
                                        "entity": "this",
                                        "replace": "false"
                                    },
                                    {
                                        "function": "minecraft:set_nbt",
                                        "tag": "{CustomModelData:%s,ctc:{id:\"%s\", from:\"geegaz:ggpi\", traits:[\"prop\"]}}" % (model_id, model_name)
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }

            pools.append(
                {
                    "rolls": 1,
                    "entries": [
                        {
                            "type": "minecraft:loot_table",
                            "name": "%s:ggpi/items/prop/%s" % (namespace, model_name)
                        }
                    ]
                }
            )
            
            with open(f"{loottablespath}/{model_name}.json", "w") as f:
                f.write(json.dumps(loot_table, indent=4))
                self.generate_status += f"\n    {f.name}"
        
        with open(f"{loottablespath}/all_props.json", "w") as f:
            f.write(json.dumps({"pools": pools}, indent=4))
            self.generate_status += f"\n- Finished writing {f.name}"
        
        advancement = {
            "criteria": {
                "trigger": {
                    "trigger": "minecraft:tick"
                }
            },
            "display": {
                "announce_to_chat": "false",
                "description": f"{description}",

                "show_toast": "false",
                "title": f"{name}"
            },
            "parent": "geegaz:ggpi/ggpi"
        }
        if custom_icon:
            advancement["display"]["icon"] = {
                    "item": "minecraft:clay_ball",
                    "nbt" : "{CustomModelData:%s}" % custom_icon_id 
                }
        else:
            advancement["display"]["icon"] = {
                    "item": "%s" % icon
                }

        with open("%s/%s.json" % (advancementspath, namespace), "w") as f:
            f.write(json.dumps(advancement, indent=4))
            self.generate_status += f"\n- Finished writing {f.name}"
        
        #───────────────────────────────────── Finished ─────────────────────────────────────#
        self.generate_status = "\n Finished"
        message = f"Resourcepack sucessfully created in:\n{paths['target_resources']}\n\nDatapack sucessfully created in:\n{paths['target_data']}\n"
        tkmessage.showinfo("Sucess", message)


if __name__ == "__main__":
    app = App()
    app.master.title("GGPI prop pack helper")
    app.master.iconphoto(True, PhotoImage(file='Resources/icon.png'))
    app.mainloop()