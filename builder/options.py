import argparse
import json
import pytz
import os

class Options(object):
	def __init__(self, paths):
		self.test_path = paths["test"]
		self.prod_path = paths["prod"]

	# App variables
	encoding = "utf-8"

	def read_from_command_line(self):
		parser = argparse.ArgumentParser(description="Create a MyConbook database from convention data.")
		parser.add_argument("convention", metavar="convention", help="Convention name")
		parser.add_argument("--real", action="store_true", help="Update production instead of test")
		parser.add_argument("--overwrite", action="store_true", help="Overwrite existing data")
		parser.add_argument("--preview", action="store_true", help="Show preview only")
		parser.add_argument("--cron", action="store_true", help="Running inside scheduler")
		parser.add_argument("--new-maps", action="store_true", help="Update maps")

		args = parser.parse_args()
		self.convention = args.convention
		self.is_real = args.real
		self.can_overwrite = args.overwrite
		self.is_preview = args.preview
		self.is_cron = args.cron
		self.new_maps = args.new_maps

	def parse_con_info(self):
		# Read app info file
		info_file = open(self.get_data_path("info.json"), "r")
		info_str = info_file.read()
		info_file.close()

		self.info_json = json.loads(info_str)
		self.day_list = self.info_json["DayList"]
		self.calendar_url = self.info_json["CalendarURL"]
		self.thursday_offset = self.info_json["ThursdayOffset"]
		self.timezone = pytz.timezone(self.info_json["Timezone"])

	def get_data_path(self, filename):
		return "datafiles/%s/%s" % (self.convention, filename)

	def get_output_dir(self):
		if self.is_real:
			return self.prod_path
		else:
			return self.test_path

	def get_output_path(self, filename):
		return "%s/%s/%s" % (self.get_output_dir(), self.convention, filename)

	def ensure_path(self):
		data_path = self.get_data_path("")
		if not os.path.exists(data_path):
			return False

		output_path = self.get_output_path("")
		if not os.path.exists(output_path):
			os.makedirs(output_path)

		return True
