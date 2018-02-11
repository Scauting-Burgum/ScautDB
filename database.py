import sqlite3
from table import Table

class Database:
	def __init__(self, filename):
		if isinstance(filename, str):
			self.filename = filename
		else:
			raise TypeError('Filename should be a string!')

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

	def create_table(self, name, columns):
		column_string = str()

		for column in columns:
			if len(column_string) > 0:
				column_string += ','

			column_name = column[0]
			column_data_type = column[1]

			column_string += '{} {}'.format(column_name, column_data_type)

			if len(column) > 2:
				if column[2].__class__ == str:
					default_value = '"{}"'.format(column[2])
				else:
					default_value = column[2]
				column_string += ' DEFAULT {}'.format(default_value)

		query_string = 'CREATE TABLE {} ({});'.format(name, column_string)

		with self.get_connection() as connection:
			try:
				connection.execute(query_string)
			except sqlite3.OperationalError as exception:
				duplicate_table_message = 'table {} already exists'.format(name)
				if exception.args[0] == duplicate_table_message:
					from exceptions import DuplicateTableError
					raise DuplicateTableError(duplicate_table_message) from exception

		return self[name]

	def __contains__(self, table):
		if table == None or table.__class__ != Table or table.database != self:
			return False
		else:
			with self.get_connection() as connection:
				cursor = connection.execute("SELECT EXISTS(SELECT name FROM sqlite_master WHERE type='table' AND name=?);", [table.name])
				return cursor.fetchone()[0]

	def __getitem__(self, key):
		return Table(self, key)

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
