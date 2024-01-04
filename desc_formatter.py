#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse

class HelpFormatter(argparse.HelpFormatter):

    cmd_max_width = 12

    def format_sub_action(self, action, ident=2):
        if not isinstance(action, argparse._SubParsersAction):
            return None
        help = ""
        index = 0
        for (key, parser) in action.choices.items():
            help += f'{" " * ident}{key.ljust(self.cmd_max_width - ident)}\t{action._choices_actions[index].help}\n'
            index += 1
            if len(parser._actions) >= 2:
                sub = self.format_sub_action(parser._actions[1], ident=ident + 2)
                if sub:
                    help += sub
        return help

    def _format_action(self, action):
        if isinstance(action, argparse._SubParsersAction):
            return self.format_sub_action(action=action)
        return super()._format_action(action)