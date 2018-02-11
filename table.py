class Table:
	def __init__(self, database, name):
		from database import Database

		if not isinstance(database, Database):
			raise TypeError('the \"database\" argument is not an instance of ScautDB.Database')
		elif not isinstance(name, str):
			raise TypeError('the \"name\" argument is not a string')

		self.database = database
		self.name = name

		if not self in self.database:
			from exceptions import MissingTableError
			raise MissingTableError('no such table: {}'.format(self.name))

	@property
	def columns(self):
		with self.database.get_connection() as connection:
			cursor = connection.execute('PRAGMA table_info({});'.format(self.name))
			columns = [row[1] for row in cursor]
			if columns == []:
				from exceptions import MissingTableError
				raise MissingTableError('table {} does not exist'.format(self.name))
		return columns

	@property
	def rows(self):
		with self.database.get_connection() as connection:
			from sqlite3 import OperationalError
			try:
				cursor = connection.execute('select rowid from ' + self.name + ';')
				from row import Row
				rows = [Row(self, row[0]) for row in cursor]
			except OperationalError as exception:
				if exception.args[0] == 'no such table: {}'.format(self.name):
					from exceptions import MissingTableError
					raise MissingTableError(exception.args[0]) from exception
		return rows

	def __contains__(self, row):
		from row import Row
		if row == None or row.__class__ != Row or row.table != self:
			return False
		else:
			with self.database.get_connection() as connection:
				from sqlite3 import OperationalError
				try:
					cursor = connection.execute('select EXISTS(select rowid from {} where rowid = ?);'.format(self.name), [row.id])
					return cursor.fetchone()[0]
				except OperationalError as error:
					if error.args[0] == 'no such table: {}'.format(self.name):
						from exceptions import MissingTableError
						raise MissingTableError(error.args[0])

	def __iter__(self):
		# Return an iterator on the list of tables
		return iter(self.rows)

	def __getitem__(self, id):
		from row import Row
		row = Row(self, id)
		if row in self:
			return row
		else:
			from exceptions import MissingRowError
			raise MissingRowError('no row with rowid: {} in table: {}'.format(id, self.name))

	def __eq__(self, other):
		if isinstance(self, other.__class__):
			return self.name == other.name and self.database == other.database
		else:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)

	def insert(self, dictionary):
		column_string = str()
		parameter_string = str()
		parameters = list()

		for key in dictionary:
			if not key in self.columns:
				from exceptions import MissingColumnError
				raise MissingColumnError('no column: {} in table: {}'.format(key, self.name))

			if len(column_string) > 0:
				column_string += ','
				parameter_string += ','

			column_string += key
			parameter_string += '?'

			parameters.append(dictionary[key])

		with self.database.get_connection() as connection:
			from sqlite3 import OperationalError
			try:
				cursor = connection.execute('INSERT INTO {} ({}) VALUES ({});'.format(self.name, column_string, parameter_string), parameters)
				from row import Row
				return Row(self, cursor.lastrowid)
			except OperationalError as error:
				if error.args[0] == 'no such table: {}'.format(self.name):
					from exceptions import MissingTableError
					raise MissingTableError(error.args[0]) from errror
