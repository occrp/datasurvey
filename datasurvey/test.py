from cli import main
from click.testing import CliRunner
import unittest

class TestDataSurvey(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_help(self):
        result = self.runner.invoke(main, ['--help'])
        self.assertEqual(result.exit_code, 0)

    def test_normal(self):
        result = self.runner.invoke(main, ['testdata'])
        self.assertEqual(result.exit_code, 0)

    def test_size(self):
        result = self.runner.invoke(main, ['--size', 'testdata'])
        self.assertEqual(result.exit_code, 0)

    def test_mimetype(self):
        result = self.runner.invoke(main, ['--mime', 'testdata'])
        self.assertEqual(result.exit_code, 0)

    def test_output_csv(self):
        result = self.runner.invoke(main, ['--format', 'csv', 'testdata'])
        self.assertEqual(result.exit_code, 0)

    def test_output_fancy(self):
        result = self.runner.invoke(main, ['--format', 'fancy', 'testdata'])
        self.assertEqual(result.exit_code, 0)

    def test_output_badmatch(self):
        result = self.runner.invoke(main, ['--format', 'badmatch', 'testdata'])
        self.assertEqual(result.exit_code, 0)

    def test_output_report(self):
        result = self.runner.invoke(main, ['--format', 'report', 'testdata'])
        self.assertEqual(result.exit_code, 0)

    def test_packages(self):
        result = self.runner.invoke(main, ['--packages', 'testdata'])
        self.assertEqual(result.exit_code, 0)

    def test_no_packages(self):
        result = self.runner.invoke(main, ['--no-packages', 'testdata'])
        self.assertEqual(result.exit_code, 0)


if __name__ == '__main__':
    unittest.main()
