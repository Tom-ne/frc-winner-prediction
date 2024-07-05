import csv
import glob
import pandas as pd
import tba.api as tba
import threading
from time import sleep
import random

def add_match_data(match, event_key):
    sleep(random.uniform(0.5, 1.25))
    line = []

    line.append(match['match_number'])

    # Red 1
    line.append(match['alliances']['red']['team_keys'][0][3:])
    line.append(tba.get_team_win_lose_ratio(event_key, match['alliances']['red']['team_keys'][0]))
    line.append(tba.get_team_rank(match['alliances']['red']['team_keys'][0], event_key))

    # Red 2
    line.append(match['alliances']['red']['team_keys'][1][3:])
    line.append(tba.get_team_win_lose_ratio(event_key, match['alliances']['red']['team_keys'][1]))
    line.append(tba.get_team_rank(match['alliances']['red']['team_keys'][1], event_key))

    # Red 3
    line.append(match['alliances']['red']['team_keys'][2][3:])
    line.append(tba.get_team_win_lose_ratio(event_key, match['alliances']['red']['team_keys'][2]))
    line.append(tba.get_team_rank(match['alliances']['red']['team_keys'][2], event_key))

    # Blue 1
    line.append(match['alliances']['blue']['team_keys'][0][3:])
    line.append(tba.get_team_win_lose_ratio(event_key, match['alliances']['blue']['team_keys'][0]))
    line.append(tba.get_team_rank(match['alliances']['blue']['team_keys'][0], event_key))

    # Blue 2 
    line.append(match['alliances']['blue']['team_keys'][1][3:])
    line.append(tba.get_team_win_lose_ratio(event_key, match['alliances']['blue']['team_keys'][1]))
    line.append(tba.get_team_rank(match['alliances']['blue']['team_keys'][1], event_key))

    # Blue 3
    line.append(match['alliances']['blue']['team_keys'][2][3:])
    line.append(tba.get_team_win_lose_ratio(event_key, match['alliances']['blue']['team_keys'][2]))
    line.append(tba.get_team_rank(match['alliances']['blue']['team_keys'][2], event_key))


    popular_teams = ['254', '1678', '4144', '2910', '1577', '1690']

    exited = False

    for team in popular_teams:
        if team in tba.get_alliance_teams(match['alliances']['red']):
            line.append(-1)
            exited = True
            break
    
    if not exited:
        for team in popular_teams:
            if team in tba.get_alliance_teams(match['alliances']['blue']):
                line.append(1)
                exited = True
                break

    if not exited:
        line.append(0)

    line.append(tba.get_match_winner(match))

    return line


def combine_csv_files():
    csv_files = glob.glob('./tba/data/*.{}'.format('csv'))

    df_append = pd.DataFrame()
    for file in csv_files:
                df_temp = pd.read_csv(file)
                df_append = df_append.append(df_temp, ignore_index=True)

    df_append.to_csv('data.csv', index=False)

def collect_data_for_event(event, headers):
    matches = tba.get_matches_for_event(event)
    with open(f'./tba/data/data_{event}.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for match in matches:
            line = add_match_data(match, event)
            writer.writerow(line)

    print(f"finished writing data for {event}")

def main():
    events = tba.get_events_for_year(2023)

    headers = ['matchNumber', 'red1', 'red1winRatio', 'red1Rank', 'red2',
            'red2winRatio', 'red2Rank', 'red3', 'red3winRatio', 'red3Rank', 'blue1', 'blue1winRatio',
            'blue1Rank', 'blue2', 'blue2winRatio', 'blue2Rank', 'blue3', 'blue3winRatio', 'blue3Rank',
            'hasPopularTeam', 'winner']

    threads = []

    print(len(events))
    for event in events:
        print(f"collecting data for event: {event}...")
        thread = threading.Thread(target=collect_data_for_event, args=(event,headers))
        thread.setName(f"thread-{event}")
        thread.start()
        threads.append(thread)
        sleep(random.uniform(0.2, 0.45))

    for thread in threads:
        print(f"Waiting for {thread.getName()} to finish....")
        thread.join()

    for thread in threads:
        print(f"Waiting for {thread.getName()} to finish....")
        thread.join()


    print("writing final data file")
    combine_csv_files()
    print("DONE!")

if __name__ == "__main__":
    combine_csv_files()
    main()
