
import argparse
from argparse import ArgumentError
import os
import sys

from autoarchaeologist import excavators
from autoarchaeologist import ddhf

from autoarchaeologist.base import excavation

def excavation_for_args(args):
    if args.excavator is not None:
        return excavators.excavator_by_name(args.excavator)
    else:
        raise ArgumentError("no valid excavation was requsted")

def parse_arguments(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", default="/tmp/_autoarchaologist")
    parser.add_argument('--excavator', choices=excavators.__all__)
    parser.add_argument('filename')

    return parser.parse_args(args=argv)

def process_arguments(args):
    if args.dir == ".":
        args.dir = os.path.join(os.getcwd(), "_autoarchaologist")
    if args.filename is not None:
        args.filename = os.path.join(os.getcwd(), args.filename)
    else:
        raise ValueError()

    return args

def perform_excavation(args, Excavation=None):
    ctx = Excavation(html_dir=args.dir)
    ff = ctx.add_file_artifact(args.filename)

    ctx.start_examination()

    ctx.produce_html()

    print("Now point your browser at", ctx.filename_for(ctx).link)

if __name__ == "__main__":
    args = process_arguments(parse_arguments())

    try:
        os.mkdir(args.dir)
    except FileExistsError:
        pass

    perform_excavation(args, Excavation=excavation_for_args(args))
