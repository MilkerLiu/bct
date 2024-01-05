#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse, textwrap, inspect
from bct_cmd import Cmd, Arguments
from desc_formatter import HelpFormatter

__all__ = [
    'add_cmd',
]

def add_cmd(cmd: type[Cmd], ap:argparse.ArgumentParser = None):
    """
    """
    args = [(key, comment) for (key, comment) in _parse_args(cmd._arguments).items() if cmd.args_filter(key)]
    doc = "\n".join([line.strip() for line in cmd.__doc__.split('\n')])
    desc = f"{cmd._name or ''}\n{cmd._title}\n{doc}"
    if ap == None:
        # root
        _ap = argparse.ArgumentParser(description=desc, formatter_class=lambda prog: HelpFormatter(prog, max_help_position=36))
    else:
        sub_ap = ap.add_subparsers(title="Commands", metavar="")
        _ap = sub_ap.add_parser(name=cmd._name, 
                               help=cmd._title, 
                               formatter_class=lambda prog: HelpFormatter(prog, max_help_position=36),
                               description=textwrap.dedent(desc)
        )

    # add args
    for (key, comment) in args:
        attr = getattr(cmd._arguments, key)
        attr.help = comment
        _ap._add_action(attr)

    # add action
    _ap.set_defaults(func=cmd.run)

    # add sub cmd
    for sub_cmd in cmd._sub_cmds:
        add_cmd(sub_cmd, _ap)

    if ap == None:
        _set_call(_ap)

    return _ap

def _set_call(ap:argparse.ArgumentParser):
    args = ap.parse_args()
    func = args.func
    attribute_value = getattr(func, 'arguments', None) or inspect.signature(func).parameters
    func_args = list(attribute_value.items())
    args_type = None if len(func_args) == 0 else func_args[0][1]
    opt = None
    if args_type:
        opt = args_type.annotation(args)

    if opt:
        func(opt)
    else:
        func() 

def _parse_args(args: type[Arguments]):
    field_comments = {}
    if args.__base__ and args.__base__ != object:
        field_comments = _parse_args(args.__base__)
    lines = inspect.getsource(args).split('\n')
    fields = [v for v in dir(args) if not v.startswith('__')]
    _doc_str = ""
    _attr_name = ""
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
        if line.endswith('"""') and len(_doc_str) != 0:
            field_comments[_attr_name] = _doc_str.strip().strip('"""').strip()
            _doc_str = ""
            continue
        _doc_str += (line + "\n")
    return field_comments