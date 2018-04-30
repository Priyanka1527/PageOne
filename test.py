import requests
import re

#url = 'https://www.investopedia.com/tech/'

#r = requests.get(url, allow_redirects=True)
#open('file.htm', 'wb').write(r.content)


def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


url = 'https://www.investopedia.com/tech/'
r = requests.get(url, allow_redirects=True)
filename = get_filename_from_cd(r.headers.get('content-disposition'))
open(filename, 'wb').write(r.content)
