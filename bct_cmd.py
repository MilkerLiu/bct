#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse

class Opts:

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

class Cmd:
    _arguments = Opts
    """
    cmd arguments
    """
    _sub_cmds = []

    @classmethod
    def run(self, args: Opts):
        print(args)



