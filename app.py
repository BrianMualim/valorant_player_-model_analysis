# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 12:15:21 2025

@author: brian
"""

import streamlit as st
import pandas as pd
import requests
import datetime
import sys
import os

# Add the folder containing playerMatches.py to Python's import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from playerMatches import run_scraper  # function from earlier
from playerMatches import get_player_id_from_name  

input_name = st.text_input("Enter player name (e.g. Boaster):")

start_date = datetime.date(2025, 1, 1)
end_date = datetime.date.today()

input_range = st.date_input(
    "Select date range",
    value=(start_date, end_date),
    min_value=datetime.date(2020, 1, 1),
    max_value=datetime.date.today(),
    format="MM.DD.YYYY"
)

if st.button("Scrape Stats"):
    
    start_date, end_date = input_range #Unpacking dates for filter
    
    
    try:
        with st.spinner("Finding player ID..."):
            player_id, clean_name = get_player_id_from_name(input_name)

        with st.spinner("Scraping match data..."):
            data = run_scraper(player_id, clean_name, start_date, end_date)  # You must update scraper to use both
            df = pd.DataFrame(data)

        st.success(f"Scraped {len(df)} entries for {clean_name}")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, f"{clean_name}.csv", "text/csv")

    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        
        
        
        
        
        
        
