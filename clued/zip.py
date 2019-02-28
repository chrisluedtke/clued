import io, os, requests, zipfile


def extract_zip_url(data_url: str, write_path: str, flatten=True):
    '''Extracts .zip file from URL'''
    if not url.endswith('.zip'):
        raise ValueError("URL must end with '.zip'")

    r = requests.get(data_url)

    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        if flatten:
            for elem in z.infolist():
                elem.filename = os.path.basename(elem.filename)
                z.extract(elem, write_path)
        else:
            z.extractall(write_path)
