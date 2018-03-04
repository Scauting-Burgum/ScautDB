class Query:
    def __init__(self, table, columns = list(), filters = list()):
        self.table = table
        self.columns = columns
        self.filters = filters

    @property
    def column_string(self):
        column_string = 'rowid'
        
        for column in self.columns:
            column_string += ','
            column_string += column
        
        return column_string

    @property
    def filter_string(self):
        def process(filters):
            filter_string = ''

            previous_segment = None

            for f in filters:
                if filter_string != '':
                    filter_string += ' '
                if f in COMBINATORS:
                    if f == AND:
                        filter_string += 'AND'
                    elif f == OR:
                        filter_string += 'OR'
                    elif f == NOT:
                        filter_string += 'NOT'
                    previous_segment = f
                else:
                    if previous_segment in OPERATORS:
                        filter_string += 'AND '

                    if not isinstance(f[0], str):
                        filter_string += '('
                        filter_string += process(f)
                        filter_string += ')'
                    else:
                        if f[0] not in self.table.columns and f[0] != 'rowid':
                            from exceptions import MissingColumnError
                            raise MissingColumnError('No such column: {} in table: {}'.format(f[0], self.table.name))

                        filter_string += '{}'.format(f[0])

                        if f[1] == EQUAL:
                            filter_string += ' ='
                        elif f[1] == IN:
                            filter_string += ' IN'
                        elif f[1] == LIKE:
                            filter_string += ' LIKE'
                        elif f[1] == GREATER_THAN:
                            filter_string += ' >'
                        elif f[1] == LESSER_THAN:
                            filter_string += ' <'
                        elif f[1] == GREATER_THAN_OR_EQUAL_TO:
                            filter_string += ' >='
                        elif f[1] == LESSER_THAN_OR_EQUAL_TO:
                            filter_string += ' <='

                        if f[1] == IN:
                            if isinstance(f[2], Query):
                                subquery_string = str(f[2])[:-1]
                                if not 'rowid' in f[2].columns:
                                    subquery_string = subquery_string.replace('rowid,', '', 1)
                                filter_string += ' ({})'.format(subquery_string)
                            else:
                                array_substring = ''
                                for e in f[2]:
                                    if array_substring != '':
                                        array_substring += ','
                                    array_substring += '?'
                                filter_string += ' ({})'.format(array_substring)
                        else:
                            filter_string += ' ?'

                        previous_segment = f[1]

            return filter_string
        return process(self.filters)

    @property
    def parameters(self):
        def process(filters):
            parameters = list()
            
            for f in filters:
                if hasattr(f, '__getitem__'):
                    if not isinstance(f[0], str):
                        parameters += process(f)
                    elif isinstance(f[2], Query):
                        parameters += f[2].parameters
                    elif not isinstance(f[2], str) and hasattr(f[2], '__iter__'):
                        parameters += f[2]
                    else:
                        parameters.append(f[2])
            return parameters

        return process(self.filters)

    def __str__(self):
        sql = 'SELECT {} FROM {}'.format(self.column_string, self.table.name)
        if len(self.filters) > 0:
            sql += ' WHERE {}'.format(self.filter_string)
        sql += ';'
        return sql

    def execute(self):
        with self.table.database.get_connection() as connection:
            query_string = str(self)
            for column in self.columns:
        	    if column != 'rowid':
        	        query_string = query_string.replace(',{}'.format(column), '', 1)
            cursor = connection.execute(query_string, self.parameters)
            from resultset import ResultSet
            return ResultSet(self.table, cursor)

class EQUAL:
    pass

class IN:
    pass

class LIKE:
    pass

class GREATER_THAN:
    pass

class LESSER_THAN:
    pass

class GREATER_THAN_OR_EQUAL_TO:
    pass

class LESSER_THAN_OR_EQUAL_TO:
    pass

OPERATORS = [EQUAL, IN, LIKE, GREATER_THAN, LESSER_THAN, GREATER_THAN_OR_EQUAL_TO, LESSER_THAN_OR_EQUAL_TO]

class AND:
    pass

class OR:
    pass

class NOT:
    pass

COMBINATORS = [AND, OR, NOT]
