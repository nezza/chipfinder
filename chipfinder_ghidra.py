# Attempt to identify Cortex-M processor family
#@author Thomas Roth
#@category leveldown security
#@menupath
#@toolbar

import chipfinder
import os

from ghidra.program.model.symbol.SourceType import *

rm = currentProgram.getReferenceManager()
cm = currentProgram.getCodeManager()

a = currentProgram.getMinAddress()
memory = currentProgram.getMemory()

addresses = []
while True:
	i = cm.getInstructionAfter(a)
	if not i:
		break
	a = i.getAddress()

	references = rm.getReferencesFrom(a)

	for r in references:
		if r.isStackReference():
			continue

		if memory.contains(r.getToAddress()):
			continue

		ad = int(str(r.getToAddress()), 16)
		if ad in addresses:
			continue
		addresses.append(ad)

sig_path = os.path.join(chipfinder.PATH, "signatures")
cf = chipfinder.Chipfinder(sig_path, print_status=True)
hits = cf.process(addresses)
print("** Found following potential hits **")
chipfinder.tabulate(hits[:20])