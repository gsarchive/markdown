# Some small conveniences for turning text into Markdown
import sys
import re
import os.path

files = { }

def process(fn):
	with open(fn) as f: data = f.readlines()
	dlg = fn.endswith("d.md") # Dialogue is formatted slightly differently
	song = int("".join(c for c in fn if c in "0123456789") or "0") # Extract 7 from "hex07.md"
	changes = 0
	title = "???"
	firstline = "need-heading"
	last_person = {}
	for i, line in enumerate(data):
		# Quick check for trailing whitespace. Note that this doesn't (on its own) flag the file
		# for save-back, but it'll be carried through if there are any other changes made.
		if line.endswith(" \n"):
			line = data[i] = line.rstrip() + "\n"
		# Okay. Now for the real work.
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
		elif m := re.match(r"^([A-Z 0-9,]+(?: and )?[A-Z 0-9,]*\.)(.*)$", line, re.M):
			# eg "PERSON. Lorem ipsum dolor sit amet!"
			person, firstline = m.groups()
			if len(person) == 2: # Abbreviated form eg "A." - expands to most recent name starting with that letter
				person = last_person[person[0]]
			else:
				last_person[person[0]] = person
			if dlg: data[i] = "\n**" + person + "** " + firstline.strip() + "\n"
			else: data[i] = "#### " + person + "\n" + firstline.strip() + "\n"
			changes += 1
		elif m := re.match(r"^([A-Z 0-9,]+(?: and )?[A-Z 0-9,]*) (\([^)]+\.?\)\.?)(.*)$", line, re.M):
			# eg "PERSON (softly). Lorem ipsum dolor sit amet?"
			person, style, firstline = m.groups()
			if len(person) == 1: # Abbreviated form as above eg "A (aside)."
				person = last_person[person[0]].rstrip(".")
			else:
				last_person[person[0]] = person + "."
			if dlg: data[i] = "\n**" + person + "** *" + style + "* " + firstline.strip() + "\n"
			else: data[i] = "#### " + person + " *" + style + "*\n" + firstline.strip() + "\n"
			changes += 1
		elif m := re.match(r"^([A-Z 0-9,]+):_(.*)$", line, re.M):
			# eg "QUEEN:_He is the Executioner"
			data[i] = "#### " + m.group(1) + "\n" + m.group(2) + "\n"
			changes += 1
		elif line.startswith("*") and line.endswith("*\n") and i and data[i-1] != "\n":
			# Stage directions need to be separated off into their own paragraphs.
			data[i] = "\n" + data[i]
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
			if modified != data[i]:
				data[i] = modified
				changes += 1
				pass
		if firstline == "need-heading" and data[i].startswith("#### "): firstline = "grab"
		elif firstline == "grab" and data[i].strip() != "" and data[i].strip() != "&nbsp;" and not data[i].startswith("#"): firstline = data[i].strip()
		if fn.endswith("index.md") and (m := re.match(r"\* \[[^]]+\]\(([^)]+)\)", line)):
			# We have a link to a file, so we won't need to add more
			try: del files[m.group(1)]
			except KeyError: pass
	if song:
		# Ensure that we have a link to this file in the index (if we're processing the index)
		html = os.path.basename(fn).replace(".md", ".html")
		title = (title.title()
			.replace(" And ", " and ").replace(" A ", " a ").replace(" The ", " the ")
			.replace("—", "-").replace(".", "")
		)
		firstline = firstline.rstrip(",.:!— ") # No need for trailing punctuation
		if dlg: line = "* [Dialogue](" + html + ")\n"
		elif firstline == "need-heading": # No heading, so just use the first line
			line = "* [No. %d](%s) - \"%s\"\n" % (song, html, title)
		else: line = "* [No. %d](%s) - %s - \"%s\"\n" % (song, html, title, firstline)
		files[html] = line
	if fn.endswith("index.md") and files:
		# There are some files that aren't linked. Dump links in, at the bottom of the page;
		# they can be adjusted and/or moved manually.
		data.extend(v for k,v in sorted(files.items())) # Sort by file name (the dictionary key), use the value
		changes += len(files)
	if changes:
		print("Changed %d lines in %s" % (changes, fn))
		with open(fn, "w") as f: f.write("".join(data))

for fn in sys.argv[1:]:
	process(fn)
