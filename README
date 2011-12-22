About
=====

A game book is made of multiple numbered paragraphs, set out in a random
order across multiple pages. At most paragraphs, the reader is able to make
some sort of choice as to how the story progresses.

<http://en.wikipedia.org/wiki/Gamebook>

Usage
=====

To make books with this script, you will need to use some rather ugly looking
syntax. At the beginning of a book, you need some header information. This looks
like:
    <data
    *author Colin `tex' Dingle
    *title Amazingly titled book>

Each paragraph looks like this:
    <meetcat
    You walk into the room. You notice a faint glow emitting from a rainbow
    stretching towards a small creature you cannot distinctly see. As you look
    at the creature, you realise to noise you have been hearing consistently for
    the last five hours is coming from this tiny creature. `Nyan nyan nyan...'
    *option approach the creature [seenyan]
    *option run away very fast [diehorribly]>

The `<` and `>` mark the start and end of the paragraph.

`meetcat` is the unique name for this paragraph. This is the name used to
refer to the paragraph from elsewhere in the book.

The text in the middle of the paragraph is what is read by the reader. Remember
this is going to be placed directly in a LaTeX document, so you can use LaTeX
commands pretty much anywhere it seems reasonable, unless my strange parsing
code fails a bit.

The `*` denotes some sort of command. In this case, the command is `option`,
which gives the reader the option to choose between different paths. The bit
in square brackets is the name of the paragraph to go to if the reader chooses
this option. The text in between is the text you give to the reader to describe
the choice.

The available options are:

   `option -- give the reader the option to do something
    goto -- make the reader jump to a paragraph
    enemy -- add an aggressive enemy to the paragraph. Looks like
        *enemy enemy name [skl 99 sta 99] win [winning paragraph] lose [loosing paragraph]`

Licence
=======

This software is released under the GPLv3. See COPYING for more details