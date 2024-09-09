# Some small conveniences for turning text into Markdown
import sys
import re

def process(fn):
	with open(fn) as f: data = f.readlines()
	dlg = fn.endswith("d.md") # Dialogue is formatted slightly differently
	song = int("".join(c for c in fn if c in "0123456789") or "0") # Extract 7 from "hex07.md"
	changes = 0
	for i, line in enumerate(data):
		if line.startswith("breadcrumb: No. "):
			correct = "breadcrumb: No. " + str(song) + "\n"
			if line != correct:
				data[i] = correct
				changes += 1
		elif m := re.match(r"^## No. ([0-9]+): (.*)$", line, re.M):
			num, title = m.groups()
			if int(num) != song:
				data[i] = "## No. %d: %s\n" % (song, title)
				changes += 1
		elif m := re.match(r"^## Dialogue following No. ([0-9]+)", line, re.M):
			num, = m.groups()
			if int(num) != song:
				data[i] = "## Dialogue following No. %d\n" % song
				changes += 1
		elif m := re.search(r"([0-9]+)\.(kar|mid)", line, re.I): # unanchored - find anything that looks like a filename
			num, ext = m.groups()
			if int(num) != song:
				data[i] = "%s%02d.%s%s" % (line[:m.start()], song, ext, line[m.end():])
				changes += 1
		elif m := re.match(r"^([A-Z 0-9]+\.)(.*)$", line, re.M):
			# eg "PERSON. Lorem ipsum dolor sit amet!"
			person, firstline = m.groups()
			if dlg: data[i] = "\n**" + person + "** " + firstline.strip() + "\n"
			else: data[i] = "#### " + person + "\n" + firstline.strip() + "\n"
			changes += 1
		elif dlg and (m := re.match(r"^([A-Z 0-9]+) (\([^)]+\.?\)\.?)(.*)$", line, re.M)):
			# eg "PERSON (softly). Lorem ipsum dolor sit amet?"
			person, style, firstline = m.groups()
			data[i] = "\n**" + person + "** *" + style + "* " + firstline.strip() + "\n"
			changes += 1
		# Check for any parenthesized sections. These might be actual spoken parentheses, or
		# they might be stage directions. Since stage directions are more common, and it's
		# easier to spot italicized text than to notice what ought to be italicized, we make
		# EVERY parenthesis emphasized. That said, though, this only makes sense the first
		# time we check this; so we only do this check if there are other changes already
		# being made. That way, if you delete the asterisks manually, they won't come back
		# unless you disrupt it in some way (easiest is to damage the song number somewhere).
		if changes:
			# Note that we use data[i] rather than line, in case this line has itself been changed already
			modified = re.sub(r"(?<![]a-z*[])(\([^)]+\.?\)\.?)(?!\*)", "*\\1*", data[i])
			if modified != line:
				data[i] = modified
				changes += 1
				pass
	if changes:
		print("Changed %d lines in %s" % (changes, fn))
		with open(fn, "w") as f: f.write("".join(data))

for fn in sys.argv[1:]:
	process(fn)
