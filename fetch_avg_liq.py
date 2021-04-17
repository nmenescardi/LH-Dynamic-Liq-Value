"""LH bot script helper to update liquidation values automatically using a 24hs aveage for each coin"""

__author__ = "Nicolas Menescardi"
__version__ = "1.0.0"
__license__ = "GNU General Public License v3.0"

import requests
import json
import os
import sys
import argparse
from datetime import datetime
from time import sleep
from Settings.Settings import Settings

SETTINGS = []

def exit_with_error(msg):
    print(msg)
    print('Press Enter to exit.')
    input()
    exit()


def get_page_source():
    try:
        res = requests.get('https://liquidation.wtf/api/v0/liquidations/by_coin')
    except Exception as e:
        exit_with_error('Unable to get webpage.')
    else:
        return res.content.decode()


def extract_data_points(source):
    return json.loads(source)


def load_coin_data():
    global SETTINGS
    try:
        var_pairs_file = open(SETTINGS['var_pairs_file_path'])
        backup_var_pairs_file()
        coin_data = json.load(var_pairs_file)
    except FileNotFoundError:
        exit_with_error('varPairs file not found: ' + SETTINGS['var_pairs_file_path'])
    else:
        var_pairs_file.close()
        return coin_data


def modify_coin_data(data_points, coin_data):
    global SETTINGS
    for point in data_points['data']:

        if 'coins' in coin_data:
            coins = coin_data['coins'] # modifying vairPairs.json
        else:
            coins = coin_data # modifying coins.json

        for coin in coins:
            if coin['symbol'] == point['symbol']:
                min_liq_value = SETTINGS['general_min_liq_value']
                max_liq_value = SETTINGS['general_max_liq_value']
                percentage_factor = SETTINGS['general_percentage_factor']

                if 'min_lick_value' in coin:
                    min_liq_value = float(coin['min_lick_value'])
                if 'max_lick_value' in coin:
                    max_liq_value = float(coin['max_lick_value'])
                if 'percentage_factor' in coin:
                    percentage_factor = float(coin['percentage_factor'])

                average_usdt = float(point['average_usdt'])
                liq_value_percentage = average_usdt + average_usdt * percentage_factor
                
                if liq_value_percentage < min_liq_value:
                    liq_value = min_liq_value
                elif liq_value_percentage > max_liq_value:
                    liq_value = max_liq_value
                else:
                    liq_value = liq_value_percentage

                coin['lickvalue'] = str(int(liq_value))


def write_coin_data(coin_data):
    global SETTINGS
    var_pairs_file = open(SETTINGS['var_pairs_file_path'], 'w')
    json.dump(coin_data, var_pairs_file, indent=4)
    var_pairs_file.close()


def backup_var_pairs_file():
    global SETTINGS
    today = datetime.today()
    month = str(today.month)
    day = str(today.day)
    hour = str(today.hour)
    minute = str(today.minute)
    if len(month) == 1:
        month = '0' + month
    if len(day) == 1:
        day = '0' + day
    if len(hour) == 1:
        hour = '0' + hour
    if len(minute) == 1:
        minute = '0' + minute

    timestamp = str(today.year) + '_' + month + '_' + day + '_' + hour + '_' + minute
    try:
        w_file = open(os.path.join(SETTINGS['backup_dir_name'], SETTINGS['var_pairs_file_path'] + '_' + timestamp + '.json'), 'w')
    except FileNotFoundError:
        os.mkdir(SETTINGS['backup_dir_name'])
        w_file = open(os.path.join(SETTINGS['backup_dir_name'], SETTINGS['var_pairs_file_path'] + '_' + timestamp + '.json'), 'w')

    w_file.write(open(SETTINGS['var_pairs_file_path']).read())
    w_file.close()


def main():
    global SETTINGS

    if '-d' in sys.argv:
        SETTINGS['run_as_daemon'] = True

    while True:
        print('Getting page source...')
        page_source = get_page_source()

        print('Extracting data points...')
        data_points = extract_data_points(page_source)

        print('Loading coin data...')
        coin_data = load_coin_data()

        print('Updating coin data...')
        modify_coin_data(data_points, coin_data)

        print('Writing coin data...')
        write_coin_data(coin_data)

        print('Done.')

        if SETTINGS['run_as_daemon']:
            print('Waiting ' + str(SETTINGS['daemon_wait_time_minutes']) + ' minutes.')
            sleep(60 * SETTINGS['daemon_wait_time_minutes'])
        else:
            break

    print('Success. Press Enter to exit.')
    input()


if __name__ == '__main__':
    settings_handler = Settings(description="Fetch and update liq values.")
    SETTINGS = settings_handler.get()
    main()
