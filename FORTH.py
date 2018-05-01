## @file
## @brief Virtual py/FORTH Machine

import sys

## enable logging to file
sys.stdout = open('log.log','w')

## @defgroup sym Symbolic Class System
## @brief object system for metaprogramming
## @{

## base object
class Object:
    ## construct generic object from value
    ## @returns object in `<T:V>` form: class/type tag, and single value
    ## @returns but any object able to work as universal constructor`
    def __init__(self, V):
        ## class/type tag
        self.tag = self.__class__.__name__.lower()
        ## single object value
        self.val = V
        ## `nest[]`ed elements /ordered/
        self.nest = []
        ## `attr{}`ibutes /associative, unordered/
        self.attr = {}
    ## represent in string form
    def __repr__(self): return self.dump()
    ## dump object in tree form
    def dump(self,depth=0):
        S = self.pad(depth) + self.head()
        for i in self.attr:
            S += self.pad(depth+1) + self.attr[i].head(prefix='%s = '%i)
        for j in self.nest:
            S += j.dump(depth+1)
        return S
    ## dump object in short `[prefix]<T:V>` form
    ## @param[in] prefix optional prefix
    def head(self,prefix=''):
        return '%s<%s:%s>' % (prefix,self.tag,self.val)
    ## pad with tabs in tree dump
    def pad(self,N):
        return '\n'+'\t'*N
    ## `object[key]=value`
    def __setitem__(self,K,V):
        self.attr[K] = V ; return self
    ## @returns object[key]
    def __getitem__(self,K):
        return self.attr[K]
    ## `object << something`        
    def __lshift__(self,o):
        self.nest.append(o) ; return self
    ## popo fron `nest[]` stack-like
    def pop(self):
        return self.nest.pop()
        
## primitive
class Primitive(Object): pass

## symbol
class Sym(Primitive): pass

## data container    
class Container(Object): pass

## LIFO stack
class Stack(Container): pass
    
## Vocabulary (associative array)
class Voc(Container):
    ## operator `<<` will push function to `attr{}`ibutes area
    def __lshift__(self,o):
        self.attr[o.__name__] = Fn(o)
        
## elements with execution semantics
class Active(Object): pass

## function wrapped from VM
class Fn(Active):
    ## @param[in] F function written in Python
    def __init__(self,F):
        Active.__init__(self,F.__name__)
        ## store pointer to function being executed
        self.fn = F
    ## execution semantics implements via function call
    def __call__(self):
        self.fn()

## @}

## @defgroup fvm FORTH Virtual Machine
## @brief light stack virtual machine on top of Python runtime
## @{ 

## data stack
D = Stack('DATA')
## global vocabulary
W = Voc('FORTH')

## `BYE ( -- )` stop system
def BYE(): sys.exit(0)
W << BYE

## `? ( -- )` print data stack
## @returns data stack dump in stdout/console
def PrintStack(): print D
W['?'] = Fn(PrintStack)

## `?? ( -- )` print stack, vocabulary, and stop system
## @returns data stack and vocabulary dumps inn stdout/console
## @returns exit from system 
def DumpStop(): PrintStack() ; WORDS() ; BYE()
W['??'] = Fn(DumpStop)

## `WORDS ( -- )` print vocabulary
## @returns vocabulary log in stdout/console
def WORDS(): print W
W << WORDS

## @}

## @defgroup lexer Syntax Parser (lexer only)
## @brief script parser using PLY library
## @{

import ply.lex  as lex

## token types supported by lexer
tokens = ['SYM']

## comments
t_ignore_COMMENT = '[\\\#].*'

## new line rule increments line counter
def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

## symbol token
def t_SYM(t):
    r'[a-zA-Z0-9_\?\:\;]+'
    t.value = Sym(t.value) ; return t

## lexer error callback
def t_error(t): raise SyntaxError(t)

## lexer stack allows nested .inc ludes
lexer = []

## @}

## @defgroup compiler interpreter/compiler
## @ingroup fvm
## @{

## `WORD ( -- wordname )` get next word name from source code stream
def WORD():
    token = lexer[-1].token()
    if not token: BYE()
    D << token.value
    
## `FIND ( wordname - xt )` lookup definition in vocabulary
## @param[in] wordname word name should be lookup
## @param[out] xt object can be executed by EXECUTE
## @returns xt execution token: object can be executed by EXECUTE
def FIND():
    WN = D.pop().val    # get word name
    D << W[WN]          # lookup in vocabulary
    
## `EXECUTE ( xt -- )` execute object
def EXECUTE(): D.pop()()
W << EXECUTE

## `INTERPRET ( -- )` script interpreter
## @param[in] SRC source code string
def INTERPRET(SRC):
    global lexer ; lexer += [lex.lex()] # allocate new lexer
    lexer[-1].input(SRC)                # feed source code
    while True:
        WORD()
        FIND()
        EXECUTE()
    del lexer[-1]                       # drop finished lexer

## @}

## @defgroup gui GUI
## @brief GUI subsystem

## @defgroup gl OpenGL
## @brief Accelerated OpenGL graphics
## @ingroup gui

import wx, wx.stc
import threading
# OpenGL
import wx.glcanvas
from OpenGL.GL import *

## OpenGL canvas
## @ingroup gl
class GUI_canvas(wx.glcanvas.GLCanvas):
    ## create GL canvas
    def __init__(self,parent):
        wx.glcanvas.GLCanvas.__init__(self,parent,wx.ID_ANY,size=(64,32))
        ## OpenGL context
        self.context = wx.glcanvas.GLContext(self)
        # bind paint event to drawer
        self.Bind(wx.EVT_PAINT,self.OnDraw)
    ## process GL draw event
    def OnDraw(self,e):
        self.SetCurrent(self.context)
        glClearColor(.1,.2,.3,1)
        glClear(GL_COLOR_BUFFER_BIT)
        self.SwapBuffers()

## GUI thread
## @ingroup gui
class GUI_thread(threading.Thread):
    ## construct (single) GUI thread
    def __init__(self):
        threading.Thread.__init__(self)
        ## wx application
        self.app = wx.App()
        ## main window
        self.main = wx.Frame(None,wx.ID_ANY,str(sys.argv))
        ## menu
        self.menubar = wx.MenuBar()
        ## file menu
        self.file = wx.Menu()
        self.menubar.Append(self.file,'&File')
        ## file/new
        self.new = self.file.Append(wx.ID_NEW,'&New')
        ## file/open
        self.open = self.file.Append(wx.ID_OPEN,'&Open')
        ## file/save
        self.save = self.file.Append(wx.ID_SAVE,'&Save')
        ## file/save as
        self.saveas = self.file.Append(wx.ID_SAVEAS,'Save &ass')
        ## file/close
        self.close = self.file.Append(wx.ID_CLOSE,'&Close') 
        ## file/exit
        self.file.AppendSeparator()
        self.exit = self.file.Append(wx.ID_EXIT,'E&xit')
        self.main.Bind(wx.EVT_MENU, self.onClose, self.exit)
        ## help menu
        self.help = wx.Menu()
        self.menubar.Append(self.help,'&Help')
        # help/about
        self.help.Append(wx.ID_ABOUT,'&About\tF1')
        ## command console/editor
        self.console = wx.stc.StyledTextCtrl(self.main)
        # set zoom in/out keys
        self.console.CmdKeyAssign(ord('='),wx.stc.STC_SCMOD_CTRL,wx.stc.STC_CMD_ZOOMIN)
        self.console.CmdKeyAssign(ord('-'),wx.stc.STC_SCMOD_CTRL,wx.stc.STC_CMD_ZOOMOUT)
        # enable line numbering
        self.console.SetMarginType(1,wx.stc.STC_MARGIN_NUMBER)
        # set numbering bar width (in pixels)
        self.console.SetMarginWidth(1,32)
        ## OpenGL window
        ## @ingroup gl
        self.glw = wx.Frame(self.main,wx.ID_ANY,'GL',size=(320,240))
        ## OpenGL canvas
        ## @ingroup gl
        self.glw.canvas = GUI_canvas(self.glw)
    ## process app close event
    def onClose(self,e):
        self.glw.Close()
        self.main.Close()
    ## activate GUI thread
    def run(self):
        # main window
        self.main.SetMenuBar(self.menubar)
        self.main.Show()
        # gl window
        self.glw.Show()
        # GUI loop
        self.app.MainLoop()
## singleton thread process all GUI events
gui_thread = GUI_thread()

## start and transfer control to GUI
def GUI(): gui_thread.start() ; gui_thread.join()
W << GUI

## @}

if __name__ == '__main__':
    try:
        ## source code of init file from command line
        ## (or `src.src` if not given)
        SRC = open(sys.argv[1]).read()
    except IndexError:
        SRC = open('src.src').read()
    INTERPRET(SRC)
    

