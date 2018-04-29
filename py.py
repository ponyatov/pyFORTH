## @file
## @brief Virtual py/FORTH Machine

## @defgroup sym Symbolic Class System
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
## @{ 

D = Stack('DATA') ; print D
W = Voc('FORTH') ; print W

def PrintStack(): print D
W['?'] = PrintStack

def DumpStop(): PrintStack() ; WORDS() ; BYE()
W['??'] = DumpStop

## @}

## @defgroup lexer Syntax Parser (lexer only)
## @{

import ply.lex  as lex

tokens = ['SYM']

def t_KEY(t):
    r'[a-zA-Z0-9_]+'
    return t

def t_error(t): raise SyntaxError(t)

lexer = [] # lexer stack allows nested .inc ludes

# @}

# interpreter
# @ingroup fvm
def INTERPRET(SRC):
    pass

INTERPRET('''
''')
