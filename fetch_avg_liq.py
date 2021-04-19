"""LH bot script helper to update liquidation values automatically using a 24hs aveage"""
__author__ = "Nicolas Menescardi"
__version__ = "1.0.0"
__license__ = "GNU General Public License v3.0"

import json
import os
import sys
from datetime import datetime
from time import sleep

import requests

from logger.app_logger import AppLogger
from settings.settings import Settings


class LiqValue:
    """Main Module class"""

    def __init__(self):
        settings_handler = Settings(description="Fetch and update liq values.")
        self.settings = settings_handler.get()
        self.logger = AppLogger().get()

    def exit_with_error(self, msg):
        """Helper function to show errors and exit"""
        self.logger.error(msg)
        sys.exit()

    def get_page_source(self):
        """Fetch and return API Response"""
        try:
            self.logger.debug("Fetching API data")
            res = requests.get("https://liquidation.wtf/api/v0/liquidations/by_coin")
        except requests.RequestException:
            self.exit_with_error("Unable to get webpage.")
        else:
            return res.content.decode()

    def load_coin_data(self):
        """Helper function to show errors and exit"""
        try:
            self.logger.debug("Opening coins config file")
            var_pairs_file = open(self.settings["var_pairs_file_path"])
            self.backup_var_pairs_file()
            coin_data = json.load(var_pairs_file)
            self.logger.debug(coin_data)
        except FileNotFoundError:
            self.exit_with_error(
                "varPairs file not found: " + self.settings["var_pairs_file_path"]
            )
        else:
            var_pairs_file.close()
            return coin_data

    def modify_coin_data(self, data_points, coin_data):
        """It modifies the liq value configuration for each coin"""
        for point in data_points["data"]:

            if "coins" in coin_data:
                coins = coin_data["coins"]  # modifying vairPairs.json
            else:
                coins = coin_data  # modifying coins.json

            for coin in coins:
                if coin["symbol"] == point["symbol"]:
                    min_liq_value = self.settings["general_min_liq_value"]
                    max_liq_value = self.settings["general_max_liq_value"]
                    percentage_factor = self.settings["general_percentage_factor"]

                    if "min_lick_value" in coin:
                        min_liq_value = float(coin["min_lick_value"])
                    if "max_lick_value" in coin:
                        max_liq_value = float(coin["max_lick_value"])
                    if "percentage_factor" in coin:
                        percentage_factor = float(coin["percentage_factor"])

                    average_usdt = float(point["average_usdt"])
                    liq_value_percentage = (
                        average_usdt + average_usdt * percentage_factor
                    )

                    if liq_value_percentage < min_liq_value:
                        liq_value = min_liq_value
                    elif liq_value_percentage > max_liq_value:
                        liq_value = max_liq_value
                    else:
                        liq_value = liq_value_percentage

                    new_lickvalue = int(liq_value)
                    percent_change = self.get_percent_change(
                        int(coin["lickvalue"]), new_lickvalue
                    )
                    self.logger.info(
                        "%s \t %s \t -> \t %s (%s)",
                        coin["symbol"],
                        coin["lickvalue"],
                        new_lickvalue,
                        percent_change,
                    )
                    coin["lickvalue"] = str(new_lickvalue)

    def get_percent_change(self, previous, current):
        """Get percentage of change between current and previous liq values"""
        if current == previous:
            return 0
        try:
            change = round((abs(current - previous) / previous) * 100.0, 2)
            sign = "+" if current >= previous else "-"
            return sign + str(change) + "%"
        except ZeroDivisionError:
            self.logger.error("Exception trying to divide by zero")
            return 0

    def write_coin_data(self, coin_data):
        """Writes modified data on config file"""
        var_pairs_file = open(self.settings["var_pairs_file_path"], "w")
        json.dump(coin_data, var_pairs_file, indent=4)
        var_pairs_file.close()

    def backup_var_pairs_file(self):
        """Helper function to backup old configuration"""
        self.logger.debug("Backing up old configuration")
        today = datetime.today()
        month = str(today.month)
        day = str(today.day)
        hour = str(today.hour)
        minute = str(today.minute)
        if len(month) == 1:
            month = "0" + month
        if len(day) == 1:
            day = "0" + day
        if len(hour) == 1:
            hour = "0" + hour
        if len(minute) == 1:
            minute = "0" + minute

        timestamp = (
            str(today.year) + "_" + month + "_" + day + "_" + hour + "_" + minute
        )
        filename = self.settings["var_pairs_file_path"] + "_" + timestamp + ".json"
        self.logger.debug("filename is: %s", filename)
        try:
            w_file = open(os.path.join(self.settings["backup_dir_name"], filename), "w")
        except FileNotFoundError:
            os.mkdir(self.settings["backup_dir_name"])
            w_file = open(os.path.join(self.settings["backup_dir_name"], filename), "w")

        w_file.write(open(self.settings["var_pairs_file_path"]).read())
        w_file.close()

    def main(self):
        """Main method to hanlde the process"""
        if "-d" in sys.argv:
            self.settings["run_as_daemon"] = True

        while True:
            self.logger.info("Getting page source...")
            page_source = self.get_page_source()

            self.logger.info("Extracting data points...")
            data_points = json.loads(page_source)

            self.logger.info("Loading coin data...")
            coin_data = self.load_coin_data()

            self.logger.info("Updating coin data...")
            self.modify_coin_data(data_points, coin_data)

            self.logger.info("Writing coin data...")
            self.write_coin_data(coin_data)

            self.logger.info("Done.")

            if self.settings["run_as_daemon"]:
                msg = (
                    "Waiting "
                    + str(self.settings["daemon_wait_time_minutes"])
                    + " minutes."
                )
                self.logger.info(msg)
                sleep(60 * self.settings["daemon_wait_time_minutes"])
            else:
                break


if __name__ == "__main__":
    liq_value_saver = LiqValue()
    liq_value_saver.main()
