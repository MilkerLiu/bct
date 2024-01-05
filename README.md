## command tools

这是一个未`argparse`包装的工具库，可以方便的整合命令和参数

命令分为根命令和子命令
每个命令都可以配置若干参数，参数具有各种类型

有以下优点：
* 对于多个命令，参数有时是一样的，bct 的参数配置采用OOP的思路，可以在命令上再次对参数进行配置  
* 传入命令函数的参数具有类型，提升开发效率，以及进行重构
* 基于注释/文档注释的方式对命令和参数进行help提示，减杀代码中的重复的内容

### 开始使用

全局默认参数
```
# file: test/globe_args.py

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
```

根命令
```
# file: test/cmd_1.py

class Arguments(globe_args.Arguments):
    target: str = bct_cmd.CommonArg(['-t', '--target'], dest='target')
    """
    Target Use custom desc
    """

class Cmd(bct_cmd.Cmd):
    """
    this a mine cmd desc
    """
    _title = "Mine Command"
    _arguments = Arguments
    _sub_cmds = [ cmd_1_1.Cmd ] # 注册子命令

    @classmethod
    def run(self, args: Arguments):
        print(self, args)
```

注册根命令
```
import bct_parser

bct_parser.add_cmd(cmd_1.Cmd)
```

查看help
```
# python3 __init__.py -h

Mine Command

this a mine cmd desc

optional arguments:
  -h, --help                  show this help message and exit
  -t TARGET, --target TARGET  Target Use custom desc
  --color                     Show log color
  --skip, --no-skip           Ship warning

Commands:
  cmd_1_1       this a sub cmd cmd_1_1 title
```

编写子命令（同根命令，需要额外指定 子命令名称）
```
#file: test/cmd_1_1.py

class Arguments(globe_args.Arguments): # 继承所有全局命令
    pass

class Cmd(bct_cmd.Cmd):
    """
    this is sub cmd desc
    hahahah
    """
    _name = "cmd_1_1"
    _title = "this a sub cmd cmd_1_1 title"
    _arguments = Arguments

    @classmethod
    def args_filter(self, argument: str): # 过滤掉部分用不到的命令
        return argument not in ['target']

    @classmethod
    def run(self, args: Arguments): # 执行命令
        print(self, args)
```

show help
```
cmd_1_1
this a sub cmd cmd_1_1 title

this is sub cmd desc
hahahah

optional arguments:
  -h, --help         show this help message and exit
  --color            Show log color
  --skip, --no-skip  Ship warning
```

执行命令
```
# python3 __init__.py -t aa --color
# <class 'test.cmd_1.Cmd'> <class 'test.cmd_1.Arguments'> - args: target: aa, color: True, skip: False


# python3 __init__.py cmd_1_1 --color
# <class 'test.cmd_1_1.Cmd'> <class 'test.cmd_1_1.Arguments'> - args: target: None, color: True, skip: False
```


### 参数型类

* CommonArg: 普通参数，可指定 -x, --xxxx, dest, choice(枚举类型)
* TrueArg: bool, 携带该参数值为True，反之为False
* FalseArg: bool, 携带该参数值为False，反之为True
* ListArg: list, --targets arm64 x86_64, => [arm64, x86_64]
* BoolArg: bool, 会自动生成反向参数，--color, 自动生成 --no-color, 携带为True，反向/不携带为 False


