"""
############################################################
Kanban - Agile Workflow
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/03/29
:Status: This is a "work in progress"
:Revision: 0.1.8
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__. 
"""
__author__  = "Carlo E. T. Oliveira (carlo@nce.ufrj.br)"
__version__ = "0.1"
__date__    = "2013/03/29"

REPO = '/studio/activlets/%s'
BRYTHON = False

def _logger(*a):
    print(a)
        
if not '__package__' in dir():
    import svg
    import html
    logger = log
    BRYTHON = True
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
    def remove(self, element, node):
        """Remove a element from a DOM node"""
        self.doc[node].removeChild(element)
    def confirmation(self, query_text):
        """Open a confimation dialog and return the choice"""
        return confirm(query_text)
    def set_style(self, target, **kwargs):
        """Set the style attribute of a DOM element"""
        #logger('styyle %s'%kwargs)
        target.style= kwargs
    def set_attrs(self, target, **kwargs):
        """Set the attributes defined as key arguments of a target DOM element"""
        for attr, value in kwargs.items():
            setattr( target, attr, value)


class Draggable:
    """ Interface for something that can be dragged. :ref:`Draggable`
    """
    def _drag_start(self, ev):
        ev.data[ITEM]=self.ob_id
        ev.data.effectAllowed = 'move'
    def _mouse_over(self,ev):
        ev.target.style.cursor = "pointer"
    def _drag_over(self,ev):
        ev.data.dropEffect = 'move'
        ev.preventDefault()
    def _drop(self,ev):
        ev.preventDefault()
        item_id = ev.data[ITEM]
        item = self.container.get_item(item_id)
        self.do_drop(item)
    def do_drop(self,item):
        """Template action when element receives a dropped item"""
        pass

class Composite(Draggable):
    """ Interface of containement, contained by and contains peers. :ref:`Composite`
    """
    def get_dimensions(self):
        """get dimensions for component."""
        pass
    def arrange(self, left, top, width, height, margin = 4, offy = 40):#, **kwargs):
        """Deploy this component in a container"""
        dims = {'position':'absolute',
            'left':left + margin/2, 'top':top, # * height + offy,
            'width':width - margin, 'height':height - margin,
            'backgroundColor':self.color}
        self.gui.set_style(self.avatar, **dims)
    def _build_avatar(self,gui, obid, color, node, clazz, drag, events):
        self.avatar = self.gui.div('', node = node, draggable= drag
                    , id=obid,   Class=clazz)
        dims = self.get_dimensions()
        self.arrange(dims['left'],dims['top'],dims['width'],dims['height'], dims['margin'])
        gui.set_attrs(self.avatar, **events)
    def append(self, component):
        """Append a new component."""
        self.items.append(component)
    def remove(self, component):
        """Remove a  component."""
        self.items.remove(component)
        self._rearrange_components(component)
    def attach(self, container, dims):
        """attach to a new container."""
        self.container.remove(self)
        self.container = container
        self.top, self.width = dims['top'],dims['width']
        self.arrange(dims['left'],self.top*68+42,self.width,dims['height'], dims['margin'])
        container.append(self)
    def _rearrange_components(self, component):
        """dettach from this container and sort components."""
        pass

OBID = 0

class Task(Composite):
    """ A Task represented by a colored note. :ref:`Task`
    """
    def delete_object(self):
        """Delete this item from Board and Dom"""
        if self.gui.confirmation('Deseja realmente apagar %s?'% self.ob_id):
            self.container.remove(self)
            logger('delete %s'%self.ob_id)
            self.gui.remove(self, PANEL)
    def __init__(self, gui, container, color, left, top, width):
        global OBID
        self.gui, self.container, self.color = gui, container, color
        self.ob_id, self.top, self.width = 'task_%d'%OBID, top, width
        self.left = left
        container.register(self)
        OBID += 1
        events = dict(ondragover = self._drag_over, ondrop = self._drop,
            ondragstart = self._drag_start,onmouseover = self._mouse_over)
        self._build_avatar(gui, self.ob_id, color, PANEL, "task-note", True, events)
    def get_dimensions(self):
        """get dimensions for component."""
        dims = dict(left = self.left, top = 42 + self.top*68,
                width = self.width, height = 68, margin=4)
        return dims

class Task_panel:
    """ A panel representing several steps of the task flow. :ref:`Task_panel`
    """
    def __init__(self,gui, container):
        self.gui, self.left, self.width = gui, 80, 100
        self.panels = [self._build_panel(i,color, container)
                       for i, color in enumerate(BACKGROUNDS)]
    def _build_panel(self,i, color, container):
        self.width = 80 + (PANELS - i) * 60
        panel_div = Step_board(self.gui, i, color, self.left, self.width, container)
        BRYTHON and panel_div.__init__(self.gui, i, color, self.left, self.width, container)
        self.left += self.width
        return panel_div

class Color_tab(Draggable):
    """ A color markers for new tasks. :ref:`Color_tab`
    """
    def __init__(self,gui, color, left, top, container):
        self.gui, self.color, self.ob_id, self.container = gui, color, color, container
        #self.tab = self._build_tab(color, left, top, 16)
        container.register(self)
        #logger('Color_tab init top %s color %s  tab %s'%(top,color, self))
    def _build_tab(self,gui, color, left, top, width):
        avatar = gui.div('', node= HEAD, draggable=True,
                    id=color, Class="color-tabs")
        args = {'position':'absolute','left':left,
            'top':top, 'width':width, 'height':40, 'backgroundColor':color}
        gui.set_style(avatar, **args)
        gui.set_attrs(avatar,
            ondragstart = self._drag_start,onmouseover = self._mouse_over,
            ondragover = self._drag_over, ondrop = self._drop)
        return avatar
    def get_color(self):
        """Get the color of the tab"""
        return self.color
    def attach(self, container, dims):
        """Deploy a new task in a stepboard"""
        left, top, width = dims['left'],dims['top'],dims['width']
        task = Task(self.gui, container, self.color, left, top, width)
        BRYTHON and task.__init__(self.gui, container, self.color, left, top, width)
        container.append(task)
    def delete(self, ev):
        pass
    def do_drop(self,item):
        logger(' delete item %s id %s del %s'%(item, item.ob_id,dir(item)))
        item.delete_object()

class Color_pallete:
    """ A collecion of color markers for new tasks. :ref:`Color_pallete`
    """
    def __init__(self, gui, container):
        self.gui, self.container = gui, container
        #self.colors = [ self._build_color(i,color, container)
        #               for i, color in enumerate(COLORS)]
        #self.colors = { color:self._build_color(i,color, container)
        #               for i, color in enumerate(COLORS)}
        colors = {}
        for i, color  in enumerate(COLORS):
            cl =self._build_color(i,color, container)
            colors[color] = cl
        self.colors = colors
    def _build_color(self,i, color, container):
        # create a DIV for each color label
        left = 0
        top = 42*i #(i//15)
        gui = self.gui
        color_tab = Color_tab(gui, color, left , top, container)
        BRYTHON and color_tab.__init__(gui, color, left , top, container)
        #logger('Color_pallete build top %s color %s  tab %s'%(top,color, color_tab))
        color_tab._build_tab(self.gui,color, left, top, 16)
        return color_tab #(color, color_tab)
        

class Step_board(Composite):
    """ A board to hold tasks within a step in the task workflow. :ref:`Step_board`
    """
    def __init__(self, gui, i, color, left, width, panel):
        # create a DIV for each AREA (ie each country)
        self.gui, self.left, self.width, self.container = gui, left, width, panel
        self.color = color
        self.items = []
        events = dict(ondragover = self._drag_over, ondrop = self._drop)
        self._build_avatar(gui, 'panel%d'%i, color, PANEL, "task-panel", False, events)
    def get_dimensions(self):
        """get dimensions for component."""
        dims = dict(left = self.left, top = 40,
                width = self.width, height = 500, margin=0)
        return dims
    def get_item(self, item):
        """Get a tab with the given object id key"""
        return self.container.get_item(item)
    def register(self, item):
        """Register an item  with the given object id key"""
        self.container.register(item)
    def remove(self, task):
        """Remove a task from a stepboard"""
        def ts (t=task):
            return t
        ind = [i for i in self.items if i is not task]
        logger('task indesx %s'%ind)
        self.items= ind
        #self.items.remove(task)
    def _next_position(self):
        return dict(left=self.left, top=len(self.items), width=self.width,
                    height = 68, margin=4)
        return (self.left, len(self.items), self.width)
    def _drag_start(self, ev):
        pass
    def _mouse_over(self,ev):
        pass
    def do_drop(self,item):
        item.attach(self,self._next_position())
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
    def register(self, item):
        """Register an item  with the given object id key"""
        self.items[item.ob_id] = item
    def remove(self, item):
        """Remove an item  with the given object id key"""
        self.items.pop(item.ob_id)
    def get_item(self, ob_id):
        """Get a tab with the given object id key"""
        return self.items[ob_id]
    def _build_project_selector(self):
        return Color_pallete(self.gui, self)
    def _build_label_selector(self):
        pass
    def _build_workflow_area(self):
        return Task_panel(self.gui, self)
        pass
    def __init__(self,gui):
        self.gui = gui
        self.items = {}
        self.head_bar = self._build_project_selector()
        self.label_bar = self._build_label_selector()
        self.task_bar = self._build_workflow_area()
         
def main(dc, gui, div_ids, repo):
    """ Starting point """
    global REPO
    REPO = repo
    return Kanban(gui)
