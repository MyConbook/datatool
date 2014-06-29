import os
import json

class Version(object):
	def __init__(self, options):
		self.options = options
		self.file_path = options.get_output_path("version.json")

	def read(self):
		self.is_new = not os.path.exists(self.file_path)
		if not self.is_new:
			# Read version file
			ver_file = open(self.file_path, "r")
			ver_str = ver_file.read()
			ver_file.close()

			ver_json = json.loads(ver_str)
			self.map_ver = int(ver_json["mapver"])
			self.database_ver = int(ver_json["dbver"])
			self.calendar_checksum = ver_json["calhash"]
		else:
			self.map_ver = 0
			self.database_ver = 0
			self.calendar_checksum = None

	def write(self):
		new_json = json.dumps({"dbver": self.database_ver, "calhash": self.calendar_checksum, "mapver": self.map_ver})

		if self.options.is_preview:
			print new_json
			return

		json_file = open(self.file_path, "w")
		json_file.write(new_json)
		json_file.close()

	def increment_db(self):
		self.database_ver = self.database_ver + 1

	def increment_map(self):
		self.map_ver = self.map_ver + 1

	def set_calendar_checksum(self, checksum):
		if self.calendar_checksum == checksum:
			return False

		self.calendar_checksum = checksum
		return True
