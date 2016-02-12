import os
import logging
import mimetypes

from datasurvey.auction import scan_path
from datasurvey.util import checksum, sizeof_fmt, guess_encoding

log = logging.getLogger(__name__)


class Scanner(object):

    def __init__(self, store, parent, name):
        self.store = store
        self.parent = parent
        self.name = guess_encoding(name)

    def scan(self):
        pass

    def bid(self):
        return

    def descend(self, name):
        scan_path(self.store, self, name)

    def cleanup(self):
        pass

    def get_child_path_name(self, name):
        return os.path.join(self.path_name, name)

    def get_child_real_path(self, name):
        return os.path.join(self.real_path, name)

    @property
    def root(self):
        return self.parent is None

    @property
    def path_name(self):
        if self.root:
            return ''
        return self.parent.get_child_path_name(self.name)

    @property
    def real_path(self):
        if self.root:
            return self.name
        return self.parent.get_child_real_path(self.name)


class FileScanner(Scanner):

    SYSTEM_FILES = ['.DS_Store', '.gitignore', '.hgignore', 'Thumbs.db']

    def bid(self):
        if os.path.isfile(self.real_path):
            return 1

    def scan(self):
        self.emit_file(self.real_path)

    def emit_file(self, file_path):
        return  # HACK HACK HACK
        size = os.path.getsize(file_path)
        _, ext = os.path.splitext(file_path)
        mime, enc = mimetypes.guess_type(file_path, strict=False)
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
            'sha1': checksum(file_path)
        })


class DirectoryScanner(Scanner):

    IGNORE = ['.git', '.hg', '__MACOSX']

    def bid(self):
        if os.path.isdir(self.real_path):
            return 2

    def scan(self):
        if self.name in self.IGNORE:
            return
        log.info("Reading directory: %s", self.path_name)
        for name in os.listdir(self.real_path):
            self.descend(name)
