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
                try:
                    # Player name
                    player_name_elements = element.find_all("span", class_="master-games-username")
                    player1 = player_name_elements[0].get_text(strip=True)
                    player2 = player_name_elements[1].get_text(strip=True)

                    # Player rating
                    if len(element.find_all("span", class_="master-games-user-rating")) < 2:
                        rating1 = rating2 = "(nan)"
                    else:
                        ratings_elements = element.find_all("span", class_="master-games-user-rating")
                        rating1 = ratings_elements[0].get_text(strip=True)
                        rating2 = ratings_elements[1].get_text(strip=True)

                    # States & Opening
                    stats_opening_elements_temp = element.find("a", class_="master-games-content-stats")
                    stats_opening_elements = stats_opening_elements_temp.find_all("span")
                    stats = stats_opening_elements[0].get_text(strip=True)
                    opening = stats_opening_elements[1].get_text(strip=True)

                    # Result
                    result = element.find("td", class_="master-games-text-center").find("a").get_text(strip=True)

                    if result[:1] == '½':
                        wining1 = 0.5
                    else:
                        wining1 = result[:1]

                    if result[-1:] == '½':
                        wining2 = 0.5
                    else:
                        wining2 = result[-1:]

                    # Moves
                    moves = element.find("td", class_="master-games-text-right").find("a").get_text(strip=True)

                    # Year
                    year = element.find("a", class_="master-games-date").get_text(strip=True)

                    matches.append([
                        player1, wining1, rating1, player2, wining2, 
                        rating2, stats, opening, moves, year
                    ])

                except Exception as e:
                    print(f"Error processing element: {e}")
    df = pd.DataFrame(matches, columns=[
        "Player1 Name", "Number of player1 wining round", 
        "Ranking of player1", "Player2 Name", 
        "Number of player1 wining round", "Ranking of player2", 
        "Stats", "Opening", "Moves", "Year"
    ])
    df.to_csv("output.csv", index=False)
    print("Data saved to output.csv")
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