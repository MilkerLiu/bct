#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import bct_cmd

class Arguments(bct_cmd.Arguments):
    target: str = bct_cmd.CommonArg(['-t', '--target'], dest='target')
    """
    Target
    """

    color: bool = bct_cmd.TrueArg(['--color'], dest='color')
    """
    Show log color
    """
    
    skip: bool = bct_cmd.BoolArg(['--skip'], dest='skip', default=False)
    """
    Ship warning
    """