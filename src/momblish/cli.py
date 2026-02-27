import argparse

from momblish import Momblish


def build_parser():
    parser = argparse.ArgumentParser(
        prog='momble',
        description='Generate nonsense words from the default English corpus or a supplied corpus file.',
    )
    parser.add_argument(
        '--corpus',
        help='Analyze words from the given corpus file instead of the default English dictionary.',
    )
    parser.add_argument(
        '--rebuild-cache',
        action='store_true',
        help='Rebuild the cached analyzed corpus before generating the word.',
    )
    parser.add_argument('length', type=int, help='Length of the word to generate.')
    parser.add_argument(
        'prefix',
        nargs='?',
        help='Optional prefix the generated word must start with.',
    )
    return parser


def load_momblish(corpus_path=None, rebuild_cache=False):
    if corpus_path:
        return Momblish.from_file(corpus_path, rebuild_cache=rebuild_cache)
    return Momblish.english(rebuild_cache=rebuild_cache)


def main(argv=None):
    args = build_parser().parse_args(argv)
    word = load_momblish(
        corpus_path=args.corpus,
        rebuild_cache=args.rebuild_cache,
    ).word(
        args.length,
        prefix=args.prefix,
    )
    print(word)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
