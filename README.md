#  NBA Player Stats Comparator

A Python-based web application that scrapes NBA player statistics from [Basketball Reference](https://www.basketball-reference.com/) and compares them against LeBron James using a Flask web interface.

---

## Features

- Scrapes player statistics using `requests`, `BeautifulSoup`, and `pandas`
- Uses multithreading to speed up HTTP requests
- Compares selected player stats against LeBron James
- Displays results in a simple, interactive Flask web app
- Validates and cleans data with JupyterLab before deployment

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/nba-comparator.git
cd nba-comparator

```

2. **Install Dependencies**
```
pip install -r requirements.txt
```

4. Start the Flask Server
```
python app.py
```

6. Open the app
Open your browser and go to:
```
http://127.0.0.1:5000
```

8. Usage
Enter the name of any NBA player to compare their statistics with LeBron James.


