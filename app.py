from flask import Flask, render_template, redirect, url_for
from bs4 import BeautifulSoup
import pandas as pd
import requests
from threading import Thread

import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

session = requests.Session()

# Webscraper Logic
def find_player(player_name):

    # Turn player name into lower case
    name_lowercase = player_name.lower()
    surname = name_lowercase.split(' ')[1]

    api_key = os.getenv("api_key")
    target_url = f'https://www.basketball-reference.com/players/{surname[0]}/'
    scraper_url = f'http://api.scraperapi.com?api_key={api_key}&url={target_url}'

    response = session.get(scraper_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        print(f"Player menu parsed successfully!")
    else:
        print(f"Failed to retrieve page, status code: {response.status_code}")

    player_menu = soup.find('table', {'id': 'players'})

    found_html_id = None  # track if a valid player is found

    for row in player_menu.find_all('tr')[1:]:
        strong_tag = row.find('strong')
        if strong_tag:
            a_tag = strong_tag.find('a')
            if a_tag and a_tag.text.lower() == name_lowercase:
                found_html_id = a_tag['href']
                break 
    # If no player found, return None
    else: 
        return None
    
    html_id = found_html_id
    
    # Individual Player Homepage
    target_url1= f'https://www.basketball-reference.com{html_id}/'
    scraper_url1 = f'http://api.scraperapi.com?api_key={api_key}&url={target_url1}'

    response = session.get(scraper_url1)

    if response.status_code == 200:
        homepage = BeautifulSoup(response.text, 'lxml')
        print(f"{player_name} parsed successfully!")
    else:
        print(f"Failed to retrieve page, status code: {response.status_code}")

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

    return player


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        playername = request.form["player"]
        player_data = {}

        def wrapper(name, key):
            player_data[key] = find_player(name)

        # Create threads for both player lookups
        t1 = Thread(target=wrapper, args=(playername, 'player'))
        t2 = Thread(target=wrapper, args=('Lebron James', 'lebron'))

        # Start both threads
        t1.start()
        t2.start()

        # Wait for both threads to finish
        t1.join()
        t2.join()

        player = player_data.get('player')
        lebron = player_data.get('lebron')

        # Check for invalid player
        if player is None:
            return render_template("login.html", error=True)
        
        return render_template("base.html", player=player, lebron=lebron)
    else:   
        return render_template("login.html", error=False)

if __name__ == "__main__":
    app.run(debug=True)
    
