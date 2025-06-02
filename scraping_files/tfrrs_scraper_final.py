"""
Script to get all performances from all schools in the MIAC from the last four track seasons. Note: if necessary, script can
be reworked to remove all dependencies.
"""


from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import time

# Get MIAC home URL and make soup object
HOME_URL = "https://www.tfrrs.org/leagues/1408.html"
html = urlopen(HOME_URL).read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

# Go to each teams page and grab performances for the specified seasons
links = soup.find("table", class_="tablesaw table-striped table-bordered table-hover").find_all("a")
# season_ids = [382, 369, 335, 322, 292, 279, 255, 240]
season_ids = {
    "Outdoor 2025": 382,
    "Indoor 2025": 369,
    "Outdoor 2024": 335,
    "Indoor 2024": 322,
    "Outdoor 2023": 292,
    "Indoor 2023": 279,
    "Outdoor 2022": 255,
    "Indoor 2022": 240,
    "Outdoor 2021": 216,
    "Indoor 2021": 205,
    "Outdoor 2020": 189,
    "Indoor 2020": 178,
    "Outdoor 2019": 160,
    "Indoor 2019": 148,
    "Outdoor 2018": 131,
    "Indoor 2018": 125
}
df = pd.DataFrame()
n = len(links)
m = len(season_ids)
for i, link in enumerate(links):
    temp_df = pd.DataFrame()
    for j, id in enumerate(season_ids.keys()):

        # Grab performances for the given team and season
        time.sleep(0.5)
        team_page = urlopen(f"{link.get("href")}?config_hnd={season_ids[id]}").read().decode("utf-8")
        team_soup = BeautifulSoup(team_page, "html.parser")
        performance_link = team_soup.find("a", string="ALL PERFORMANCES").get("href")
        time.sleep(0.5)
        performance_page = urlopen(performance_link).read().decode("utf-8")
        page_soup = BeautifulSoup(performance_page, "html.parser")
        events = page_soup.find_all("h3", class_="font-weight-500")
        l = len(events)

        # Grab all performances for each event by forming columns for each relevant data label
        for k, event in enumerate(events):
            data = {}
            div = event.find_next("div", class_="performance-list-body")
            keys = set([el.get("data-label") for el in div.find_all("div", attrs={"data-label":True})])
            for key in keys:
                if key == "Athlete":
                    names = [" ".join(el.get_text().split()).split(',') for el in div.find_all("div", attrs={"data-label": key})]
                    data["First Name"] = list(map(lambda x: x[1], names))
                    data["Last Name"] = list(map(lambda x: x[0], names))
                else:
                    data[key] = [" ".join(el.get_text().split()) for el in div.find_all("div", attrs={"data-label": key})]
            data["Event"] = [" ".join(event.get_text().split()) for i in range(len(div.find_all("div", attrs={"data-label": list(keys)[0]})))]
            data["Season"] = id
            temp_df = pd.concat([temp_df, pd.DataFrame(data)], ignore_index=True)
            
            percentage = (i/n) + (j/(m*n)) + (k/(l*m*n))
            print(f'{percentage*100:.2f}%', end='\r')
        temp_df["School"] = link.get_text()
        temp_df["Category"] = link.get("href")
    df = pd.concat([df, temp_df], ignore_index=True)

# Label as m/f and save to csv
df["Category"] = df["Category"].map(lambda x: x[x.index("college_")+8])
df.drop(columns=["Place", "Conv"], inplace=True)
df.to_csv("../data/MIAC_data_final.csv", index=False)