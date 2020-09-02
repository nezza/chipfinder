# Generate signatures for chipfinder.
# Thomas Roth thomas.roth@leveldown.de

# More information:
# https://leveldown.de/blog/svd-loader/
# License: GPLv3

from cmsis_svd.parser import SVDParser
import argparse
import sys
import os
import csv

parser = argparse.ArgumentParser(description="Generate a chipfinder signature from an SVD file.")
parser.add_argument("svd_file", help="SVD file to load")
parser.add_argument("signature_file", help="Signature file to write")
args = parser.parse_args()

print(args)
print("Loading SVD file...")
parser = SVDParser.for_xml_file(str(args.svd_file))
print("\tDone!")

peripherals = parser.get_device().peripherals

rows = 0
print("Writing signature file...")
with open(args.signature_file, "w") as csvfile:
	w = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for peripheral in peripherals:
		try:
			for register in peripheral.registers:
				w.writerow([peripheral.base_address + register.address_offset])
				rows += 1
		except:
			continue

print(f"\tDone, wrote {rows} rows.")
