# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 12:15:21 2025

@author: brian
"""

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import sys
import os

# Add the folder containing playerMatches.py to Python's import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from playerMatches import run_scraper  # function from earlier


def get_player_id_from_name(player_name: str) -> str:
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
            return parts[1], parts[2]  # return (player_id, player_name)
    
    raise ValueError(f"No player found for name: {player_name}")
    
    

input_name = st.text_input("Enter player name (e.g. Boaster):")

if st.button("Scrape Stats"):
    try:
        with st.spinner("Finding player ID..."):
            player_id, clean_name = get_player_id_from_name(input_name)

        with st.spinner("Scraping match data..."):
            data = run_scraper(player_id, clean_name)  # You must update scraper to use both
            df = pd.DataFrame(data)

        st.success(f"Scraped {len(df)} entries for {clean_name}")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, f"{clean_name}.csv", "text/csv")

    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"Unexpected error: {e}")