from ply import lex, yacc
from ply.lex import TOKEN

## 词法分析部分
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
# t_EQ_ = r'-eq'
# t_NE_ = r'-ne'
# t_GE_ = r'-ge'
# t_LE_ = r'-le'
# t_a_ = r'-a'
# t_b_ = r'-b'
# t_c_ = r'-c'
# t_d_ = r'-d'
# t_e_ = r'-e'
# t_f_ = r'-f'
# t_g_ = r'-g'
# t_k_ = r'-k'
# t_L_ = r'-L'
# t_n_ = r'-n'
# t_o_ = r'-o'
# t_p_ = r'-p'
# t_r_ = r'-r'
# t_s_ = r'-s'
# t_S_ = r'-S'
# t_u_ = r'-u'
# t_w_ = r'-w'
# t_x_ = r'-x'
# t_z_ = r'-z'
# 声明tokens
tokens = [
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
             # 'EQ_',
             # 'NE_',
             # 'GE_',
             # 'LE_',
             # 'a_',
             # 'b_',
             # 'c_',
             # 'd_',
             # 'e_',
             # 'f_',
             # 'g_',
             # 'k_',
             # 'L_',
             # 'n_',
             # 'o_',
             # 'p_',
             # 'r_',
             # 's_',
             # 'S_',
             # 'u_',
             # 'w_',
             # 'x_',
             # 'z_'
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
    r'[1-9][0-9]*'
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

    lexer = lex.lex(debug=0)

    # 语法部分
    precedence = (
        ('left', 'LOR'),
        ('left', 'LAND'),
        ('left', 'EQUALS', 'NE'),
        ('left', 'GT', 'GE', 'LT', 'LE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDES')
    )


# 参数变量


def p_error(p):
    print("Syntax error at '%s', '%s'" % (p.value, p.lineno))


def p_translation_unit(p):
    ''' translation_unit : external_decl
                             | translation_unit external_decl
    '''


# |declstmt
def p_external_decl(p):
    ''' external_decl : funcdef
    '''


def p_menthodsymbol(p):
    ''' menthodsymbol : IDENTIFIER
    '''


def p_statement_list(p):
    ''' statement_list : statement
                       | statement statement_list
    '''




# 函数定义
def p_funcdef(p):
    ''' funcdef : FUNCTION menthodsymbol LPAREN RPAREN LBRACE statement_list RBRACE
                | FUNCTION menthodsymbol LBRACE statement_list RBRACE
                | menthodsymbol LPAREN RPAREN LBRACE statement_list RBRACE
    '''
    print("一个函数")


def p_jump_statement(p):
    ''' jump_statement : return_statement
                       | continue_statement
                       | break_statement
    '''


def p_return_statement(p):
    ''' return_statement : RETURN expression
    '''


def p_continue_statement(p):
    ''' continue_statement : CONTINUE
    '''


def p_break_statement(p):
    ''' break_statement : BREAK
    '''


def p_varsymbol(p):
    ''' varsymbol : IDENTIFIER
    '''


# | declstmt
#                       | while_statement
#                       | funccall_stmt
#                       | jump_statement
#                       | selection_statement

def p_statement(p):
    ''' statement : assignment_statement
                  | jump_statement
                  | declstmt
                  | while_statement
    '''
    print("statement")


def p_while_statement(p):
    ''' while_statement : WHILE expression DO statement_list
                        | WHILE expression DO statement_list DONE statement_list
    '''


def p_declstmt(p):
    ''' declstmt : arrydecl
    '''


def p_arrydecl(p):
    ''' arrydecl : varsymbol LPAREN expression RPAREN
    '''


def p_assignment_statement(p):
    '''assignment_statement : cast_expr EQUALS expression'''


# | funccal_expr
def p_expression(p):
    ''' expression : binary_expr
    '''


def p_cast_expr(p):
    ''' cast_expr : unary_expr
                  | primary_expr
    '''


def p_constant(p):
    ''' constant : INT_CONSTANT
                  | FLOATING_CONSTANT
                  | STRING_CONSTANT1
                  | STRING_CONSTANT2
    '''


def p_primary_expr(p):
    ''' primary_expr : varsymbol
                    | constant
    '''


# | funccall_expr
# 一元操作符
def p_binary_expr(p):
    ''' binary_expr : binary_expr PLUS binary_expr
                  | binary_expr MINUS binary_expr
                  | binary_expr TIMES binary_expr
                  | binary_expr DIVIDES binary_expr
                  | binary_expr GT binary_expr
                  | binary_expr LT binary_expr
                  | binary_expr LE binary_expr
                  | binary_expr GE binary_expr
                  | binary_expr EQ binary_expr
                  | binary_expr NE binary_expr
                  | binary_expr LAND binary_expr
                  | binary_expr LOR binary_expr
                  | LPAREN binary_expr RPAREN
                  | cast_expr

    '''


def p_unary_expr(p):
    ''' unary_expr : unary_op primary_expr
    '''


# 可能存在问题
def p_unary_op(p):
    ''' unary_op : VALUE
    '''


if __name__ == '__main__':
    data = '''
function sdasd(){a=11}
function dsfsd{s=121 
return 8+192}
aslda(){w=asd}
'''
lexer = lex.lex()
lexer.input(data)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
lexer = lex.lex()
parser = yacc.yacc(debug=True)
lexer.lineno = 1
s = parser.parse(data)
print(s)
