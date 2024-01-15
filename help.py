#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
from . import bct_cmd as bct_cmd

class Arguments(bct_cmd.Arguments):
    pass

cmd_max_width = 40

def format_key(key, ident:int = 2):
    return f'{" " * ident}{key.ljust(cmd_max_width - ident)}'

class Cmd(bct_cmd.Cmd):
    _arguments = Arguments
    _name = "help"
    _title = "show all helps info"

    @classmethod
    def run(self, args: Arguments):
        ap = bct_cmd.bct_parser.root_cmd
        ap.print_usage()
        print(ap.description)
        print('Commnads:')
        self.print_ap(ap)
            

    @classmethod
    def print_ap(self, ap: argparse.ArgumentParser, ident=2):
        for asb in ap._subparsers._actions:
            if isinstance(asb, argparse._HelpAction):
                continue
            if len(asb.option_strings) > 0:
                if asb.dest not in ['color', 'verbose']:
                    key = format_key(', '.join(asb.option_strings), ident=ident)
                    print(key, asb.help)
            if isinstance(asb, argparse._SubParsersAction):
                for subactions in asb._choices_actions:
                    cmd = format_key(subactions.dest, ident=ident)
                    print(cmd, subactions.help)
                    aap = asb.choices[subactions.dest]  
                    self.print_ap(aap, ident=ident+2)