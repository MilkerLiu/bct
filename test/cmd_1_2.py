#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import bct_cmd

class Arguments(bct_cmd.Arguments):

    common: str = bct_cmd.CommonArg(['-c', '--common'], dest='common')
    """Common arg"""
    choice: str = bct_cmd.CommonArg(['--choice'], choices=['a', 'b'], dest='choice')
    """Common arg choice"""
    list: [str] = bct_cmd.ListArg(['-l', '--list'], dest='list')
    """List arg"""
    true: bool = bct_cmd.TrueArg(['-t', '--true'], dest='true')
    """True arg"""
    false: bool = bct_cmd.FalseArg(['-f', '--false'], dest='false')
    """Flase arg"""
    boolean: bool = bct_cmd.BoolArg(['-b', '--boolean'], dest='boolean')
    """Boolean arg"""


class Cmd(bct_cmd.Cmd):
    """
    this is sub cmd desc
    hahahah
    """
    _name = "cmd_1_2"
    _title = "this a sub cmd cmd_1_2 title"
    _arguments = Arguments

    @classmethod
    def run(self, args: Arguments):
        print(self, args)