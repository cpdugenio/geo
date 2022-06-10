import argparse
import sys

from .learned import create_learned_svg

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd')
    subparsers.required = True
    learned_parser = subparsers.add_parser('learned')
    learned_parser.set_defaults(func=create_learned_svg)
    args = parser.parse_args()
    args.func(args)
