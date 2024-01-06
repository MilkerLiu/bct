#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import bct_cmd
import global_args

class Arguments(global_args.Arguments):
    pass

class Cmd(bct_cmd.Cmd):
    """
    this is sub cmd desc
    hahahah
    """
    _name = "cmd_1_1"
    _title = "this a sub cmd cmd_1_1 title"
    _arguments = Arguments

    @classmethod
    def args_filter(self, argument: str):
        return argument not in ['target']

    @classmethod
    def run(self, args: Arguments):
        print(self, args)