========
momblish
========

Momblish is a library for generating fake words in any phoenetic.

http://mentalfloss.com/article/69880/7-fake-words-ended-dictionary

It is named after a "fake" word put into the OED on accident.


Momblish uses trigram analysis to generate (mostly) pronounacble gibberish - so
it can be used for any language that can be n-gram analyzed.

Description
===========

To use moblish, import it -

.. code:: python

    from momblish import Momblish

    m = Momblish.english()


Currently - only the english corpus is available.


Each time you load the English momblish it will perform an analysis on
`/usr/share/dict` and use that data to generate nonsense words.

To avoid this computation overhead, you can save the pre-analyzed corpus
as a file and read it in on demand.

.. code:: python

    from mombmlish import Momblish
    from momblish.corpus import Corpus

    m = Momblish.english()
    m.corpus.save('/tmp/corpus.json')

    c = Corpus.load('/tmp/corpus.json')
    n = Momblish(c)

To get Momblish to generate words for you call `word` on a Momblish instance.

`sentence` will make a generator you can feed to your program to make word lists
of varying length.

.. code:: python
    m.word()                     #= > 'PONESSAL'
    m.word(10)                   #= > 'MIDONIHYLA'
    m.word(6, prefix='d')        #= > 'D...'
    w = m.sentence()             #= > <generator object Momblish.sentence at 0x10513dc78>
    next(w)                      #= > 'TICK'
    next(w)                      #= > 'DRIXY'
    next(w)                      #= > 'UNREA'
    m.sentence(3, word_length=5) #= > ['LEDGE', 'DEAKA', 'HONGI']

There is also a command line interface for quick generation without writing code.

.. code:: console
    $ momble 6
    $ momble 7 dabc
    $ momble --rebuild-cache 7 dabc
    $ momble --corpus /tmp/words.txt 7 dabc

Note
====

This project has been set up using PyScaffold 3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
