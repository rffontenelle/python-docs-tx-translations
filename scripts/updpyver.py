#!/usr/bin/env python3
# Update versions.txt with latest status from Python devguide

from argparse import ArgumentParser
from bs4 import BeautifulSoup
from packaging.version import parse
from pathlib import Path
import json
import re
import requests
import sys


def get_from_devguide() -> list:
    """
    Returns a list of bug-fix and security-fix releases from
    a JSON file in devguide, which is used to generate info
    on version.rst for https://devguide.python.org/versions/.
    
    Returns:
        A list containing the versions.
    
    Raises:
        JSONDecodeError: If an error occurs when parsing the data as JSON.
    """
    raw_root_url = 'https://raw.githubusercontent.com/python/devguide/main'
    url = f'{raw_root_url}/include/release-cycle.json'
    
    r = requests.get(url, allow_redirects=True)
    if r.status_code != 200:
        exit(f'ERROR: Collect Python versions failed, no connection to: {url}')

    try:
        data = json.loads(r.content.decode(r.apparent_encoding))
        versions = [k for k, v in data.items()
                    if v['status'] in ['bugfix', 'security']]
        return versions
    except json.JSONDecodeError:
        sys.exit("ERROR: Unable to parse response as a JSON object")


def get_latest_version() -> str:
    """
    Returns the latest beta or release candidate version of Python.

    This function scrapes the Python download page to gather version
    information and selects the latest one.
    Versions that are either alpha or stable are excluded from the results.
    
    Returns:
        str: The latest beta or release candidate version of Python.
             If no version is found, or if the latest version is
             either alpha or stable, returns 'None'.
    """
    url = 'https://www.python.org/downloads/source/'
    pattern = r'Python 3.[\d]+.[\d]+((rc|b)[\d]+)? '
    
    r = requests.get(url, allow_redirects=True)
    if r.status_code != 200:
        sys.exit(f'ERROR: Unable to collect data from: {url}')
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    versions = []
    for item in soup.find_all('a'):
        m = re.match(pattern, item.get_text())
        if m:
            version = m.group().split(' ')[1]
            versions.append(version)
    
    latest = max(versions, default=None, key=lambda v: parse(v))
    
    if parse(latest).pre and parse(latest).pre[0] in ['b', 'rc']:
        return latest
    else:
        return None


def update_versions_file(versions_file: str):
    """
    Writes Python versions in *versions_file* using info gathered by
    the get_from_devguide() and get_latest_version() functions.
    """
    versions = get_from_devguide()
    latest = get_latest_version()

    # Store version in major.minor versioning scheme (e.g. 3.11)
    if latest:
        major_version = re.match(r'3.[\d]+', latest).group()
        versions.insert(0, major_version)

    with open(versions_file, 'w') as f:
        f.write(f"{versions}\n")

    print('Contents stored:\n', "\n ".join(map(str, versions)))


def main():
    RUNNABLE_SCRIPTS = ('update_versions_file')

    parser = ArgumentParser()
    parser.add_argument('cmd', choices=RUNNABLE_SCRIPTS)
    options = parser.parse_args()

    script_path = Path(__file__)
    rootdir = script_path.parent.parent.absolute()
    versions_file = str(rootdir) + '/.github/versions.txt'

    eval(options.cmd)(versions_file)


if __name__ == '__main__':
    main()
