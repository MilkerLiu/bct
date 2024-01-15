#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse, textwrap, inspect
import bct_cmd
import desc_formatter

__all__ = [
    'add_cmd',
]

root_cmd = None

def add_cmd(cmd: type[bct_cmd.Cmd], ap:argparse.ArgumentParser = None, sub_ap: argparse._SubParsersAction = None):
    """
    """
    args = [(key, comment) for (key, comment) in _parse_args(cmd._arguments).items() if cmd.args_filter(key)]
    doc = "\n".join([line.strip() for line in (cmd.__doc__ or "").split('\n')])
    desc = f"{cmd._name or ''}\n{cmd._title}\n{doc}"
    is_root = ap == None
    if ap == None:
        ap = argparse.ArgumentParser(description=desc, formatter_class=lambda prog: desc_formatter.HelpFormatter(prog, max_help_position=36))
    else:
        ap = sub_ap.add_parser(name=cmd._name, 
                               help=cmd._title, 
                               formatter_class=lambda prog: desc_formatter.HelpFormatter(prog, max_help_position=36),
                               description=textwrap.dedent(desc)
        )

    # add args
    for (key, comment) in args:
        attr = getattr(cmd._arguments, key)
        attr.help = comment
        ap._add_action(attr)

    # add action
    ap.set_defaults(_cmd=cmd)

    # add sub cmd
    sub_ap = ap.add_subparsers(title="Commands", metavar="")
    for sub_cmd in cmd._sub_cmds:
        add_cmd(sub_cmd, ap, sub_ap)

    # set call
    if is_root:
        global root_cmd
        root_cmd = ap
        args = ap.parse_args()
        # run default cmd for config
        cmd.run(cmd._arguments(**args.__dict__))
        # run sub cmd
        sub_cmd:bct_cmd.Cmd = args._cmd
        sub_cmd.run(cmd._arguments(**args.__dict__))

    return ap


def _parse_attr_name(line: str):
    items = line.split(":")
    if len(items) < 2:
        return None
    return items[0].strip()

def _parse_args(args: type[bct_cmd.Arguments]):
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