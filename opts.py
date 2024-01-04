#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse
import args

class KOpts:
    target: str = ""
    """
    """

    def __init__(self):
        pass

    class Meta:
        fields = []
        target = args.BoolArg(['-t', '--color'], dest='color', default=False, metavar=None, help='target url')

def make(parser: argparse.ArgumentParser):
    args.make_args(parser, KOpts)