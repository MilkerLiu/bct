#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse

__all__ = [
    'Cmd',
    'Arguments', 'EmptyArguments',
    'CommonArg', 'TrueArg', 'FalseArg', 'ListArg', 'BoolArg',
]

CommonArg = argparse._StoreAction
TrueArg = argparse._StoreTrueAction
FalseArg = argparse._StoreFalseAction
ListArg = argparse._AppendAction
BoolArg = argparse.BooleanOptionalAction

class Arguments:

    def __init__(self, args: argparse.Namespace = None) -> None:
        if args == None:
            return
        for (key, value) in args.__dict__.items():
            if callable(value):
                continue
            self.__setattr__(key, value)

    def __str__(self) -> str:
        args = ', '.join([f'{k}: {v}' for k, v in self.__dict__.items() if not k.startswith('_')])
        return f'{self.__class__} - args: {args}'

class EmptyArguments(Arguments):
    pass
  

class Cmd:
    """
    Document or describe for current cmd
    """

    _name: str = None
    """
    root cmd, this value is ignore
    sub cmd must key 'name' unique

    use for desc
    """
    _title: str = ""
    """
    current cmd title, use for help title
    """

    _arguments = Arguments
    """
    cmd arguments
    """
    _sub_cmds = []
    """sub commands"""

    @classmethod
    def args_filter(self, argument: str):
        """Filter arguments, if return true, this args bind to current cmd"""
        return True

    @classmethod
    def run(self, args: Arguments):
        pass


