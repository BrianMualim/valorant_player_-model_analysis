# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 08:33:08 2025

@author: brian
"""
import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def run_scraper(player_id: int, player_name: str, output_dir: str = r"C:\Users\brian\Downloads\valo_scraper") -> list:
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
        match_list = driver.find_elements(By.CLASS_NAME, "mod-dark")[0].find_elements(By.TAG_NAME, "a")
        match_list[match_counter].click()
        time.sleep(2)

        date = driver.find_elements(By.CLASS_NAME, "moment-tz-convert")[0].text
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
        
        if match_counter >= 2:
            break
        
        driver.get(f"https://www.vlr.gg/player/matches/{player_id}/{player_name}/?page=1")
        time.sleep(1)

    driver.quit()

    # Save CSV
    os.makedirs(output_dir, exist_ok=True)
    csv_file_path = os.path.join(output_dir, f"{player_name}.csv")

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        field_names = ["Date", "Team1", "Team1_ELO", "Team2", "Team2_ELO", "Map", "Name", "Agent", "Kills", "Deaths", "Assists"]
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(player_list)

    return player_list


# f0rsaken = run_scraper(9801, "f0rsaken")



# Add date filter pre-scrape
# Add map filter post-scrape
with open(csv_output_file, 'w', newline= '') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames = field_names)
    writer.writeheader()
    writer.writerows(player_list)   
