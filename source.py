# test


import requests, time  # requests pulls URLs, time tracks how long pull takes
from bs4 import BeautifulSoup  # HTML parser, translates data from html to python
player = []

httpResponses = {  # dictionary of common status codes NOT including 200
    # do research down the line to see if any can be resolved              
                 
    # 200s - success
    201: "Resource successfully created",
    204: "Request successful, no content returned",
    
    # 300s - redirection
    301: "Resource permanently moved to a new location",
    302: "Resource temporarily found at another location",
    307: "Resource temporarily redirected to a new location",  # similar to 302, but resolving requires user to maintain same HTTP method
    308: "Resource permanently redirected to a new location",  # similar to 301, but resolving requires user to maintain same HTTP method
    
    # 400s - client error
    400: "Client sent invalid request",
    401: "Authentication required to access resource",
    403: "Access forbidden to resource",
    404: "Requested resource not found",
    405: "HTTP method not allowed for resource",
    
    # 500s - server error
    500: "Server encountered an unexpected error",
    502: "Invalid response from upstream server",
    503: "Service is currently unavailable",
    504: "Upstream server timeout occurred",
}

teamRosters = {  #WIP
    # figure out how to have a team roster here from pbleagues
    # would have to have the pull request somehow sign in before attempting to pull the data
}

requestStartTime = time.time()
url = input(f"Paste link for dataset and hit enter\n")
response = requests.get(url)
requestEndTime = time.time()


if response.status_code == 200:  # successful grab
    print(f"\nRequest successful | {((requestEndTime - requestStartTime) * 1000):.0f} ms")
else:  # unsuccessful grab
    if response.status_code in httpResponses:  # list of most common responses NOT including 200 
        print(f"\nRequest failed - {response.status_code}: {httpResponses[response.status_code]} | {((requestEndTime - requestStartTime) * 1000):.0f} ms")
    else:  # cover all case where the status code is not within the dictionary
        print(f"\nRequest failed, case not covered - {response.status_code} | {((requestEndTime - requestStartTime) * 1000):.0f} ms")
        

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

