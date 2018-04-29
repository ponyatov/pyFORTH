## @file
## @brief Virtual py/FORTH Machine

## @defgroup sym Symbolic Class System
## @brief object system for metaprogramming
## @{

## base object
class Object:
    def __init__(self, V):
        self.tag = self.__class__.__name__.lower() ; self.val = V
        self.next = [] ; self.attr = {}
    def __repr__(self):
        return '<%s:%s>' % (self.tag,self.val)
    def __setitem__(self,K,V):
        self.attr[K] = V ; return self

## data container    
class Container(Object): pass

## LIFO stack
class Stack(Container): pass
    
## Vocabulary (associative array)
class Voc(Container): pass

## @}

## @defgroup fvm FORTH Virtual Machine
## @brief light stack virtual machine on top of Python runtime
## @{ 

## data stack
D = Stack('DATA')
## global vocabulary
W = Voc('FORTH')

## `? ( -- )` print data stack
def PrintStack(): print D
W['?'] = PrintStack

## `?? ( -- )` print stack, vocabulary, and stop system
def DumpStop(): PrintStack() ; WORDS() ; BYE()
W['??'] = DumpStop

## @}

## @defgroup lexer Syntax Parser (lexer only)
## @brief script parser using PLY library
## @{

import ply.lex  as lex

## token types supported by lexer
tokens = ['SYM']

## new line rule increments line counter
def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

## symbol token
def t_SYM(t):
    r'[a-zA-Z0-9_]+'
    return t

## lexer error callback
def t_error(t): raise SyntaxError(t)

## lexer stack allows nested .inc ludes
lexer = []

## @}

## `INTERPRET ( -- )` script interpreter
## @ingroup fvm
## @param[in] SRC source code string
def INTERPRET(SRC):
    global lexer ; lexer += [lex.lex()] # allocate new lexer
    lexer[-1].input(SRC)                # feed source code
    while True:
        token = lexer[-1].token()
        if not token: break
        print token
    del lexer[-1]                       # drop finished lexer

INTERPRET('''
''')
