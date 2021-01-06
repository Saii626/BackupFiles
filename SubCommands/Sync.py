#!/usr/bin/env python3

import sys
from pathlib import Path
from colorama import Fore, init
from SubCommand import SubCommand
from Git import Git, GitStatus
from Globals import *

init(autoreset=True)

class Sync(SubCommand):
	"""
	Syncs the repo
	"""

	subparser_args = ('sync', {'help': 'Sync the backup folder. If no option is provided, does all the steps', 'aliases': ['sy']})
	arguments = {'--add': {'help': 'Stages all uncommited changes and untracked files', 'nargs': '?', 'const': True}, '--commit': 
		{'help': 'Commits all changes', 'nargs': '?', 'const': True}, '--msg':
		{'help': 'Used only with commit. If ommited, a system generated commit msg is used'}, '--push':
		{'help': 'Pushes all commits', 'nargs': '?', 'const': True}}
	
	def execute(self, args):
		self.log.info(args)
		add = True if args.add else False
		commit = True if args.commit else False
		push = True if args.push else False
		msg = args.msg

		if (not add) and (not commit) and (not push):
			add = True
			commit = True
			push = True

		git = Git()

		if add and git.project_status() in [GitStatus.UNTRACKED, GitStatus.UNSTAGED]:
			print("git add")
			self.safe_call(lambda: git.add(stdout=sys.stdout, stderr=sys.stderr), 'Git add failed')

		if commit and git.project_status() is GitStatus.UNCOMMITED:
			print("git commit")
			self.safe_call(lambda: git.commit(msg=msg, stdout=sys.stdout, stderr=sys.stderr), 'Git commit failed')

		if push and git.project_status() is GitStatus.UNSYNCED:
			print("git push")
			self.safe_call(lambda: git.push(stdout=sys.stdout, stderr=sys.stderr), 'Git push failed')
			notify(Urgency.LOW, 'Backup sync', 'Complete')

	def safe_call(self, fn, error: str):
		p = fn()
		if p.returncode != 0:
			notify(Urgency.HIGH, 'Backup sync', error)
			exit(1)
