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
from Logger.AppLogger import AppLogger

class LiqValue():
    
    def __init__(self):
        settings_handler = Settings(description="Fetch and update liq values.")
        self.settings = settings_handler.get()
        self.logger = AppLogger().get()

    def exit_with_error(self, msg):
        print(msg)
        exit()


    def get_page_source(self):
        try:
            self.logger.debug('Fetching API')
            res = requests.get('https://liquidation.wtf/api/v0/liquidations/by_coin')
        except Exception as e:
            self.exit_with_error('Unable to get webpage.')
        else:
            return res.content.decode()


    def extract_data_points(self, source):
        return json.loads(source)


    def load_coin_data(self):
        try:
            var_pairs_file = open(self.settings['var_pairs_file_path'])
            self.backup_var_pairs_file()
            coin_data = json.load(var_pairs_file)
        except FileNotFoundError:
            self.exit_with_error('varPairs file not found: ' + self.settings['var_pairs_file_path'])
        else:
            var_pairs_file.close()
            return coin_data


    def modify_coin_data(self, data_points, coin_data):
        for point in data_points['data']:

            if 'coins' in coin_data:
                coins = coin_data['coins'] # modifying vairPairs.json
            else:
                coins = coin_data # modifying coins.json

            for coin in coins:
                if coin['symbol'] == point['symbol']:
                    min_liq_value = self.settings['general_min_liq_value']
                    max_liq_value = self.settings['general_max_liq_value']
                    percentage_factor = self.settings['general_percentage_factor']

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


    def write_coin_data(self, coin_data):
        var_pairs_file = open(self.settings['var_pairs_file_path'], 'w')
        json.dump(coin_data, var_pairs_file, indent=4)
        var_pairs_file.close()


    def backup_var_pairs_file(self):
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
            w_file = open(os.path.join(self.settings['backup_dir_name'], self.settings['var_pairs_file_path'] + '_' + timestamp + '.json'), 'w')
        except FileNotFoundError:
            os.mkdir(self.settings['backup_dir_name'])
            w_file = open(os.path.join(self.settings['backup_dir_name'], self.settings['var_pairs_file_path'] + '_' + timestamp + '.json'), 'w')

        w_file.write(open(self.settings['var_pairs_file_path']).read())
        w_file.close()


    def main(self):

        if '-d' in sys.argv:
            self.settings['run_as_daemon'] = True

        while True:
            print('Getting page source...')
            page_source = self.get_page_source()

            print('Extracting data points...')
            data_points = self.extract_data_points(page_source)

            print('Loading coin data...')
            coin_data = self.load_coin_data()

            print('Updating coin data...')
            self.modify_coin_data(data_points, coin_data)

            print('Writing coin data...')
            self.write_coin_data(coin_data)

            print('Done.')

            if self.settings['run_as_daemon']:
                print('Waiting ' + str(self.settings['daemon_wait_time_minutes']) + ' minutes.')
                sleep(60 * self.settings['daemon_wait_time_minutes'])
            else:
                break


if __name__ == '__main__':
    liq_value_saver = LiqValue()
    liq_value_saver.main()
