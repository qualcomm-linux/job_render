import os
from urllib.parse import urlparse

def is_url(url):
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return True
        else:
            return False
    except ValueError:
        return False

def is_local_path(path):
    if os.path.exists(path):
        return True
    else:
        return False
    
def extract_directory_name(path):
    directory = os.path.dirname(path)
    if directory.startswith(('/','\\')):
        directory = directory[1:]
    return directory

def extract_file_name(path):
    return os.path.basename(path)