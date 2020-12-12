#!/usr/bin/env python3

import json, logging
from BackupLocation import BackupLocation
from typing import List
from pathlib import Path

class ConfigFile:
	config_file = ''

	"""
	Represents the config file. Has helper method to iterate over all BackupLocations
	"""
	def __init__(self):
		self.log = logging.getLogger('backup.configFile')
		if not ConfigFile.config_file.exists():
			self.log.info('Config file doesnot exists. Creating one')
			ConfigFile.config_file.touch(mode=0o644)

		try:
			with ConfigFile.config_file.open() as file:
				raw_json = json.load(file)

			self.locations = []
			for item in raw_json:
				self.locations.append(BackupLocation.from_json(item))
		except:
			self.log.error('Unable to read config config_file')
			self.locations = []

	def __iter__(self):
		self.n = 0
		return self

	def __next__(self):
		if self.n < len(self.locations):
			loc = self.locations[self.n]
			self.n += 1
			return loc
		else:
			raise StopIteration

	def add_location(self, location: BackupLocation):
		self.locations.append(location)

	def get_parent(self, location: Path):
		self.log.debug(f'{location} {self.locations}')
		for loc in self.locations:
			if str(location).startswith(str(loc.back_path)):
				self.log.debug(f'Found match {loc}')
				return loc.dest
		return None

	def write_file(self):
		with ConfigFile.config_file.open('w') as file:
			locations_array = []

			for loc in self.locations:
				locations_array.append(loc.to_json())
			json.dump(locations_array, file, indent=4)


