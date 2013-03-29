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
BACKGROUNDS ="#330066 #330099 #CCCCFF #9999FF".split()
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
    def __init__(self,gui):
        self.left = 80
        self.width = 100
        PANELS = len(BACKGROUNDS)
        self.panels = [self._build_panel(i,color)
                       for i, color in enumerate(BACKGROUNDS)]
    def _build_panel(self,i, color):
        # create a DIV for each AREA (ie each country)
        ctag = gui.div('', node = PANEL, draggable=False, id='panel%d'%i,
                       Class="task-panel")
        self.width = 100 + (PANELS - i) * 60
        _top = 20 #100+30*(i-15*(i//15))
        ctag.style= {'position':'absolute','left':self.left,'top':_top,
            'width':self.width,'height':400, 'background-color':color}
        self.left += self.width
        ctag.ondragover = self._drag_over
        ctag.ondrop = self._drop
        return ctag
    def _drag_over(self,ev):
        ev.data.dropEffect = 'move'
        ev.preventDefault()
    def _drop(self,ev):
        ev.preventDefault()
        src_id = ev.data[ITEM]
        elt = self.panels[src_id]
        if ev.target.id==countries[int(src_id)]:
            # dropped on the right country
            elt.style.left = ev.x-elt.clientWidth/2
            elt.style.top = ev.y-elt.clientHeight/2
            elt.draggable = False # don't drag any more
            elt.style.cursor = "auto"
        else:
            # back where we started
            go_back(elt,ev)

class Color_pallete:
    """ A collecion of color markers for new tasks. :ref:`Color_pallete`
    """
    def __init__(self,gui):
        self.gui = gui
        self.colors = [self._build_color(i,color)
                       for i, color in enumerate(COLORS)]
    def _build_color(self,i, color):
        # create a DIV for each color label
        color_tab = self.gui.div('', node= HEAD, draggable=True,
                    id='color_%s'%color[1:], Class="color-tabs")
        #left = 10+110*(i//15)
        #_top = 100+30*(i-15*(i//15))
        left = 10+20*i #(i//15)
        _top = 10 #100+30*(i-15*(i//15))
        #color_tab.style= {'position':'absolute','left':left,'top':_top,
        #    'width':16,'height':16, 'background-color_tab':color_tab}
        self.gui.set_style(color_tab, **{'position':'absolute','left':left,
            'top':_top,'width':16,'height':16, 'backgroundColor':color})
        self.gui.set_attrs(color_tab,
            ondragstart = self._drag_start,onmouseover = self._mouse_over,
            ondragover = self._drag_over, ondrop = self._drop)
        #color_tab.ondragstart = self._drag_start
        #color_tab.onmouseover = self._mouse_over
        ## drag and drop event handlers
        #color_tab.ondragover = self._drag_over
        #color_tab.ondrop = self._drop
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
        

class Task:
    """ A Kanban workflow plugin for the Activ platform. :ref:`Task`
    """
    pass

class Step_board:
    """ A board to hold tasks within a step in the task workflow. :ref:`Step_board`
    """
    def __init__(self,i, color, left, width, panel):
        # create a DIV for each AREA (ie each country)
        self.panel = panel
        self.board = board = gui.div('', node = PANEL, draggable=False,
                id='panel%d'%i, Class="task-panel")
        _top = 20 #100+30*(i-15*(i//15))
        board.style= {'position':'absolute','left':left,'top':_top,
            'width':width,'height':400, 'background-color':color}
        board.ondragover = self._drag_over
        board.ondrop = self._drop
    def _drag_over(self,ev):
        ev.data.dropEffect = 'move'
        ev.preventDefault()
    def _drop(self,ev):
        ev.preventDefault()
        task_id = ev.data[ITEM]
        self.panel.deploy_task(task_id)
    pass

class Dust_bin:
    """ A Kanban workflow plugin for the Activ platform. :ref:`Dust_bin`
    """
    pass

class Kanban:
    """ A Kanban workflow plugin for the Activ platform. :ref:`kanban`
    """
    def _build_project_selector(self):
        return Color_pallete(self.gui)
    def _build_label_selector(self):
        pass
    def _build_workflow_area(self):
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
