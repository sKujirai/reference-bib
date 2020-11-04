import sys
import os
import shutil
import logging
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bibtexexpression import BibtexExpression
import csv
import pandas as pd
from module.get_encoding import get_encoding
from module.bib_unit import BibUnitData


def read_bib_file(bib_file):
    """
    .bibファイル読み込み
    """
    logger = logging.getLogger('LogBib')

    if not os.path.isfile(bib_file):
        logger.error('.bib does not exist: ' + bib_file)
        sys.exit(1)

    try:
        with open(bib_file, 'r', encoding=get_encoding(bib_file)) as fl:
            data_db = bibtexparser.load(fl)
            return data_db.entries
    except BibtexExpression.ParseException as pe:
        raise Exception(pe)
    except Exception as e:
        logger.error('Cannot read .bib file: ' + bib_file)
        logger.error(e)
        sys.exit(1)


def get_bib_lists_no_duplicate(bib_lists):
    """
    文献リストから重複を削除する
    """
    logger = logging.getLogger('LogBib')
    bib_lists_no_duplicate = []
    title_sets = set()
    key_sets = set()
    for bib in bib_lists:
        key = bib['ID']
        title = bib['title']
        if key not in key_sets and title not in title_sets:
            key_sets.add(key)
            title_sets.add(title)
            bib_lists_no_duplicate.append(bib)
        else:
            logger.warning('Duplication detected')
            logger.warning('[key] ' + key)
            logger.warning('[Title] ' + title)
    return bib_lists_no_duplicate


def get_value(bib, key):
    """
    辞書の値取得
    """
    try:
        val = bib[key]
    except Exception:
        val = ''
    return val


def output_tsv(bib_lists, output_file):
    """
    文献リストをTSV出力
    """
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        tag_list = ['ID', 'author', 'title', 'journal', 'volume', 'number', 'pages', 'publisher', 'year', 'ENTRYTYPE', 'keywords', 'memo', 'abstract', 'url']
        writer.writerow(tag_list)
        for bib in bib_lists:
            line = [get_value(bib, id) for id in tag_list]
            writer.writerow(line)


if __name__ == '__main__':

    # Logger設定
    logger = logging.getLogger('LogBib')
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    handler_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(handler_format)
    logger.addHandler(stream_handler)

    logger.info('Start .bib reader.....')

    # データ追加先の.bibファイル情報読み込み
    print('Input reference .bib file path: ', end='')
    reference_bib_path = input().strip()
    ref_data = read_bib_file(reference_bib_path)
    get_bib_lists_no_duplicate(ref_data)

    # 追加する.bibデータ読込み
    input_bib_data = []
    while True:
        print('Select mode')
        print('[1] Read from .bib file')
        print('[2] Read from .csv file')
        print('[3] Input data manually')
        print('[0] exit')
        input_str = input().strip()
        if int(input_str) == 1:
            print('Input .bib path: ', end='')
            bib_path = input()
            bib_datas = read_bib_file(bib_path)
            for dat in bib_datas:
                bib_unit_data = BibUnitData()
                input_bib_data.append(bib_unit_data.read_bib_data(dat))
            break
        if int(input_str) == 2:
            print('Input .csv path: ', end='')
            tsv_path = input()
            tsv_datas = pd.read_csv(tsv_path, sep='\t', encoding='utf-8')
            tsv_datas = tsv_datas.T.to_dict().values()
            for dat in tsv_datas:
                bib_unit_data = BibUnitData()
                input_bib_data.append(bib_unit_data.read_bib_data(dat))
            break
        elif int(input_str) == 3:
            bib_unit_data = BibUnitData()
            input_bib_data.append(bib_unit_data.read_bib_data())
            break
        elif int(input_str) == 0:
            logger.info('.....Exit')
            sys.exit(0)

    # データ統合
    ref_keys = [dat['ID'] for dat in ref_data]
    print(ref_keys)
    for dat in input_bib_data:
        APPEND_DATA = True
        if dat['ID'] in ref_keys:
            logger.warning('.bib data already exists')
            logger.warning('[key] ' + dat['ID'])
            APPEND_DATA = False
            while True:
                print('Overwrite? [0] No (default) [1] Yes : ')
                input_str = input().strip()
                if input_str == '' or int(input_str) == 0:
                    break
                elif int(input_str) == 1:
                    ref_data[ref_keys.index(dat['ID'])] = dat
                    break
        if APPEND_DATA:
            ref_data.append(dat)

    # .bibファイルに出力
    logger.info('Output .bib file: ' + reference_bib_path)
    backup_path = reference_bib_path + '.bak'
    shutil.copy(reference_bib_path, backup_path)
    db = BibDatabase()
    db.entries = ref_data
    writer = BibTexWriter()
    writer.indent = '    '  # indent entries with 4 spaces instead of single space
    try:
        with open(reference_bib_path, 'w', encoding='utf-8') as fl:
            fl.write(writer.write(db))
    except Exception as e:
        logger.error('Cannot write .bib file: ' + reference_bib_path)
        logger.error(e)
        if os.path.exists(reference_bib_path):
            os.remove(backup_path)
            shutil.move(backup_path, reference_bib_path)
        sys.exit(1)

    if os.path.isfile(backup_path):
        os.remove(backup_path)

    # 文献リストをTSV形式で出力
    while True:
        print('Output .csv file path: ', end='')
        output_csv_path = input().strip()
        if not output_csv_path == '':
            break
    try:
        if os.path.isfile(output_csv_path):
            os.remove(output_csv_path)
        output_tsv(ref_data, output_csv_path)
    except Exception as e:
        logger.error('Cannot write .csv file: ' + output_csv_path)
        logger.error(e)
        sys.exit(1)

    logger.info('Program end')
