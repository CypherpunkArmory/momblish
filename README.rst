========
momblish
========

Momblish is a small library and CLI for generating fake-but-pronounceable
words from a source corpus.

http://mentalfloss.com/article/69880/7-fake-words-ended-dictionary

It is named after a "fake" word put into the OED on accident.


Momblish uses trigram analysis to generate (mostly) pronounceable gibberish, so
it can be used for any language that can be n-gram analyzed.

Description
===========

To use momblish, import it.

.. code:: python

    from momblish import Momblish

    m = Momblish.english()

The built-in English loader analyzes the system dictionary once and caches the
result in the XDG cache directory.

.. code:: python

    from momblish import Momblish
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
    m.word(7, prefix='dabc')     #= > 'DABCADC'
    w = m.sentence()             #= > <generator object Momblish.sentence at 0x10513dc78>
    next(w)                      #= > 'TICK'
    next(w)                      #= > 'DRIXY'
    next(w)                      #= > 'UNREA'
    m.sentence(3, word_length=5) #= > ['LEDGE', 'DEAKA', 'HONGI']

You can also analyze your own corpus file.

.. code:: python

    custom = Momblish.from_file('/tmp/words.txt')
    custom.word(8, prefix='tr')

There is also a command line interface for quick generation without writing code.

.. code:: console

    $ momble 6
    $ momble 7 dabc
    $ momble --rebuild-cache 7 dabc
    $ momble --corpus /tmp/words.txt 7 dabc

The CLI uses the cached analyzed corpus when available. Pass
`--rebuild-cache` to force re-analysis of either the default English corpus or
the file supplied with `--corpus`.
