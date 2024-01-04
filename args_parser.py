#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
from argparse import ArgumentParser
import textwrap
import inspect
from . import formatter

__all__ = [
    'BaseOpts',
    'make_args',
    'run_args', 
    'formatter']

class Meta:
    pass

Field = ArgumentParser.add_argument

class BaseOpts():
    def __init__(self, args: argparse.Namespace = None) -> None:
        if args == None:
            return
        for (key, value) in args.__dict__.items():
            if callable(value):
                continue
            self.__setattr__(key, value)

    @classmethod
    def meta(self):
        info = self.__doc__.strip().split('\n')
        name = info[0].split(":")[1].strip()
        help = info[1].split(":")[1].strip()
        desc = '\n'.join(info[2:]).strip()
        comments = self.comment_for_attributes()
        return name, help, desc, comments

    @classmethod        
    def make(self, arguments:argparse.ArgumentParser) -> None:
        pass

    @classmethod
    def comment_for_attributes(self):
        lines = inspect.getsource(self).split('\n')
        fields = [v for v in dir(self) if not v.startswith('_')]
        _doc_str = ""
        _attr_name = ""
        field_comments = {}
        for _, line in enumerate(lines, start=1):
            attr, _, _ = line.rpartition(":")
            attr_name = attr.strip()
            if attr_name in fields:
                if "#" in line:
                    _, _, comment = line.partition("#")
                    field_comments[attr_name] = comment.strip()
                    continue
                _doc_str = ""
                _attr_name = attr_name
                continue
            if _attr_name is None or _attr_name == "":
                continue
            _doc_str += (line + "\n")
            if line.endswith('"""'):
                field_comments[_attr_name] = _doc_str.strip().strip('"""').strip()
                _doc_str = ""
                continue
        return field_comments

def run_args(args: argparse.Namespace):
    func = args.func
    attribute_value = getattr(func, 'arguments', None) or inspect.signature(func).parameters
    func_args = list(attribute_value.items())
    args_type = None if len(func_args) == 0 else func_args[0][1]
    if args_type:
        opt = args_type.annotation(args)
        args.func(opt)
    else:
        args.func()

def make_args(subparsers:argparse._SubParsersAction, opt:BaseOpts):
    name, help, desc, comments = opt.meta()
    cmd:argparse.ArgumentParser = subparsers.add_parser(name=name, 
                                                        help=help, 
                                                        formatter_class=argparse.RawTextHelpFormatter,
                                                        description=textwrap.dedent(desc)
    )
    func = opt.make(cmd)
    cmd.set_defaults(func=func)
    all_comments_keys = comments.keys()
    for action in cmd._actions:
        dest = action.dest
        if dest in all_comments_keys:
            action.help = comments[dest]