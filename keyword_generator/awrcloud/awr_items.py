__author__ = 'fabrice'

class AwrKeyword:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def __repr__(self):
        return "%s (id=%s)" % (self.name, self.id)

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name


class AwrGroup:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def __repr__(self):
        return "%s (id=%s)" % (self.name, self.id)

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name
