# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 06:28:06 2025

@author: brian
"""

import requests
from bs4 import BeautifulSoup

URL = 'https://www.vlr.gg/player/' + '438'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
header = soup.find_all('div', class_="player-header")[0]
name = header.find_all('h1', class_="wf-title")[0].get_text().strip()
real_name = soup.find_all('h2', class_="player-real-name")[0].get_text().strip()

if len(header.find_all('a')) > 1:
    twitterHandle = header.find_all('a')[0]['href']
    twitchHandle = header.find_all('a')[1]['href']
else:
    twitterHandle = ""
    twitchHandle = ""

country = header.find_all('div', class_="ge-text-light")[0].get_text().strip()

container1 = soup.find_all('div', class_="player-summary-container-1")[0]
if len(container1.find_all('div', class_="wf-card")) > 1:
    currentTeamCard = container1.find_all('div', class_="wf-card")[1].find('a')
    teamIcon = "https:" + currentTeamCard.find('img')['src']
    teamName = currentTeamCard.find_all('div')[1].find('div').get_text().strip()
    desc = currentTeamCard.find_all('div')[1].find_all('div')[2].get_text().strip()
else:
    teamIcon = ""
    teamName = ""
    desc = ""

pastTeams = []
if len(container1.find_all('div', class_="wf-card")) > 2:
    teams = container1.find_all('div', class_= "wf-card")[2].find_all('a')
    
    for team in teams:
        oldTeamIcon = "https:" + team.find('img')['src']
        oldTeamName = team.find_all('div')[1].find_all('div')[0].get_text().strip()
        oldTeamDesc = team.find_all('div')[1].find_all('div')[2].get_text().strip()
        oldTeam = {
            'name': oldTeamName,
            'icon': oldTeamIcon,
            'desc': oldTeamDesc
            }
        pastTeams.append(oldTeam)
        



