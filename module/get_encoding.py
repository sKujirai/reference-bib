import sys
import locale


def get_encoding(file_path):
    """
    Check encoding
    """
    locale.setlocale(locale.LC_ALL, '')
    with open(file_path, 'rb') as fl:
        datas = fl.read()
    try:
        datas.decode('utf-8')
        return 'utf-8'
    except UnicodeDecodeError:
        try:
            datas.decode('cp932')
            return 'cp932'
        except UnicodeDecodeError:
            sys.exit('[ERROR] Encoding error')
            return None
