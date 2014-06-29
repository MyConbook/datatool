MyConbook
=========
MyConbook is a convention scheduling and guidebook application for your smartphone written by AndrewNeo.

If you are convention wishing to use MyConbook, please contact us instead to be published in the official app!

[MyConbook website](http://myconbook.net)

Directory structure
-------------------
The official MyConbook DataTool setup is as follows:

* `data2/` - Data directory published by HTTP
  * `info.json` - Con list and update info
  * `con1/` - Convention A
  * `con2/` - Convention B
* `test2/` - Test directory published by HTTP
  * `info.json`
  * `con1/`
  * `con2/`
* `_tool/` - This repository

### info.json structure
```
{
	"versions": {
		"android": 21 // Latest Android app version
	},
	"cons": {[
		{"path": "condir", "name": "Convention Name", "details": "Secondary line"}
		// Multiple cons are optional
	]}
}
```

If you want to use different directory names, change the options at the top of `mkdb.py`.


Adding a convention
-------------------
To add a convention, you need to create it in the `datafiles` directory. The subdirectory name for the con will be what you reference it by with the `mkdb.py` command line.

Inside should be a set of tab-seperated values files to build guide data, and a seperate `info.json` that defines base data. See [this Google Spreadsheet](https://docs.google.com/spreadsheet/ccc?key=0ArUq24tOO-47dFA4UmJmc2szaWR6U21jZnYtbkx0c1E&usp=sharing) for a template of the columns. Google Spreadsheets copies to the clipboard as tabs, for easy pasting into the text files.

The data files are the following, required unless otherwise marked:

* `info.json` - Convention information including schedule link and dates (see below)
* `restaurants.txt` - Restaurant guide (optional)
* `bars.txt` - Bars guide (optional)
* `stores.txt` - Stores guide (optional)
* `atms.txt` - ATMs guide (optional)
* `dealers.txt` - Dealers list
* `coninfo.txt` - Convention info
* `hotels.txt` - Hotel list
* `buildingmaps.txt` - Building map list

### info.json structure
```
{
	"Convention": "Convention Name",
	"DayList": ["2014-07-03", "2014-07-04", "2014-07-05", "2014-07-06"], // Array of dates for the schedule
	"CalendarURL": "", // URL for iCal file
	"ThursdayOffset": 0, // How many days before/after the first DayList day is a Thursday? If DayList[0] is a Friday this should be -1.
	"AreaMapURL": "", // URL for area map
	"ProviderDetails": "Data provided by MyConbook.", // Attribution shown on About screen
	"Timezone": "US/Pacific", // Timezone for convention, should be a Python timezone string
	"HasGuide": 1, // Set to 1 if we have guide files configured, 0 if no guide or using a URL
	"GuideURL": "" // Optional URL to open if no guide files configured
}
```


Publishing a convention
-----------------------
* Preview output JSON in console: `./mkdb.py --preview <name>`
* Push to testing: `./mkdb.py <name>`
* Push to production: `./mkdb.py --real <name>`
* Push and ignore unchanged schedule: `./mkdb.py --overwrite <name>` (add --real for production)
* Update maps: `./mkdb.py --new-maps <name>` (add --real for production)
* Run quietly in cron: `./mkdb.py --real --cron <name>`


License
-------
MyConbook for Android is licensed under the Apache license. See LICENSE.txt.

Redistributions **may not** use the official MyConbook data source without permission.
