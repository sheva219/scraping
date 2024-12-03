import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_national_ranking():
    url = "https://footballdatabase.com/ranking/azerbaijan/1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    ranking_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        clubs = soup.find_all(class_='limittext')
        for club in clubs:
            ranking_data.append(club.get_text(strip=True))
        return ranking_data
    else:
        print(f"Failed to fetch national ranking page. Status code: {response.status_code}")
        return []

def get_competition_data(ranking_data, urls):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    matches_data = []

    for url in urls:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            elements = soup.find_all(class_='club-gamelist-match')
            elements = elements[1:]

            for element in elements:
                try:
                    competition_name = element.find("a", class_="club-gamelist-match-info limittext").get_text(strip=True)
                    match_date = element.find("a", class_="club-gamelist-match-info limittext text-right").get_text(strip=True)
                    home_team = element.find("div", class_="club-gamelist-match-clubs").find("a").get_text(strip=True)
                    try:
                        home_team_ranking = ranking_data.index(home_team) + 1
                    except ValueError:
                        home_team_ranking = 0
                    score = element.find("div", class_="club-gamelist-match-score text-center").get_text(strip=True)
                    goal1 = score[:1]
                    goal2 = score[-1:]
                    if goal1 == goal2:
                        earning_score1 = earning_score2 = 1
                    elif goal1 > goal2:
                        earning_score1 = 3
                        earning_score2 = 0
                    else:
                        earning_score1 = 0
                        earning_score2 = 3
                    away_team = element.find_all("div", class_="club-gamelist-match-clubs")[1].find("a").get_text(strip=True)
                    try:
                        away_team_ranking = ranking_data.index(away_team) + 1
                    except ValueError:
                        away_team_ranking = 0
                    matches_data.append([
                        competition_name, match_date, home_team, goal1, earning_score1,
                        home_team_ranking, away_team, goal2, earning_score2, away_team_ranking
                    ])
                except Exception as e:
                    print(f"Error processing element: {e}")
        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")

    df = pd.DataFrame(matches_data, columns=[
        "Competition", "Date", "Home Team", "Number of Goal", "Earning_score", 
        "Home Team National Ranking", "Away Team", "Number of Goal", 
        "Earning score", "Away Team National Ranking"
    ])
    df.to_csv("output.csv", index=False)
    print("Data saved to output.csv")

def main():
    ranking_data = get_national_ranking()
    urls = [
        "https://footballdatabase.com/clubs-scores/qarabag/1",
        "https://footballdatabase.com/clubs-scores/qarabag/2"
    ]
    get_competition_data(ranking_data, urls)

if __name__ == "__main__":
    main()
