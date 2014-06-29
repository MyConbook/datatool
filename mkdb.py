#!/usr/bin/python

# mkdb.py
# Consolidate convention data into a database
# 2014 MyConbook

import sys
import builder
from builder import helper

# Read command line
options = builder.Options({"test": "../test2", "prod": "../data2"})
options.read_from_command_line()
options.parse_con_info()

def pce(msg, error=False):
	if error or not options.is_cron:
		print msg

if not options.ensure_path():
	pce("Convention data directory does not exist.", True)
	sys.exit(-1)

# Parse con version file
con_version = builder.Version(options)
con_version.read()

# Pack maps
if options.new_maps or con_version.is_new:
	map_packer = builder.Maps(options, con_version)
	map_packer.pack()
	con_version.increment_map()

	if options.new_maps and not con_version.is_new:
		con_version.write()
		pce("Maps updated. Map version %d." % (con_version.map_ver))
		sys.exit(0)

con_version.increment_db()

# Check schedule for duplicate data
schedule = builder.Schedule(options)
schedule.download()
if not options.can_overwrite and not schedule.calculate_hash(con_version):
	pce("Calendar files matched, not updating database.")
	sys.exit(0)

# Open outputs
database = builder.Database(options)
database.create()
output = {}

# Parse schedule
schedule.parse(database, output)

# Parse regular TSVs
parse_list = [
	builder.Dealers,
	builder.Restaurants,
	builder.Bars,
	builder.Stores,
	builder.Atms,
	builder.ConInfo,
	builder.Hotels,
	builder.BuildingMaps
]

for item in parse_list:
	inited = item(options)
	inited.parse(database, output)

# Write con info
con_info = builder.Info(options, con_version)
con_info.parse(database, output)

# Save
database.close()
helper.write_output(options, output)
con_version.write()

# Finish
pce("Completed %s. Database version %d." % (options.convention, con_version.database_ver))
