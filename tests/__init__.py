__author__ = 'fabrice'

import os
def get_fixture_file(relative_path):
        return os.path.dirname(os.path.realpath(__file__)) + "/" + relative_path