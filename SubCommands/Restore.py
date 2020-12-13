#!/usr/bin/env python3

from pathlib import Path
from SubCommand import SubCommand
from ConfigFile import ConfigFile

class Restore(SubCommand):
	"""
	Restores a path from backup.
	"""

	subparser_args = ('restore', {'help': 'Restores a path from backup location', 'aliases': ['rs']})
	arguments = { 'src': {'help': 'Location to restore. If not specified, all locations are restored', 'default': None, 'nargs': '?'}}
	
	def execute(self, args):

		self.log.info(args)
		src = Path(args.src).resolve() if args.src else None
		self.log.debug(f'Will try to restore {src}')

		config_file = ConfigFile()
		if not src:
			self.log.info('Restoring all locations')
			for loc in config_file:
				self.log.debug(f'Restoring {loc} location')
				loc.restore()
		else:
			for loc in config_file:
				if str(loc.orig_path) == str(src):
					self.log.info(f'Restoring {loc} location')
					loc.restore()
					return
			self.log.error(f'{src} if not being backed up')
