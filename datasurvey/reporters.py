import csv

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
