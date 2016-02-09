import dataset


class Store(object):

    def __init__(self, db_path):
        if db_path is None:
            self.engine = dataset.connect('sqlite:///:memory:')
        else:
            self.engine = dataset.connect('sqlite:///%s' % db_path)
        self.table = self.engine['files']
        self.table.delete()

    def emit(self, data):
        self.table.insert(data)

    def save(self, fh):
        dataset.freeze(self.table, fileobj=fh)
