#!/usr/bin/env python
# coding: utf-8

# # Data Cleaning

# ## Imports

# In[1]:


import json
from pprint import pp
from functools import reduce
import re


# ### Read-in

# In[2]:


with open('../Data/character_table.json', encoding="utf-8") as f:
    data = json.load(f)
    
with open('../Data/skill_table.json', encoding="utf-8") as f:
    skill_data = json.load(f)


# ## Transform

# In[3]:


cleaned_data = {}
mapper = {"CASTER": "Caster",
          "MEDIC" : "Medic",
          "PIONEER" : "Vanguard",
          "SNIPER": "Sniper",
          "SPECIAL" : "Specialist",
          "SUPPORT" : "Supporter",
          "TANK" : "Defender",
          "WARRIOR" : "Guard",
          "TOKEN" : "Summoned Unit",
          "TRAP" : "Obstacle"}

replace_dict = {
    "atk" : "ATK",
    "def" : "DEF",
    "max hp" : "Max HP",
    "hp" : "HP",
    "block" : "Block",
    "range" : "Range",
    "\n" : " ",
    "deployment points" : "Deployment Points"
}

pattern = re.compile(r'<[^>]*>')


# In[4]:


def get_name(unit):
    return unit["name"]


# In[5]:


def get_class(unit):
    return mapper[unit["profession"]]


# In[6]:


def get_tags(unit):
    return unit["tagList"]


# In[7]:


def get_trait(unit):
    if unit["description"]:
        return pattern.sub("",unit["description"])
    else:
        return None


# In[8]:


def get_rarity(unit):
    return unit["rarity"] + 1


# In[9]:


def get_talents(unit):
    talent_list = unit["talents"]
    try:
        return [{talent["name"] : talent["description"] for talent in talents["candidates"] if talent["requiredPotentialRank"] == 0} for talents in talent_list]
    except TypeError:
        return None


# In[10]:


def get_skills(unit):
   skill_list = []
   skills = [skill["skillId"] for skill in unit["skills"]]
   try:
       for i, skill in enumerate(skills):
           name = skill_data[skill]["levels"][0]["name"]
           bb = { row["key"] : row["value"] for row in skill_data[skill]["levels"][0]["blackboard"]}
           skill_text = skill_data[skill]["levels"][-1]["description"].replace("-","")
           try:
               skill_text = reduce(lambda x,y: x.replace(y, replace_dict[y]), replace_dict, pattern.sub("",skill_text.lower().replace(":0%",":.0%").format(**bb)).capitalize())
           except KeyError:
               skill_text = skill_subroutine(skill_text, bb)
           unit_name = get_name(unit)
           skill_list.append({name : skill_text.replace(unit_name.lower(),unit_name)})
       return skill_list
   except KeyError:
       return None


# In[11]:


def skill_subroutine(skill_text, bb):
    skill_pattern = re.compile(r'{[^}]*\.')
    dict_pattern = re.compile(r'^([^.]+\.)')

    skill_text = skill_pattern.sub("{", skill_text)
    bb = {dict_pattern.sub("", key) : value for key, value in bb.items()}

    return reduce(lambda x,y: x.replace(y, replace_dict[y]), replace_dict, pattern.sub("",skill_text.replace(":0%",":.0%").format(**bb)))


# In[17]:


cleaned_data = {}
for key, unit in data.items():
    cleaned_data[get_name(unit)] = {
        "rarity" : get_rarity(unit),
        "class" : get_class(unit),
        "tags" : get_tags(unit),
        "trait" : get_trait(unit),
        "talents" : get_talents(unit),
        "skills" : get_skills(unit),
        "image" : f"https://raw.githubusercontent.com/Aceship/AN-EN-Tags/master/img/characters/{key}_1.png",
        "internal_id" : key
    }
    if cleaned_data[get_name(unit)]['rarity'] > 3:
        cleaned_data["image_e2"] = f"https://raw.githubusercontent.com/Aceship/AN-EN-Tags/master/img/characters/{key}_2.png"


# ## Load

# In[13]:


with open('../Data/cleaned_characters.json', 'w') as f:
    json.dump(cleaned_data, f, indent=4)

