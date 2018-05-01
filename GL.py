## @defgroup gl OpenGL
## @brief Accelerated OpenGL graphics
## @ingroup gui

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
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen(wx.WHITE,11))
        dc.DrawLine(0,0,64,32)

class GUI_thread(threading.Thread):
    def __init__(self):
        ## OpenGL window
        ## @ingroup gl
        self.glw = wx.Frame(self.main,wx.ID_ANY,'GL',size=(320,240))
        ## OpenGL canvas
        ## @ingroup gl
        self.glw.canvas = GUI_canvas(self.glw)
    def onClose(self,e):
        self.glw.Close()
    def run(self):
        # gl window
        self.glw.Show()
