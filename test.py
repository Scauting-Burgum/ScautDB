import unittest

class TestRow(unittest.TestCase):
    def test___init__(self):
        from row import Row
        from database import Database

        try:
            import os
            os.remove('test_Row.__init__.db')
        except OSError:
            pass

        db = Database('test_Row.__init__.db')

        with self.assertRaises(TypeError):
            Row(None, 1)

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])

        from exceptions import MissingRowError

        with self.assertRaises(MissingRowError):
            Row(table, 1)

        expectedRow = table.insert({'name':'Albert', 'age':13})

        self.assertEqual(Row(table, 1), expectedRow)

    def test___setitem__(self):
        from row import Row
        from database import Database

        try:
            import os
            os.remove('test_Row.__setitem__.db')
        except OSError:
            pass

        db = Database('test_Row.__setitem__.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])

        row = table.insert({'name':'Albert', 'age':13})

        row['name'] = 'Joran'
        self.assertEqual(row['name'], 'Joran')

        row['age'] = 14
        self.assertEqual(row['age'], 14)

        from exceptions import MissingColumnError

        with self.assertRaises(MissingColumnError):
            row['nonexistentcolumn'] = 'A very boring value...'

        row.delete()

        from exceptions import MissingRowError

        with self.assertRaises(MissingRowError):
            row['age'] = 14

    def test___getitem__(self):
        from row import Row
        from database import Database

        try:
            import os
            os.remove('test_Row.__getitem__.db')
        except OSError:
            pass

        db = Database('test_Row.__getitem__.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])

        row = table.insert({'name':'Albert', 'age':13})

        self.assertEqual(row['name'], 'Albert')

        self.assertEqual(row['age'], 13)

        from exceptions import MissingColumnError

        with self.assertRaises(MissingColumnError):
            row['nonexistentcolumn']

        row.delete()

        from exceptions import MissingRowError

        with self.assertRaises(MissingRowError):
            row['age']

    def test___iter__(self):
        from row import Row
        from database import Database

        try:
            import os
            os.remove('test_Row.__iter__.db')
        except OSError:
            pass

        db = Database('test_Row.__iter__.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])

        row = table.insert({'name':'Albert', 'age':13})

        expected_list = ['Albert', 13]

        actual_list = [field for field in row]

        self.assertEqual(expected_list, actual_list)

        row.delete()

        from exceptions import MissingRowError

        with self.assertRaises(MissingRowError):
            for field in row:
                pass

    def test_delete(self):
        from row import Row
        from database import Database

        try:
            import os
            os.remove('test_Row.delete.db')
        except OSError:
            pass

        db = Database('test_Row.delete.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])

        row = table.insert({'name':'Albert', 'age':13})

        row.delete()

        from exceptions import MissingRowError

        with self.assertRaises(MissingRowError):
            Row(table, 1)

    def test___ne__(self):
        from row import Row
        from database import Database

        try:
            import os
            os.remove('test_Row.__ne__.db')
        except OSError:
            pass

        db = Database('test_Row.__ne__.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])

        row = table.insert({'name':'Albert', 'age':13})
        row2 = table.insert({'name':'Joran', 'age':13})

        self.assertTrue(row != row2)
        self.assertFalse(row != row)

    def test___eq__(self):
        from row import Row
        from database import Database

        try:
            import os
            os.remove('test_Row.__eq__.db')
        except OSError:
            pass

        db = Database('test_Row.__eq__.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])

        row = table.insert({'name':'Albert', 'age':13})
        row2 = table.insert({'name':'Joran', 'age':13})

        self.assertFalse(row == row2)
        self.assertTrue(row == row)

class TestTable(unittest.TestCase):
    def test___init__(self):
        from table import Table
        from database import Database

        try:
            import os
            os.remove('test_Table.__init__.db')
        except OSError:
            pass

        db = Database('test_Table.__init__.db')

        from exceptions import MissingTableError

        with self.assertRaises(MissingTableError):
            Table(db, 'people')

        actual_table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])
        expected_table = Table(db, 'people')

        self.assertEqual(expected_table, actual_table)

    def test_columns(self):
        from table import Table
        from database import Database

        try:
            import os
            os.remove('test_Table.columns.db')
        except OSError:
            pass

        db = Database('test_Table.columns.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])

        self.assertEqual(table.columns, ['name', 'age'])

        try:
            import os
            os.remove('test_Table.columns.db')
        except OSError:
            pass

        db = Database('test_Table.columns.db')

        from exceptions import MissingTableError

        with self.assertRaises(MissingTableError):
            table.columns

    def test_rows(self):
        from table import Table
        from database import Database

        try:
            import os
            os.remove('test_Table.rows.db')
        except OSError:
            pass

        db = Database('test_Table.rows.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])

        table.insert({'name':'Albert', 'age':13})
        table.insert({'name':'Joran', 'age':13})

        self.assertEqual(table.rows, [table[1], table[2]])

        try:
            import os
            os.remove('test_Table.rows.db')
        except OSError:
            pass

        db = Database('test_Table.rows.db')

        from exceptions import MissingTableError

        with self.assertRaises(MissingTableError):
            table.rows

    def test___contains__(self):
        from table import Table
        from database import Database

        try:
            import os
            os.remove('test_Table.__contains__.db')
        except OSError:
            pass

        db = Database('test_Table.__contains__.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])

        row = table.insert({'name':'Albert', 'age':13})

        self.assertIn(row, table)

        row2 = table.insert({'name':'Joran', 'age':13})

        row2.delete()

        self.assertNotIn(row2, table)

        try:
            import os
            os.remove('test_Table.__contains__.db')
        except OSError:
            pass

        db = Database('test_Table.__contains__.db')

        from exceptions import MissingTableError

        with self.assertRaises(MissingTableError):
            row in table

    def test___iter__(self):
        from table import Table
        from database import Database

        try:
            import os
            os.remove('test_Table.__iter__.db')
        except OSError:
            pass

        db = Database('test_Table.__iter__.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])

        row = table.insert({'name':'Albert', 'age':13})
        row2 = table.insert({'name':'Joran', 'age':13})

        actual_list = [row for row in table]
        expected_list = [row, row2]

        self.assertEqual(actual_list, expected_list)

        try:
            import os
            os.remove('test_Table.__iter__.db')
        except OSError:
            pass

        db = Database('test_Table.__iter__.db')

        from exceptions import MissingTableError

        with self.assertRaises(MissingTableError):
            for row in table:
                pass

    def test___getitem__(self):
        from table import Table
        from database import Database

        try:
            import os
            os.remove('test_Table.__getitem__.db')
        except OSError:
            pass

        db = Database('test_Table.__getitem__.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])

        row = table.insert({'name':'Albert', 'age':13})

        self.assertEqual(table[1], row)

        row.delete()

        from exceptions import MissingRowError

        with self.assertRaises(MissingRowError):
            table[1]

        try:
            import os
            os.remove('test_Table.__getitem__.db')
        except OSError:
            pass

        from exceptions import MissingTableError

        with self.assertRaises(MissingTableError):
            table[1]

    def test___eq__(self):
        from table import Table
        from database import Database

        try:
            import os
            os.remove('test_Table.__eq__.db')
        except OSError:
            pass

        db = Database('test_Table.__eq__.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])
        table2 = db.create_table('companies', [('name', 'TEXT'), ('address', 'TEXT')])

        self.assertTrue(table == table)
        self.assertFalse(table == table2)

    def test___ne__(self):
        from table import Table
        from database import Database

        try:
            import os
            os.remove('test_Table.__ne__.db')
        except OSError:
            pass

        db = Database('test_Table.__ne__.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])
        table2 = db.create_table('companies', [('name', 'TEXT'), ('address', 'TEXT')])

        self.assertFalse(table != table)
        self.assertTrue(table != table2)

    def test_insert(self):
        from table import Table
        from database import Database

        try:
            import os
            os.remove('test_Table.insert.db')
        except OSError:
            pass

        db = Database('test_Table.insert.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])

        row = table.insert({'name':'Albert', 'age':13})

        self.assertEqual(row, table[1])

        row2 = table.insert({'name':'Joran'})

        self.assertEqual(row2, table[2])
        self.assertEqual(row2['age'], 0)

        from exceptions import MissingColumnError

        with self.assertRaises(MissingColumnError):
            table.insert({'name':'Albert', 'address':'Somewhere'})

class TestDatabase(unittest.TestCase):
    def test___init__(self):
        from database import Database

        try:
            import os
            os.remove('test_Database.__init__.db')
        except OSError:
            pass

        db = Database('test_Database.__init__.db')

        self.assertIsInstance(db, Database)

        with self.assertRaises(TypeError):
            Database(None)

    def test_get_connection(self):
        from database import Database

        try:
            import os
            os.remove('test_Database.get_connection.db')
        except OSError:
            pass

        db = Database('test_Database.get_connection.db')

        from sqlite3 import Connection

        self.assertIsInstance(db.get_connection(), Connection)

    def test_tables(self):
        from database import Database

        try:
            import os
            os.remove('test_Database.tables.db')
        except OSError:
            pass

        db = Database('test_Database.tables.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])
        table2 = db.create_table('companies', [('name', 'TEXT'), ('address', 'TEXT')])

        self.assertEqual(db.tables, [table, table2])

    def test_create_table(self):
        from database import Database

        try:
            import os
            os.remove('test_Database.create_table.db')
        except OSError:
            pass

        db = Database('test_Database.create_table.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])

        self.assertEqual(table, db['people'])

        self.assertEqual(table.database, db)
        self.assertEqual(table.name, 'people')

        with db.get_connection() as connection:
            cursor = connection.execute('PRAGMA table_info(\'people\');')
            actual_data = [(row[1], row[2], row[4]) for row in cursor]
            self.assertEqual([('name', 'TEXT', None), ('age', 'INTEGER', '0')], actual_data)

        from exceptions import DuplicateTableError

        with self.assertRaises(DuplicateTableError):
            db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])

    def test___contains__(self):
        from database import Database

        try:
            import os
            os.remove('test_Database.__contains__.db')
        except OSError:
            pass

        db = Database('test_Database.__contains__.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])

        self.assertIn(table, db)

        try:
            import os
            os.remove('test_Database.__contains__.db')
        except OSError:
            pass

        self.assertNotIn(table, db)

    def test___getitem__(self):
        from database import Database

        try:
            import os
            os.remove('test_Database.__getitem__.db')
        except OSError:
            pass

        db = Database('test_Database.__getitem__.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])

        self.assertEqual(table, db['people'])

        from exceptions import MissingTableError

        with self.assertRaises(MissingTableError):
            db['companies']

    def test___iter__(self):
        from database import Database

        try:
            import os
            os.remove('test_Database.__iter__.db')
        except OSError:
            pass

        db = Database('test_Database.__iter__.db')

        table1 = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])
        table2 = db.create_table('companies', [('name', 'TEXT'), ('address', 'TEXT')])

        self.assertEqual([table for table in db], [table1, table2])

    def test___eq__(self):
        from database import Database

        try:
            import os
            os.remove('test_Database.__eq__1.db')
            os.remove('test_Database.__eq__2.db')
        except OSError:
            pass

        db1 = Database('test_Database.__eq__1.db')
        db2 = Database('test_Database.__eq__2.db')

        self.assertTrue(db1 == db1)
        self.assertFalse(db1 == db2)

    def test___ne__(self):
        from database import Database

        try:
            import os
            os.remove('test_Database.__ne__1.db')
            os.remove('test_Database.__ne__2.db')
        except OSError:
            pass

        db1 = Database('test_Database.__ne__1.db')
        db2 = Database('test_Database.__ne__2.db')

        self.assertFalse(db1 != db1)
        self.assertTrue(db1 != db2)

class TestQuery(unittest.TestCase):
    def test___init__(self):
        from database import Database

        try:
            import os
            os.remove('test_Query.__init__.db')
        except OSError:
            pass

        db = Database('test_Query.__init__.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER')])
        
        from query import Query
        query = Query(table)

        self.assertIsInstance(query, Query)

    def test_column_string(self):
        from database import Database

        try:
            import os
            os.remove('test_Query.column_string.db')
        except OSError:
            pass

        db = Database('test_Query.column_string.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER')])
        
        from query import Query
        query = Query(table)

        self.assertEqual(query.column_string, 'rowid')

        query = Query(table, ['rowid'])

        self.assertEqual(query.column_string, 'rowid')

        query = Query(table, ['name','age'])

        self.assertEqual(query.column_string, 'rowid,name,age')

    def test_filter_string(self):
        from database import Database

        try:
            import os
            os.remove('test_Query.filter_string.db')
        except OSError:
            pass

        db = Database('test_Query.filter_string.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER')])

        from query import Query
        query = Query(table)

        self.assertEqual(query.filter_string, '')

        from query import EQUAL

        query = Query(table, filters=[('name', EQUAL, 'A nonexistent name!')])

        self.assertEqual(query.filter_string, 'name = ?')

        from query import GREATER_THAN

        query = Query(table, filters=[(('name', EQUAL, 'A nonexistent name!'), ('age', GREATER_THAN, 18))])

        self.assertEqual(query.filter_string, '(name = ? AND age > ?)')

        from query import NOT, AND, OR

        query = Query(table, filters=[(NOT, (('name', EQUAL, 'Albert'), AND, ('age', EQUAL, 13))), OR, ('name', EQUAL, 'Joran')])

        self.assertEqual(query.filter_string, '(NOT (name = ? AND age = ?)) OR name = ?')

        query1 = Query(table, columns=['name'] ,filters=[('age', GREATER_THAN, 13)])

        from query import IN

        query2 = Query(table, filters=[(NOT, (('name', EQUAL, 'Albert'), AND, ('age', EQUAL, 13))), OR, ('name', IN, query1)])

        self.assertEqual(query2.filter_string, '(NOT (name = ? AND age = ?)) OR name IN (SELECT name FROM people WHERE age > ?)')
    def test_parameters(self):
        from database import Database

        try:
            import os
            os.remove('test_Query.parameters.db')
        except OSError:
            pass

        db = Database('test_Query.parameters.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER')])

        from query import Query
        query = Query(table)

        self.assertEqual(query.parameters, [])

        from query import EQUAL, GREATER_THAN

        query1 = Query(table, filters=[(('name', EQUAL, 'A nonexistent name!'), ('age', GREATER_THAN, 18))])

        self.assertEqual(query1.parameters, ['A nonexistent name!', 18])

        from query import IN

        query2 = Query(table, filters=[(('name', EQUAL, 'A nonexistent name!'), ('age', GREATER_THAN, 18)), ('name', IN, query1)])

        self.assertEqual(query2.parameters, ['A nonexistent name!', 18, 'A nonexistent name!', 18])

        query = Query(table, filters=[('name', IN, ['Albert', 'Joran'])])

        self.assertEqual(query.parameters, ['Albert', 'Joran'])

    def test___str__(self):
        from database import Database

        try:
            import os
            os.remove('test_Query.__str__.db')
        except OSError:
            pass

        db = Database('test_Query.__str__.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER')])

        from query import Query

        query = Query(table)

        self.assertEqual(str(query), 'SELECT rowid FROM people;')

        query = Query(table, ['name'])

        self.assertEqual(str(query), 'SELECT rowid,name FROM people;')

        from query import GREATER_THAN

        query = Query(table, ['name'], [('age', GREATER_THAN, 18)])

        self.assertEqual(str(query), 'SELECT rowid,name FROM people WHERE age > ?;')

    def test_execute(self):
        from database import Database

        try:
            import os
            os.remove('test_Query.__str__.db')
        except OSError:
            pass

        db = Database('test_Query.__str__.db')

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER')])

        from query import Query

        query = Query(table)

        rs = query.execute()

        from resultset import ResultSet

        self.assertIsInstance(rs, ResultSet)
        
        self.assertEqual([r for r in rs], [])

if __name__ == '__main__':
    unittest.main()
