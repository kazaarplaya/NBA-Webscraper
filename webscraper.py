import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

import os
from dotenv import load_dotenv
load_dotenv()

def find_player(player_name):
    # Turn player name into lower case
    name_lowercase = player_name.lower()
    
    surname = name_lowercase.split(' ')[1]

    api_key = os.getenv("api_key")
    target_url = f'https://www.basketball-reference.com/players/{surname[0]}/'
    scraper_url = f'http://api.scraperapi.com?api_key={api_key}&url={target_url}'

    response = requests.get(scraper_url)

    # Save html as a file
    if response.status_code == 200:
        with open('player.html', 'w', encoding='utf-8') as file:
            file.write(response.text)
        print("Player menu HTML saved successfully!")
    else:
        print(f"Failed to retrieve page, status code: {response.status_code}")

    # Parse saved page
    with open('player.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'lxml')

    player_menu = soup.find('table', {'id': 'players'})

    for row in player_menu.find_all('tr')[1:]:
        strong_tag = row.find('strong')
        if strong_tag:
            a_tag = strong_tag.find('a')
            if a_tag:
                if (a_tag.text).lower() == name_lowercase:
                    html_id = a_tag['href']
                    print(html_id)

    # Individual Player Homepage
    target_url1= f'https://www.basketball-reference.com{html_id}/'
    scraper_url1 = f'http://api.scraperapi.com?api_key={api_key}&url={target_url1}'

    response = requests.get(scraper_url1)

    # Save html as a file
    if response.status_code == 200:
        with open('player_homepage.html', 'w', encoding='utf-8') as file:
            file.write(response.text)
        print("Player HTML saved successfully!")
    else:
        print(f"Failed to retrieve page, status code: {response.status_code}")

    # Parse saved page
    with open('player_homepage.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    homepage = BeautifulSoup(html_content, 'lxml')

    per_game_table = homepage.find('table', id="per_game_stats")
    info = homepage.find('div', id="meta")

    player = {}
    player['NAME'] = info.select_one("span").text

    height = re.search(r'(\d-\d)', info.text)
    player['HEIGHT'] = height.group()

    row = per_game_table.find('tr', {'id': 'per_game_stats.2025'})

    img_tag = homepage.select_one("div.media-item img")
    player['IMG'] = img_tag["src"] if img_tag else ""

    if row: 
        player['TEAM'] = row.find('td', {'data-stat':'team_name_abbr'}).text
        player['AGE'] = row.find('td', {'data-stat': 'age'}).text
        player['POS'] = row.find('td', {'data-stat': "pos"}).text
        player['PPG'] = float(row.find('td', {'data-stat': "pts_per_g"}).text)
        player['APG'] = float(row.find('td', {'data-stat': "ast_per_g"}).text)
        player['RPG'] = float(row.find('td', {'data-stat': "trb_per_g"}).text)
        player['BLK'] = float(row.find('td', {'data-stat': "blk_per_g"}).text)
        player['STL'] = float(row.find('td', {'data-stat': "stl_per_g"}).text)
        
    print(player)
    
find_player("LeBron James")








# api_key = 'c705a34d71164fb13fa0a4ca3eccb356'
# target_url = 'https://www.basketball-reference.com/players/a/'

# scraper_url = f'http://api.scraperapi.com?api_key={api_key}&url={target_url}'

# response = requests.get(scraper_url)

# # Save html as a file
# if response.status_code == 200:
#     with open('player.html', 'w', encoding='utf-8') as file:
#         file.write(response.text)
#     print("Page saved successfully!")
# else:
#     print(f"Failed to retrieve page, status code: {response.status_code}")

# # Parse saved page
# with open('player.html', 'r', encoding='utf-8') as file:
#     html_content = file.read()

# soup = BeautifulSoup(html_content, 'lxml')

# player_menu = soup.find('table', {'id': 'players'})

# player = {} 

# for row in player_menu.find_all('tr')[1:]:
#     strong_tag = row.find('strong')
#     if strong_tag:
#         a_tag = strong_tag.find('a')
#         if a_tag:
#             # player['NAME'] = a_tag.text
#             html_id = a_tag['href']
#             print(f"{player['NAME']} | {html_id}")

# with open('sga.html', 'r', encoding='utf-8') as file:
#     sga = file.read()
    
# sga_html = BeautifulSoup(sga, 'lxml')

# per_game_table = sga_html.find('table', id="per_game_stats")
# info = sga_html.find('div', id="meta")

# player['NAME'] = info.select_one("span").text

# height = re.search(r'(\d-\d)', info.text)
# player['HEIGHT'] = height.group()


# row = per_game_table.find('tr', {'id': 'per_game_stats.2025'})

# img_tag = sga_html.select_one("div.media-item img")
# player['IMG'] = img_tag["src"] if img_tag else ""

# if row: 
#     player['TEAM'] = row.find('td', {'data-stat':'team_name_abbr'}).text
#     player['AGE'] = row.find('td', {'data-stat': 'age'}).text
#     player['POS'] = row.find('td', {'data-stat': "pos"}).text
#     player['PPG'] = float(row.find('td', {'data-stat': "pts_per_g"}).text)
#     player['APG'] = float(row.find('td', {'data-stat': "ast_per_g"}).text)
#     player['RPG'] = float(row.find('td', {'data-stat': "trb_per_g"}).text)
#     player['BLK'] = float(row.find('td', {'data-stat': "blk_per_g"}).text)
#     player['STL'] = float(row.find('td', {'data-stat': "stl_per_g"}).text)
    
# print(player)
    



    
    # Filter rows where the 'NAME' column matches the input
    # result = nba[nba['NAME'].str.lower() == name_lowercase]

    # # Return the first match as a dictionary
    # if not result.empty:
    #     return result.iloc[0].to_dict()  
    # else:
    #     return "Player not found"