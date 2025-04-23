# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 15:46:14 2025

@author: warlo
"""

import requests, bs4, re, random


def get_mobid(): #get random npc id
    
    url = "https://classicdb.ch/?npcs"
    
    res = requests.get(url)
    res.raise_for_status
    
    npcs = bs4.BeautifulSoup(res.text, 'html.parser')
    npcs = str(npcs)
   
    
    npc_ids = re.findall(r'id:(\d+)', npcs)
    
    npc_ids = [str(i) for i in npc_ids]
    
    
    random_npc_id = random.choice(npc_ids)
    
    return random_npc_id


def get_soup(mob_id):
    
    url = f"https://classicdb.ch/?npc={mob_id}"
    res = requests.get(url)
    res.raise_for_status()
    classicdb = bs4.BeautifulSoup(res.text, 'html.parser')
    
    return classicdb



def get_scripts(soup):
    
    scripts = soup.find_all('script')
    return scripts
    
def get_name(mob_id): #get name
    
    classicdb = get_soup(mob_id)
    name = classicdb.h1.text.replace(' - NPC', '')
    
    return name


def get_animation(mob_id):
    
    classicdb = get_soup(mob_id)
    scripts = get_scripts(classicdb)
    
    for script in scripts:

        match = re.search(r'\[li\]Model:\s*(\d+)\[/li\]', script.text, re.IGNORECASE)
        if match:
            model_id = match.group(1).replace(',', '')
            return f'https://classicdb.ch/models/{model_id}.gif'

    
    
def get_stat(mob_id): # get stats
    
    classicdb = get_soup(mob_id)
    scripts = get_scripts(classicdb)
    stats = ["health", "armor", "level", "damage",]
    stat_dict = {}
    for script in scripts:
         for stat in stats:
            if stat == "damage":
                match = re.search(r'["\']?damage["\']?\s*[:=]\s*([\d,]+)\s*-\s*([\d,]+)', script.text, re.IGNORECASE) #regex for the damage
                if match:

                        min_damage = int(match.group(1).replace(",", '')) #min damage
                        max_damage = int(match.group(2).replace(",", '')) #max damage
                    
                        stat_dict["damage"] = (min_damage, max_damage)
                        
                
            else:
                match = re.search(rf'["\']?{stat}["\']?\s*:\s*([\d,]+)', script.text, re.IGNORECASE) #regex, regular expression to find the target and remove the extra
                if match:
                
                    stat_dict[stat] = int(match.group(1).replace(',', ''))# remove commas and health and convert to int
         

            if len(stat_dict) == 4:
                break
            
    return stat_dict                

#name = get_name()