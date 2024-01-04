#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import opts
from desc_formatter import HelpFormatter

parser = argparse.ArgumentParser(description='bilibili command tools, all in one', formatter_class=HelpFormatter)
cmd=parser.add_argument('-n', '--no-color', dest='no_color', action="store_true", help='print colorful logs')
# parser.add_argument('--target', required=True, type = str, help='target labels')
parser.add_argument('--cpu', default = '', type = str, help='ios_x86_64')
parser.add_argument('--opt', default = '3', type = str, help='1 or 2 or 3')
# parser._add_action(Opts.Meta.target)
opts.make(parser)
# print(cmd)
# print(Opts.Meta.target)
args = parser.parse_args()
print(args)