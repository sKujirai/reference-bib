import os
import sys
import logging
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bibtexexpression import BibtexExpression
from module.get_encoding import get_encoding


class BibUnitData:
    """
    文献ごとの項目管理
    """

    def __init__(self):

        # .bib data
        self.data = {}

        # Logger
        self.logger = logging.getLogger('LogBib')

        # 文献種別
        self.bib_types = ['article', 'book', 'booklet', 'inbook', 'incollection', 'proceedings', 'inproceedings', 'manual', 'phdthesis', 'masterthesis', 'techreport', 'unpublished', 'misc']

        # 文献種別ごとの項目を設定
        # article
        self.article_item = ['author', 'title', 'journal', 'year', 'keywords', 'memo']
        self.article_option = ['volume', 'number', 'pages', 'issn', 'doi', 'url', 'abstract', 'eprint', 'publisher']
        # book
        self.book_item = ['author', 'title', 'publisher', 'year', 'keywords', 'memo']
        self.book_option = ['editor', 'volume', 'number', 'series', 'address', 'edition', 'issn', 'doi', 'url', 'abstract']
        # booklet
        self.booklet_item = ['title', 'keywords', 'memo']
        self.booklet_option = ['author', 'howpublished', 'address', 'year', 'issn', 'doi', 'url', 'abstract']
        # inbook
        self.inbook_item = ['author', 'title', 'chapter', 'publisher', 'year', 'keywords', 'memo']
        self.inbook_option = ['editor', 'pages', 'volume', 'number', 'series', 'type', 'address', 'edition', 'issn', 'doi', 'url', 'abstract']
        # incollection
        self.incollection_item = ['author', 'title', 'booktitle', 'publisher', 'year', 'keywords', 'memo']
        self.incollection_option = ['editor', 'volume', 'number', 'series', 'type', 'chapter', 'pages', 'address', 'edition', 'issn', 'doi', 'url', 'abstract']
        # proceedings
        self.proceedings_item = ['title', 'year', 'keywords', 'memo']
        self.proceedings_option = ['editor', 'volume', 'number', 'series', 'address', 'organization', 'publisher', 'issn', 'doi', 'url', 'abstract']
        # inproceedings
        self.inproceedings_item = ['author', 'title', 'booktitle', 'year', 'keywords', 'memo']
        self.inproceedings_option = ['editor', 'volume', 'number', 'series', 'pages', 'address', 'organization', 'publisher', 'issn', 'doi', 'url', 'abstract']
        # manual
        self.manual_item = ['title', 'keywords', 'memo']
        self.manual_option = ['author', 'organization', 'address', 'edition', 'year', 'issn', 'doi', 'url', 'abstract']
        # PhD thesis
        self.phdthesis_item = ['author', 'title', 'school', 'year', 'keywords', 'memo']
        self.phdthesis_option = ['type', 'address', 'url', 'abstract']
        # masterthesis
        self.masterthesis_item = ['author', 'title', 'school', 'year', 'keywords', 'memo']
        self.masterthesis_option = ['type', 'address', 'url', 'abstract']
        # technical report
        self.techreport_item = ['author', 'title', 'institution', 'year', 'keywords', 'memo']
        self.techreport_option = ['type', 'number', 'address', 'issn', 'doi', 'url', 'abstract']
        # unpublished
        self.unpublished_item = ['author', 'title', 'keywords', 'memo']
        self.unpublished_option = ['year', 'doi', 'url', 'abstract']
        # misc
        self.misc_item = ['keywords', 'memo']
        self.misc_option = ['author', 'title', 'howpublished', 'year', 'issn', 'doi', 'url', 'abstract', 'eprint']

        # Key used in system
        self.key_system = ['ID', 'ENTRYTYPE']

    def read_bib_data(self, bib_data=None):
        """
        Read .bib data
        """

        # Pythonでは関数のオーバーライドができないようなのでこう書くしかない？
        if bib_data is None:
            print('Input entry type: ', end='')
            entrypoint = input()
            self.data['ENTRYTYPE'] = entrypoint
            print('Input key: ', end='')
            self.data['ID'] = input()
        else:
            # self.read_bib_file(bib_file)
            self.data = bib_data
            entrypoint = self.data['ENTRYTYPE']

        print(self.data['ID'])

        if entrypoint == 'article':
            self.item = self.article_item
            self.option = self.article_option
        elif entrypoint == 'book':
            self.item = self.book_item
            self.option = self.book_option
        elif entrypoint == 'booklet':
            self.item = self.booklet_item
            self.option = self.booklet_option
        elif entrypoint == 'inbook':
            self.item = self.inbook_item
            self.option = self.inbook_option
        elif entrypoint == 'incollection':
            self.item = self.incollection_item
            self.option = self.incollection_option
        elif entrypoint == 'proceedings':
            self.item = self.proceedings_item
            self.option = self.proceedings_option
        elif entrypoint == 'inproceedings':
            self.item = self.inproceedings_item
            self.option = self.inproceedings_option
        elif entrypoint == 'manual':
            self.item = self.manual_item
            self.option = self.manual_option
        elif entrypoint == 'phdthesis':
            self.item = self.phdthesis_item
            self.option = self.phdthesis_option
        elif entrypoint == 'masterthesis':
            self.item = self.masterthesis_item
            self.option = self.masterthesis_option
        elif entrypoint == 'techreport':
            self.item = self.techreport_item
            self.option = self.techreport_option
        elif entrypoint == 'unpublished':
            self.item = self.unpublished_item
            self.option = self.unpublished_option
        elif entrypoint == 'misc':
            self.item = self.misc_item
            self.option = self.misc_option
        else:
            self.logger.error('Invalid entry point')
            entry_points_str = ''
            for ent in self.bib_types:
                entry_points_str += ent + ', '
            self.logger.error('Entry point list: ' + entry_points_str)
            sys.exit(1)

        self.key_insufficient = self.item.copy()
        self.key_insufficient_option = self.option.copy()

        # 未入力の項目を調査
        self.update_unset_key()

        # 未入力の項目の値を読み込み
        self.read_value()

        # 不要な項目を削除
        self.remove_unnecessary_key()

        return self.data

    def read_bib_file(self, bib_file):

        if not os.path.isfile(bib_file):
            self.logger.error('.bib does not exist: ' + bib_file)
            sys.exit(1)

        try:
            with open(bib_file, 'r', encoding=get_encoding(bib_file)) as fl:
                data_db = bibtexparser.load(fl)
                self.data = data_db.entries[0]
        except BibtexExpression.ParseException as pe:
            raise Exception(pe)
        except Exception as e:
            self.logger.error('Cannot read .bib file: ' + bib_file)
            self.logger.error(e)
            sys.exit(1)

    def update_unset_key(self):
        for key in self.data.keys():
            if key in self.key_insufficient:
                self.key_insufficient.remove(key)
            if key in self.key_insufficient_option:
                self.key_insufficient_option.remove(key)

    def read_value(self):

        # 必須項目
        for key in self.key_insufficient:
            while True:
                print('[', key, '] (Required) : ', end='')
                val = input().strip()
                if val == '':
                    continue
                self.data[key] = val
                break

        # 任意項目
        for key in self.key_insufficient_option:
            print('[', key, '] : ', end='')
            self.data[key] = input()

    def remove_unnecessary_key(self):

        keys = list(self.data.keys())
        for key in keys:
            if key not in self.item and key not in self.option and key not in self.key_system:
                del self.data[key]
