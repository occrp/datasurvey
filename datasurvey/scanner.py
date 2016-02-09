import os
import logging
import mimetypes

from datasurvey.auction import scan_path
from datasurvey.util import checksum, sizeof_fmt

log = logging.getLogger(__name__)


class Scanner(object):

    def __init__(self, store, parent, name):
        self.store = store
        self.parent = parent
        self.name = name

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
        return os.path.join(self.parent.path_name, self.name)

    @property
    def real_path(self):
        if not self.root:
            return os.path.join(self.parent.real_path, self.name)
        return self.name


class FileScanner(Scanner):

    SYSTEM_FILES = ['.DS_Store', '.gitignore', '.hgignore', 'Thumbs.db']

    def bid(self):
        if os.path.isfile(self.real_path):
            return 1

    def scan(self):
        size = os.path.getsize(self.real_path)
        _, ext = os.path.splitext(self.real_path)
        mime, enc = mimetypes.guess_type(self.real_path, strict=False)
        mime = mime or enc
        self.store.emit({
            'path_name': self.path_name,
            'name': self.name,
            'type': 'file',
            'size': size,
            'system': self.name in self.SYSTEM_FILES,
            'extension': ext.strip('.').lower(),
            'mime_type': mime,
            'size_human': sizeof_fmt(size),
            'sha1': checksum(self.real_path)
        })


class DirectoryScanner(Scanner):

    def bid(self):
        if os.path.isdir(self.real_path):
            return 2

    def scan(self):
        log.info("Reading directory: %s", self.path_name)
        for name in os.listdir(self.real_path):
            scan_path(self.store, self, name)
