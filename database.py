import sqlite3
from table import Table

class Database:
	def __init__(self, filename):
		self.filename = filename

	def get_connection(self):
		# Return a connection to the database
		return sqlite3.connect(self.filename)

	@property
	def tables(self):
		# Get a connection to the database
		with self.get_connection() as connection:
			# Fetch the name of each table
			cursor = connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
			# Create a list of tables
			tables = [Table(self, row[0]) for row in cursor]
		# Return the list containing the tables
		return tables

	def __contains__(self, table):
		if table == None or table.__class__ != Table or table.database != self:
			return False
		else:
			with self.get_connection() as connection:
				cursor = connection.execute("SELECT EXISTS(SELECT name FROM sqlite_master WHERE type='table' AND name=?);", [table.name])
				return cursor.fetchone()[0]

	def __getitem__(self, key):
		# Create a table object with said name
		table = Table(self, key)
		# Check if table exists
		if table in self:
			# Return the table
			return table
		else:
			# Throw a KeyException
			raise KeyError('There is no table in the database with the name:\'{}\''.format(key))

	def __iter__(self):
		# Return an iterator on the list of tables
		return iter(self.tables)

	def __eq__(self, other):
		if isinstance(self, other.__class__):
			return self.filename == other.filename
		else:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)
