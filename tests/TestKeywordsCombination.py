from keyword_generator.kw_generator.generator_objects import KeywordSets, Keywords, Keyword, Pattern, \
    KeywordsCombination

__author__ = 'fabrice'

import unittest

class TestKeywordsCombination(unittest.TestCase):

    def test(self):
        keyword_sets = KeywordSets([
            Keywords("service", [
                Keyword("development", ["en"]),
                Keyword("developpement", ["fr"])
            ]),
            Keywords("location", [
                Keyword("Geneva", ["en"]),
                Keyword("Geneve", ["fr"]),
                Keyword("Genf", ["de"])
            ]),
            Keywords("theme", [
                Keyword("Drupal", ["en", "fr"]),
                Keyword("AEM", ["en", "fr", "de"])
            ]),
        ])

        patterns = [
            Pattern('service location', keyword_sets),
            Pattern('service theme', keyword_sets)
        ]
        langs = ["fr", "en"]

        expected = ["developpement geneve",
                    "developpement drupal",
                    "developpement aem",
                    "development geneva",
                    "development drupal",
                    "development aem",
                    ]



        kwc = KeywordsCombination(patterns, langs)

        result = kwc.generate()

        self.assertEqual(expected, result.keys())

if __name__ == '__main__':
    unittest.main()