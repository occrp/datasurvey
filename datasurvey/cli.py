#!/usr/bin/python
import os
import sys
import click
import chardet
from magic import Magic
from packages import package_handlers
from reporters import outputmodes

def guess_encoding(text):
    if text is None or len(text) == 0:
        return
    if isinstance(text, unicode):
        return text
    enc = chardet.detect(text)
    out = enc.get('encoding', 'utf-8')
    if out is None:
        # Awkward!
        return text
    # print u"%s --[%s]-> %s" % (text, out, text.decode(out))
    return text.decode(out)

class Scanner:
    def __init__(self, **options):
        self.options = options
        self.mime = options['mime']
        self.progress = options['progress']
        self.magic = Magic(magic_file='magic.db', mime=self.mime, uncompress=False)
        self._reset()

    def _reset(self):
        self.types = {}
        self.files = {}
        self.total = 0

    def get_file_magic(self, path):
        return self.magic.from_file(path)

    def scan_file(self, path, buffer=None):
        if buffer:
            mime = self.magic.from_buffer(buffer)
        elif path:
            buffer = open(path, 'rb')
            mime = self.magic.from_file(path)
        else:
            print "Can't do anything without a filename or buffer."
            return

        if mime in package_handlers.keys() and self.options['packages']:
            try:
                a = package_handlers[mime](buffer)
                self.scan_archive(path, a)
            except:
                self.register_file(path, mime)
        else:
            self.register_file(path, mime)

    def register_file(self, path, mime):
        if not mime in self.types: self.types[mime] = []
        self.files[path] = {}
        self.files[path]['mime'] = mime
        if self.options['size']:
            try:
                stat = os.stat(path)
                self.files[path]['size'] = stat.st_size
            except:
                self.files[path]['size'] = 0
        self.types[mime].append(path)

    def scan_archive(self, path, archive):
        for (filename, fh) in archive:
            self.total += 1
            try:
                filename = guess_encoding(filename)
                path = guess_encoding(path)
                npath = os.path.join(path, filename)
                self.scan_file(npath, fh)
            except:
                self.scan_file(None, fh)

            #except UnicodeDecodeError, e:
            #    print "Unicode decoding error: %s/%s" % (e.encoding, ":".join("{:02x}".format(ord(c)) for c in filename))
            #    continue

    def scan_path(self, path):
        for root, directory, files in os.walk(path):
            for file in files:
                self.total += 1
                path = os.path.join(root, file)
                self.scan_file(path)
                if self.progress and self.total % 10 == 0:
                    print "\rScanned %d files..." % self.total,
                    sys.stdout.flush()

        if self.progress:
            print ""


@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--mime', is_flag=True, help="Show mime types")
@click.option('--format', type=click.Choice(outputmodes.keys()),
    default="report", help="Choose output format")
@click.option('--size', is_flag=True, help="Show file sizes")
@click.option('--target', type=click.File('w'), default='-', help="Output to file")
@click.option('--progress', is_flag=True, help="Show scanning progress")
@click.option('--packages/--no-packages', default=True, help="Descend into packages? (Default: yes)")
def main(path, **options):
    scanner = Scanner(**options)
    scanner.scan_path(path)
    reporter = outputmodes[options['format']](options, scanner)
    reporter.report()


if __name__ == "__main__":
    main()
