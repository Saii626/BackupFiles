#!/usr/bin/env python3

import os, sys, shutil

if (len(sys.argv) != 2):
    print('Usage: safe_delete <file|folder>')
    exit(1)

file = sys.argv[1]
if not os.path.isabs(file):
    file = os.path.abspath(file)

trash_folder = os.path.expanduser('~/.local/trash')
parent_folder = os.path.dirname(file)

if parent_folder == trash_folder:
    if os.path.isfile(file):
        os.remove(file)
    else:
        shutil.rmtree(file)
    print(f'Deleted {file}')
else:
    shutil.move(file, trash_folder)
    print(f'Moved {file} to {trash_folder}')


