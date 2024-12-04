import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_competition_data(urls):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    matches = []
    for url in urls:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            elements = soup.find_all(class_="master-games-master-game")
            for element in elements:
                match = []
                try:
                    # Player name
                    elms = element.find_all("span", class_="master-games-username")
                    player1 = elms[0].get_text(strip=True)
                    player2 = elms[1].get_text(strip=True)
                    
                    # Player rating
                    elms = element.find_all("span", class_="master-games-user-rating")
                    rating1 = elms[0].get_text(strip=True)
                    rating2 = elms[1].get_text(strip=True)
                    
                    # States & Opening
                    elms = element.find_all("a", class_="master-games-content-stats")
                    elms = elms.find_all("span")
                    # States
                    states = elms[0].get_text(strip=True)
                    # Opening
                    opening = elms[1].get_text(strip=True)
                    
                    # Result
                    
                    
                    match.append(player1)
                    match.append(player2)
                    match.append(rating1)
                    match.append(rating2)
                    match.append(states)
                    match.append(opening)
                    match.append(result)
                    matches.append(match)
                except Exception as e:
                    print(f"Error processing element: {e}")
    print(len(matches))
    print(matches[0])
def main():
    urls = [
        "https://www.chess.com/games/search?fromSearchShort=1&p1=Nijat+Abasov&playerId=44585&page=1",
        "https://www.chess.com/games/search?fromSearchShort=1&p1=Nijat+Abasov&playerId=44585&page=2",
        "https://www.chess.com/games/search?fromSearchShort=1&p1=Nijat+Abasov&playerId=44585&page=3",
        "https://www.chess.com/games/search?fromSearchShort=1&p1=Nijat+Abasov&playerId=44585&page=4"
    ]
    get_competition_data(urls)

if __name__ == "__main__":
    main()