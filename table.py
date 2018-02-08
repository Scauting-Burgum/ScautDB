from row import Row

class Table:
	def __init__(self, database, name):
		self.database = database
		self.name = name

	@property
	def columns(self):
		with self.database.get_connection() as connection:
			cursor = connection.execute('select * from {} LIMIT 1;'.format(self.name))
			columns = [row[0] for row in cursor.description]
		return columns

	@property
	def rows(self):
		with self.database.get_connection() as connection:
			cursor = connection.execute('select rowid from ' + self.name + ';')
			rows = [Row(self, row[0]) for row in cursor]
		return rows

	def __contains__(self, row):
		if row == None or row.__class__ != Row or row.table != self:
			return False
		else:
			with self.database.get_connection() as connection:
				cursor = connection.execute('select EXISTS(select rowid from {} where rowid = ?);'.format(self.name), [row.id])
				return cursor.fetchone()[0]

	def __iter__(self):
		# Return an iterator on the list of tables
		return iter(self.rows)

	def __getitem__(self, id):
		row = Row(self, id)
		if row in self:
			return row
		else:
			raise KeyError('There is no row in table:\'{}\' with the rowid:{}'.format(self.name, id))

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
			if len(column_string) > 0:
				column_string += ','
				parameter_string += ','

			column_string += key
			parameter_string += '?'

			parameters.append(dictionary[key])

		with self.database.get_connection() as connection:
			cursor = connection.execute('INSERT INTO {} ({}) VALUES ({});'.format(self.name, column_string, parameter_string), parameters)
			return Row(self, cursor.lastrowid)
