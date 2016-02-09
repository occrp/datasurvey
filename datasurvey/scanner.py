import os

from datasurvey.auction import scan_path


class Scanner(object):

    def __init__(self, store, parent, path):
        self.store = store
        self.parent = parent
        self.path = path

    def scan(self):
        pass

    def bid(self):
        return 0

    @property
    def root(self):
        return self.parent is None

    @property
    def path_name(self):
        if self.root:
            return ''
        return os.path.join(self.parent.path_name, self.path)

    @property
    def real_path(self):
        if not self.root:
            return os.path.join(self.parent.real_path, self.path)
        return self.path


class FileScanner(Scanner):

    def bid(self):
        if os.path.isfile(self.real_path):
            return 1

    def scan(self):
        self.store.emit(name=self.path_name)


class DirectoryScanner(Scanner):

    def bid(self):
        if os.path.isdir(self.real_path):
            return 2

    def scan(self):
        for file_name in os.listdir(self.real_path):
            scan_path(self.store, self, file_name)
