"""
############################################################
Kanban - Visual
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/06/21
:Status: This is a "work in progress"
:Revision: 0.1.1
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.
"""
texto = "Olá Carlo! Hoje houve um imprevisto que não me possibilitou ir a aula"+\
" da pós que você me convidou. Tenho interesse de assistir a aula."
class Visual:
    """Build visual parts.
    """
    def __init__(self, doc, gui):
        """Build a task list. """
        divmain = doc["main"]
        self.gui = gui
        self.tasks = self.gui.DIV('',id="tasks")
        divmain <= self.tasks
        self.tasks = self.gui.DIV('',id="tasks")
        divmain <= self.tasks

    def build_section(self, text = texto, title= "tarefa"):
        """Build a section div for tasks. """
        h = self.gui.H3()
        span = self.gui.SPAN(title, style = dict(
             textAlign = "left", color = "red"))
        h <= span
        self.tasks <= h
        div_style = style=dict(border = "2px red solid", 
            float = "left", width = "99%", padding = 5, fontSize = 10)
        self.section = self.gui.DIV("", Class="rounded-corners", 
                                    style = div_style)
        self.tasks <= self.section
        return self.section
    def build_task(self, text = texto, sect = None):
        """Build a task div. """
        sect = sect or self.section
        task = self.gui.DIV(text, style=dict(float="left", width="100%"))
        hr = self.gui.HR(noshade="")
        sect <= task
        task <= hr
        print ("aqui")
