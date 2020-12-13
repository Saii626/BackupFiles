#!/usr/bin/env python3

import argparse, logging, importlib, sys
from pathlib import Path
from Globals import PROJECT_DIR

class SubCommand:

	# To be overriden by the subclass
	subparser_args = ()
	arguments = {}

	# Not to be overriden by the subclasse
	log = logging.getLogger('backup.subcommand')
	loaded_modules = False
	command_map = {}

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
			if isinstance(name_or_flag, str):
				parser.add_argument(name_or_flag, **other_args)
			elif isinstance(name_or_flag, list):
				parser.add_argument(*name_or_flag, **other_args)

	@staticmethod
	def get_all_subcommands():
		"""
		Returns a list of SubCommand class's subclasses
		"""
		if not SubCommand.loaded_modules:
			subcommands_folder = PROJECT_DIR.joinpath('SubCommands')
			sys.path.append(subcommands_folder)
		
			for path in subcommands_folder.iterdir():
				p = str(path.name)
				if p.endswith(".py") and not p.startswith('__'):
					module = str(path.name)[:-3]
					SubCommand.log.debug(f'Importing {module} module')
					importlib.import_module(f'SubCommands.{module}')
			SubCommand.loaded_modules = True
		
		subcommands = SubCommand.__subclasses__()

		for cmd in subcommands:
			name = cmd.subparser_args[0]
			SubCommand.command_map[name] = cmd

			aliases = cmd.subparser_args[1].get('aliases')
			if aliases:
				for a in aliases:
					SubCommand.command_map[a] = cmd
		return subcommands

	@staticmethod
	def get_command(name: str):
		"""
		Returns the SubCammand class of the particular name
		"""
		#for cmd_cls in SubCommand.get_all_subcommands():
		#	if cmd_cls.subparser_args[0].lower() == name.lower():
		#		return cmd_cls
		return SubCommand.command_map[name]

