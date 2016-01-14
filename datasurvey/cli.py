#!/usr/bin/python
import os
import click
from magic import Magic

class Recognizer:
    def recognize(self, file):
        raise NotImplemented()

class RecognizeCSV:
    pass


class Scanner:
    def __init__(self, mime=False):
        self.magic = Magic(magic_file='magic.db', mime=mime, uncompress=True)
        self._reset()

    def _reset(self):
        self.types = {}
        self.total = 0

    def scan_file(self, file):
        return self.magic.from_file(file)

    def scan(self, path):
        for root, directory, files in os.walk(path):
            for file in files:
                self.total += 1
                mime = self.scan_file(os.path.join(root, file))
                if not mime in self.types: self.types[mime] = []
                self.types[mime].append(file)

    def report(self):
        for t, fs in self.types.iteritems():
            print "%-35s: %d (%d%%)" % (t, len(fs), len(fs)*100/self.total)


@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--mime', is_flag=True)
def main(path, mime):
    s = Scanner(mime)
    s.scan(path)
    s.report()


if __name__ == "__main__":
    main()
