#!/usr/bin/env python3

import logging, argparse, sys
from SubCommand import SubCommand
from pathlib import Path
from Globals import PROJECT_DIR

FORMAT = '%(asctime)-15s [%(levelname)s] %(name)s: %(message)s'
logging.basicConfig(filename=str(PROJECT_DIR.joinpath('backup.log')), encoding='utf-8', level=logging.DEBUG)
#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=FORMAT)
log = logging.getLogger('backup')


if __name__ == '__main__':
	# Create arg parser from subcommands, parse the arguments, instantiate appropriate subcommand and execute it
	parser = argparse.ArgumentParser(prog=Path(__file__).name)
	subparsers = parser.add_subparsers(help='additional help', required=True, dest='subparser')

	subcommands = SubCommand.get_all_subcommands()
	for command_cls in subcommands:
		command_cls.add_arg_parser(subparsers)

	args = parser.parse_args()
	log.info(f'Commandline args: {args}')
	selected_cmd = SubCommand.get_command(args.subparser)

	cmd = selected_cmd().execute(args)
