#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse, textwrap, inspect
from bct_cmd import Cmd, Opts
from desc_formatter import HelpFormatter

def add_cmd(cmd: type[Cmd], ap:argparse.ArgumentParser = None):
    """
    """
    meta = _parse_doc(cmd)
    if ap == None:
        # root
        _ap = argparse.ArgumentParser(description=meta['desc'], formatter_class=HelpFormatter)
    else:
        sub_ap = ap.add_subparsers(title="Commands", metavar="")
        _ap = sub_ap.add_parser(name=meta['name'], 
                               help=meta['help'], 
                               formatter_class=argparse.RawTextHelpFormatter,
                               description=textwrap.dedent(meta['doc'])
        )

    # add args
    for (key, comment) in meta['args']:
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
        
def _parse_doc(cmd: type[Cmd]):
    metas = {}
    infos = cmd.__doc__.strip().split('\n')
    for line in infos:
        _l = line.strip()
        if _l.startswith("@"):
            spi = _l.index(':')
            key = _l[1:spi].strip()
            value = _l[spi+1:].strip()
            metas[key] = value
        else:
            key = "doc"
            value = '\n'.join(infos[len(metas.keys()):]).strip()
            metas[key] = value
            break
    args = _parse_args(cmd._arguments)
    metas['args'] = [(key, comment) for (key, comment) in args.items()]
    return metas

def _parse_args(args: type[Opts]):
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