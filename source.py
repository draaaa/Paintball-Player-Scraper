'''
IMPORTANT
it seems that keeping track of player stats is a recent thing, or the data for the player stats (starting at 2023 and before) are not accessible. 
this means either one of two things

    1. stop here, and say it's finished (boring)
        dont really wanna do this, because quitting from one roadblock like this is lame and stupid

    2. expand the scope, shift the data collection
        this means either leaving the player stat scraper as it's own thing entirely, and rennovating this code for using team stats instead
        using team stats will require a login (i think) so this shit is about to get much, much more complex

whether i flip this project on it's head or not, it's been fun to work on it, despite the trials and tribulations and mounts of stress that came with it at first
however, continuing to work on it will only look better for myself
whatever happens now, is completely up to myself
'''


from rich.table import Table
from rich.console import Console
from rich.text import Text
import requests, time  # requests pulls URLs, time tracks how long pull takes
from bs4 import BeautifulSoup  # HTML parser, translates data from html to python


console = Console()
table = Table(title = "Player Stats")  # title for table
player = []


events = {    # player stats from lone star, mid-atlantic, and windy city seem to be missing from the website for the 2023 season  
    2023 : {  
        "Sunshine State Major" : "https://pbleagues.com/event/7927/player-stats",
        "World Cup"            : "https://pbleagues.com/event/8196/player-stats",
        "Overall"              : "https://pbleagues.com/players-stats-rankings?league=316&year=2023"
    },
    2024 : {
        "Las Vegas Major"    : "https://pbleagues.com/event/8334/player-stats", 
        "Lone Star Major"    : "https://pbleagues.com/event/8335/player-stats",
        "Mid-Atlantic Major" : "https://pbleagues.com/event/8336/player-stats",
        "Windy City Major"   : "https://pbleagues.com/event/8337/player-stats", 
        "World Cup"          : "https://pbleagues.com/event/8338/player-stats",
        "Overall"            : "https://pbleagues.com/players-stats-rankings?league=316&year=2024"
    }
}


teamRosters = {  #WIP
    # figure out how to have a team roster here from pbleagues
    # would have to have the pull request somehow sign in before attempting to pull the data
}


eventYearInput = int(input(f"Enter the year of the event for the dataset\n"))
if eventYearInput not in events:  # year not in events dictionary, program termed
    print("Input not in events dictionary")
    quit()
eventNameInput = input(f"Enter the name of the event\n")
if eventNameInput not in events[eventYearInput]:  # event name not under year, program termed
    print(f"Input not in events dictionary for {eventYearInput}")
    quit()
url = events[eventYearInput][eventNameInput]


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
table.add_column("Points Won", justify = "right")
table.add_column("Points Lost", justify = "right")
table.add_column("Point Win %", justify = "right")


# sortMethod MUST match exact input from one of the tables - have to create a condition where this is not met
sortMethod = input(f"Stat to sort by: ")
sortedPlayer = sorted(player, key = lambda player: player[sortMethod])


def valueStyle(type, val1, val2):  # return text color 

    if str(type.lower()) == "rank":  # return color based on rank
        if val1 <= 50 and val1 > 20:
            return "gold3"
        elif val1 <= 20 and val1 > 3:
            return "chartreuse4"
        elif val1 <= 3:
            return "chartreuse1"

    elif str(type.lower()) == "winpercent":  # return color based on win percent
        if val1 <= 20:
            return "red3"
        elif val1 > 20 and val1 <= 40:
            return "dark_goldenrod"
        elif val1 > 40 and val1 <= 60:
            return "gold3"
        elif val1 > 60 and val1 <= 80:
            return "chartreuse4"
        elif val1 > 80 and val1 <= 100:
            return "chartreuse1"
        else:
            return "grey93" 

    elif str(type.lower()) == "pointswon":  # return color based on points won
        if val1 > val2:
            return "chartreuse1"
        elif val1 == val2:
            return "gold3"

    elif str(type.lower()) == "pointslost":  # return color based on points lost
        if val1 < val2:
            return "red3"
        elif val1 == val2:
            return "gold3"


for stat in sortedPlayer:  # loop to add data to table

    rankText = Text(  # dynamic text to change style of rank
        f"{str(stat['Rank'])}",
        style = valueStyle("Rank", stat["Rank"], None)
    )


    teamsText = Text(  # dynamic text modified if multiple teams exist for the entry
    " / ".join(stat["Team"].split(", ")) if ", " in stat["Team"] else stat["Team"]
    )


    pointWinPercentText = Text(  # dynamic text to change style of point win %
        f"{stat['Point Win Percent']:.2f}%",
        style = valueStyle("WinPercent", stat["Point Win Percent"], None)
    )


    pointWinText = Text(  # dynamic text to change style of points won
        f"{stat['Points Won']}",
        style = valueStyle("PointsWon", stat["Points Won"], stat["Points Lost"])
    )


    pointLoseText = Text(  # dynamic text to change style of points lost
        f"{stat['Points Lost']}",
        style = valueStyle("PointsLost", stat["Points Won"], stat["Points Lost"])
    )


    table.add_row(  # data added to table
    rankText,
    stat["Name"],
    teamsText,
    str(stat["Matches Played"]),
    str(stat["Points Played"]),
    pointWinText,
    pointLoseText,
    pointWinPercentText
    )
    

console.print(table)
