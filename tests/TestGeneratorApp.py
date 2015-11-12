from __future__ import absolute_import
from keyword_generator.kw_generator import generate_combinations

from tests import get_fixture_file

__author__ = 'fabrice'

import unittest

class TestKeywords(unittest.TestCase):
    def test(self):

        generated_keywords = generate_combinations(get_fixture_file("fixtures/generator"))
        expected = ["developpement geneve",
                    "developpement drupal",
                    "developpement aem",
                    "development geneva",
                    "development drupal",
                    "development aem",
                    ]
        self.assertEqual(expected, generated_keywords.keys())

if __name__ == '__main__':
   unittest.main()