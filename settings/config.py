"""Helper structure to set default config"""  # pylint: disable=line-too-long

import sys

default_config = [
    {
        "arg": "--config-file",
        "type": str,
        "default": "varPairs.json",
        "dest": "var_pairs_file_path",
        "help": "Config file path.",
    },
    {
        "arg": "--bk-dir",
        "type": str,
        "default": "varPairs_backup",
        "dest": "backup_dir_name",
        "help": "Backup directory name.",
    },
    {
        "arg": "--min",
        "type": int,
        "default": 700,
        "dest": "general_min_liq_value",
        "help": "General Minimum Liq Value.",
    },
    {
        "arg": "--max",
        "type": int,
        "default": sys.maxsize,
        "dest": "general_max_liq_value",
        "help": "General Maximum Liq Value.",
    },
    {
        "arg": "--percent",
        "type": float,
        "default": -0.1,
        "dest": "general_percentage_factor",
        "help": "Factor to modify the liq value percentually. Eg: -0.1 to reduce 10%, 0.3 to increase 30%",  # noqa: E501
    },
    {
        "arg": "--deamon",
        "action": "store_true",
        "dest": "run_as_daemon",
        "help": "Run script on deamon mode.",
    },
    {
        "arg": "--deamon-sleep",
        "type": int,
        "default": 1,
        "dest": "daemon_wait_time_minutes",
        "help": "Minutes to wait between each run.",
    },
]
