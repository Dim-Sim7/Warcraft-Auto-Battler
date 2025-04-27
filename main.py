# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 19:44:53 2025

@author: warlo
"""

import tkinter as tk
from auto_battler_gui import Animate_Gif
from auto_battler_gui import BattleWindow
from unit import Unit
import scrape_classicdb as scd

def main():
    
    # Create a root tkinter window
    
    root = tk.Tk()
    
    
    # Create enemies
    
    id1 = scd.get_mobid()
    id2 = scd.get_mobid()
    
    enemy1 = Unit.set_unit(id1)
    enemy2 = Unit.set_unit(id2)
    

    
    #Initialise gifs and pack
    gif1 = Animate_Gif(root, scd.get_animation(id1))
    gif1.pack()
    gif2 = Animate_Gif(root, scd.get_animation(id2))
    gif2.pack()
    
    # run the window
    window = BattleWindow(enemy1, enemy2)
    window.run()
    

    
    



main()