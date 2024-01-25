#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse

__all__ = [
    'Cmd',
    'Arguments', 'EmptyArguments',
    'CommonArg', 'TrueArg', 'FalseArg', 'ListArg', 'BoolArg', 'VersionArg'
]

CommonArg = argparse._StoreAction
TrueArg = argparse._StoreTrueAction
FalseArg = argparse._StoreFalseAction
ListArg = argparse._AppendAction
BoolArg = argparse.BooleanOptionalAction
VersionArg = argparse._VersionAction

class _Arguments:

    def __init__(self, **kwargs) -> None:
        for k in dir(self):
            if k.startswith('_'):
                continue
            setattr(self, k, getattr(self, k).default)
        for (k, v) in kwargs.items():
            if k.startswith('_'):
                continue
            setattr(self, k, v)

    def __str__(self) -> str:
        args = ', '.join([f'{k}: {v}' for k, v in self.__dict__.items() if not k.startswith('_')])
        return f'{self.__class__} - args: {args}'
    

class Arguments(_Arguments):
    pass


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

    _arguments = EmptyArguments
    """
    cmd arguments
    """
    _sub_cmds = []
    """sub commands"""

    @classmethod
    def run(self, args: Arguments):
        pass


