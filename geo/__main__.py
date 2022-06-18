import argparse
import sys

from .anki import create_anki_groupings
from .learned import create_learned_svg, create_unlearned_svg

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd')
    subparsers.required = True
    learned_parser = subparsers.add_parser('learned')
    learned_parser.set_defaults(func=create_learned_svg)
    unlearned_parser = subparsers.add_parser('unlearned')
    unlearned_parser.set_defaults(func=create_unlearned_svg)
    anki_parser = subparsers.add_parser('anki')
    anki_parser.set_defaults(func=create_anki_groupings)
    args = parser.parse_args()
    args.func(args)
