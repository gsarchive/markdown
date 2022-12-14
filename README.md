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

To push out a live version using an SSHFS mount:

    $ sshfs gsarchive:public_html ../live
    $ python build.py ../live

To make the site available on the LAN, add your local IP: `-H 192.168.0.123`

Where necessary, the target file name and breadcrumb trail can be customized:

    ---
    target: index.htm
    parent: web_op/index.md
    ---

Otherwise target will be the same path as the .md file but with .html. Use only
where necessary to maintain backward compatibility. TODO: See about creating
redirects and having the canonical name able to move to the default.

Automatic breadcrumbing and TOC generation can be done on the basis of the
front-matter titles, and optionally explicit parentage (otherwise dirname is
used as a logical default).

TODO: Figure out the discrepancies between str|slugify and what goes into a
heading's ID. "Tennyson & Gilbert" got a double hyphen in the ID but not in
the TOC, which uses |slugify to try to achieve the same result.

TODO: Autogenerate breadcrumbs from paths. This will require a preparse step
as per TOC generation. Take the title from the front matter YAML and store it;
for this purpose, it may be most convenient to have the root page stored in
`dirname/index.md` with a target of `dirname/html/index.html`, rather than
having a weird sideways step into the html directory. Possible bonus: having
redirects from eg `princess_ida/` to `princess_ida/html/index.html` may be of
value for anyone who trims the URL.
