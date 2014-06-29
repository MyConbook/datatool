import json
import datetime

class Info(object):
	def __init__(self, options, version):
		self.options = options
		self.version = version

	def parse(self, db, output_json):
		info_json = self.options.info_json

		# Add info
		info = {
			"BuildDate": datetime.datetime.now().isoformat(),
			"Version": self.version.database_ver,
			"Convention": info_json["Convention"],
			"ProviderDetails": info_json["ProviderDetails"],
			"AreaMapURL": info_json["AreaMapURL"],
			"HasGuide": info_json["HasGuide"],
			"GuideURL": info_json["GuideURL"]
		}

		db.execute("CREATE TABLE info (KeyName text PRIMARY KEY, KeyValue text)")

		for (k, v) in info.iteritems():
			db.execute("INSERT INTO info VALUES (?, ?)", (k, v))

		# Add daylist
		db.execute("CREATE TABLE daylist (_id integer PRIMARY KEY, Day text)")
		for day in self.options.day_list:
			db.execute("INSERT INTO daylist VALUES (NULL, ?)", (day, ))

		db.commit()

		output_json.update({"info": info, "daylist": self.options.day_list})
