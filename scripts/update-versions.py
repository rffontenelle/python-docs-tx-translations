#!/usr/bin/python3
# Update versions.txt with latest status from Python devguide

from bs4 import BeautifulSoup
from packaging.version import parse
import csv
import io
import re
import requests
import sys


versions_file = '.github/versions.txt'

def warning(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_from_devguide():
    """
    Returns a list of released versions.
    Extract bug-fix and security-fix releases from a devguide's CSV,
    which is used by version.rst for https://devguide.python.org/versions/
    """
    url = 'https://raw.githubusercontent.com/python/devguide/main/include/branches.csv'
    
    r = requests.get(url, allow_redirects=True)
    if r.status_code != 200:
        sys.exit(f'ERROR: Unable to collect Python versions, connection failed with: {url}')
        return None
    
    reader = csv.DictReader(r.content.decode(r.apparent_encoding).splitlines(), delimiter = ',')
    
    branches = []
    for row in reader:
        if row['Status'] in ['bugfix', 'security']:
            branches.append((row['Branch']))
    
    return branches


def get_latest_version():
    """
    Return the latest development Python version.
    Browse the Download page from Python website looking for versions,
    and filter the content to get only the latest. If the latest version is
    alpha or stable version, then return an empty string because we do not
    want alpha version and stable ones are already listed in devguide.
    """
    url = 'https://www.python.org/downloads/source/'
    
    # Match occurences like "3.11.0", "3.12.0a2", etc.
    pattern = 'Python 3\.[\d]+\.[\d]+((a|rc|b])[\d]+)?'
    
    r = requests.get(url)
    if r.status_code != 200:
        warning(f'WARNING: Unable to collect data from: {url}')
        return None
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    latest = ''
    for item in soup.find_all('a'):
        m = re.match(pattern,item.get_text())
        if m:
            current_version = m.group().split(' ')[1]
            if not latest:
                latest = current_version
            else:
                if parse(current_version) > parse(latest):
                    latest = current_version
    
    if parse(latest).pre and parse(latest).pre[0] in ['b', 'rc']:
        return latest
    else:
        return None


versions = get_from_devguide()
latest = get_latest_version()

# Store version in major.minor versioning scheme (e.g. 3.11) 
if latest:
    major_version = re.match('3.[\d]+', latest).group()
    versions.insert(0, major_version)

with open(versions_file, 'w') as f:
    f.write(f"{versions}\n")
