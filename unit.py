# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 19:57:27 2025

@author: warlo
"""
##WARCRAFT AUTO-BATTLER CLASS: UNIT. 
import time
import random
import sys
import scrape_classicdb

class Unit:
    def __init__(self, name, health, armor, level, attack_damage, attack_message):
        self.name = name
        self.health = health
        self.armor = armor
        self.level = level
        self.attack_damage = attack_damage
        self.attack_message = attack_message
        self.isAlive = True
    
    def set_unit():
        
        mob_id = scrape_classicdb.get_mobid()
        name = scrape_classicdb.get_name(mob_id)
        stats = scrape_classicdb.get_stat(mob_id)
        if "armor" not in stats:
            stats["armor"] = 0
        if "level" not in stats:
            stats["level"] = 0
        print(name)
        print(stats)
        mob = Unit(name, stats['health'], stats['armor'], stats['level'], (stats['damage']), "attacks the enemy")
        print(f"mob.attack_damage = {mob.attack_damage}, type = {type(mob.attack_damage)}")
        
        return mob
        
    
    def take_damage(self, enemy):
        if self.health > 0:
        
            damage_reduction = self.armor / (self.armor + 400 + (85 * self.level)) 
            attack_range = list(range(enemy.attack_damage[0], enemy.attack_damage[1] + 1)) # turn tuple into array 
            attack_damage = random.choice(attack_range) # choose random number from array
            attack_damage = int(attack_damage - (attack_damage * damage_reduction))
            crit = random.randint(1, 100)
            
            if crit <= 5:
                attack_damage *= 2
                self.health -= attack_damage 
                print(f"{enemy.name} {enemy.attack_message} for {attack_damage} damage! CRIT!!!!!") 
            else:
                self.health -= attack_damage
                print(f"{enemy.name} {enemy.attack_message} for {attack_damage} damage!") 
                time.sleep(1)
            print (f"{self.name} has {self.health} health remaining")
            if self.health <= 0:
                self.isAlive = False
                print(f"{enemy.name} kills {self.name}")
                print(f"{self.name} is dead")
                sys.exit()

        else:
            self.isAlive = False
            print(f"{enemy.name} kills {self.name}")
            print(f"{self.name} is dead")
            sys.exit()

    
    def attack(self, enemy): #tiger(self) attack boar(enemy)
        while self.isAlive and enemy.isAlive:
            #self attacks first

            enemy.take_damage(self) # boar take damage from tiger
            time.sleep(1)
            self.take_damage(enemy) #tiger take damage from boar
            time.sleep(1)
            

mob1 = Unit.set_unit()
mob2 = Unit.set_unit()

mob1.attack(mob2)

                
    
        

            
        
        
        