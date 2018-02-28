class Query:
    def __init__(self, table, columns, filters):
        self.table = table
        self.columns = columns
        self.filters = filters

    @property
    def column_string(self):
        return 'rowid'
        # column_string = ''
        #
        # for column in self.columns:
        #     if column_string != '':
        #         column_string += ','
        #
        #     column_string += column
        #
        # return column_string

    @property
    def filter_string(self):
        filter_string = ''

        previous_segment = None

        for f in self.filters:
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

                if f[0] not in self.table.columns:
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
                        filter_string += ' ({})'.format(str(f[2])[:-1])
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

    @property
    def parameters(self):
        parameters = list()

        for f in self.filters:
            if hasattr(f, '__getitem__'):
                if isinstance(f[2], Query):
                    parameters += f[2].parameters
                else:
                    parameters.append(f[2])

        return parameters

    def __str__(self):
        return 'SELECT {} FROM {} WHERE {};'.format(self.column_string, self.table.name, self.filter_string)

    def execute(self):
        with self.table.database.get_connection() as connection:
            cursor = connection.execute(str(self), self.parameters)
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
