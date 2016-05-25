import codecs
import string
import datetime
from database import Database, TableHandler
import helper

class Data(TableHandler):
	def __init__(self, options, data_path, table_name, columns):
		TableHandler.__init__(self, table_name, columns)
		self.options = options
		self.file_path = options.get_data_path(data_path)

	def parse(self, db, output_json):
		self.create_table(db)

		file_content = codecs.open(self.file_path, "r", self.options.encoding)
		column_count = len(self.columns)
		json_out = []

		for row in file_content:
			values = helper.trim_proper(row, column_count)
			args = self.insert_row(db, values)
			json_out.append(args)
			self.addl_parse(db, output_json, args)

		file_content.close()
		db.commit()
		output_json.update({self.table_name: json_out})

	def addl_parse(self, db, output_json, args):
		pass

class Dealers(Data):
	columns = [("Name", Database.C_TCN), "Location", "URL", "Description"]

	def __init__(self, options):
		Data.__init__(self, options, "dealers.txt", "dealers", self.columns)

class Restaurants(Data):
	columns = [("Name", Database.C_TCN), ("Category", Database.C_TCN), ("Rating", Database.C_I), ("Dollars", Database.C_I), "Address", "Phone", "Comments", "URL", "Thursday", "Friday", "Saturday", "Sunday", ("Delivery", Database.C_I), ("Closed", Database.C_I), "PlaceID", "YelpID"]
	datestr1 = "%m/%d/%Y %I%p"
	datestr2 = "%m/%d/%Y %I:%M%p"

	def __init__(self, options):
		Data.__init__(self, options, "restaurants.txt", "restaurants", self.columns)

	def create_table(self, cursor):
		Data.create_table(self, cursor)
		cursor.execute("CREATE TABLE restauranthours (_id integer PRIMARY KEY, RestaurantID integer, StartPeriod timestamp, EndPeriod timestamp)");
		cursor.execute("CREATE VIEW openrestaurants AS SELECT r.*, (SELECT COUNT(*) AS c FROM restauranthours WHERE RestaurantID = r._id and StartPeriod < DATETIME('now','localtime') and EndPeriod > DATETIME('now','localtime')) AS IsOpen, (SELECT COUNT(*) AS c FROM restauranthours WHERE RestaurantID = r._id) AS HasHours FROM restaurants AS r;");
		cursor.execute("CREATE VIEW restaurantcategories AS SELECT MIN(_id) AS _id, Category FROM restaurants GROUP BY Category ORDER BY Category");

	def parse(self, db, output_json):
		output_json["restauranthours"] = []
		Data.parse(self, db, output_json)

	def addl_parse(self, cursor, json_list, args):
		firstDate = datetime.datetime.strptime(self.options.day_list[0], "%Y-%m-%d") + datetime.timedelta(days=self.options.thursday_offset)
		did = 0
		dayArgCollection = [args["Thursday"], args["Friday"], args["Saturday"], args["Sunday"]]

		for day in dayArgCollection:
			dayOfCon = firstDate + datetime.timedelta(days=did)
			did += 1
			if (day == None): continue
			if (day.find("Closed") > -1): continue
			if (day.find("?") > -1): continue
			if (day.find("Reservation") > -1): continue
			for tp in day.split(";"):
				tpstr = dayOfCon.strftime("%m/%d/%Y ")
				if (day.find("24") > -1):
					tpstr1 = tpstr + "12am"
					tpstr2 = tpstr + "11:59pm"
				else:
					tps = tp.split("-")
					tpstr1 = tpstr + tps[0].replace(" ", "")
					if not tpstr1.endswith("m"):
						tpstr1 = tpstr1 + "m"
					tpstr2 = tpstr + tps[1].replace(" ", "")
					if not tpstr2.endswith("m"):
						tpstr2 = tpstr2 + "m"
				if (tpstr1.find(":") > 0): suse = self.datestr2
				else: suse = self.datestr1
				if (tpstr2.find(":") > 0): euse = self.datestr2
				else: euse = self.datestr1
				startS = datetime.datetime.strptime(tpstr1, suse)
				endS = datetime.datetime.strptime(tpstr2, euse)
				if (endS < startS): endS = endS + datetime.timedelta(days=1)
				rargs = {"ID": None, "RestaurantID": args["ID"], "StartPeriod": startS.isoformat(), "EndPeriod": endS.isoformat()}
				cursor.execute("INSERT INTO restauranthours VALUES (:ID, :RestaurantID, :StartPeriod, :EndPeriod)", rargs)
				rargs.update({"ID": cursor.get_last_row_id()})
				json_list["restauranthours"].append(rargs)

	def cleanup_args(self, args):
		if (args["Category"] is None):
			args["Category"] = "(None)"

		if (args["YelpID"] is not None):
			args["YelpID"] = args["YelpID"].replace("http://www.yelp.com/biz/", "")

class Bars(Data):
	columns = [("Name", Database.C_TCN), ("Category", Database.C_TCN), "Address", "Phone", "Comments", "URL", "Thursday", "Friday", "Saturday", "Sunday", "PlaceID", "YelpID"]

	def __init__(self, options):
		Data.__init__(self, options, "bars.txt", "bars", self.columns)

class Stores(Data):
	columns = [("Name", Database.C_TCN), ("Category", Database.C_TCN), "Address", "Phone", "Comments", "URL", "Thursday", "Friday", "Saturday", "Sunday", "PlaceID"]

	def __init__(self, options):
		Data.__init__(self, options, "stores.txt", "stores", self.columns)

class Atms(Data):
	columns = [("Name", Database.C_TCN), "Category", ("Building", Database.C_TCN), "Address", "PlaceID"]

	def __init__(self, options):
		Data.__init__(self, options, "atms.txt", "atms", self.columns)

class ConInfo(Data):
	columns = ["Name", "Location", "Details", "MapName"]

	def __init__(self, options):
		Data.__init__(self, options, "coninfo.txt", "coninfo", self.columns)

class Hotels(Data):
	columns = ["Name", "Address", "Phone", "PlaceID"]

	def __init__(self, options):
		Data.__init__(self, options, "hotels.txt", "hotels", self.columns)

class BuildingMaps(Data):
	columns = ["Name", "Filename"]

	def __init__(self, options):
		Data.__init__(self, options, "buildingmaps.txt", "buildingmaps", self.columns)
