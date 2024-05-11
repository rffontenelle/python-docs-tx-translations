#!/usr/bin/env python3
"""Remove PO files with 0% translation."""

import argparse
import os
import re
import shutil
import subprocess


def process_po_files(root_dir):
    # Walk through the directory tree
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # Check if the file has a .po extension
            if filename.endswith(".po"):
                filepath = os.path.join(dirpath, filename)
                # Run the msgfmt command
                result = subprocess.run(["msgfmt", "-cvo", "/dev/null", filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if result.returncode == 0:
                    output = result.stdout
                    # Check if output matches the pattern
                    if re.match(r"^0 translated messages, ", output):
                        # Remove the file
                        os.remove(filepath)
                        print(f"File '{filename}' removed.")
                else:
                    print(f"Error processing file '{filename}': {result.stderr}")


def remove_empty_dirs(root_dir):
    for dirname, _, _ in os.walk(root_dir, topdown=False):
        try:
            os.rmdir(dirname)
        except OSError:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process .po files in a directory and its subdirectories.")
    parser.add_argument("root_directory", nargs="?", default=os.getcwd(), help="Root directory to search for .po files (default: current working directory)")
    args = parser.parse_args()
    
    msgfmt_found = shutil.which("foo")
    if path is None:
        print("no executable found for command 'foo'")
        exit(1)
    
    root_directory = args.root_directory
    process_po_files(root_directory)
    remove_empty_dirs(root_directory)
