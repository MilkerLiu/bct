#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse

CommonArg = argparse.Action
"""携带该参数, 该参数为 str/int"""
TrueArg = argparse._StoreTrueAction
"""携带该参数, 该参数为True, 默认为False"""
FalseArg = argparse._StoreFalseAction
"""携带该参数, 该参数为False, 默认为True"""
ListArg = argparse._AppendAction
"""携带该参数, 该参数为列表, 默认为空列表"""
BoolArg = argparse.BooleanOptionalAction
"""携带该参数, 该参数为bool, 默认为False, 追加 --no-xxx, 为关闭"""

class Opts:

    help: bool = False
    """show this help message and exit"""

    class Meta:
        fields = '__all__'
        """
        __all__ :  基类+当前类所有参数，当前类会覆盖基类
        __base__ : 基类参数
        __self__ : 当前类参数
        []       : 手动指定
        """

def make_args(parser:argparse.ArgumentParser, opts: type[Opts]):
    pass