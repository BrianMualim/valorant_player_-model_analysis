<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 12:17:38 2025

@author: brian
"""

import csv
import re
import time
import os
import datetime
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import threading
from your_scraper_file import run_scraper  # your scraping logic here

def start_scraping():
    player = player_entry.get()
    if not player:
        messagebox.showerror("Error", "Please enter a player ID")
        return

    # Run in background to avoid freezing GUI
    threading.Thread(target=run_scraper, args=(player,), daemon=True).start()

# GUI setup
root = tk.Tk()
root.title("Valorant Stats Scraper")

tk.Label(root, text="Enter player ID:").pack(pady=5)
player_entry = tk.Entry(root)
player_entry.pack(pady=5)

tk.Button(root, text="Start Scraping", command=start_scraping).pack(pady=10)

root.mainloop()

# player_id = "boaster"

# df = pd.read_csv(r"C:\\Users\\brian\\Downloads\\valo_scraper\\" + player_id + ".csv",  encoding='latin1')

# columns_to_check = ['Kills', 'Deaths', 'Assists']



=======
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 12:17:38 2025

@author: brian
"""

import csv
import re
import time
import os
import datetime
import pandas as pd


player_id = "boaster"

df = pd.read_csv(r"C:\\Users\\brian\\Downloads\\valo_scraper\\" + player_id + ".csv",  encoding='latin1')




>>>>>>> 6a1f8d2b621e45ba1566ffdfde637aa944d35c23
