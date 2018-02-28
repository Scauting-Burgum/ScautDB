class ResultSet:
    def __init__(self, table, cursor):
        self._fetched_rows = list()
        self.table = table
        self._cursor = cursor

    def __iter__(self):
        return ResultSetIterator(self)

class ResultSetIterator:
    def __init__(self, resultSet):
        self._i = 0
        self.resultSet = resultSet

    def __next__(self):
        if len(self.resultSet._fetched_rows) > self._i:
            self._i += 1
            return self.resultSet[self._i]
        else:
            self._i += 1
            raw_row = self.resultSet._cursor.fetchone()
            if raw_row is None:
                raise StopIteration()
            from row import Row
            row = Row(self.resultSet.table, raw_row[0])
            self.resultSet._fetched_rows.append(row)
            return row
