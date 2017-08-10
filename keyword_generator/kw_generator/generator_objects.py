from collections import OrderedDict
import itertools

class Keyword:
    def __init__(self, keyword, langs):
        self._keyword = keyword
        self._langs = langs

    def is_lang(self, lang):
        return lang in self._langs

    def __eq__(self, other):
        return self._keyword == other

    def __repr__(self):
        return self._keyword

class Keywords:
    def __init__(self, topic, keywords):
        self._topic = topic
        self._keywords = keywords

    def get_keywords_for_lang(self, langs):
        return [
            keyword for keyword in self._keywords if any([keyword.is_lang(lang) for lang in langs])
        ]

class KeywordSets:
    def __init__(self, set_list):
        self._keyword_sets = {
            keywords._topic : keywords
                for keywords in set_list
        }

    def __getitem__(self, topic):
        return self._keyword_sets[topic]

class Pattern:
    def __init__(self, pattern_str, pattern_langs, tags, keyword_sets):
        self.pattern_str = pattern_str
        self._keyword_sets = keyword_sets
        self.tags = tags.strip().split("|")
        self.langs = pattern_langs.strip().split("|")
        self.topics = [key.strip() for key in pattern_str.split(" ")]

    def generate_combinations(self, lang):
        combinations = [
            self._keyword_sets[topic].get_keywords_for_lang([lang]) for topic in self.topics
        ]
        return itertools.product(*combinations)

class KeyphraseProperties:
    def __init__(self, topics, lang, tags):
        self.topics = set(topics)
        self.lang = set([lang])
        self.tags = tags

    def merge(self, groups):
        self.topics.update(groups.topics)
        self.lang.update(groups.lang)


class KeywordsCombination:

    def __init__(self, patterns):
        self._patterns = patterns

    def generate(self):
        result = OrderedDict()
        for pattern in self._patterns:
            for lang in pattern.langs:
                print(pattern.pattern_str, lang)
                combinations = pattern.generate_combinations(lang)
                for combination in combinations:
                    keyphrase = self.combination_to_keyphrase(combination)
                    infos = KeyphraseProperties(pattern.topics, lang, pattern.tags)
                    if keyphrase in result:
                        result[keyphrase].merge(infos)
                    else:
                        result[keyphrase] = infos
        return result

    def combination_to_keyphrase(self, combination):
        return " ".join([repr(c).lower() for c in combination])


