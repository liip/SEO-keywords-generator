import os
import click

import keyword_generator.csv as csv
from keyword_generator.kw_generator.generator_objects import KeywordSets
from .generator_objects import KeywordsCombination
from .generator_objects import Keywords
from .generator_objects import Keyword
from .generator_objects import Pattern

__author__ = 'fabrice'


def read_patterns_csv(filepath, keyword_sets):
    return [Pattern(row[0], row[1], row[2] if len(row)>1 else "", keyword_sets) for row in csv.get_rows(filepath)]

def read_keywords_csv(filepath, keyword_set_name):
    keywords = [Keyword(row[0], set([lang for lang in row[1].split("|")])) for row in csv.get_rows(filepath)]
    return Keywords(keyword_set_name, keywords)

def path_join(path1, path2):
    p1 = path1 if path1[-1]!='/' else path1[:-1]
    p2 = path2 if path2[0]!='/' else path2[1:]
    return '/'.join([p1, p2])

def read_keyword_sets(dir):
    files = os.listdir(dir)
    keywords = []
    for filepath in files:
        if filepath[-4:] == '.csv':
            keywords.append(read_keywords_csv(path_join(dir, filepath), filepath[:-4]))
    return KeywordSets(keywords)

def generate_combinations(root_dir, pattern_file="patterns.csv"):
    keyword_sets = read_keyword_sets(path_join(root_dir, "keyword_placeholders"))
    patterns = read_patterns_csv(path_join(root_dir, pattern_file), keyword_sets)
    return KeywordsCombination(patterns).generate()

def save_combinations(filepath, generatedResult):
    exportedRows = csv.save_csv(filepath,
                 [
                     [
                         keyphrase,
                         "|".join(sorted(infos.lang)),
                         "|".join(sorted(infos.topics)),
                         "|".join(sorted(infos.tags))
                     ] for keyphrase, infos in iter(sorted(generatedResult.items()))
                 ],
                 ["keyphrase", "lang", "topics", "tags"])
    click.echo("Number of generated keywords : " + str(exportedRows))
