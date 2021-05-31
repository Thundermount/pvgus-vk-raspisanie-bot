import requests
from bs4 import BeautifulSoup
import time


group_index = ""
def get_schedule(date, group):
    response = requests.get("https://www.tolgas.ru/services/raspisanie/")
    group = group.upper()
    group = group.replace(" ","")
    soup = BeautifulSoup(response.text, "html.parser")
    select_input = soup.find(id="vr")
    options = select_input.find_all("option")
    for option in options:
        if option.get_text() == group:
            group_index = option['value']
            break
    if not group_index: return

    response = requests.post(
        "https://www.tolgas.ru/services/raspisanie/",
        data = {
            "rel": "0",
            "grp": "0",
            "prep": "0",
            "audi": "0",
            "vr" : group_index,
            "from": date,
            "to": date,
            "submit_button": "%CF%CE%CA%C0%C7%C0%D2%DC"
        }
    )

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", id="send")
    rows = table.find_all("tr")
    result = ""
    i = 0
    for row in rows:
        i+=1
        if i == 1: continue
        cols = row.find_all("td")
        for col in cols:
            result+=col.get_text()+"    "
        result += "\n"
    
    return result