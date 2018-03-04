class Field(object):
    def __init__(self, table, name, rowid_attribute = 'id'):
        self.table = table
        self.name = name
        self.rowid_attribute = rowid_attribute

    def __get__(self, instance, owner):
        return self.table[instance.__getattribute__(self.rowid_attribute)][self.name]

    def __set__(self, instance, value):
        self.table[instance.__getattribute__(self.rowid_attribute)][self.name] = value
