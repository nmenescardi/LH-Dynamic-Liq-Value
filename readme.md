
install Python 3

run `python -m pip install requests`

place varPairs.json into same directory

modify `general_min_liq_value` & `general_max_liq_value` for general min/max values

add `min_lick_value` and `max_lick_value` into varPairs.json for specific min/max values for each coin. For example:
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
