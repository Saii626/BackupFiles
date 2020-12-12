#!/usr/bin/env python3

import logging, argparse, os, subprocess, sys
from pathlib import Path
from colorama import Fore, init
from SubCommand import SubCommand
from ConfigFile import ConfigFile

#logging.basicConfig(filename='backup.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger('backup')

init(autoreset=True)

def notify(urgency, title, body):
	"""
	Helper function to easily call notify-send
	"""
	if not hasattr(notify, 'env'):
		# Use DBUS_SESSION_BUS_ADDRESS so that we can show notification even if run
		# from SHELL which don't have the env variable (eg: cronjob)
		if 'DBUS_SESSION_BUS_ADDRESS' not in os.environ:
			dbus_file = os.path.join(Path.home(), '.dbus/Xdbus') 
			with open(dbus_file) as f:
				file_contents = f.readline()

			parts = file_contents.split('=', maxsplit=1)

			notify.env = {**os.environ, parts[0].strip(): parts[1].strip()}
		else:
			notify.env = os.environ


	subprocess.run(['notify-send', '--app-name=app.saikat.SyncConfigurations',
		'--urgency=%s'%urgency, title, body], check=True, env=notify.env)

def status():
	config_file = ConfigFile()

	log.info('Tracked paths:')
	for loc in config_file:
		log.info(f'{loc.src} {Fore.RED}-> {Fore.CYAN} {os.path.join(BACKUP_FOLDER, os.path.basename)}')
	log.info(f'\nGit Status: {GIT.status()}')

def backup(git):
	status = git.status()
	was_unsynced = False

	if status == GitStatus.UNTRACKED or status == GitStatus.UNSTAGED:
		was_unsynced = True
		git.add()
		status = git.status()

	if status == GitStatus.UNCOMMITED:
		was_unsynced = True
		git.commit()
		status = git.status()

	if status == GitStatus.UNSYNCED:
		was_unsynced = True
		git.push()
		status = git.status()

	if status == GitStatus.SYNCED and was_unsynced:
		notify('normal', 'Synced changes', 'Local config changes synced with Github')

if __name__ == '__main__':
	# Setup environment
	project_folder = Path(__file__).resolve().parent
	backup_folder = Path(project_folder).joinpath('backup/')
	working_folder = Path.cwd()

	env = {'backup_folder': backup_folder, 'working_folder': working_folder, 'project_folder': project_folder}
	ConfigFile.config_file = Path(project_folder).joinpath('synced_paths.json')

	if not backup_folder.exists():
		log.info('backup folder doesnot exists. Creating one')
		backup_folder.mkdir()

	# Create arg parser from subcommands, parse the arguments, instantiate appropriate subcommand and execute it
	parser = argparse.ArgumentParser(prog=os.path.basename(__file__))
	subparsers = parser.add_subparsers(help='additional help', required=True, dest='subparser')

	subcommands = SubCommand.get_all_subcommands(env)
	for command_cls in subcommands:
		command_cls.add_arg_parser(subparsers)

	args = parser.parse_args()
	selected_cmd = SubCommand.get_command(args.subparser)

	cmd = selected_cmd().execute(args)
