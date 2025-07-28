from flask import Flask, render_template, redirect, url_for, request
from bs4 import BeautifulSoup
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

import os
os.environ["FLASK_ENV"] = "development"
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Webscraper Logic
def find_player(player_name):
    # Create a folder for saved HTML files
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    save_folder = os.path.join(BASE_DIR, "saved_html")
    os.makedirs(save_folder, exist_ok=True)

    # Turn player name into lower case
    name_lowercase = player_name.lower()
    surname = name_lowercase.split(' ')[1]

    api_key = os.getenv("api_key")
    target_url = f'https://www.basketball-reference.com/players/{surname[0]}/'
    scraper_url = f'http://api.scraperapi.com?api_key={api_key}&url={target_url}'

    response = requests.get(scraper_url)

    # Save html as a file
    player_menu_path = os.path.join(save_folder, "player_menu.html")
    if response.status_code == 200:
        with open(player_menu_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"Player menu HTML saved successfully! -> {player_menu_path}")
    else:
        print(f"Failed to retrieve page, status code: {response.status_code}")

    # Parse saved page
    with open(player_menu_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'lxml')
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

    response = requests.get(scraper_url1)

    # Save html as a file
    player_homepage_path = os.path.join(save_folder, f"{name_lowercase.replace(' ','_')}_homepage.html")

    if response.status_code == 200:
        with open(player_homepage_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"Player HTML saved successfully! -> {player_homepage_path}")
    else:
        print(f"Failed to retrieve page, status code: {response.status_code}")

    # Parse saved page
    with open(player_homepage_path, 'r', encoding='utf-8') as file:
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

    return player


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        playername = request.form["player"]
        player = find_player(playername)

        if player is None:
            return render_template("login.html", error=True)
        
        lebron = find_player('Lebron James')
        return render_template("base.html", player=player, lebron=lebron)
    else:   
        return render_template("login.html", error=False)

if __name__ == "__main__":
    app.run(debug=True)
    
