# Markdown files for G&S Archive

Source code for files in the [Gilbert and Sullivan Archive](https://gsarchive.net/).

Files in this repository are considered authoritative. The corresponding HTML
files will be rebuilt as needed, and should not be manually edited. Any file
in the main web site directory which does NOT have a corresponding Markdown
file here is its own entity and is authoritative.

To build and test locally:

* Install Ruby
* gem install bundler
* bundle install
* bundle exec jekyll serve

It should auto-detect changes to Markdown or layout files. If you change the
configuration in _config.yml, restart Jekyll.

To make the site available on the LAN, add your local IP: `-H 192.168.0.123`

Where necessary, the target file name to be customized:

    ---
    target: index.htm
    ---

Otherwise it should be the same path as the .md file but with .html. Use only
where necessary to maintain backward compatibility. TODO: See about creating
redirects and having the canonical name able to move to the default.

TODO: Figure out the discrepancies between str|slugify and what goes into a
heading's ID. "Tennyson & Gilbert" got a double hyphen in the ID but not in
the TOC, which uses |slugify to try to achieve the same result.
