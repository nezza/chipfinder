#!/usr/bin/env python2

import os
from os import listdir
import csv
import sys
import operator
import tqdm
from tabulate import tabulate

class ChipEntry:
	def __init__(self, name, address):
		self.name = name
		self.address = int(address)

class Chip:
	def __init__(self, file):
		f = open(file, "r'")
		r = csv.reader(f, delimiter=',', quotechar='"')
		self.name = file[:-15]
		addresses = []
		for row in r:
			# print(row[1])
			addresses.append(int(row[1]))
		self.addresses = set(addresses)
		# print("Loaded %s - %d addresses" % (self.name, len(self.addresses)))

	def match(self, address):
		if address in self.addresses:
			return True
		return False

print("Loading signatures...")
dir_path = os.path.dirname(os.path.realpath(__file__))
files = listdir(os.path.join(dir_path, "signatures"))
chips = []
for f in tqdm.tqdm(files):
	if not f.endswith(".chipfinder"):
		continue

	chips.append(Chip(os.path.join(dir_path, "signatures", f)))


f = open(sys.argv[1])
hits = []
lines = f.readlines()

print("Processing...")
i = 0
for chip in tqdm.tqdm(chips):
	# print(chip.name)
	i += 1
	count = 0
	for line in lines:
		address = int(line)
		# print(address)
		if chip.match(address):
			count += 1
	hits.append([chip.name, count])
hits = sorted(hits, key=operator.itemgetter(1), reverse=True)
print("\nTop chip hits:")
print(tabulate(hits[:15]))

# print hits
