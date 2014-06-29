import os
import sqlite3
import string

class Database(object):
	"""Database"""

	C_T = "text"
	C_TCN = "text COLLATE NOCASE"
	C_I = "int"
	C_D = "date"

	def __init__(self, options):
		self.options = options
		self.file_path = options.get_output_path("conbook.sqlite")
		self.tmp_path = self.file_path + ".tmp"

	def create(self):
		if self.options.is_preview:
			self.conn = sqlite3.connect(":memory:")
		else:
			if os.path.exists(self.tmp_path):
				os.remove(self.tmp_path)
			self.conn = sqlite3.connect(self.tmp_path)

		self.cursor = self.conn.cursor()

	def close(self):
		"""Close database"""
		if self.cursor is not None:
			self.cursor.close()
			self.cursor = None

		if self.conn is not None:
			self.conn.close()
			self.conn = None

		# Move temp file to real path
		if not self.options.is_preview:
			if os.path.exists(self.file_path):
				os.remove(self.file_path)

			os.rename(self.tmp_path, self.file_path)

	def execute(self, *args, **kwargs):
		self.cursor.execute(*args, **kwargs)

	def commit(self):
		self.conn.commit()

	def get_last_row_id(self):
		return self.cursor.lastrowid

class TableHandler(object):
	def __init__(self, table_name, columns):
		self.table_name = table_name
		self.columns = map(self.format_columns, columns)
		self.column_names = map(lambda c: c[0], self.columns)

	def format_columns(self, column_obj):
		if isinstance(column_obj, str):
			return (column_obj, Database.C_T)
		else:
			return column_obj

	def create_table_typing(self, column_obj):
		return "%s %s" % column_obj

	def create_table(self, db):
		"""Create table"""
		insert_sql = string.join(map(self.create_table_typing, self.columns), ", ")
		db.execute("CREATE TABLE %s (_id integer PRIMARY KEY, %s)" % (self.table_name, insert_sql))

	def insert_row(self, db, values):
		args = dict(zip(self.column_names, values))
		self.cleanup_args(args)
		params = string.join(map(lambda c: ":" + c, self.column_names), ", ")
		db.execute("INSERT INTO %s VALUES (NULL, %s)" % (self.table_name, params), args)
		args.update({"ID": db.get_last_row_id()})

		return args

	def cleanup_args(self, args):
		pass
