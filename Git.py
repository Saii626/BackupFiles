#!/usr/bin/env python3

import subprocess, logging
from datetime import datetime
from enum import Enum

class GitStatus(Enum):
	UNTRACKED = 0
	UNSTAGED = 1
	UNCOMMITED = 2
	UNSYNCED = 3
	SYNCED = 4

	def __repr__(self):
		if self == UNTRACKED:
			return 'Untracked'
		elif self == UNSTAGED:
			return 'Unstaged'
		elif self == UNCOMMITED:
			return 'Uncommited'
		elif self == UNSYNCED:
			return 'Unsynced'
		elif self == SYNCED:
			return 'Synced'

class Git:
	"""
	Helper class to interact with git
	"""
	def __init__(self):
		self.log = logging.getLogger('backup.git')

	def __run_git(self, args):
		p = subprocess.run(['git', *args], capture_output=True)
		self.log.debug(f'returncode: {p.returncode}')
		if p.returncode != 0:
			self.log.error(f'Git error:\n{p.stdout.decode("utf-8")}')
			exit(1)
		return p.stdout.decode('utf-8')

	def status(self):
		self.log.debug('git status')
		git_status = self.__run_git(['status'])

		if 'Untracked files' in git_status:
			return GitStatus.UNTRACKED
		elif 'Changes not staged for commit' in git_status:
			return GitStatus.UNSTAGED
		elif 'Changes to be committed' in git_status:
			return GitStatus.UNCOMMITED
		elif 'Your branch is ahead' in git_status:
			return GitStatus.UNSYNCED
		elif 'up to date' in git_status:
			return GitStatus.SYNCED

	def add(self):
		self.log.debug('git add')
		return self.__run_git(['add', '-A'])
	
	def commit(self):
		self.log.debug('git commit')
		return self.__run_git(['commit', '-m', 'Autocommit at %s'%(datetime.now().replace(microsecond=0).isoformat())])
	
	def push(self):
		self.log.debug('git push')
		return self.__run_git(['push', 'origin', 'master'])
	
