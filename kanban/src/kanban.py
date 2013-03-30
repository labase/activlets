"""
############################################################
Kanban - Agile Workflow
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/03/29
:Status: This is a "work in progress"
:Revision: 0.1.0
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__. 
"""
__author__  = "Carlo E. T. Oliveira (carlo@nce.ufrj.br)"
__version__ = "0.1"
__date__    = "2013/03/29"

REPO = '/studio/activlets/%s'

def _logger(*a):
    print(a)
        
if not '__package__' in dir():
    import svg
    import html
    logger = log
    pass
else:
    logger = _logger
    pass

COLORS = """#CCFF66 #669933 #CCFFCC #99CC33 #CC6699 #993366 #FFCCCC #CC3399
#FFCC66 #996633 #FFCCCC #CC9933 #6666CC #336699 #CCCCFF #3366CC""".split()
BACKGROUNDS ="#666666 #999999 #CCCCCC #EEEEEE".split()
PANELS = len(BACKGROUNDS)
HEAD, LABELS, PANEL, ITEM = 'head labels panel item'.split()

class GUI:
    """ A factory for html elements. :ref:`GUI`
    """
    def __init__(self, doc, gui):
        self.doc, self.gui = doc, gui
        pass
    def div(self, text, node, draggable=False, id='nono', Class="rounded-corners"):
        """Create a HTML DIV element"""
        element = self.gui.DIV(text, draggable=draggable, id=id, Class=Class)
        self.doc[node] <= element
        return element
    def set_style(self, target, **kwargs):
        """Set the style attribute of a DOM element"""
        logger('style %s'%kwargs)
        target.style= kwargs
    def set_attrs(self, target, **kwargs):
        """Set the attributes defined as key arguments of a target DOM element"""
        for attr, value in kwargs.items():
            setattr( target, attr, value)

class Task_panel:
    """ A panel representing several steps of the task flow. :ref:`Task_panel`
    """
    def __init__(self,gui, board):
        self.gui, self.left, self.width = gui, 80, 100
        self.panels = [self._build_panel(i,color, board)
                       for i, color in enumerate(BACKGROUNDS)]
    def _build_panel(self,i, color, board):
        # create a DIV for each AREA (ie each country)
        self.width = 80 + (PANELS - i) * 60
        panel_div = Step_board(self.gui, i, color, self.left, self.width, board)
        self.left += self.width
        return panel_div

class Color_tab:
    """ A color markers for new tasks. :ref:`Color_tab`
    """
    def __init__(self,gui, color, left, top =10, width =16, board= None):
        self.gui, self.color, self.board = gui, color, board
        self.tab = self._build_color(color=color, left=left,
                                     top =top, width =width)
    def get_color(self):
        """Get the color of the tab"""
        return self.color
    def deploy(self, board, left, top, width):
        """Deploy a new task in a stepboard"""
        task = Task(self.gui, board, self.color, left, top, width)
        board.deploy(task)
        return task
    def _build_color(self, color, left, top =10, width =16):
        # create a DIV for each color label
        color_tab = self.gui.div('', node= HEAD, draggable=True,
                    id='color_%s'%color[1:], Class="color-tabs")
        self.gui.set_style(color_tab, **{'position':'absolute','left':left,
            'top':top, 'width':width, 'height':16, 'backgroundColor':color})
        self.gui.set_attrs(color_tab,
            ondragstart = self._drag_start,onmouseover = self._mouse_over,
            ondragover = self._drag_over, ondrop = self._drop)
        return color_tab
    def delete(self, ev):
        pass
    def _drag_start(self, ev):
        ev.data[ITEM]= self.color#ev.target.id
        ev.data.effectAllowed = 'move'
    def _mouse_over(self,ev):
        ev.target.style.cursor = "pointer"
    def _drag_over(self,ev):
        ev.data.dropEffect = 'move'
        ev.preventDefault()
    def _drop(self,ev):
        ev.preventDefault()
        color_id = ev.data[ITEM]
        item = self.board.get_tab(color_id)
        
        if confirm('Deseja realmente apagar %?'% item.identify()):
            item.delete()

class Color_pallete:
    """ A collecion of color markers for new tasks. :ref:`Color_pallete`
    """
    def __init__(self,gui, board):
        self.gui, self.board = gui, board
        self.colors =dict([ self._build_color(i,color, board)
                       for i, color in enumerate(COLORS)])
    def _build_color(self,i, color, board):
        # create a DIV for each color label
        left = 10+20*i #(i//15)
        color_tab = Color_tab(self.gui, color = color, left = left, board= board)
        return (color, color_tab)
        

class Task:
    """ A Task represented by a colored note. :ref:`Task`
    """
    def __init__(self, gui, board, color, left, top, width):
        self.gui, self.board, self.color = gui, board, color
        self._build_color(color, left, top, width)
    def identify(self):
        """Get the color of the tab"""
        return self.color
    def _build_color(self, color, left, top, width):
        # create a DIV for each color label
        top = 42 + top*68
        self.task = color_tab = self.gui.div('', node= PANEL, draggable=True,
                    id='color_%s'%color[1:], Class="task-note")
        self.gui.set_style(color_tab, **{'position':'absolute','left':left+2,
            'top':top,'width':width-4,'height':64, 'backgroundColor':color})
        self.gui.set_attrs(color_tab,
            ondragstart = self._drag_start,onmouseover = self._mouse_over,
            ondragover = self._drag_over, ondrop = self._drop)
        return color_tab
    def _drag_start(self, ev):
        ev.data[ITEM]=ev.target.id
        ev.data.effectAllowed = 'move'
    def _mouse_over(self,ev):
        ev.target.style.cursor = "pointer"
    def _drag_over(self,ev):
        ev.data.dropEffect = 'move'
        ev.preventDefault()
    def _drop(self,ev):
        ev.preventDefault()
        item = ev.data[ITEM]
        if self.gui.confirm('Deseja realmente apagar %?'% item.identify()):
            item.delete()
        
    pass

class Step_board:
    """ A board to hold tasks within a step in the task workflow. :ref:`Step_board`
    """
    def __init__(self, gui, i, color, left, width, panel):
        # create a DIV for each AREA (ie each country)
        self.gui, self.left, self.width, self.panel = gui, left, width, panel
        self.tasks = []
        self._build_board(i, color)
    def deploy(self, task):
        """Deploy a new task in a stepboard"""
        self.tasks.append(task)
    def _build_board(self,i, color):
        self.board = panel_div = self.gui.div('', node = PANEL, draggable=False
                    , id='panel%d'%i,   Class="task-panel")
        _top = 40
        self.gui.set_style(panel_div, **{'position':'absolute','left':self.left,
            'top':_top,'width':self.width,'height':400, 'backgroundColor':color})
        self.gui.set_attrs(panel_div,
            ondragover = self._drag_over, ondrop = self._drop)
    def _next_position(self):
        return (self.left, len(self.tasks), self.width)
    def _drag_over(self,ev):
        ev.data.dropEffect = 'move'
        ev.preventDefault()
    def _drop(self,ev):
        ev.preventDefault()
        color_id = ev.data[ITEM]
        logger('deploy color %s %s %s'%(color_id, color_id, self._next_position()))
        item = self.panel.get_tab(color_id)
        logger('deploy color %s %s %s'%(item, color_id, self._next_position()))
        item.deploy(self, *self._next_position())
    pass

class Dust_bin:
    """ A Kanban workflow plugin for the Activ platform. :ref:`Dust_bin`
    """
    pass

class Kanban:
    """ A Kanban workflow plugin for the Activ platform. :ref:`kanban`
    """
    def get_tab(self, color):
        """Get a tab with the given key color"""
        return self.head_bar.colors[color]
    def _build_project_selector(self):
        return Color_pallete(self.gui, self)
    def _build_label_selector(self):
        pass
    def _build_workflow_area(self):
        return Task_panel(self.gui, self)
        pass
    def __init__(self,gui):
        self.gui = gui
        self.head_bar = self._build_project_selector()
        self.label_bar = self._build_label_selector()
        self.task_bar = self._build_workflow_area()
         
def main(dc, gui, div_ids, repo):
    """ Starting point """
    global REPO
    REPO = repo
    return Kanban(gui)
