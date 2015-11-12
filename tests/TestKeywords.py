from keyword_generator.kw_generator.generator_objects import Keyword, Keywords

__author__ = 'fabrice'

import unittest

class TestKeywords(unittest.TestCase):

    def test(self):
        kws = Keywords("truc", [
            Keyword("lala", ["fr"]),
            Keyword("lili", ["de"]),
            Keyword("lolo", ["en"]),
            Keyword("lulu", ["fr", "de"]),
        ])

        keywords_for_lang = kws.get_keywords_for_lang(["fr", "en"])

        self.assertEqual(["lala", "lolo", "lulu"], keywords_for_lang)

if __name__ == '__main__':
    unittest.main()