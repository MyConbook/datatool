import icalendar
import urllib2
import hashlib
import string
import re
import datetime
from database import Database, TableHandler

class Schedule(TableHandler):
	columns = [("Title", Database.C_TCN), "Description", ("Category", Database.C_TCN), ("Location", Database.C_TCN), ("StartDate", Database.C_D), ("EndDate", Database.C_D)]

	def __init__(self, options):
		TableHandler.__init__(self, "schedule", self.columns)
		self.options = options

	def download(self):
		# Download schedule
		mysock = urllib2.urlopen(self.options.calendar_url);
		self.file_content = mysock.read();
		mysock.close();

	def calculate_hash(self, version):
		# Calculate MD5 sum
		m = hashlib.md5();
		hash_text = re.sub("DTSTAMP:.+\\r\\n", "", self.file_content)
		m.update(hash_text);
		md5 = m.hexdigest();
		return version.set_calendar_checksum(md5)

	def parse(self, db, output_json):
		if not self.file_content:
			raise ValueError("file_content is empty")

		self.create_table(db)
		real_tz = self.options.timezone
		json_out = []

		# Parse calendar
		cal = icalendar.Calendar.from_ical(self.file_content)
		for component in cal.walk("VEVENT"):
			title = component["summary"]
			try:
				desc = component["description"]
			except KeyError:
				desc = None
			category = component.decoded("categories", None)
			loc = component.decoded("location", "(None)")
			origstart = component["dtstart"].dt
			startdate = origstart
			if not isinstance(startdate, datetime.datetime):
				# Item is all-day
				continue
			if not startdate.tzinfo:
				startdate = real_tz.localize(startdate)
			startdate = real_tz.normalize(startdate.astimezone(real_tz)).isoformat()
			if not "dtend" in component:
				# Item has start time but not end time
				enddate = origstart
			else:
				enddate = component["dtend"].dt
			if not enddate.tzinfo:
				enddate = real_tz.localize(enddate)
			enddate = real_tz.normalize(enddate.astimezone(real_tz)).isoformat()
			values = [title, desc, category, loc, startdate, enddate]
			
			args = self.insert_row(db, values)
			json_out.append(args)
		
		output_json.update({self.table_name: json_out})
