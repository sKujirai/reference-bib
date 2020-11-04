import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import pandas as pd
from module.get_encoding import get_encoding


bib_file = 'reference.bib'
csv_file = 'key_url.csv'


def get_index(l, x):
    if x in l:
        return l.index(x)
    else:
        return -1


if __name__ == '__main__':

    with open(bib_file, 'r', encoding=get_encoding(bib_file)) as fl:
        data_db = bibtexparser.load(fl)
    bib_datas = data_db.entries

    tsv_datas = pd.read_csv(csv_file, sep='\t', encoding='utf-8', dtype=str, na_filter=False)
    IDs = tsv_datas['ID'].tolist()
    URLs = tsv_datas['url'].tolist()

    for dat in bib_datas:
        idx = get_index(IDs, dat['ID'])
        if idx != -1:
            dat['url'] = URLs[idx]

    db = BibDatabase()
    db.entries = bib_datas
    writer = BibTexWriter()
    writer.indent = '    '  # indent entries with 4 spaces instead of single space

    with open(bib_file, 'w', encoding='utf-8') as fl:
        fl.write(writer.write(db))

    print('URL updated')
