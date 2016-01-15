#!/usr/bin/python
import os
import click
from magic import Magic

class Scanner:
    def __init__(self, mime=False):
        self.magic = Magic(magic_file='magic.db', mime=mime, uncompress=True)
        self.mime = mime
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



class Reporter:
    def __init__(self, scanner):
        self.scanner = scanner

    def report(self):
        raise NotImplemented()

class ReportCSV(Reporter):
    def report(self):
        print "\"filename\",\"%s\"" % (["type", "mimetype"][self.scanner.mime])
        for t, fs in self.scanner.types.iteritems():
            for f in fs:
                print "\"%s\",\"%s\"" % (f, t)

class ReportAggregate(Reporter):
    def report(self):
        for t, fs in self.scanner.types.iteritems():
            print "%-35s: %d (%d%%)" % (t, len(fs), len(fs)*100/self.scanner.total)


outputmodes = {
    "csv":      ReportCSV,
    "report":   ReportAggregate,
}

@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--mime', is_flag=True)
@click.option('--output', type=click.Choice(outputmodes.keys()), default="report")
def main(path, mime, output):
    s = Scanner(mime)
    s.scan(path)
    reporter = outputmodes[output](s)
    reporter.report()


if __name__ == "__main__":
    main()
