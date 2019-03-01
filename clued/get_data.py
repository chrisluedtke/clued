import io, os,  re, requests, zipfile
from typing import List

from bs4 import BeautifulSoup

__all__ = [
    'extract_zip_url',
    'get_uci_data_urls',
    'get_uci_attributes',
]

def extract_zip_url(url: str, write_path: str, flatten=True):
    '''Extract .zip file from URL to local machine'''
    if not url.endswith('.zip'):
        raise ValueError("URL must end with '.zip'")

    r = requests.get(url)

    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        if flatten:
            for elem in z.infolist():
                elem.filename = os.path.basename(elem.filename)
                z.extract(elem, write_path)
        else:
            z.extractall(write_path)


def get_uci_data_urls(url: str) -> List[str]:
    if not url.startswith('https://archive.ics.uci.edu/ml/datasets/'):
        raise ValueError('URL not recognized')

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    df_url = soup.find('a', string='Data Folder', href=True)

    if not df_url:
        raise ValueError('No "Data Folder" element on page')

    db_url = 'https://archive.ics.uci.edu/ml' + df_url['href'].strip('.')

    r = requests.get(db_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    data_urls = []
    for ext in [".data", ".names", ".zip"]:
        data_url = soup.find(string=re.compile(ext), href=True)
        if data_url:
            data_url = db_url + data_url['href']
            print(data_url)
            data_urls.append(data_url)

    return data_urls


def get_uci_attributes(url: str):
    if not url.endswith('.names'):
        raise ValueError("URL must end with '.names'")

    r = requests.get(url)

    attr_found, blank_count = [False] * 2
    attrs = {}
    for i, line in enumerate(r.text.split('\n')):
        if 'Attribute Information' in line:
            attr_found = True
            continue
        if attr_found and not line:
            blank_count += 1
            if blank_count==2:
                break
            continue
        if attr_found:
            attr = (line.replace('  ', '')
                        .replace('\t', '')
                        .replace('.', '').split(':'))
            attrs[attr[0]] = attr[1]

    return attrs
