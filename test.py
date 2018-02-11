import unittest

class TestRow(unittest.TestCase):
    def test___init__(self):
        from row import Row
        from database import Database

        db = Database('test___init__.db')

        with self.assertRaises(TypeError):
            Row(None, 1)

        table = db.create_table('people', [('name', 'TEXT'), ('age', 'INTEGER', 0)])

        from exceptions import MissingRowError

        with self.assertRaises(MissingRowError):
            Row(table, 1)

        expectedRow = table.insert({'name':'Albert', 'age':13})

        self.assertEquals(Row(table, 1), expectedRow)

if __name__ == '__main__':
    unittest.main()
