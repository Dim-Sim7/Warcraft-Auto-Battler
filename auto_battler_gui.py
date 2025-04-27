# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 17:25:48 2025

@author: warlo
"""

from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import requests
from io import BytesIO
import io
import scrape_classicdb as scd
import threading

class Animate_Gif(tk.Label):
    def __init__(self, master, url, delay=100):
        super().__init__(master)
        
        self.url = url
        self.delay = delay
        self.idx = 0
        self.frames = []
        self.durations = []
        self.after(10000, self.load_gif)
        
    
    def animate(self):
        if self.frames:
            self.idx = (self.idx + 1) % len(self.frames)
            self.config(image=self.frames[self.idx])
            self.after(self.delay, self.animate)
        
    def load_gif(self):
        try:
            response = requests.get(self.url)
            img_data = response.content
            img = Image.open(io.BytesIO(img_data))
                
                    # Convert gif into frames
            self.frames = []
            self.durations = []
            for frame in range(getattr(img, "n_frames", 1)):
                img.seek(frame)  # Move to each frame in the gif
                frame_image = ImageTk.PhotoImage(img.copy())  # Convert frame to PhotoImage
                self.frames.append(frame_image)
                duration = img.info.get("duration", 100)
                self.durations.append(duration)
            
            # Store the frames as a reference to prevent garbage collection
            self._frames = self.frames  # This stores the frames as instance variables
            
            # Display the first frame
            self.config(image=self.frames[0])
            self.after(self.durations[0], self.animate)
            
        except Exception as e:
            print("Failed to load GIF:", e)

class BattleWindow:
    
    def __init__(self, enemy1, enemy2):
        self.enemy1 = enemy1
        self.enemy2 = enemy2
        self.running = True
        self.root = tk.Tk()
        self.root.title("Warcraft Auto Battler")
        
        self.enemy_labels = {}
        self.setup_ui()
        
        self.thread = threading.Thread(target=self.start_battle)
        self.thread.daemon = True
        self.thread.start()
    

    
    def setup_ui(self):
        container = tk.Frame(self.root)
        container.pack(pady=20)
        
        left_frame = self.create_enemy_frame(container, self.enemy1)
        left_frame.pack(side="left", padx=20)
        
        right_frame = self.create_enemy_frame(container, self.enemy2)
        right_frame.pack(side="right", padx=20)
       
    
    
    def create_enemy_frame(self, parent, enemy):
        frame = tk.Frame(parent, padx=10, pady=10)
        
        tk.Label(frame, text=enemy.name, font=("Helvetica", 14, "bold")).pack()
        
        content_frame = tk.Frame(frame)
        content_frame.pack(side="top", padx=10)
        
        gif = Animate_Gif(frame, scd.get_animation(enemy.mob_id), delay=100)
        gif.pack(side="left")
        
        stats = (
            f"Level: {enemy.level}\n"
            f"HP: {enemy.health}\n"
            f"Attack: {enemy.attack_damage}\n"
            f"Armor: {enemy.armor}"
        )
        
        stats_label = tk.Label(content_frame, text=stats, font=("Helvetica", 12))
        stats_label.pack(side="left", padx=20)
        
        self.enemy_labels[enemy.name] = stats_label
        
        return frame
        
    def update_stats(self):
        
        if not self.running:
            return # don't update if window is closing
        
        try:
            for enemy in [self.enemy1, self.enemy2]:
                stats = (
                    f"Level: {enemy.level}\n"
                    f"HP: {enemy.health}\n"
                    f"Attack: {enemy.attack_damage}\n"
                    f"Armor: {enemy.armor}"
                )
                self.enemy_labels[enemy.name].config(text=stats)
        
        except tk.TclError:
            pass
    def start_battle(self):
        
        while self.running and self.enemy1.isAlive and self.enemy2.isAlive:
            self.enemy1.attack(self.enemy2)
            self.root.after(0, self.update_stats) # update gui

            if self.enemy2.health <= 0:
                break

            self.enemy2.attack(self.enemy1)
            self.root.after(0, self.update_stats)  # <--- update GUI
            if self.enemy1.health <= 0:
                break

    def close(self):
        self.running = False
        self.root.destroy()
        
    def run(self):
        
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.mainloop()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        