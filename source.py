''' links that can be used for testing
https://pbleagues.com/players-stats-rankings?league=316&year=2024
https://pbleagues.com/players-stats-rankings?league=316&round=event=8334&year=2024&division=255-42
'''

from rich.table import Table
from rich.console import Console
from rich.text import Text
import requests, time  # requests pulls URLs, time tracks how long pull takes
from bs4 import BeautifulSoup  # HTML parser, translates data from html to python


console = Console()
table = Table(title = "Player Stats")  # title for table
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
formattedTable = soup.find("table", class_="table table-striped table-hover table-condensed playersTable")
formattedRows = formattedTable.find("tbody").find_all("tr")  # locate rows containing <tr>


for row in formattedRows:  # extract data for each row
    cells = row.find_all("td")  # extract elements from <td> rows
    if len(cells) < 10:
        continue
    player.append({
        "Rank": int(cells[0].text.strip()), 
        "Name": " ".join(cells[1].text.strip().split()), 
        "Team": " ".join(cells[2].text.strip().split()),
        "Matches Played": int(cells[3].text.strip()),
        "Points Played": int(cells[4].text.strip()),
        "Points Won": int(cells[5].text.strip()),
        "Points Lost": int(cells[6].text.strip()),
        "Points Tied": int(cells[7].text.strip()),
        "Point Win Percent": float(cells[9].text.strip().replace('%', ''))
    })


#               ("columnname", justify (default = left), style = "color? do more research")
table.add_column("Rank", justify = "right")
table.add_column("Name")
table.add_column("Team", no_wrap = True)
table.add_column("Matches Played", justify = "right")
table.add_column("Points Played", justify = "right")
table.add_column("Point Win %", justify = "right")


# sortMethod MUST match exact input from one of the tables - have to create a condition where this is not met
sortMethod = input(f"Stat to sort by: ")
sortedPlayer = sorted(player, key = lambda player: player[sortMethod])


def pointWinPercentStyle(x):  # return color name based on argument
    if x <= 20:
        return "dark_red"
    elif x > 20 and x <= 40:
        return "dark_goldenrod"
    elif x > 40 and x <= 60:
        return "gold3"
    elif x > 60 and x <= 80:
        return "chartreuse2"
    elif x > 80 and x <= 100:
        return "chartreuse1"
    else:
        return "grey93"


for stat in sortedPlayer:  # loop to add data to table
    
    teams = stat["Team"].split(", ")
    if len(teams) > 1:  # if there is more than 1 team
        formattedTeams = " / ".join(teams)
    else:
        formattedTeams = stat["Team"]
        
    pointWinPercentText = Text(  # dynamic text to change style 
        f"{stat['Point Win Percent']:.2f}%",
        style = pointWinPercentStyle(stat["Point Win Percent"])
    )
    
    
    table.add_row(  # data added to table
    str(stat["Rank"]),
    stat["Name"],
    formattedTeams,
    str(stat["Matches Played"]),
    str(stat["Points Played"]),
    pointWinPercentText
    )
    
console.print(table)
