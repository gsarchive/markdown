#!/usr/bin/env python
# Should be compatible with both Python 2 and Python 3, as long as
# all filenames are ASCII. It's sad to have to say that in 2022, but
# the G&S Archive doesn't seem to have Python 3 installed.
import json
import os
import subprocess
import sys
import yaml # ImportError? pip install pyyaml

destdir = "../public_html"
if len(sys.argv) > 1:
	# TODO: better arg parsing plsthx
	if os.path.exists(sys.argv[1]): destdir = sys.argv[1]
	else: print("Unknown argument") # yeah like I said

# Build a JSON file of all H2s in all Markdown files
try: os.mkdir("_data")
except OSError: pass # TODO as below, only ignore "exists"

toc, links, trail, crumbs = { }, { }, { }, { }
for root, dirs, files in os.walk("."):
	# Don't recurse into any underscore or dot prefixed directories
	dirs[:] = [d for d in dirs if d == d.lstrip("_.")]
	if "index.md" in files:
		# Always process index first (and files are done before dirs, so that's safe)
		files.remove("index.md")
		files.insert(0, "index.md")
	for file in files:
		if not file.endswith(".md"): continue
		with open(root + "/" + file) as f: data = f.read()
		name = (root + "/" + file)[2:] # Slice off "./" at the start of the file
		toc[name] = [chunk.split("\n", 1)[0] for chunk in ("\n" + data).split("\n## ")[1:]]
		path = name.replace("html/", "")
		front = { }
		try: front = next(yaml.safe_load_all(data))
		except (StopIteration, yaml.scanner.ScannerError): pass # No front matter? Use empty front matter.
		if path.endswith("index.md"): path = os.path.dirname(path)
		# When looking at a directory page, save its title.
		if "title" in front:
			# Try to recreate the HTML file name pattern Jekyll uses
			# Worst case, if this gets it wrong, just add an explicit
			# "target: whatever.html" in the Markdown frontmatter.
			destname = front.get("target") or os.path.basename(name).replace(".md", ".html")
			dest = os.path.normpath(name + "/../" + destname)
			links[path] = "[%s](/%s)" % (front["title"], dest)
		# For all pages, look for a parent and copy in the breadcrumbs and title
		parent = os.path.normpath(path + "/../" + front.get("parent", "."))
		trail[path] = trail.get(parent, [])
		par = links.get(parent)
		if par: trail[path] = trail[path] + [par]
		crumbs[name] = trail[path]
with open("_data/toc.json", "w") as f:
	json.dump(toc, f)
with open("_data/breadcrumbs.json", "w") as f:
	json.dump(crumbs, f)

# Call on Ruby to do most of the build work
subprocess.call(["jekyll", "build"])

# Move files from _site to ../public_html

for root, dirs, files in os.walk("_site"):
	origin = root
	if root.startswith("_site"): root = root[5:] # Older Pythons don't have removeprefix
	dest = destdir + root#.removeprefix("_site")
	try: os.mkdir(dest)
	except OSError: pass # TODO: Only ignore "file exists"
	print(root)
	for file in files:
		# See if the file has a marker sending it elsewhere
		destname = file
		with open(origin + "/" + file) as f: data = f.read()
		for line in data.split("\n", 5)[:5]: # Scan the first five lines, max, for a "target" marker
			_, target, fn = line.partition("MD TARGET:")
			if target:
				# This should really be removesuffix, but again, older Pythons.
				# (Note that it would have to remove "*/" too, for CSS files)
				destname = fn.rsplit("-->", 1)[0].strip()
				break
		# If possible, try to move the file. Way quicker, and atomic,
		# but needs the staging area and destination to be on the same
		# file system - NOT one of them being an SSHFS mount.
		try:
			os.rename(origin + "/" + file, dest + "/" + destname)
			continue
		except OSError: pass
		# TODO: Stat the files to see if they've changed, rather than
		# relying on a (slow) content comparison
		try:
			with open(dest + "/" + destname) as f:
				if data == f.read(): continue # Not changed, don't overwrite
		except IOError as e: # FileNotFoundError
			if e.errno != 2: raise
		with open(dest + "/" + destname, "w") as f:
			f.write(data)
