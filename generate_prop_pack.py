import os
import json
import random

def create_dirs(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass


pack_name = os.path.basename(os.getcwd())
namespace = pack_name.lower().replace(" ", "_")
models_path = "./assets/minecraft/models"
loot_tables_path = "./data/%s/loot_tables/ggpi/items/prop" % namespace
advancements_path = "./data/%s/advancements/ggpi" % namespace

base_id = 1700000
base_file = {
    "parent": "item/generated",
    "textures": {
        "layer0": "item/clay_ball"
    }
}
overrides = []

for filepath in os.listdir("%s/prop" % models_path):
    if filepath.endswith(".json"):
        base_id += 1
        if base_id//10000 > 170:
            raise IndexError(
                "Too many models (congrats on making THAT many) !")
        name = filepath.rsplit('.', 1)[0]
        overrides.append(
            {
                "predicate": {
                    "custom_model_data": base_id
                },
                "model": "prop/%s" % name
            }
        )

base_file["overrides"] = overrides

with open("%s/item/clay_ball.json" % models_path, "w") as f:
    j = json.dumps(base_file, indent=4)
    f.write(j)

#--- Datapack creation ---#

create_dirs(loot_tables_path)
create_dirs(advancements_path)

# Will be used to write the final loot table
pools = []

for model in overrides:
    name = model["model"].split("/")[-1]
    id = model["predicate"]["custom_model_data"]
    with open("%s/%s.json" % (loot_tables_path, name), "w") as f:
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
                                        "text": "%s" % name.replace("_", " ").title(),
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
                                    "tag": "{CustomModelData:%s,ctc:{id:\"%s\", from:\"geegaz:ggpi\", traits:[\"prop\"]}}" % (id, name)
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        f.write(json.dumps(loot_table, indent=4))
    pools.append(
        {
            "rolls": 1,
            "entries": [
                {
                    "type": "minecraft:loot_table",
                    "name": "%s:ggpi/items/prop/%s" % (namespace, name)
                }
            ]
        }
    )
        
with open("%s/all_props.json" % loot_tables_path, "w") as f:
    f.write(json.dumps({"pools": pools}, indent=4))

with open("./pack.mcmeta", "w") as f:
    mcmeta = {
        "pack": {
            "description": "A props pack",
            "pack_format": 5
        }
    }
    f.write(json.dumps(mcmeta, indent=4))

with open("%s/%s.json" % (advancements_path, namespace), "w") as f:
    advancement = {
        "criteria": {
            "trigger": {
                "trigger": "minecraft:tick"
            }
        },
        "display": {
            "announce_to_chat": "false",
            "description": "A props pack",
            "icon": {
                "item": "minecraft:clay_ball"
            },
            "show_toast": "false",
            "title": "%s" % pack_name
        },
        "parent": "geegaz:ggpi/ggpi"
    }
    f.write(json.dumps(advancement, indent=4))