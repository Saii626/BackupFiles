#!/usr/bin/env python3

import argparse, logging, importlib, sys
from pathlib import Path

class SubCommand:

	subparser_args = ()
	arguments = {}
	log = logging.getLogger('backup.subcommand')
	loaded_modules = False

	def __init__(self):
		self.log = logging.getLogger(f'backup.subcommand.{self.__class__.subparser_args[0]}')

	def execute(self, args):
		"""
		Run the subcommand with any extra arguments provided at commandline
		"""
		pass

	@classmethod
	def add_arg_parser(cls, subparsers):
		"""
		Add argparser to the subparsers for argument parsing
		"""
		parser = subparsers.add_parser(cls.subparser_args[0], **(cls.subparser_args[1]))
		for (name_or_flag, other_args) in cls.arguments.items():
			parser.add_argument(name_or_flag, **other_args)

	@staticmethod
	def set_attributes(attributes):
		"""
		Few values in attributes:
			backup_folder: Path
			project_folder: Path
			working_folder: Path
		"""
		SubCommand.log.debug(f'Subcommand env: {attributes}')
		for (k, v) in attributes.items():
			setattr(SubCommand, k, v)

	
	@staticmethod
	def get_all_subcommands(attributes):
		"""
		Returns a list of SubCommand class's subclasses
		"""
		if not SubCommand.loaded_modules:
			SubCommand.set_attributes(attributes)

			subcommands_folder = Path(SubCommand.project_folder).joinpath('SubCommands')
			sys.path.append(subcommands_folder)
		
			for path in subcommands_folder.iterdir():
				p = str(path.name)
				if p.endswith(".py") and not p.startswith('__'):
					module = str(path.name)[:-3]
					SubCommand.log.debug(f'Importing {module} module')
					importlib.import_module(f'SubCommands.{module}')
			SubCommand.loaded_modules = True
		return SubCommand.__subclasses__()

	@staticmethod
	def get_command(name: str):
		"""
		Returns the SubCammand class of the particular name
		"""
		for cmd_cls in SubCommand.get_all_subcommands(None):
			if cmd_cls.subparser_args[0].lower() == name.lower():
				return cmd_cls
		return None

