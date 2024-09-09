# Some small conveniences for turning text into Markdown
import sys
import re

def process(fn):
	with open(fn) as f: data = f.readlines()
	dlg = fn.endswith("d.md") # Dialogue is formatted slightly differently
	changes = 0
	for i, line in enumerate(data):
		if m := re.match(r"^([A-Z 0-9]+\.)(.*)$", line, re.M):
			# eg "PERSON. Lorem ipsum dolor sit amet!"
			person, firstline = m.groups()
			if dlg: data[i] = "\n**" + person + "** " + firstline.strip() + "\n"
			else: data[i] = "#### " + person + "\n" + firstline.strip() + "\n"
			changes += 1
		if dlg and (m := re.match(r"^([A-Z 0-9]+) (\(.*\.?\)\.?)(.*)$", line, re.M)):
			print(m.groups())
			# eg "PERSON (softly). Lorem ipsum dolor sit amet?"
			person, style, firstline = m.groups()
			data[i] = "\n**" + person + "** *" + style + "* " + firstline.strip() + "\n"
			changes += 1
	if changes:
		print("Changed %d lines in %s" % (changes, fn))
		with open(fn, "w") as f: f.write("".join(data))

for fn in sys.argv[1:]:
	process(fn)
