<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 08:33:08 2025

@author: brian
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime



def get_player_id_from_name(player_name: str) -> str:
    
    # print("Hello")
    search_url = f"https://www.vlr.gg/search/?q={player_name}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the first link to a player profile
    result = soup.find("a", href=lambda x: x and x.startswith("/player/"))

    if result:
        href = result["href"]  # e.g., /player/438/boaster
        parts = href.strip("/").split("/")  # ['player', '438', 'boaster']
        if len(parts) >= 3:
            
            time.sleep(2)
            return parts[1], parts[2]  # return (player_id, player_name)
    
    raise ValueError(f"No player found for name: {player_name}")
    
    
    

def run_scraper(player_id: int, player_name: str, 
                start_date: datetime, end_date: datetime,
                output_dir: str = r"C:\Users\brian\Downloads\valo_scraper") -> list:
    os.environ['PATH'] += r"C:/Program Files/ChromeDriver"
    
    
    driver = webdriver.Chrome()
    player_list = []

    driver.get(f"https://www.vlr.gg/player/matches/{player_id}/{player_name}/?page=1")
    time.sleep(2)
    
    #page for match list
    match_list = driver.find_elements(By.CLASS_NAME, "mod-dark")[0].find_elements(By.TAG_NAME, "a")
    match_counter = 0
    
    # page for each match
    for _ in match_list:
        date = driver.find_elements(By.CLASS_NAME, "m-item-date")[match_counter].text.split()[0]
        date = datetime.datetime.strptime(date, '%Y/%m/%d').date()
        
        if date > end_date:
            match_counter += 1
            continue  # Skip future match
        
        if date < start_date:
            break  # Older than desired range
        
        
        
        match_list = driver.find_elements(By.CLASS_NAME, "mod-dark")[0].find_elements(By.TAG_NAME, "a")
        match_list[match_counter].click()
        time.sleep(2)

        # print(date)
        # date = driver.find_elements(By.CLASS_NAME, "moment-tz-convert")[0].text # Take date from VODS
        
        team1 = driver.find_elements(By.CLASS_NAME, "wf-title-med")[0].text
        team1_elo = driver.find_elements(By.CLASS_NAME, "match-header-link-name-elo")[0].text[1:-1]
        team2 = driver.find_elements(By.CLASS_NAME, "wf-title-med")[1].text
        team2_elo = driver.find_elements(By.CLASS_NAME, "match-header-link-name-elo")[1].text[1:-1]

        games = driver.find_elements(By.CLASS_NAME, "vm-stats-gamesnav-item")
        game_counter = 1

        for _ in games[:-1]:
            map_name = games[game_counter].find_element(By.TAG_NAME, "div").text
            games[game_counter].click()
            time.sleep(1)

            players = driver.find_elements(By.XPATH, "//table[contains(@class, 'wf-table-inset')]/tbody/tr")

            for player in players:
                name = player.find_element(By.CLASS_NAME, "mod-player").find_element(By.CLASS_NAME, "text-of").text

                if name.strip().lower() != player_name.strip().lower():
                    continue

                agent = player.find_element(By.CLASS_NAME, "mod-agents").find_element(By.TAG_NAME, "img").get_attribute("title")
                kills = player.find_element(By.CLASS_NAME, "mod-vlr-kills").find_element(By.CLASS_NAME, "mod-both").text
                deaths = player.find_element(By.CLASS_NAME, "mod-vlr-deaths").find_element(By.CLASS_NAME, "mod-both").text
                assists = player.find_element(By.CLASS_NAME, "mod-vlr-assists").find_element(By.CLASS_NAME, "mod-both").text

                profile = {
                    "Date": date,
                    "Team1": team1,
                    "Team1_ELO": team1_elo,
                    "Team2": team2,
                    "Team2_ELO": team2_elo,
                    "Map": map_name,
                    "Name": name,
                    "Agent": agent,
                    "Kills": kills,
                    "Deaths": deaths,
                    "Assists": assists
                }

                # Duplicate check
                if player_list:
                    last = player_list[-1]
                    if last["Kills"] == kills and last["Deaths"] == deaths and last["Assists"] == assists:
                        continue

                player_list.append(profile)
                break

            game_counter += 1
            
            

        match_counter += 1
        
        # if match_counter >= 2:
        #     break
        
        driver.get(f"https://www.vlr.gg/player/matches/{player_id}/{player_name}/?page=1")
        time.sleep(1)
        
        
        
    driver.quit()


    # This is for manual saving, there's another way of user saving in app.py
    # # Save CSV
    # os.makedirs(output_dir, exist_ok=True)
    # csv_file_path = os.path.join(output_dir, f"{player_name}.csv")

    # with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    #     field_names = ["Date", "Team1", "Team1_ELO", "Team2", "Team2_ELO", "Map", "Name", "Agent", "Kills", "Deaths", "Assists"]
    #     writer = csv.DictWriter(csv_file, fieldnames=field_names)
    #     writer.writeheader()
    #     writer.writerows(player_list)

    return player_list


# Add map filter post-scrape

# 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

################## TEST CASES

# start_date = datetime.date(2025, 7, 1)
# end_date = datetime.date(2025, 8, 4)

# f0rsaken = run_scraper(9801, "f0rsaken", start_date, end_date)
# f0rsaken = get_player_id_from_name('f0rsaken')



# os.environ['PATH'] += r"C:/Program Files/ChromeDriver"
# driver = webdriver.Chrome()
# player_list = []

# driver.get(f"https://www.vlr.gg/player/matches/438/boaster/?page=1")

# time.sleep(2)

# #page for match list
# match_list = driver.find_elements(By.CLASS_NAME, "mod-dark")[0].find_elements(By.TAG_NAME, "a")
# match_counter = 0
# match_list[match_counter].click()
# time.sleep(2)

# games = driver.find_elements(By.CLASS_NAME, "vm-stats-gamesnav-item")
# game_counter = 1

# map_name = games[game_counter].find_element(By.TAG_NAME, "div").text
# games[game_counter].click()
