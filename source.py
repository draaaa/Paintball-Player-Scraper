''' links that can be used for testing
https://pbleagues.com/players-stats-rankings?league=316&year=2024
https://pbleagues.com/players-stats-rankings?league=316&round=event=8334&year=2024&division=255-42
'''

'''TODO (priority based)
1. sorting methods
'''


import requests, time  # requests pulls URLs, time tracks how long pull takes
from bs4 import BeautifulSoup  # HTML parser, translates data from html to python
player = []


teamRosters = {  #WIP
    # figure out how to have a team roster here from pbleagues
    # would have to have the pull request somehow sign in before attempting to pull the data
}


url = input(f"Paste link for dataset and hit enter\n")
try:  # request successful
    requestStartTime = time.time()
    response = requests.get(url, timeout = 20)
    response.raise_for_status()
    requestEndTime = time.time()
    print(f"\nRequest successful | {((requestEndTime - requestStartTime) * 1000):.0f} ms")

except requests.exceptions.Timeout:  # request failed, timeout
    requestEndTime = time.time()
    print(f"\nRequest failed - Request timed out | {((requestEndTime - requestStartTime) * 1000):.0f} ms")

except requests.exceptions.HTTPError as e:  # request failed, HTTP error
    requestEndTime = time.time()
    print(f"\nRequest failed - HTTP Error {e} | {((requestEndTime - requestStartTime) * 1000):.0f} ms")

except requests.exceptions.RequestException as e:  # request failed, acts as catchall 
    requestEndTime = time.time()
    print(f"\nRequest failed - {e} | {((requestEndTime - requestStartTime) * 1000):.0f} ms")


soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table", class_="table table-striped table-hover table-condensed playersTable")
rows = table.find("tbody").find_all("tr")  # locate rows containing <tr>


for row in rows:  # extract data for each row
    cells = row.find_all("td")  # extract elements from <td> rows
    if len(cells) < 10:
        continue
    player.append({
        "Rank": int(cells[0].text.strip()), 
        "Name": cells[1].text.strip(), 
        "Team": cells[2].text.strip(),
        "Matches Played": int(cells[3].text.strip()),
        "Points Played": int(cells[4].text.strip()),
        "Points Won": int(cells[5].text.strip()),
        "Points Lost": int(cells[6].text.strip()),
        "Points Tied": int(cells[7].text.strip()),
        "Point Win Percent": float(cells[9].text.strip().replace('%', ''))
    })


for stat in player:  # poorly structured print statement
    print(stat)