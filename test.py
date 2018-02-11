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
            row['age'] = 14

if __name__ == '__main__':
    unittest.main()
