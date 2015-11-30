import csv
from keyword_generator.utils import OrderedSet

__author__ = 'fabrice'

delimiter = ","
quotechar = "'"

def get_rows(filepath):
    print ("reading '%s'" % filepath)
    with open(filepath, 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
        return [line[1] for line in enumerate(rows) if line[0] != 0]

def read_csv_column_distinct(filepath, column_index, quote_char=quotechar):
    print ("reading '%s'" % filepath)
    with open(filepath, 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=delimiter, quotechar=quote_char)
        values = OrderedSet()
        first = True
        for row in rows:
            if first:
                first = False
                continue
            values.add(row[column_index].lower())
    return values

def save_csv(filepath, lines, headers):
    with open(filepath, 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=delimiter,
                                quotechar=quotechar)
        spamwriter.writerow(headers)
        exportedRows = 0
        for line in lines:
            spamwriter.writerow(line)
            exportedRows+=1
        return exportedRows