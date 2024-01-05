#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import bct_cmd
from . import globe_args, cmd_1_1, cmd_1_2

class Arguments(globe_args.Arguments):
    target: str = bct_cmd.CommonArg(['-t', '--target'], dest='target')
    """
    Target Use custom desc
    """

class Cmd(bct_cmd.Cmd):
    """
    this a mine cmd desc
    """
    _title = "Mine Command"
    _arguments = Arguments
    _sub_cmds = [cmd_1_1.Cmd]

    @classmethod
    def run(self, args: Arguments):
        print(self, args)