#!/usr/bin/env python
# Should be compatible with both Python 2 and Python 3, as long as
# all filenames are ASCII. It's sad to have to say that in 2022, but
# the G&S Archive doesn't seem to have Python 3 installed.
import os
import subprocess
import sys

destdir = "../public_html"
if len(sys.argv) > 1:
	# TODO: better arg parsing plsthx
	if os.path.exists(sys.argv[1]): destdir = sys.argv[1]
	else: print("Unknown argument") # yeah like I said

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
