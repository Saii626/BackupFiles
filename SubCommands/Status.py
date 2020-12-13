#!/usr/bin/env python3

import sys
from colorama import Fore, init
from SubCommand import SubCommand
from ConfigFile import ConfigFile
from Git import Git

init(autoreset=True)

class Status(SubCommand):
	"""
	Gets the status of backup
	"""

	subparser_args = ('status', {'help': 'Gets status of backup', 'aliases': ['st']})
	arguments = {}
	
	def execute(self, args):
		self.log.info(args)

		config_file = ConfigFile()

		print('Tracked paths:')
		for loc in config_file:
			print(f'{Fore.CYAN}{loc.orig_path} {Fore.RED}-> {Fore.BLUE} {loc.back_path}')

		print('\n')
		git = Git()
		git.status(stdout=sys.stdout, stderr=sys.stderr)

