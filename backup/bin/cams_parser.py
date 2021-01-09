#!/usr/bin/env python3

import sys, casparser
from pathlib import Path

def parse_cams_file(file_path: Path):
	pdf = casparser.read_cas_pdf(str(file_path), "", output='json')

	print(pdf)


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("File name required")
		print(f"Usage: {sys.argv[0]} <filename>")
		sys.exit(1)

	cams_file = Path(sys.argv[1])
	if not cams_file.exists() or not cams_file.is_file():
		print("No such file found")
		sys.exit(1)
	
	parse_cams_file(cams_file)




