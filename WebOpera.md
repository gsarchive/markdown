Building a Markdown Web Opera
=============================

General notes
-------------

For the most part, generating a Web Opera from Markdown should be fairly
straight-forward. Use one of the existing collections as an example, copy,
tweak, have at it! A few points worth noting:

* The text2md.py script will help with a lot of the hack-work. See below.
* Heading level 4 triggers song-like display. In songs that don't need to
  have an indication of who's singing, "#### &nbsp;" will make that happen;
  in dialogue sections, avoid using head-4 anywhere.
* The CSS "poem" class can be used in dialogue to indicate that a section
  is preformatted. Indent every line by a few spaces and have "{:.poem}" at
  the end. In order for the formatting to look correct, it is sometimes
  necessary to start with "&nbsp;" on an indented line.
* After making any edits, run `python3 build.py` to rebuild the files. This
  assumes that the directory `../public_html` is the correct destination;
  if not, use `python3 build.py ../live` or any other destination directory.

Building with text2md.py
------------------------

`python3 text2md.py path/to/web_opera/*.md`

TODO: Explain all the things it does. Until this section is filled in, read
the source code.

