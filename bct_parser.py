#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse, textwrap, inspect
from bct_cmd import Cmd, Arguments
from desc_formatter import HelpFormatter

__all__ = [
    'add_cmd',
]

def add_cmd(cmd: type[Cmd], ap:argparse.ArgumentParser = None, sub_ap: argparse._SubParsersAction = None):
    """
    """
    args = [(key, comment) for (key, comment) in _parse_args(cmd._arguments).items() if cmd.args_filter(key)]
    doc = "\n".join([line.strip() for line in (cmd.__doc__ or "").split('\n')])
    desc = f"{cmd._name or ''}\n{cmd._title}\n{doc}"
    is_root = ap == None
    if ap == None:
        ap = argparse.ArgumentParser(description=desc, formatter_class=lambda prog: HelpFormatter(prog, max_help_position=36))
    else:
        ap = sub_ap.add_parser(name=cmd._name, 
                               help=cmd._title, 
                               formatter_class=lambda prog: HelpFormatter(prog, max_help_position=36),
                               description=textwrap.dedent(desc)
        )

    # add args
    for (key, comment) in args:
        attr = getattr(cmd._arguments, key)
        attr.help = comment
        ap._add_action(attr)

    # add action
    ap.set_defaults(func=cmd.run)

    # add sub cmd
    for sub_cmd in cmd._sub_cmds:
        if sub_ap == None:
            sub_ap = ap.add_subparsers(title="Commands", metavar="")
        add_cmd(sub_cmd, ap, sub_ap)

    # set call
    if is_root:
        _set_call(ap)

    return ap

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


def _parse_attr_name(line: str):
    items = line.split(":")
    if len(items) < 2:
        return None
    return items[0].strip()

def _parse_args(args: type[Arguments]):
    field_comments = {}
    if args.__base__ and args.__base__ != object:
        field_comments = _parse_args(args.__base__)
    source = inspect.getsource(args)
    lines = source.split('\n')
    fields = [v for v in dir(args) if not v.startswith('__')]
    asts = []
    for index, line in enumerate(lines, start=1):
        attr_name = _parse_attr_name(line)
        valid_attr = attr_name in fields
        if valid_attr:
            pre = None if len(asts) == 0 else asts[-1]
            if pre:
                pre.append(index)
                asts[-1] = pre
            asts.append([attr_name, index])
    pre = None if len(asts) == 0 else asts[-1]
    if pre:
        pre.append(len(lines))
        asts[-1] = pre
    # 解析注释
    for (name, start, end) in asts:
        _comment = "\n".join(lines[start:end-1])
        _comment = _comment.strip().strip('"""').strip()
        _comment = "\n".join([v.strip() for v in _comment.split("\n")])
        field_comments[name] = _comment
    return field_comments