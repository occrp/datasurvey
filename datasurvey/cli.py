#!/usr/bin/python
import os
import sys
import click
import csv
from magic import Magic
from packages import package_handlers

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
        else:
            buffer = open(path, 'rb')
            mime = self.magic.from_file(path)

        if mime in package_handlers.keys() and self.options['packages']:
            a = package_handlers[mime](buffer)
            self.scan_archive(path, a)
        else:
            if not mime in self.types: self.types[mime] = []
            self.files[path] = {}
            self.files[path]['mime'] = mime
            if self.options['size']:
                stat = os.stat(path)
                self.files[path]['size'] = stat.st_size
            self.types[mime].append(path)

    def scan_archive(self, path, archive):
        for (filename, fh) in archive:
            path = os.path.join(path, filename)
            self.total += 1
            self.scan_file(path, fh)

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

class Reporter:
    def __init__(self, options, scanner):
        self.options = options
        self.scanner = scanner
        self.outfile = options['target']

    def report(self):
        raise NotImplemented()


class ReportCSV(Reporter):
    def report(self):
        writer = csv.writer(self.options['target'])

        headers = ["filename", ["type", "mimetype"][self.scanner.mime]]
        if self.options['size']:
            headers.append('size')

        writer.writerow(headers)
        for f, details in self.scanner.files.iteritems():
            line = [f, details['mime']]
            if self.options['size']:
                line.append(details['size'])
            writer.writerow(line)

class ReportAggregate(Reporter):
    def report(self):
        for t, fs in self.scanner.types.iteritems():
            self.outfile.write("%-35s: %d (%d%%)\n" % (t, len(fs),
                len(fs)*100/self.scanner.total))

class ReportBadmatch(Reporter):
    badmatches = ["text/plain", "application/octet-stream"]

    def report(self):
        for t in self.badmatches:
            self.outfile.write("\n# %s\n\n" % (t))
            for fs in self.scanner.types[t]:
                self.outfile.write(" * %s\n" % (fs))
            self.outfile.write("\n")


outputmodes = {
    "csv":      ReportCSV,
    "report":   ReportAggregate,
    "badmatch": ReportBadmatch,
}

@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--mime', is_flag=True, help="Show mime types")
@click.option('--format', type=click.Choice(outputmodes.keys()),
    default="report", help="Choose output format")
@click.option('--size', is_flag=True, help="Show file sizes")
@click.option('--target', type=click.File('w'), default='-')
@click.option('--progress', is_flag=True, help="Show scanning progress")
@click.option('--packages/--no-packages', default=True, help="Descend into packages")
def main(path, **options):
    scanner = Scanner(**options)
    scanner.scan_path(path)
    reporter = outputmodes[options['format']](options, scanner)
    reporter.report()


if __name__ == "__main__":
    main()
