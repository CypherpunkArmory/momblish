#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from momblish import Momblish
from momblish.corpus_analyzer import CorpusAnalyzer
from momblish.cli import main


test_corpus = [
   'abcd',
   'abdc',
   'acbd',
   'acdb',
   'adbc',
   'adcb',
   'bacd',
   'badc',
   'bcad',
   'bcda',
   'bdac',
   'bdca',
   'cabd',
   'cadb',
   'cbad',
   'cbda',
   'cdab',
   'cdba',
   'dabc',
   'dacb',
   'dbac',
   'dbca',
   'dcab',
   'dcba'
]


def build_momblish(corpus_path=None, rebuild_cache=False):
    return Momblish(CorpusAnalyzer(test_corpus).corpus)


def test_momble_generates_word(monkeypatch, capsys):
    monkeypatch.setattr('momblish.cli.load_momblish', build_momblish)

    random.seed(10)
    exit_code = main(['6'])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == 'CADCBA\n'


def test_momble_generates_word_with_prefix(monkeypatch, capsys):
    monkeypatch.setattr('momblish.cli.load_momblish', build_momblish)

    random.seed(10)
    exit_code = main(['7', 'dabc'])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == 'DABCADC\n'


def test_momble_can_rebuild_cache(monkeypatch, capsys):
    calls = []

    def fake_load_momblish(corpus_path=None, rebuild_cache=False):
        calls.append((corpus_path, rebuild_cache))
        return build_momblish()

    monkeypatch.setattr('momblish.cli.load_momblish', fake_load_momblish)

    random.seed(10)
    exit_code = main(['--rebuild-cache', '6'])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == 'CADCBA\n'
    assert calls == [(None, True)]


def test_momble_can_use_custom_corpus(monkeypatch, capsys, tmp_path):
    calls = []
    corpus_file = tmp_path / 'custom.txt'
    corpus_file.write_text('\n'.join(test_corpus))

    def fake_load_momblish(corpus_path=None, rebuild_cache=False):
        calls.append((corpus_path, rebuild_cache))
        return build_momblish()

    monkeypatch.setattr('momblish.cli.load_momblish', fake_load_momblish)

    random.seed(10)
    exit_code = main(['--corpus', str(corpus_file), '7', 'dabc'])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == 'DABCADC\n'
    assert calls == [(str(corpus_file), False)]
