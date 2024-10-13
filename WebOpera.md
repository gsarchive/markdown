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

There are a lot of detailly aspects to the web opera formatting, such as
bolding the name of the person who's speaking, ensuring that MIDI files are
correctly linked, and so on. To help with these, the text2md script can be
used. It is idempotent - that is to say, running it again on the same file
will have no effect - so it should be safe to run it on an entire batch of
files repeatedly as you are working on them.

It automatically updates a number of minutiae, such as the song number in
headings and links, and ensuring that there's an entry in index.md for every
page that exists. In files that end "d.md" eg "aiw03d.md", it also transforms
dialogue sections such as this:

   PERSON. Lorem ipsum dolor sit amet!
   OTHER PERSON. What is the French for that?
   P. Lorem ipsum isn't English.
   O (huffily). Queens never make bargains.

into the correct markdown:

   **PERSON.** Lorem ipsum dolor sit amet!

   **OTHER PERSON.** What is the French for that?

   **PERSON.** Lorem ipsum isn't English.

   **OTHER PERSON** *(huffily).* Queens never make bargains.

This performed the following transformations:

* A person's name, followed by a dot, becomes bolded.
* A single-letter abbreviation is expanded to the most recent name starting with that letter.
* A name followed by a style notation will have the style italicized.

In a file that is not treated as dialogue, it instead will transform into lyrics:

   #### PERSON.
   Lorem ipsum dolor sit amet!
   #### OTHER PERSON.
   What is the French for that?
   #### PERSON.
   Lorem ipsum isn't English.
   #### OTHER PERSON *(huffily).*
   Queens never make bargains.

The H4 elements are placed appropriately by CSS, and so will visually appear on the same
line as the text following them.

For the convenience of converting karaoke lyrics into markdown, it will also recognize
underscore separators to indicate the singer:

   ALICE:_Cheshire Pussy, thanks to thee,
   for the things you've told to me.

becomes

   #### ALICE
   Cheshire Pussy, thanks to thee,
   for the things you've told to me.

In many cases, all that is required is removing all hyphens, and the rest of the file
will transcribe correctly, with just minor tweaking required.
TODO: Have a script that rips all the lyrics from a .kar file - the inverse of augment.pike
from the karaoke/ repo.
