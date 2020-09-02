#!/usr/bin/env python2

import os
from os import listdir
import csv
import sys
import operator

try:
	from tqdm import tqdm
except:
	# No status if we don't have tqdm
	def tqdm(l):
		return l

try:
	from tabulate import tabulate
except:
	def tabulate(l):
		max_entry_length = max(len(i[0]) for i in l)
		for i in l:
			print("%s%s   %d" % (i[0], ' ' * (max_entry_length - len(i[0])), i[1]))

# Workaround for __file__ not being available in the Ghidra script
PATH = os.path.dirname(__file__)


class ChipEntry:
	def __init__(self, name, address):
		self.name = name
		self.address = int(address)

class Chip:
	def __init__(self, file):
		f = open(file, "r")
		r = csv.reader(f, delimiter=',', quotechar='"')
		self.name = os.path.basename(file[:-11])
		addresses = []
		for row in r:
			addresses.append(int(row[0]))
		self.addresses = set(addresses)

	def match(self, address):
		if address in self.addresses:
			return True
		return False


class Chipfinder:
	def p(self, s):
		if self.print_status:
			print(s)

	def __init__(self, signature_directory, print_status=False):
		self.print_status = print_status
		self.chips = []
		self.p("Loading signatures...")
		files = listdir(signature_directory)
		for f in tqdm(files):
			if not f.endswith(".chipfinder"):
				continue
			self.chips.append(Chip(os.path.join(signature_directory, f)))


	def process(self, addresses):
		hits = []
		self.p("Processing...")
		for chip in tqdm(self.chips):
			count = 0
			for address in addresses:
				# address = int(address)
				if chip.match(address):
					# print(hex(address))
					count += 1
			hits.append([chip.name, count])
		hits = sorted(hits, key=operator.itemgetter(1), reverse=True)
		return hits


if __name__ == "__main__":
	dir_path = os.path.dirname(os.path.realpath(__file__))
	sig_path = os.path.join(dir_path, "signatures")
	cf = Chipfinder(sig_path, print_status=True)
	f = open(sys.argv[1])
	hits = []
	addresses = []
	for line in f.readlines():
		addresses.append(int(line))
	addresses = set(addresses)
	hits = cf.process(addresses)
	print("\nTop chip hits:")
	print(tabulate(hits[:100]))
