#!/usr/bin/env python
# Should be compatible with both Python 2 and Python 3, as long as
# all filenames are ASCII. It's sad to have to say that in 2022, but
# the G&S Archive doesn't seem to have Python 3 installed.
import os
import subprocess

# Call on Ruby to do most of the build work
subprocess.call(["jekyll", "build"])

# Move files from _site to ../public_html
# TODO: Copy instead, but only files that were changed by Jekyll.
# Would require checking the file timestamps, but would avoid the
# hassle of touching every file managed by Jekyll, and also the
# window of file removal when copying files that haven't changed.

for root, dirs, files in os.walk("_site"):
	origin = root
	if root.startswith("_site"): root = root[5:] # Older Pythons don't have removeprefix
	dest = "../public_html" + root#.removeprefix("_site")
	try: os.mkdir(dest)
	except OSError: pass # TODO: Only ignore "file exists"
	print(root)
	for file in files:
		os.rename(origin + "/" + file, dest + "/" + file)
