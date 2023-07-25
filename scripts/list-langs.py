#!/usr/bin/env python3
"""Prints the list of languages tracked in the repository."""

from argparse import ArgumentParser
import git
import os

def list_tracked_dirs(git_root):
    """Get the list of tracked directories in the repository in *git_root*"""
    repo = git.Repo(git_root)
    tracked_files = repo.git.ls_tree("--full-tree", "--name-only", "HEAD").splitlines()
    return tracked_files

def filter_ignored_entries(file_list: list, ignored_entries: list) -> list:
    """Filter out the ignored entries, to return the valid languages codes"""
    filtered_files = [file_name for file_name in file_list if file_name not in ignored_entries]
    return filtered_files

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--git-root', default=os.getcwd(), required=False)
    args = parser.parse_args()

    git_root = git.Repo(args.git-root, search_parent_directories=True).working_dir
    ignored_entries = ['.tx', 'pot']

    tracked_files = list_tracked_dirs(git_root)
    languages = filter_ignored_entries(tracked_files, ignored_entries)
    
    print(languages)
