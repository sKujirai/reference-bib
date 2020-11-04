import csv
import bibtexparser
from module.get_encoding import get_encoding


bib_file = 'reference.bib'
csv_file = 'key_url.csv'


if __name__ == '__main__':

    with open(bib_file, 'r', encoding=get_encoding(bib_file)) as fl:
        data_db = bibtexparser.load(fl)

    bib_datas = data_db.entries

    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        tags = ['ID', 'url']
        writer.writerow(tags)
        for bib in bib_datas:
            line = [bib['ID'], bib['url']]
            writer.writerow(line)

    print('Key-URL lists generated')
