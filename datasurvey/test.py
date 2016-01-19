from cli import main
from click.testing import CliRunner
import unittest

class TestDataSurvey(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_help(self):
        result = self.runner.invoke(main, ['--help'])

    def test_normal(self):
        result = self.runner.invoke(main, ['testdata'])

    def test_size(self):
        result = self.runner.invoke(main, ['--size', 'testdata'])

    def test_mimetype(self):
        result = self.runner.invoke(main, ['--mime', 'testdata'])

    def test_output_csv(self):
        result = self.runner.invoke(main, ['--format', 'csv', 'testdata'])

    def test_output_pretty(self):
        result = self.runner.invoke(main, ['--format', 'pretty', 'testdata'])

    def test_output_badmatch(self):
        result = self.runner.invoke(main, ['--format', 'badmatch', 'testdata'])

    def test_output_report(self):
        result = self.runner.invoke(main, ['--format', 'report', 'testdata'])

    def test_packages(self):
        result = self.runner.invoke(main, ['--packages', 'testdata'])
        result = self.runner.invoke(main, ['--no-packages', 'testdata'])


if __name__ == '__main__':
    unittest.main()
