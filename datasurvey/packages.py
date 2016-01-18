import gzip
import bz2
import rarfile
import zipfile
import tarfile

class PackageHandler:
    def __init__(self, buffer):
        self.buffer = buffer

    def __iter__(self):
        for name in self.archive.namelist():
            info = self.archive.getinfo(name)
            if hasattr(info, 'isdir') and info.isdir():
                continue
            if name[-1] == "/":
                continue
            with self.archive.open(name) as ar:
                # TODO: Handle archives
                outbuf = ar.read(1000)

            yield (name, outbuf)

class ZipHandler(PackageHandler):
    MIMETYPES = ["application/zip"]
    def __init__(self, buffer):
        PackageHandler.__init__(self, buffer)
        self.archive = zipfile.ZipFile(buffer)

class RarHandler(PackageHandler):
    MIMETYPES = ["application/x-rar-compressed"]
    def __init__(self, buffer):
        PackageHandler.__init__(self, buffer)
        self.archive = zipfile.RarFile(buffer)



package_handlers = {}

def register_handler(handler):
    for mt in handler.MIMETYPES:
        package_handlers[mt] = handler

register_handler(ZipHandler)
register_handler(RarHandler)
