Python script to update a [Lick Hunter](http://www.lickhunter.com/) config script with an average of the last 24hs Binance futures liquidation values for each coin.

<br/>

# **Table of contents**

<!--ts-->
* [Installation](#installation)
    * [Requirements](#requirements)
    * [Install Dependencies](#install-dependencies)
    * [LH Config File](#lh-config-file)
* [General Config](#general-config)

<br/>

**Installation**
================

Requirements
------------
Base requirements: [Python 3](https://www.python.org/) & [pip](https://pip.pypa.io/en/stable/).

Dependencies are handled using [Pipenv](https://pypi.org/project/pipenv/). To install it:

```sh
$ pip install pipenv
```


<br/>

Install Dependencies
------------
```
$ pipenv install
```

<br/>

LH Config File
------------
place your `varPairs.json` (LHPC) or `pairs.json` (LH) into the root directory


<br/><br/>

**General Config**
==================

There is a config file for general settings: `settings/config.py`. You can place default values there or pass them as script arguments like: 
```sh
python fetch_avg_liq.py --config-file=varPairs.json
```

To see available arguments: 
```sh
$ python fetch_avg_liq.py -h
```


Use `min` & `max` settings as the general min/max values. It is useful to define a 'safety' range in where the liq value cannot exceed.
Anyway, the previous values can be overriden for a specific pair placing inside its configuraton the following properties:  `min_lick_value` and `max_lick_value`. For example:
```
{
	"symbol":  "1INCH",
	"longoffset":  "7.5",
	"shortoffset":  "7.5",
	"lickvalue":  "400",
	"min_lick_value":  "300",
	"max_lick_value":  "1000",
	"var_enabled":  true,
	"var_staticList":  true,
	"var_whiteList":  true,
	"var_blackList":  false,
	"tmp_kline_age":  "",
	"tmp_color":  "Black"
},
```

Also, there is a percentage factor that can be used to modify the average liq value. Eg: -0.1 to reduce 10%, or 0.3 to increase 30%
Use the `percent` setting to modify this value for all coins. Also, there is a property to override this factor for a specific pair: 
```
{
	"symbol":  "1INCH",
	"longoffset":  "7.5",
	"shortoffset":  "7.5",
	"lickvalue":  "400",
	"percentage_factor":  "0.8",
	...
},
```
