import os
import logging
import shutil
import rarfile
import zipfile
import tarfile
import tempfile

from datasurvey.scanner import FileScanner

log = logging.getLogger(__name__)


class PackageScanner(FileScanner):

    def __init__(self, store, parent, name):
        super(PackageScanner, self).__init__(store, parent, name)
        self.extract_dir = tempfile.mkdtemp()

    @property
    def real_path(self):
        return self.extract_dir

    @property
    def package_path(self):
        if not self.root:
            return os.path.join(self.parent.real_path, self.name)
        return self.name

    def scan(self):
        self.emit_file(self.package_path)
        try:
            self.unpack_to_directory()
            for name in os.listdir(self.extract_dir):
                self.descend(name)
        finally:
            self.cleanup()

    def unpack_to_directory(self):
        raise NotImplemented()

    def cleanup(self):
        try:
            shutil.rmtree(self.extract_dir)
        except:
            pass


class ZipFileScanner(PackageScanner):

    IGNORE_EXT = ['docx', 'xlsx', 'pptx', 'ods', 'odt']

    def unpack_to_directory(self):
        log.info("Reading ZIP file: %s", self.path_name)
        with zipfile.ZipFile(self.package_path, 'r') as fh:
            fh.extractall(path=self.extract_dir)

    def bid(self):
        if os.path.isdir(self.package_path):
            return
        _, ext = os.path.splitext(self.package_path.lower())
        ext = ext.strip('.')
        if ext in self.IGNORE_EXT:
            return
        if zipfile.is_zipfile(self.package_path):
            return 3


class TarFileScanner(PackageScanner):

    def unpack_to_directory(self):
        log.info("Reading tarball: %s", self.path_name)
        with tarfile.TarFile(self.package_path, 'r') as fh:
            fh.extractall(path=self.extract_dir)

    def bid(self):
        if os.path.isdir(self.package_path):
            return
        if tarfile.is_tarfile(self.package_path):
            return 3


class RarFileScanner(PackageScanner):

    def unpack_to_directory(self):
        log.info("Reading RAR file: %s", self.path_name)
        with rarfile.RarFile(self.package_path, 'r') as fh:
            fh.extractall(path=self.extract_dir)

    def bid(self):
        if os.path.isdir(self.package_path):
            return
        if rarfile.is_rarfile(self.package_path):
            return 3
