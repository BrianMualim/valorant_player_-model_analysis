# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 18:22:39 2025

@author: brian
"""

from os import name
import requests
from bs4 import BeautifulSoup
from requests.api import head

#id must be a number

URL = 'https://www.vlr.gg/team/'+id
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
header_info = {}
roster_info = []
transaction_info = []