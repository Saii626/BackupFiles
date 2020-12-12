#!/usr/bin/env python3

from pathlib import Path
from SubCommand import SubCommand
from ConfigFile import ConfigFile
from BackupLocation import BackupLocation

class Add(SubCommand):

	subparser_args = ('add', {'help': 'add a path to backup list'})
	arguments = {'src': {'help': 'src path to backup'}}
	
	def execute(self, args):
		"""
		Add a path to backup. If it is a file, create a hardlink to it in git repository.
		If its a folder, copy contents to git repo and add a symlink to it.
		"""
		self.log.info(args)
		src = Path(args.src).resolve()

		config_file = ConfigFile()
		parent = config_file.get_parent(src)
		if not parent:
			self.log.debug('New path to be backed up')

			dest = Path(SubCommand.backup_folder).joinpath(src.name)
			backup_loc = BackupLocation(src, dest)
			backup_loc.backup()

			config_file.add_location(backup_loc)
			config_file.write_file()
		else:
			log.info(f'Path {src} is already backed up under {parent}')


