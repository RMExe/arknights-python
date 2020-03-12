#!/usr/bin/env python
# coding: utf-8

# # Discord Embed

# ## Imports

import json
import discord
from fuzzywuzzy.process import extractOne


# ### Read-in

with open("../Data/cleaned_characters.json", encoding="UTF-8") as f:
    data = json.load(f)


operators = list(filter(lambda x: x not in ['Medic Drone', 'Tentacle', 'Mirage', 'Roadblock', 'Stun Generator', 'Gate', 'Detector', 'Jammer', 'Turret'], data.keys()))


# ## Transform

def make_fields(unit):
    fields = [{"name" : "Trait", "value" : unit["trait"]}] + make_talents(unit) + make_skills(unit)
    return fields


def make_talents(unit):
    return [{"name" : key, "value" : value} for talent in unit["talents"] for key, value in talent.items()]


def make_skills(unit):
    return [{"name" : key, "value" : value, "inline" : True} for skill in unit["skills"] for key, value in skill.items()]


def build_dict(name):
    unit = data[name]
    url = "https://aceship.github.io/AN-EN-Tags/akhrchars.html?opname="
    icon_url = "https://raw.githubusercontent.com/Aceship/AN-EN-Tags/master/img/classes/class_{}.png"
    av_url = "https://raw.githubusercontent.com/Aceship/AN-EN-Tags/master/img/avatars/{}.png"
    embed_dict = {
        "title" : name,
        "description" : "★" * unit["rarity"],
        "url" : url + name,
        "thumbnail" : {
            "url" : av_url.format(unit["internal_id"])
        },
        "image" : {
            "url" : unit["image"]
        },
        "author" : {
            "name" : unit["class"],
            "icon_url" : icon_url.format(unit["class"].lower())
        },
        "fields" : make_fields(unit)
    }
    
    return embed_dict


def build_arknights_embed(name, elite=1):
    return discord.Embed.from_dict(build_dict(name))


def arknights(name):
    result = extractOne(name, operators)
    embed = build_arknights_embed(result[0])
    return embed

