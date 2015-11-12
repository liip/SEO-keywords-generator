from keyword_generator.awrcloud import pages_parser
from keyword_generator.awrcloud.awr_items import AwrKeyword, AwrGroup
from tests import get_fixture_file

__author__ = 'fabrice'

import unittest

class TestPageParser(unittest.TestCase):

    def test_parse_keywords_page(self):
        with open(get_fixture_file("fixtures/html/keywords_page.html"), "r") as f:
            s = f.read()
        keywords = pages_parser.parse_keywords_from_html(s)
        self.assertEqual(
            [
                AwrKeyword(u"responsive design", "1"),
                AwrKeyword(u"analytics", "2")
            ],
            keywords
        )

    def test_get_total_keywords(self):
        with open(get_fixture_file("fixtures/html/keywords_page.html"), "r") as f:
            s = f.read()
        number = pages_parser.parse_total_keywords(s)
        self.assertEqual(2, number)

    def test_parse_groups_page(self):
        with open(get_fixture_file("fixtures/html/groups_page.html"), "r") as f:
            s = f.read()
        groups = pages_parser.parse_groups_from_html(s)
        print (groups)
        self.assertEqual(
            [
                AwrGroup(u"sdf", "36"),
                AwrGroup(u"coco", "37")
            ],
            groups
        )

    def test_parse_projects_page(self):
        with open(get_fixture_file("fixtures/html/projects_page.html"), "r") as f:
            s = f.read()
        groups = pages_parser.parse_projects_from_html(s)
        print (groups)

        self.assertEqual(
            [
                ('1', 'liip.ch'),
                ('4', 'www.f-p-sa.ch'),
                ('2', 'giampierobodino.com'),
                ('3', 'https://www.swissaid.ch/')
            ],
            groups
        )

if __name__ == '__main__':
    unittest.main()