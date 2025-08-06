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

    
def setup_driver() -> webdriver.Chrome:
    os.environ['PATH'] += r"C:/Program Files/ChromeDriver"
    return webdriver.Chrome()

def get_match_links(driver, player_id, player_name, page):
    url = f"https://www.vlr.gg/player/matches/{player_id}/{player_name}/?page={page}"
    driver.get(url)
    time.sleep(1)
    
    try:
        match_links = driver.find_elements(By.CLASS_NAME, "mod-dark")[0].find_elements(By.TAG_NAME, "a")
        date_elements  = driver.find_elements(By.CLASS_NAME, "m-item-date")
        
        if not match_links or not date_elements:
            return [], []
        return match_links, date_elements
    
    except IndexError:
        return [], []
        

def get_match_date(date_element) -> datetime.date:
    date_text = date_element.text.split()[0]
    return datetime.datetime.strptime(date_text, '%Y/%m/%d').date()


def parse_match_metadata(driver):
    team1 = driver.find_elements(By.CLASS_NAME, "wf-title-med")[0].text
    team1_elo = driver.find_elements(By.CLASS_NAME, "match-header-link-name-elo")[0].text[1:-1]
    team2 = driver.find_elements(By.CLASS_NAME, "wf-title-med")[1].text
    team2_elo = driver.find_elements(By.CLASS_NAME, "match-header-link-name-elo")[1].text[1:-1]
    return team1, team1_elo, team2, team2_elo


def parse_game_stats(driver, player_name, date, team1, team1_elo, team2, team2_elo):
    profiles = []
    games = driver.find_elements(By.CLASS_NAME, "vm-stats-gamesnav-item")

    # Go through each game
    for game_counter in range(1, len(games)):
        try:
            map_name = games[game_counter].find_element(By.TAG_NAME, "div").text
            games[game_counter].click()
            time.sleep(1)

            players = driver.find_elements(By.XPATH, "//table[contains(@class, 'wf-table-inset')]/tbody/tr")
            
            # Finding correct player
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

                profiles.append(profile)
                break
        except:
            continue

    return profiles

def run_scraper(player_id: int, player_name: str, 
                start_date: datetime, end_date: datetime,
                output_dir: str = r"C:\Users\brian\Downloads\valo_scraper") -> list:
    
    
    driver = setup_driver()
    player_list = []
    page = 1
    
    while True:
        
        
        match_links, date_elements = get_match_links(driver, player_id, player_name, page)
        
        if not match_links:
            break
        
        
        # i is used to get each date based on index
        for i in range(len(match_links)):
            
            match_links, date_elements = get_match_links(driver, player_id, player_name, page)
            date = get_match_date(date_elements[i])
            
            if date > end_date:
                continue
            if date < start_date:
                driver.quit()
                return player_list
            
            # Refresh clickable match links
            match_links[i].click()
            time.sleep(1)
            
            try:
                team1, team1_elo, team2, team2_elo = parse_match_metadata(driver)
            except:
                driver.back()
                time.sleep(1)
                continue
            
            
            profiles = parse_game_stats(driver, player_name, date, team1, team1_elo, team2, team2_elo)
            
            # Code for redundancy in stats
            for profile in profiles:
                
                if player_list and profile["Kills"] == player_list[-1]["Kills"] and \
                   profile["Deaths"] == player_list[-1]["Deaths"] and \
                   profile["Assists"] == player_list[-1]["Assists"]:
                    continue
                
                player_list.append(profile)

            driver.back()
            time.sleep(1)

        page += 1
            
    driver.quit()
    return player_list




# Add map filter post-scrape

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
