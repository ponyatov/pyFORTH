class Object:
    def __init__(self, V):
        self.tag = self.__class__.__name__.lower() ; self.val = V
        self.next = [] ; self.attr = {}
    def __repr__(self):
        return '<%s:%s>' % (self.tag,self.val)
    def __setitem__(self,K,V):
        self.attr[K] = V ; return self
    
class Container(Object): pass

class Stack(Container): pass
    
class Voc(Container): pass

D = Stack('DATA') ; print D
W = Voc('FORTH') ; print W

def PrintStack(): print D
W['?'] = PrintStack

def DumpStop(): PrintStack() ; WORDS() ; BYE()
W['??'] = DumpStop

import ply.lex  as lex

tokens = ['SYM']

def t_KEY(t):
    r'[a-zA-Z0-9_]+'
    return t

def t_error(t): raise SyntaxError(t)

lexer = [] # lexer stack allows nested .inc ludes

INTERPRET('''
''')
