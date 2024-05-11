#!/usr/bin/env python3
"""Prints the list of languages in a repository."""

import os

from argparse import ArgumentParser
from json import dumps
from pathlib import Path


def list_dirs(root):
    """Get the list of not empty and not hidden directories in the repository in *root*"""
    return sorted(
        [
            el.name
            for el in root.iterdir()
            if any(el.glob("**/*.po")) and not el.name.startswith(".")
        ]
    )


def filter_ignored_entries(dirs: list, ignored_entries: list) -> list:
    """Filter out the ignored entries, to return the valid languages codes"""
    filtered_dirs = [dir_name for dir_name in dirs if dir_name not in ignored_entries]
    return filtered_dirs


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=os.getcwd(), required=False)
    args = parser.parse_args()

    root = Path(args.root)
    ignored_entries = ["pot"]

    dirs = list_dirs(root)
    languages = filter_ignored_entries(dirs, ignored_entries)

    print(dumps(languages))
