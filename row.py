class Row:
	def __init__(self, table, id):
		self.table = table
		self.id = id

	def __setitem__(self, key, value):
		with self.table.database.get_connection() as connection:
			# Check if the column exists in the table
			if key in self.table.columns:
				# Execute the update statement
				connection.execute("UPDATE {} SET {}=? WHERE rowid = ?;".format(self.table.name, key), [value, self.id])
			else:
				# Raise a KeyError
				raise KeyError("There is no column in table:'{}' with the name:'{}'!".format(self.table.name, key))

	def __getitem__(self, key):
		with self.table.database.get_connection() as connection:
			# Check if the column exists in the table
			if key in self.table.columns:
				# Select the value from the database
				cursor = connection.execute("SELECT {} FROM {} WHERE rowid=?;".format(key, self.table.name), [self.id])
				# Return the value
				return cursor.fetchone()[0]
			else:
				# Raise a KeyError
				raise KeyError("There is no column in table:'{}' with the name:'{}'!".format(self.table.name, key))

	def __iter__(self):
		# Create a list containing each value, then return the iterator for that list
		return iter([self[column] for column in self.table.columns])

	def __eq__(self, other):
		if isinstance(self, other.__class__):
			return self.id == other.id and self.table == other.table
		else:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)

	def delete(self):
		with self.table.database.get_connection() as connection:
			connection.execute('DELETE FROM {} WHERE rowid=?;'.format(self.table.name), [self.id])