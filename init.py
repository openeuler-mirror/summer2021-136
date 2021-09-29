import json

from ply import lex
from ply.lex import TOKEN

#####词法分析部分#####
# 处理保留字
reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'elif': 'ELIF',
    'fi': 'FI',
    'for': 'FOR',
    'in': 'IN',
    'do': 'DO',
    'done': 'DONE',
    'while': 'WHILE',
    'until': 'UNTIL',
    'case': 'CASE',
    'esac': "ESAC",
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'function': 'FUNCTION'
}
t_OR = r'\|'
t_DF = r';'
t_DGT = r'>>'
t_DLT = r'<<'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_BAND = r'&'
t_DIVIDES = r'/'
t_EQUALS = r'='
t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='
t_EQ = r'=='
t_NE = r'!='
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMI = r';;'
t_LAND = r'&&'
t_LOR = r'\|\|'
t_LNOT = r'!'
t_MOD = r'%'
t_VALUE = r'\$'
t_GMERGE = r'>&'
t_LMERGE = r'<&'
# 声明tokens
tokens = [
             'DF',
             'OR',
             'FLOATING_CONSTANT',
             'INT_CONSTANT',
             'STRING_CONSTANT1',
             'STRING_CONSTANT2',
             'DGT',
             'DLT',
             'PLUS',
             'MINUS',
             'TIMES',
             'BAND',
             'DIVIDES',
             'EQUALS',
             'GT',
             'LT',
             'GE',
             'LE',
             'EQ',
             'NE',
             'LBRACE',
             'RBRACE',
             'LBRACKET',
             'RBRACKET',
             'LPAREN',
             'RPAREN',
             'SEMI',
             'LAND',
             'LOR',
             'LNOT',
             'MOD',
             'VALUE',
             'GMERGE',
             'LMERGE',
             'IDENTIFIER',
         ] + list(reserved.values())

# 空格 制表符 回车这些不可见符号都忽略
t_ignore = ' \t\r'


# 解析错误的时候直接抛出异常
def t_error(self):
    raise Exception('error {} at line {}'.format(self.value[0], self.lineno))


# 记录行号，方便出错定位
def t_newline(self):
    r'\n+'
    self.lexer.lineno += len(self.value)


# #风格的单行注释
def t_ignore_COMMENT1(self):
    r'\#[^\n]*'
    pass


# :<<eof  eof风格的多行注释
def t_ignore_COMMENT4(self):
    r':<<eof[^(eof)]*eof'


# :<<!     !风格的多行注释
def t_ignore_COMMENT2(self):
    r':<<![^!]*!'
    pass


# :,    ,风格的多行注释
def t_ignore_COMMENT3(self):
    r':,[^,]*,'


# 变量名规则
def t_IDENTIFIER(self):
    r'[a-zA-Z_][0-9a-zA-Z_]*'
    self.type = reserved.get(self.value, 'IDENTIFIER')
    return self


# 浮点数值的定义
exponent_part = r"""([eE][-+]?[0-9]+)"""
fractional_constant = r"""([0-9]*\.[0-9]+)|([0-9]+\.)"""
floating_constant = '((((' + fractional_constant + ')' + exponent_part + '?)|([0-9]+' + exponent_part + '))[FfLl]?)'


@TOKEN(floating_constant)
def t_FLOATING_CONSTANT(self):
    r'\d+(\.\d+)?'
    self.value = float(self.value)
    return self


# 整数值的定义
def t_INT_CONSTANT(self):
    r'[0-9][0-9]*'
    self.value = int(self.value)
    return self


# "字符串值的定义
def t_STRING_CONSTANT1(self):
    r'\"([^\\\n]|(\\.))*?\"'
    self.type = 'STRING_CONSTANT1'
    return self


# '字符串值的定义
def t_STRING_CONSTANT2(self):
    r'\'([^\\\n]|(\\.))*?\''
    self.type = 'STRING_CONSTANT2'
    return self


##### 分析分词后的语段 #####
# 获得所有以下形式的函数，返回一个list，list[0]存储提取函数后的剩余序列
# list[1]存储函数列表，每个单元的第一个元素是函数名，第二个元素是函数的内容
# function funcname(){------}
# funcname(){------}
def getfunc1(tokens):
    out = []  # 用于保存提取函数后的剩余词汇
    functions = []  # 用于保存函数
    tem = []  # 用于零时存放函数
    contect = []  # 用于储存函数文本内容
    flag = 0  # 用于括号的匹配
    state = 0  # 用于保存状态信息
    for x in tokens:
        if state == 0 and x.type == 'IDENTIFIER':
            tem.append(x.value)
            out.append(x)
            state = 1
        elif state == 1 and x.type == 'LPAREN':
            state = 2
        elif state == 2 and x.type == 'RPAREN':
            state = 3
        elif state == 3 and x.type == 'LBRACE':
            state = 4
            flag += 1
        elif state == 4 and flag != 0:
            if x.type == 'LBRACE':
                flag += 1
            elif x.type == 'RBRACE':
                flag -= 1
            contect.append(x)
        elif state == 4 and flag == 0:
            tem.append(contect)
            functions.append(tem)
            tem = []
            contect = []
            state = 0
            out.pop()
            if state == 0 and x.type == 'IDENTIFIER':
                tem.append(x.value)
                out.append(x)
                state = 1
        else:
            tem = []
            contect = []
            state = 0
            out.append(x)
    return [out, functions]


# 获得所有以下形式的函数
# function funcname{-------}
def getfunc2(tokens):
    out = []  # 用于保存提取函数后的剩余词汇
    functions = []  # 用于保存函数
    tem = []  # 用于零时存放函数
    contect = []  # 用于储存函数文本内容
    flag = 0  # 用于括号的匹配
    state = 0  # 用于保存状态信息
    for x in tokens:
        if state == 0 and x.type == 'FUNCTION':
            state = 1
        elif state == 1 and x.type == 'IDENTIFIER':
            tem.append(x.value)
            state = 2
        elif state == 2 and x.type == 'LBRACE':
            state = 3
            flag += 1
        elif state == 3 and flag != 0:
            if x.type == 'LBRACE':
                flag += 1
            elif x.type == 'RBRACE':
                flag -= 1
            contect.append(x)
        elif state == 3 and flag == 0:
            tem.append(contect)
            functions.append(tem)
            tem = []
            contect = []
            state = 0
            if state == 0 and x.type == 'FUNCTION':
                state = 1
        else:
            tem = []
            contect = []
            state = 0
            out.append(x)
    return [out, functions]


# 解析commands文件中包含的所有命令
def getcommandslist():
    with open('commands.json') as f:
        commandslist = json.load(f)
        for x in commandslist.keys():
            commandslist[x] = 0
    return commandslist


# 获得直接调用的命令
def getsurecommands(tokens, commandslist):
    out = commandslist
    for x in tokens:
        if x.type == 'IDENTIFIER' and (out.get(x.value) is not None):
            out[x.value] += 1
    return out


# 获得间接调用的命令
def getfunctioncommands(tokens, functionlist, commandslist):
    out = commandslist
    for x in functionlist:
        for y in tokens:
            if y.type == 'IDENTIFIER' and y.value == x[0]:
                out = getsurecommands(x[1], out)
                out = getfunctioncommands(x[1], functionlist, out)
    return out


# 获得可能调用的命令，包括下列情况
# if----fi
# for----done
# while----done
# case----esac
def getpossiblecommands(tokens):
    out = []
    possiblelist = []
    state = 0
    for x in tokens:
        if x.type in ['IF', 'FOR', 'WHILE', 'UNTIL', 'CASE'] and state == 0:
            state = 1
        elif state != 0:
            if x.type in ['FI', 'DONE', 'ESAC']:
                state -= 1
            elif x.type in ['IF', 'FOR', 'WHILE', 'UNTIL', 'CASE']:
                state += 1
            else:
                possiblelist.append(x)
        else:
            out.append(x)
    return [out, possiblelist]


# 识别带有重启关闭开启服务的命令
def getsystemcommand(tokens):
    stemcommandlist = []
    tem = ''
    state = 0
    for x in tokens:
        if x.type == 'IDENTIFIER' and x.value == 'systemctl' and state == 0:
            tem += x.value
            tem += ' '
            state = 1
        elif state == 1:
            tem += x.value
            tem += ' '
            state = 2
        elif state == 2:
            tem += x.value
            stemcommandlist.append(tem)
            tem = ''
            state = 0
    return stemcommandlist


# 输入一个要识别的内容，返回一个字典，每个项的值代表了命令调用的情况
# value为0，没有被调用
# value大于0，一定被调用
# value小于0，命令存在于判断循环语句中，可能被调用
def init(data):
    # 将文本内容分词，转化成token序列
    lexer = lex.lex()
    lexer.input(data)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    # 获取带有重启关闭开启服务的命令
    lll = getsystemcommand(tokens)
    # 获取可能调用的命令
    tokens, tem3 = getpossiblecommands(tokens)
    tem1 = getsurecommands(tem3, getcommandslist())
    # 获取函数
    tokens, funclist = getfunc1(tokens)
    tokens, tem2 = getfunc2(tokens)
    funclist += tem2
    # 获取直接调用的命令
    out1 = getsurecommands(tokens, getcommandslist())
    # 获取间接调用的命令
    out2 = getfunctioncommands(tokens, funclist, getcommandslist())
    # 获取可能间接调用的命令
    out3 = getfunctioncommands(tem3, funclist, getcommandslist())
    for key, value in out1.items():
        out1[key] += out2[key]
    for key, value in out1.items():
        if value == 0 and tem1[key] != 0:
            out1[key] = -1
    for key, value in out1.items():
        if value == 0 and out3[key] != 0:
            out1[key] = -1
    return [out1, lll]


# 输入一个由init函数生成的四元组列表，两两的产生对比信息。
def comparescriptlist(commandslist):
    out = []
    for x in range(len(commandslist) - 1):
        for y in range(x + 1, len(commandslist)):
            out.append(comparescript(commandslist[x], commandslist[y]))
    return out


# 用于判断每个命令的出现状态
def getstate(i):
    if i > 0:
        return 'called'
    elif i == 0:
        return 'nocalled'
    elif i == -1:
        return 'possible'


# 输入两个包含脚本信息的四元组，产生对比信息
def comparescript(script1, script2):
    out = []
    tem = []
    out.append(script1[0])
    out.append(script2[0])
    out.append(script1[1])
    out.append(script2[1])
    for key, value in script1[2].items():
        if getstate(script1[2][key]) != getstate(script2[2][key]):
            tem.append([key, getstate(script1[2][key]), key, getstate(script2[2][key])])
    out.append(tem)
    return out


# 对于GUI输入内容的分词
def getmessage(message):
    return message.split()
