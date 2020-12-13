#!/usr/bin/env python3

from pathlib import Path
from SubCommand import SubCommand
from ConfigFile import ConfigFile
from BackupLocation import BackupLocation

class Remove(SubCommand):
	"""
	Removes a path from being backed up anymore.
	"""

	subparser_args = ('remove', {'help': 'Removes a path from being backed up anymore', 'aliases': ['rm']})
	arguments = {'src': {'help': 'src to remove from backing up'}}
	
	def execute(self, args):
		self.log.info(args)
		src = Path(args.src).resolve()
		self.log.debug(f'Will try to remove {src}')

		config_file = ConfigFile()

		location = None
		for loc in config_file:
			if str(loc.orig_path) == str(src) or str(loc.back_path) == str(src):
				location = loc
				break

		if location:
			self.log.info(f'Will remove {location}')
			location.revert()

			config_file.remove_location(location)
			config_file.write_file()
		else:
			self.log.error(f'Path {src} is not being backed up')

