from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# Load URL, build soup and find events
TFRRS_URL = "https://www.tfrrs.org/all_performances/MN_college_m_Carleton.html?list_hnd=5027&season_hnd=681"
html = urlopen(TFRRS_URL).read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
events = soup.find_all("h3", class_="font-weight-500")

# Construct dataframe by building column for each data label in event, then concatenate
df = pd.DataFrame()
for event in events:
    data = {}
    div = event.find_next("div", class_="performance-list-body")
    labels = set([el.get("data-label") for el in div.find_all("div", attrs={"data-label":True})])
    for label in labels:
        data[label] = [el.get_text().strip() for el in div.find_all("div", attrs={"data-label": label})]
    data["Event"] = [event.get_text().strip() for i in range(len(div.find_all("div", attrs={"data-label": list(labels)[0]})))]
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
df["School"] = "Carleton"

df.to_csv("../data/test.csv", index=False)