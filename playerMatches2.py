# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 08:33:08 2025

@author: brian
"""

import csv
import re
import time
import os
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

os.environ['PATH'] += r"C:/Program Files/ChromeDriver"
driver = webdriver.Chrome()

player_id = "Boaster"
# page_num = (Honestly last 50 games is a pretty good sample size)

driver.get("https://www.vlr.gg/player/matches/438/+" player_id + "/?page=" + "1")  # MUST BE GENERALIZED
time.sleep(2)

match_list = driver.find_elements(By.CLASS_NAME, "mod-dark")[0].find_elements(By.TAG_NAME, "a")
match_counter = 0
player_list = []

for match in match_list:
    
    match_list = driver.find_elements(By.CLASS_NAME, "mod-dark")[0].find_elements(By.TAG_NAME, "a")
    match_list[match_counter].click()
    
    # driver.get("https://www.vlr.gg/510155/fnatic-vs-team-heretics-esports-world-cup-2025-gf") # Hard code
    
    date = driver.find_elements(By.CLASS_NAME, "moment-tz-convert")[0].text
    team1 = driver.find_elements(By.CLASS_NAME, "wf-title-med")[0].text
    team1_elo = driver.find_elements(By.CLASS_NAME, "match-header-link-name-elo")[0].text[1:-1]
    
    team2 = driver.find_elements(By.CLASS_NAME, "wf-title-med")[1].text
    team2_elo = driver.find_elements(By.CLASS_NAME, "match-header-link-name-elo")[1].text[1:-1]
    
    game_counter = 1
    games = driver.find_elements(By.CLASS_NAME, "vm-stats-gamesnav-item")
    
    for game in games[:(len(games) -  1)]:
        
        map_name = games[game_counter].find_element(By.TAG_NAME, "div").text
        specific_game = games[game_counter].click()
        
        players = driver.find_elements(By.XPATH, "//table[contains(@class, 'wf-table-inset')]/tbody/tr")
        
        # Works
        for player in players:
            
            name = player.find_element(By.CLASS_NAME, "mod-player").find_element(By.CLASS_NAME, "text-of").text
            
            if name != player_id:
                continue
        
            else:
                agent = player.find_element(By.CLASS_NAME, "mod-agents").find_element(By.TAG_NAME, "img").get_attribute("title")
                kills = player.find_element(By.CLASS_NAME, "mod-vlr-kills").find_element(By.CLASS_NAME, "mod-both").text
                deaths = player.find_element(By.CLASS_NAME, "mod-vlr-deaths").find_element(By.CLASS_NAME, "mod-both").text
                assists = player.find_element(By.CLASS_NAME, "mod-vlr-assists").find_element(By.CLASS_NAME, "mod-both").text
                
                player_profile = {
                    "Date": date,
                    "Team1": team1,
                    "Team1_ELO": team1_elo,
                    "Team2": team2,
                    "Team2_ELO": team2_elo,
                    "Map": map_name,''
                    "Name": name,
                    "Agent": agent,
                    "Kills": kills,
                    "Deaths": deaths,
                    "Assists": assists
                    }
                player_list.append(player_profile)
                
                break
            
        game_counter += 1
    
    driver.get("https://www.vlr.gg/player/matches/438/boaster/?page=" + "1")
    
    match_counter += 1
    
    if match_counter > 3:
        break


field_names = ["Date", "Team1", "Team1_ELO", "Team2",
               "Team2_ELO", "Map", "Name", "Agent", "Kills",
               "Deaths", "Assists"]

csv_output_file = r"C:\Users\brian\Downloads\\valo_scraper\boaster2.csv"

with open(csv_output_file, 'w', newline= '') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames = field_names)
    writer.writeheader()
    writer.writerows(player_list)   
