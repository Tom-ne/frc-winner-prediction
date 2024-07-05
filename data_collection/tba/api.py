import requests
import json

config_data = json.load(open("config.json"))

base_url = "https://www.thebluealliance.com/api/v3"
events_url = f"{base_url}/event/{config_data['event_key']}/teams"
headers = {"X-TBA-Auth-Key": config_data['api_key']}

def get_events_for_year(year: int):
    # https://www.thebluealliance.com/api/v3/events/2023
    events = requests.get(f'{base_url}/events/{year}/keys', headers=headers)
    return events.json()

def get_matches_for_event(event_key):
    def get_event_url(event_key):
        return f"{base_url}/event/{event_key}/matches"
    matches = requests.get(get_event_url(event_key), headers=headers)

    if matches.status_code != 200:
        TypeError("Cannot get matches for event")

    return matches.json()

def get_blue_rp(match):
    return match['score_breakdown']['blue']['rp']

def get_red_rp(match):
    return match['score_breakdown']['red']['rp']

def get_matches(team_key, year):
    def get_matches_url(team_key, year):
        return f"{base_url}/team/{team_key}/matches/{year}/simple"
    response = requests.get(get_matches_url(team_key, year), headers=headers)

    if response.status_code!= 200:
        TypeError("Cannot get teams matches.")

    return response.json()   

def get_matches_for_event_team(event_key, team_key, year):
    all_matches = get_matches(team_key, year)

    total_matches = []

    for match in all_matches:
        if match['event_key'] == event_key:
            total_matches.append(match)

    return total_matches


def get_team_win_lose_ratio(event_key: str, team_key: str):
    data = requests.get(f"{base_url}/team/{team_key}/event/{event_key}/status", headers=headers).json()

    try:
        qual_data = data['qual']['ranking']
        losses = qual_data['record']['losses'] + 1
        wins = qual_data['record']['wins']
        return wins / losses
    except:
        return 0
    
def get_team_rank(team_key: str, event_key: str):
    data = requests.get(f"{base_url}/team/{team_key}/event/{event_key}/status", headers=headers).json()

    try:
        qual_data = data['qual']['ranking']
        return qual_data['rank']
    except:
        return 0

def get_alliance_teams(alliance):
    alliance_teams = ""

    for team in alliance['team_keys']:
        alliance_teams += f"{team[3:]}, "

    return alliance_teams[:len(alliance_teams) - 2]

def get_alliance_score(alliance):
    return alliance['score']

def get_match_winner(match):
    return match['winning_alliance']
