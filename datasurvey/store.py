import dataset


class Store(object):

    def __init__(self):
        self.engine = dataset.connect('sqlite:///:memory:')
        self.table = self.engine['files']

    def emit(self, name):
        self.table.insert({
            'name': name
        })

    def save(self, fh):
        dataset.freeze(self.table, fileobj=fh)
