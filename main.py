import requests
from bs4 import BeautifulSoup
import pandas as pd
import certifi

import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("api_key")
target_url = 'https://www.basketball-reference.com/'

scraper_url = f'http://api.scraperapi.com?api_key={api_key}&url={target_url}'

response = requests.get(scraper_url)

# Save html as a file
if response.status_code == 200:
    with open('basketball_ref_homepage.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
    print("Page saved successfully!")
else:
    print(f"Failed to retrieve page, status code: {response.status_code}")

# Parse saved page
with open('basketball_ref_homepage.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'lxml')

# Select teams in dropdown menu
dropdown_menu = soup.find('select', {'id': 'select_team'})

team_names = []

# Iterate over each time in menu and append ID value 
# E.g /ATL/, /BOS/, etc. 
for option in dropdown_menu.find_all('option')[1:]:
    name = option.get('value')
    team_names.append(name)

nba_urls = []

# Create an array of html urls of each team
for team in team_names:
    team_url = f'https://www.basketball-reference.com{team}/2025.html'
    nba_urls.append(team_url)

for team in nba_urls:
    print(team)

    all_players = []

for team_url in nba_urls:
    # Use ScraperAPI's gateway to make the request
    scraperapi_url = f'http://api.scraperapi.com/?api_key={api_key}&url={team_url}'
    response = requests.get(scraperapi_url)

    # Check status code
    print(f"Requesting {team_url} => Status: {response.status_code}")

    if response.status_code != 200:
        print(f"Failed to retrieve page: {team_url}")
        continue
    
    soup = BeautifulSoup(response.text,'lxml')

    # Find per game table 
    per_game_table = soup.find('table', id="per_game_stats")

    # For each row (player), find the following stats
    for row in per_game_table.find_all('tr')[1:-1]:
        player = {}
        player['NAME'] = row.find('a').text.strip()
        
        player_cell = row.find('td', {'data-stat': 'name_display'})
        link_tag = player_cell.find('a')
        href = link_tag['href']
        player['ID'] = href.split('/')[-1].replace('.html', '')
        player['AGE'] = row.find('td', {'data-stat': "age"}).text
        player['POS'] = row.find('td', {'data-stat': "pos"}).text
        player['PPG'] = float(row.find('td', {'data-stat': "pts_per_g"}).text)
        player['APG'] = float(row.find('td', {'data-stat': "ast_per_g"}).text)
        player['RPG'] = float(row.find('td', {'data-stat': "trb_per_g"}).text)
        player['STL'] = float(row.find('td', {'data-stat': "stl_per_g"}).text)
        player['BLK'] = float(row.find('td', {'data-stat': "blk_per_g"}).text)
        player['LINK'] = f"https://www.basketball-reference.com{href}"
            
        all_players.append(player)
        
print(f"Table found: {bool(per_game_table)}")
print(f"Players so far: {len(all_players)}")

# Save stats as a df and convert into csv
nba_players = pd.DataFrame(all_players)
nba_players.to_csv('nba_players.csv', index=False)

# Read csv of nba players
nba = pd.read_csv('nba_players.csv')

def find_player(player_name):
    # Turn player name into lower case
    name_lowercase = player_name.lower()
    
    # Filter rows where the 'NAME' column matches the input
    result = nba[nba['NAME'].str.lower() == name_lowercase]

    # Return the first match as a dictionary
    if not result.empty:
        return result.iloc[0].to_dict()  
    else:
        return "Player not found"
    

print(find_player("Jordan Poole"))
print(find_player("Lebron James"))