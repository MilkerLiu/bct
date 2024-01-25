#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys, pathlib

bct_root = str(pathlib.Path(__file__).parent.parent.absolute())
print(bct_root)
sys.path.append(bct_root)

import cmd_1
import bct_parser

bct_parser.add_cmd(cmd_1.Cmd)