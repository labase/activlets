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
" da pós que você me convidou. Tenho interesse de assistir a aula e conversar"+\
"com a profa. Cristina. Pretendo aparecer na semana que vem Abraços!"

class Visual:
    """Build visual parts.
    """
    def __init__(self, doc, gui):
        """Build a task list. """
        divmain = doc["main"]
        self.gui = gui
        self.tasks = self.gui.DIV('',id="tasks")
        divmain <= self.tasks
        task = self.gui.DIV(texto, style=dict(float="left", width="100%"))
        hr = self.gui.HR(noshade="")
        self.tasks <= task
        task <= hr
        print ("aqui")

    def buid_base(self, gui):
        """Monta a casa que fica na base. """
        pass
